"""
Sprint 2 - Análise de Pull Requests do GitHub
Lab 03 - Caracterizando a atividade de code review no GitHub

Este script realiza análises estatísticas e responde às 8 questões de pesquisa (RQs)
sobre a relação entre características dos PRs e:
- Dimensão A: Feedback final das revisões (status do PR)
- Dimensão B: Número de revisões realizadas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import json
import os
from pathlib import Path

# Configuração de estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class AnalisadorPRs:
    def __init__(self, arquivo_dataset: str = "dataset_prs.csv"):
        """
        Inicializa o analisador de PRs
        
        Args:
            arquivo_dataset: Nome do arquivo CSV com os dados dos PRs
        """
        self.caminho_base = Path("/Users/pedroafonso/lab3")
        self.caminho_dataset = self.caminho_base / arquivo_dataset
        self.caminho_graficos = self.caminho_base / "graficos"
        self.caminho_graficos.mkdir(exist_ok=True)
        
        self.df = None
        self.resultados = {}
        
    def carregar_dados(self) -> bool:
        """
        Carrega o dataset de PRs
        
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        print("=" * 80)
        print("SPRINT 2 - ANÁLISE DE PULL REQUESTS")
        print("=" * 80)
        print()
        
        if not self.caminho_dataset.exists():
            print(f"❌ Erro: Arquivo {self.caminho_dataset} não encontrado!")
            print("Execute primeiro a Sprint 1 para coletar os dados.")
            return False
        
        print(f"📂 Carregando dataset: {self.caminho_dataset}")
        self.df = pd.read_csv(self.caminho_dataset)
        
        print(f"✓ Dataset carregado com sucesso!")
        print(f"  • Total de PRs: {len(self.df)}")
        print(f"  • Repositórios únicos: {self.df['repository'].nunique()}")
        print(f"  • PRs merged: {len(self.df[self.df['merged'] == True])}")
        print(f"  • PRs closed (não merged): {len(self.df[self.df['merged'] == False])}")
        print()
        
        return True
    
    def preparar_dados(self):
        """
        Prepara e limpa os dados para análise
        """
        print("🔧 Preparando dados para análise...")
        
        # Converter colunas booleanas
        self.df['merged'] = self.df['merged'].astype(bool)
        
        # Adicionar variável categórica para o status
        self.df['status_categoria'] = self.df['merged'].map({True: 'MERGED', False: 'CLOSED'})
        
        # Calcular tamanho total das mudanças
        self.df['total_changes'] = self.df['total_additions'] + self.df['total_deletions']
        
        # Criar categorias de tamanho
        self.df['tamanho_categoria'] = pd.cut(
            self.df['total_changes'],
            bins=[0, 50, 200, 500, float('inf')],
            labels=['Pequeno', 'Médio', 'Grande', 'Muito Grande']
        )
        
        # Criar categorias de tempo
        self.df['tempo_categoria'] = pd.cut(
            self.df['time_analysis_hours'],
            bins=[0, 24, 168, 720, float('inf')],
            labels=['< 1 dia', '1-7 dias', '1-30 dias', '> 30 dias']
        )
        
        # Criar categorias de descrição
        self.df['descricao_categoria'] = pd.cut(
            self.df['description_chars'],
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['Muito Curta', 'Curta', 'Média', 'Longa']
        )
        
        # Criar categorias de interações
        self.df['interacoes_categoria'] = pd.cut(
            self.df['num_comments'],
            bins=[0, 5, 15, 30, float('inf')],
            labels=['Baixa', 'Média', 'Alta', 'Muito Alta']
        )
        
        # Remover outliers extremos (opcional)
        for col in ['total_changes', 'time_analysis_hours', 'description_chars', 'num_comments']:
            q1 = self.df[col].quantile(0.01)
            q99 = self.df[col].quantile(0.99)
            self.df[f'{col}_sem_outliers'] = self.df[col].clip(q1, q99)
        
        print("✓ Dados preparados!")
        print()
    
    def calcular_correlacao(self, var1: str, var2: str) -> tuple:
        """
        Calcula correlação de Spearman entre duas variáveis
        
        Args:
            var1: Nome da primeira variável
            var2: Nome da segunda variável
            
        Returns:
            Tupla (correlação, p-valor)
        """
        # Remover valores nulos
        dados = self.df[[var1, var2]].dropna()
        
        if len(dados) < 3:
            return None, None
        
        # Correlação de Spearman (não assume distribuição normal)
        corr, p_value = stats.spearmanr(dados[var1], dados[var2])
        
        return corr, p_value
    
    def teste_mann_whitney(self, var_continua: str, var_binaria: str) -> tuple:
        """
        Realiza teste de Mann-Whitney U para comparar duas grupos
        
        Args:
            var_continua: Nome da variável contínua
            var_binaria: Nome da variável binária (deve ter 2 categorias)
            
        Returns:
            Tupla (estatística U, p-valor)
        """
        grupos = self.df[var_binaria].unique()
        
        if len(grupos) != 2:
            return None, None
        
        grupo1 = self.df[self.df[var_binaria] == grupos[0]][var_continua].dropna()
        grupo2 = self.df[self.df[var_binaria] == grupos[1]][var_continua].dropna()
        
        if len(grupo1) < 3 or len(grupo2) < 3:
            return None, None
        
        u_stat, p_value = stats.mannwhitneyu(grupo1, grupo2, alternative='two-sided')
        
        return u_stat, p_value
    
    def interpretar_correlacao(self, corr: float) -> str:
        """
        Interpreta o valor da correlação
        
        Args:
            corr: Coeficiente de correlação
            
        Returns:
            String com interpretação
        """
        abs_corr = abs(corr)
        
        if abs_corr < 0.1:
            forca = "muito fraca"
        elif abs_corr < 0.3:
            forca = "fraca"
        elif abs_corr < 0.5:
            forca = "moderada"
        elif abs_corr < 0.7:
            forca = "forte"
        else:
            forca = "muito forte"
        
        direcao = "positiva" if corr > 0 else "negativa"
        
        return f"{forca} {direcao}"
    
    def interpretar_p_valor(self, p: float) -> str:
        """
        Interpreta o p-valor
        
        Args:
            p: P-valor
            
        Returns:
            String com interpretação
        """
        if p < 0.001:
            return "altamente significativo (p < 0.001)"
        elif p < 0.01:
            return "muito significativo (p < 0.01)"
        elif p < 0.05:
            return "significativo (p < 0.05)"
        else:
            return "não significativo (p ≥ 0.05)"
    
    # ========================================================================
    # DIMENSÃO A: FEEDBACK FINAL DAS REVISÕES (STATUS DO PR)
    # ========================================================================
    
    def rq01_tamanho_vs_status(self):
        """
        RQ 01: Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
        """
        print("=" * 80)
        print("RQ 01: TAMANHO DOS PRS vs FEEDBACK FINAL")
        print("=" * 80)
        print()
        
        # Análise estatística
        u_stat, p_value = self.teste_mann_whitney('total_changes', 'merged')
        
        # Estatísticas descritivas
        merged_stats = self.df[self.df['merged'] == True]['total_changes'].describe()
        closed_stats = self.df[self.df['merged'] == False]['total_changes'].describe()
        
        print("📊 Estatísticas Descritivas:")
        print(f"\nPRs MERGED:")
        print(f"  • Média: {merged_stats['mean']:.2f} linhas")
        print(f"  • Mediana: {merged_stats['50%']:.2f} linhas")
        print(f"  • Desvio padrão: {merged_stats['std']:.2f}")
        
        print(f"\nPRs CLOSED:")
        print(f"  • Média: {closed_stats['mean']:.2f} linhas")
        print(f"  • Mediana: {closed_stats['50%']:.2f} linhas")
        print(f"  • Desvio padrão: {closed_stats['std']:.2f}")
        
        print(f"\n📈 Teste Estatístico (Mann-Whitney U):")
        print(f"  • Estatística U: {u_stat:.2f}")
        print(f"  • P-valor: {p_value:.4f}")
        print(f"  • Interpretação: {self.interpretar_p_valor(p_value)}")
        
        # Visualização
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Boxplot
        self.df.boxplot(column='total_changes_sem_outliers', by='status_categoria', ax=axes[0])
        axes[0].set_title('Distribuição do Tamanho por Status')
        axes[0].set_xlabel('Status do PR')
        axes[0].set_ylabel('Total de Mudanças (linhas)')
        plt.sca(axes[0])
        plt.xticks(rotation=0)
        
        # Violin plot
        sns.violinplot(data=self.df, x='status_categoria', y='total_changes_sem_outliers', ax=axes[1])
        axes[1].set_title('Densidade do Tamanho por Status')
        axes[1].set_xlabel('Status do PR')
        axes[1].set_ylabel('Total de Mudanças (linhas)')
        
        plt.tight_layout()
        plt.savefig(self.caminho_graficos / 'rq01_tamanho_vs_status.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Gráfico salvo: graficos/rq01_tamanho_vs_status.png")
        print()
        
        # Armazenar resultados
        self.resultados['RQ01'] = {
            'titulo': 'Tamanho dos PRs vs Feedback Final',
            'u_stat': u_stat,
            'p_value': p_value,
            'merged_mean': merged_stats['mean'],
            'closed_mean': closed_stats['mean'],
            'significativo': p_value < 0.05
        }
    
    def rq02_tempo_vs_status(self):
        """
        RQ 02: Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
        """
        print("=" * 80)
        print("RQ 02: TEMPO DE ANÁLISE vs FEEDBACK FINAL")
        print("=" * 80)
        print()
        
        # Análise estatística
        u_stat, p_value = self.teste_mann_whitney('time_analysis_hours', 'merged')
        
        # Estatísticas descritivas
        merged_stats = self.df[self.df['merged'] == True]['time_analysis_hours'].describe()
        closed_stats = self.df[self.df['merged'] == False]['time_analysis_hours'].describe()
        
        print("📊 Estatísticas Descritivas:")
        print(f"\nPRs MERGED:")
        print(f"  • Média: {merged_stats['mean']:.2f} horas ({merged_stats['mean']/24:.2f} dias)")
        print(f"  • Mediana: {merged_stats['50%']:.2f} horas ({merged_stats['50%']/24:.2f} dias)")
        print(f"  • Desvio padrão: {merged_stats['std']:.2f} horas")
        
        print(f"\nPRs CLOSED:")
        print(f"  • Média: {closed_stats['mean']:.2f} horas ({closed_stats['mean']/24:.2f} dias)")
        print(f"  • Mediana: {closed_stats['50%']:.2f} horas ({closed_stats['50%']/24:.2f} dias)")
        print(f"  • Desvio padrão: {closed_stats['std']:.2f} horas")
        
        print(f"\n📈 Teste Estatístico (Mann-Whitney U):")
        print(f"  • Estatística U: {u_stat:.2f}")
        print(f"  • P-valor: {p_value:.4f}")
        print(f"  • Interpretação: {self.interpretar_p_valor(p_value)}")
        
        # Visualização
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Boxplot
        self.df.boxplot(column='time_analysis_hours_sem_outliers', by='status_categoria', ax=axes[0])
        axes[0].set_title('Distribuição do Tempo de Análise por Status')
        axes[0].set_xlabel('Status do PR')
        axes[0].set_ylabel('Tempo de Análise (horas)')
        plt.sca(axes[0])
        plt.xticks(rotation=0)
        
        # Histogram comparativo
        merged_data = self.df[self.df['merged'] == True]['time_analysis_hours_sem_outliers']
        closed_data = self.df[self.df['merged'] == False]['time_analysis_hours_sem_outliers']
        
        axes[1].hist([merged_data, closed_data], bins=30, label=['MERGED', 'CLOSED'], alpha=0.7)
        axes[1].set_title('Histograma do Tempo de Análise por Status')
        axes[1].set_xlabel('Tempo de Análise (horas)')
        axes[1].set_ylabel('Frequência')
        axes[1].legend()
        
        plt.tight_layout()
        plt.savefig(self.caminho_graficos / 'rq02_tempo_vs_status.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Gráfico salvo: graficos/rq02_tempo_vs_status.png")
        print()
        
        # Armazenar resultados
        self.resultados['RQ02'] = {
            'titulo': 'Tempo de Análise vs Feedback Final',
            'u_stat': u_stat,
            'p_value': p_value,
            'merged_mean': merged_stats['mean'],
            'closed_mean': closed_stats['mean'],
            'significativo': p_value < 0.05
        }
    
    def rq03_descricao_vs_status(self):
        """
        RQ 03: Qual a relação entre a descrição dos PRs e o feedback final das revisões?
        """
        print("=" * 80)
        print("RQ 03: DESCRIÇÃO DOS PRS vs FEEDBACK FINAL")
        print("=" * 80)
        print()
        
        # Análise estatística
        u_stat, p_value = self.teste_mann_whitney('description_chars', 'merged')
        
        # Estatísticas descritivas
        merged_stats = self.df[self.df['merged'] == True]['description_chars'].describe()
        closed_stats = self.df[self.df['merged'] == False]['description_chars'].describe()
        
        print("📊 Estatísticas Descritivas:")
        print(f"\nPRs MERGED:")
        print(f"  • Média: {merged_stats['mean']:.2f} caracteres")
        print(f"  • Mediana: {merged_stats['50%']:.2f} caracteres")
        print(f"  • Desvio padrão: {merged_stats['std']:.2f}")
        
        print(f"\nPRs CLOSED:")
        print(f"  • Média: {closed_stats['mean']:.2f} caracteres")
        print(f"  • Mediana: {closed_stats['50%']:.2f} caracteres")
        print(f"  • Desvio padrão: {closed_stats['std']:.2f}")
        
        print(f"\n📈 Teste Estatístico (Mann-Whitney U):")
        print(f"  • Estatística U: {u_stat:.2f}")
        print(f"  • P-valor: {p_value:.4f}")
        print(f"  • Interpretação: {self.interpretar_p_valor(p_value)}")
        
        # Visualização
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Boxplot
        self.df.boxplot(column='description_chars_sem_outliers', by='status_categoria', ax=axes[0])
        axes[0].set_title('Distribuição do Tamanho da Descrição por Status')
        axes[0].set_xlabel('Status do PR')
        axes[0].set_ylabel('Tamanho da Descrição (caracteres)')
        plt.sca(axes[0])
        plt.xticks(rotation=0)
        
        # Gráfico de barras por categoria
        df_descricao = self.df.groupby(['descricao_categoria', 'status_categoria']).size().unstack(fill_value=0)
        df_descricao_pct = df_descricao.div(df_descricao.sum(axis=1), axis=0) * 100
        df_descricao_pct.plot(kind='bar', ax=axes[1], rot=45)
        axes[1].set_title('Proporção de Status por Tamanho de Descrição')
        axes[1].set_xlabel('Tamanho da Descrição')
        axes[1].set_ylabel('Porcentagem (%)')
        axes[1].legend(title='Status')
        
        plt.tight_layout()
        plt.savefig(self.caminho_graficos / 'rq03_descricao_vs_status.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Gráfico salvo: graficos/rq03_descricao_vs_status.png")
        print()
        
        # Armazenar resultados
        self.resultados['RQ03'] = {
            'titulo': 'Descrição dos PRs vs Feedback Final',
            'u_stat': u_stat,
            'p_value': p_value,
            'merged_mean': merged_stats['mean'],
            'closed_mean': closed_stats['mean'],
            'significativo': p_value < 0.05
        }
    
    def rq04_interacoes_vs_status(self):
        """
        RQ 04: Qual a relação entre as interações nos PRs e o feedback final das revisões?
        """
        print("=" * 80)
        print("RQ 04: INTERAÇÕES NOS PRS vs FEEDBACK FINAL")
        print("=" * 80)
        print()
        
        # Análise estatística para comentários
        u_stat_comments, p_value_comments = self.teste_mann_whitney('num_comments', 'merged')
        
        # Análise estatística para participantes
        u_stat_participants, p_value_participants = self.teste_mann_whitney('num_participants', 'merged')
        
        # Estatísticas descritivas - Comentários
        merged_comments = self.df[self.df['merged'] == True]['num_comments'].describe()
        closed_comments = self.df[self.df['merged'] == False]['num_comments'].describe()
        
        # Estatísticas descritivas - Participantes
        merged_participants = self.df[self.df['merged'] == True]['num_participants'].describe()
        closed_participants = self.df[self.df['merged'] == False]['num_participants'].describe()
        
        print("📊 Estatísticas Descritivas - COMENTÁRIOS:")
        print(f"\nPRs MERGED:")
        print(f"  • Média: {merged_comments['mean']:.2f} comentários")
        print(f"  • Mediana: {merged_comments['50%']:.2f} comentários")
        
        print(f"\nPRs CLOSED:")
        print(f"  • Média: {closed_comments['mean']:.2f} comentários")
        print(f"  • Mediana: {closed_comments['50%']:.2f} comentários")
        
        print(f"\n📈 Teste Estatístico - Comentários (Mann-Whitney U):")
        print(f"  • Estatística U: {u_stat_comments:.2f}")
        print(f"  • P-valor: {p_value_comments:.4f}")
        print(f"  • Interpretação: {self.interpretar_p_valor(p_value_comments)}")
        
        print(f"\n📊 Estatísticas Descritivas - PARTICIPANTES:")
        print(f"\nPRs MERGED:")
        print(f"  • Média: {merged_participants['mean']:.2f} participantes")
        print(f"  • Mediana: {merged_participants['50%']:.2f} participantes")
        
        print(f"\nPRs CLOSED:")
        print(f"  • Média: {closed_participants['mean']:.2f} participantes")
        print(f"  • Mediana: {closed_participants['50%']:.2f} participantes")
        
        print(f"\n📈 Teste Estatístico - Participantes (Mann-Whitney U):")
        print(f"  • Estatística U: {u_stat_participants:.2f}")
        print(f"  • P-valor: {p_value_participants:.4f}")
        print(f"  • Interpretação: {self.interpretar_p_valor(p_value_participants)}")
        
        # Visualização
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Boxplot - Comentários
        self.df.boxplot(column='num_comments_sem_outliers', by='status_categoria', ax=axes[0, 0])
        axes[0, 0].set_title('Distribuição de Comentários por Status')
        axes[0, 0].set_xlabel('Status do PR')
        axes[0, 0].set_ylabel('Número de Comentários')
        plt.sca(axes[0, 0])
        plt.xticks(rotation=0)
        
        # Boxplot - Participantes
        self.df.boxplot(column='num_participants', by='status_categoria', ax=axes[0, 1])
        axes[0, 1].set_title('Distribuição de Participantes por Status')
        axes[0, 1].set_xlabel('Status do PR')
        axes[0, 1].set_ylabel('Número de Participantes')
        plt.sca(axes[0, 1])
        plt.xticks(rotation=0)
        
        # Scatter plot - Comentários vs Participantes
        for status in ['MERGED', 'CLOSED']:
            data = self.df[self.df['status_categoria'] == status]
            axes[1, 0].scatter(
                data['num_comments_sem_outliers'],
                data['num_participants'],
                alpha=0.5,
                label=status,
                s=30
            )
        axes[1, 0].set_title('Comentários vs Participantes por Status')
        axes[1, 0].set_xlabel('Número de Comentários')
        axes[1, 0].set_ylabel('Número de Participantes')
        axes[1, 0].legend()
        
        # Gráfico de barras por categoria de interações
        df_interacoes = self.df.groupby(['interacoes_categoria', 'status_categoria']).size().unstack(fill_value=0)
        df_interacoes_pct = df_interacoes.div(df_interacoes.sum(axis=1), axis=0) * 100
        df_interacoes_pct.plot(kind='bar', ax=axes[1, 1], rot=45)
        axes[1, 1].set_title('Proporção de Status por Nível de Interação')
        axes[1, 1].set_xlabel('Nível de Interação')
        axes[1, 1].set_ylabel('Porcentagem (%)')
        axes[1, 1].legend(title='Status')
        
        plt.tight_layout()
        plt.savefig(self.caminho_graficos / 'rq04_interacoes_vs_status.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Gráfico salvo: graficos/rq04_interacoes_vs_status.png")
        print()
        
        # Armazenar resultados
        self.resultados['RQ04'] = {
            'titulo': 'Interações nos PRs vs Feedback Final',
            'u_stat_comments': u_stat_comments,
            'p_value_comments': p_value_comments,
            'u_stat_participants': u_stat_participants,
            'p_value_participants': p_value_participants,
            'merged_mean_comments': merged_comments['mean'],
            'closed_mean_comments': closed_comments['mean'],
            'merged_mean_participants': merged_participants['mean'],
            'closed_mean_participants': closed_participants['mean'],
            'significativo_comments': p_value_comments < 0.05,
            'significativo_participants': p_value_participants < 0.05
        }
    
    # ========================================================================
    # DIMENSÃO B: NÚMERO DE REVISÕES
    # ========================================================================
    
    def rq05_tamanho_vs_revisoes(self):
        """
        RQ 05: Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
        
        Nota: Como não temos a contagem exata de revisões no dataset, vamos usar
        o número de participantes como proxy para o número de revisões.
        """
        print("=" * 80)
        print("RQ 05: TAMANHO DOS PRS vs NÚMERO DE REVISÕES")
        print("=" * 80)
        print()
        
        # Usar num_participants como proxy para número de revisões
        corr, p_value = self.calcular_correlacao('total_changes', 'num_participants')
        
        print("📊 Análise de Correlação:")
        print(f"  • Correlação de Spearman: {corr:.4f}")
        print(f"  • P-valor: {p_value:.4f}")
        print(f"  • Interpretação da correlação: {self.interpretar_correlacao(corr)}")
        print(f"  • Significância: {self.interpretar_p_valor(p_value)}")
        
        # Estatísticas por categoria de tamanho
        print(f"\n📈 Média de Participantes por Categoria de Tamanho:")
        stats_tamanho = self.df.groupby('tamanho_categoria')['num_participants'].agg(['mean', 'median', 'std'])
        for idx, row in stats_tamanho.iterrows():
            print(f"  • {idx}: média={row['mean']:.2f}, mediana={row['median']:.2f}")
        
        # Visualização
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Scatter plot
        axes[0].scatter(
            self.df['total_changes_sem_outliers'],
            self.df['num_participants'],
            alpha=0.5,
            s=30
        )
        axes[0].set_title('Tamanho do PR vs Número de Participantes')
        axes[0].set_xlabel('Total de Mudanças (linhas)')
        axes[0].set_ylabel('Número de Participantes')
        
        # Adicionar linha de tendência
        z = np.polyfit(self.df['total_changes_sem_outliers'].dropna(), 
                       self.df['num_participants'].dropna(), 1)
        p = np.poly1d(z)
        axes[0].plot(
            sorted(self.df['total_changes_sem_outliers'].dropna()),
            p(sorted(self.df['total_changes_sem_outliers'].dropna())),
            "r--",
            alpha=0.8,
            label=f'Tendência (ρ={corr:.3f})'
        )
        axes[0].legend()
        
        # Boxplot por categoria
        self.df.boxplot(column='num_participants', by='tamanho_categoria', ax=axes[1])
        axes[1].set_title('Número de Participantes por Categoria de Tamanho')
        axes[1].set_xlabel('Categoria de Tamanho do PR')
        axes[1].set_ylabel('Número de Participantes')
        plt.sca(axes[1])
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.caminho_graficos / 'rq05_tamanho_vs_revisoes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Gráfico salvo: graficos/rq05_tamanho_vs_revisoes.png")
        print()
        
        # Armazenar resultados
        self.resultados['RQ05'] = {
            'titulo': 'Tamanho dos PRs vs Número de Revisões',
            'correlacao': corr,
            'p_value': p_value,
            'interpretacao': self.interpretar_correlacao(corr),
            'significativo': p_value < 0.05
        }
    
    def rq06_tempo_vs_revisoes(self):
        """
        RQ 06: Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
        """
        print("=" * 80)
        print("RQ 06: TEMPO DE ANÁLISE vs NÚMERO DE REVISÕES")
        print("=" * 80)
        print()
        
        # Usar num_participants como proxy para número de revisões
        corr, p_value = self.calcular_correlacao('time_analysis_hours', 'num_participants')
        
        print("📊 Análise de Correlação:")
        print(f"  • Correlação de Spearman: {corr:.4f}")
        print(f"  • P-valor: {p_value:.4f}")
        print(f"  • Interpretação da correlação: {self.interpretar_correlacao(corr)}")
        print(f"  • Significância: {self.interpretar_p_valor(p_value)}")
        
        # Estatísticas por categoria de tempo
        print(f"\n📈 Média de Participantes por Categoria de Tempo:")
        stats_tempo = self.df.groupby('tempo_categoria')['num_participants'].agg(['mean', 'median', 'std'])
        for idx, row in stats_tempo.iterrows():
            print(f"  • {idx}: média={row['mean']:.2f}, mediana={row['median']:.2f}")
        
        # Visualização
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Scatter plot
        axes[0].scatter(
            self.df['time_analysis_hours_sem_outliers'],
            self.df['num_participants'],
            alpha=0.5,
            s=30
        )
        axes[0].set_title('Tempo de Análise vs Número de Participantes')
        axes[0].set_xlabel('Tempo de Análise (horas)')
        axes[0].set_ylabel('Número de Participantes')
        
        # Adicionar linha de tendência
        z = np.polyfit(self.df['time_analysis_hours_sem_outliers'].dropna(), 
                       self.df['num_participants'].dropna(), 1)
        p = np.poly1d(z)
        axes[0].plot(
            sorted(self.df['time_analysis_hours_sem_outliers'].dropna()),
            p(sorted(self.df['time_analysis_hours_sem_outliers'].dropna())),
            "r--",
            alpha=0.8,
            label=f'Tendência (ρ={corr:.3f})'
        )
        axes[0].legend()
        
        # Boxplot por categoria
        self.df.boxplot(column='num_participants', by='tempo_categoria', ax=axes[1])
        axes[1].set_title('Número de Participantes por Categoria de Tempo')
        axes[1].set_xlabel('Categoria de Tempo de Análise')
        axes[1].set_ylabel('Número de Participantes')
        plt.sca(axes[1])
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.caminho_graficos / 'rq06_tempo_vs_revisoes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Gráfico salvo: graficos/rq06_tempo_vs_revisoes.png")
        print()
        
        # Armazenar resultados
        self.resultados['RQ06'] = {
            'titulo': 'Tempo de Análise vs Número de Revisões',
            'correlacao': corr,
            'p_value': p_value,
            'interpretacao': self.interpretar_correlacao(corr),
            'significativo': p_value < 0.05
        }
    
    def rq07_descricao_vs_revisoes(self):
        """
        RQ 07: Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
        """
        print("=" * 80)
        print("RQ 07: DESCRIÇÃO DOS PRS vs NÚMERO DE REVISÕES")
        print("=" * 80)
        print()
        
        # Usar num_participants como proxy para número de revisões
        corr, p_value = self.calcular_correlacao('description_chars', 'num_participants')
        
        print("📊 Análise de Correlação:")
        print(f"  • Correlação de Spearman: {corr:.4f}")
        print(f"  • P-valor: {p_value:.4f}")
        print(f"  • Interpretação da correlação: {self.interpretar_correlacao(corr)}")
        print(f"  • Significância: {self.interpretar_p_valor(p_value)}")
        
        # Estatísticas por categoria de descrição
        print(f"\n📈 Média de Participantes por Categoria de Descrição:")
        stats_desc = self.df.groupby('descricao_categoria')['num_participants'].agg(['mean', 'median', 'std'])
        for idx, row in stats_desc.iterrows():
            print(f"  • {idx}: média={row['mean']:.2f}, mediana={row['median']:.2f}")
        
        # Visualização
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Scatter plot
        axes[0].scatter(
            self.df['description_chars_sem_outliers'],
            self.df['num_participants'],
            alpha=0.5,
            s=30
        )
        axes[0].set_title('Tamanho da Descrição vs Número de Participantes')
        axes[0].set_xlabel('Tamanho da Descrição (caracteres)')
        axes[0].set_ylabel('Número de Participantes')
        
        # Adicionar linha de tendência
        z = np.polyfit(self.df['description_chars_sem_outliers'].dropna(), 
                       self.df['num_participants'].dropna(), 1)
        p = np.poly1d(z)
        axes[0].plot(
            sorted(self.df['description_chars_sem_outliers'].dropna()),
            p(sorted(self.df['description_chars_sem_outliers'].dropna())),
            "r--",
            alpha=0.8,
            label=f'Tendência (ρ={corr:.3f})'
        )
        axes[0].legend()
        
        # Boxplot por categoria
        self.df.boxplot(column='num_participants', by='descricao_categoria', ax=axes[1])
        axes[1].set_title('Número de Participantes por Categoria de Descrição')
        axes[1].set_xlabel('Categoria de Descrição')
        axes[1].set_ylabel('Número de Participantes')
        plt.sca(axes[1])
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.caminho_graficos / 'rq07_descricao_vs_revisoes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Gráfico salvo: graficos/rq07_descricao_vs_revisoes.png")
        print()
        
        # Armazenar resultados
        self.resultados['RQ07'] = {
            'titulo': 'Descrição dos PRs vs Número de Revisões',
            'correlacao': corr,
            'p_value': p_value,
            'interpretacao': self.interpretar_correlacao(corr),
            'significativo': p_value < 0.05
        }
    
    def rq08_interacoes_vs_revisoes(self):
        """
        RQ 08: Qual a relação entre as interações nos PRs e o número de revisões realizadas?
        """
        print("=" * 80)
        print("RQ 08: INTERAÇÕES vs NÚMERO DE REVISÕES")
        print("=" * 80)
        print()
        
        # Correlação entre comentários e participantes
        corr, p_value = self.calcular_correlacao('num_comments', 'num_participants')
        
        print("📊 Análise de Correlação:")
        print(f"  • Correlação de Spearman: {corr:.4f}")
        print(f"  • P-valor: {p_value:.4f}")
        print(f"  • Interpretação da correlação: {self.interpretar_correlacao(corr)}")
        print(f"  • Significância: {self.interpretar_p_valor(p_value)}")
        
        # Estatísticas por categoria de interações
        print(f"\n📈 Média de Participantes por Categoria de Interações:")
        stats_inter = self.df.groupby('interacoes_categoria')['num_participants'].agg(['mean', 'median', 'std'])
        for idx, row in stats_inter.iterrows():
            print(f"  • {idx}: média={row['mean']:.2f}, mediana={row['median']:.2f}")
        
        # Visualização
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Scatter plot
        axes[0].scatter(
            self.df['num_comments_sem_outliers'],
            self.df['num_participants'],
            alpha=0.5,
            s=30
        )
        axes[0].set_title('Número de Comentários vs Número de Participantes')
        axes[0].set_xlabel('Número de Comentários')
        axes[0].set_ylabel('Número de Participantes')
        
        # Adicionar linha de tendência
        z = np.polyfit(self.df['num_comments_sem_outliers'].dropna(), 
                       self.df['num_participants'].dropna(), 1)
        p = np.poly1d(z)
        axes[0].plot(
            sorted(self.df['num_comments_sem_outliers'].dropna()),
            p(sorted(self.df['num_comments_sem_outliers'].dropna())),
            "r--",
            alpha=0.8,
            label=f'Tendência (ρ={corr:.3f})'
        )
        axes[0].legend()
        
        # Boxplot por categoria
        self.df.boxplot(column='num_participants', by='interacoes_categoria', ax=axes[1])
        axes[1].set_title('Número de Participantes por Categoria de Interações')
        axes[1].set_xlabel('Categoria de Interações')
        axes[1].set_ylabel('Número de Participantes')
        plt.sca(axes[1])
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.caminho_graficos / 'rq08_interacoes_vs_revisoes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Gráfico salvo: graficos/rq08_interacoes_vs_revisoes.png")
        print()
        
        # Armazenar resultados
        self.resultados['RQ08'] = {
            'titulo': 'Interações vs Número de Revisões',
            'correlacao': corr,
            'p_value': p_value,
            'interpretacao': self.interpretar_correlacao(corr),
            'significativo': p_value < 0.05
        }
    
    def gerar_relatorio_final(self):
        """
        Gera um relatório final em formato Markdown com todos os resultados
        """
        print("=" * 80)
        print("GERANDO RELATÓRIO FINAL")
        print("=" * 80)
        print()
        
        # Criar diretório de relatórios
        caminho_relatorio = self.caminho_base / "relatorio_sprint2.md"
        
        with open(caminho_relatorio, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("# Sprint 2 - Análise de Pull Requests do GitHub\n\n")
            f.write(f"**Data da análise:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            f.write(f"**Dataset:** {len(self.df)} Pull Requests\n\n")
            f.write(f"**Repositórios analisados:** {self.df['repository'].nunique()}\n\n")
            f.write("---\n\n")
            
            # Sumário executivo
            f.write("## Sumário Executivo\n\n")
            f.write("Este relatório apresenta os resultados da análise de code review em repositórios populares do GitHub, ")
            f.write("investigando as relações entre características dos PRs e dois outcomes principais:\n\n")
            f.write("1. **Dimensão A:** Feedback final das revisões (PR merged ou closed)\n")
            f.write("2. **Dimensão B:** Número de revisões realizadas (proxy: número de participantes)\n\n")
            f.write("---\n\n")
            
            # Estatísticas descritivas gerais
            f.write("## Estatísticas Descritivas Gerais\n\n")
            
            f.write("### Status dos PRs\n\n")
            merged_count = len(self.df[self.df['merged'] == True])
            closed_count = len(self.df[self.df['merged'] == False])
            f.write(f"- **PRs Merged:** {merged_count} ({merged_count/len(self.df)*100:.1f}%)\n")
            f.write(f"- **PRs Closed (não merged):** {closed_count} ({closed_count/len(self.df)*100:.1f}%)\n\n")
            
            f.write("### Métricas Gerais\n\n")
            f.write("| Métrica | Média | Mediana | Desvio Padrão |\n")
            f.write("|---------|-------|---------|---------------|\n")
            
            metricas = ['total_changes', 'time_analysis_hours', 'description_chars', 'num_comments', 'num_participants']
            nomes = ['Mudanças (linhas)', 'Tempo (horas)', 'Descrição (chars)', 'Comentários', 'Participantes']
            
            for metrica, nome in zip(metricas, nomes):
                stats = self.df[metrica].describe()
                f.write(f"| {nome} | {stats['mean']:.2f} | {stats['50%']:.2f} | {stats['std']:.2f} |\n")
            
            f.write("\n---\n\n")
            
            # Dimensão A: Feedback Final
            f.write("## Dimensão A: Feedback Final das Revisões\n\n")
            
            # RQ01
            f.write("### RQ 01: Tamanho dos PRs vs Feedback Final\n\n")
            rq01 = self.resultados['RQ01']
            f.write(f"**Questão:** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?\n\n")
            f.write("**Resultados:**\n\n")
            f.write(f"- PRs **merged** têm em média **{rq01['merged_mean']:.2f} linhas** de mudanças\n")
            f.write(f"- PRs **closed** têm em média **{rq01['closed_mean']:.2f} linhas** de mudanças\n")
            f.write(f"- Teste Mann-Whitney U: U={rq01['u_stat']:.2f}, p={rq01['p_value']:.4f}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq01['significativo'] else '✗ Não significativo'}\n\n")
            f.write("**Interpretação:** ")
            if rq01['significativo']:
                if rq01['merged_mean'] < rq01['closed_mean']:
                    f.write("PRs menores têm maior probabilidade de serem merged.\n\n")
                else:
                    f.write("PRs maiores têm maior probabilidade de serem merged.\n\n")
            else:
                f.write("Não há evidência estatística de que o tamanho influencie o status final do PR.\n\n")
            
            f.write(f"![RQ01](graficos/rq01_tamanho_vs_status.png)\n\n")
            f.write("---\n\n")
            
            # RQ02
            f.write("### RQ 02: Tempo de Análise vs Feedback Final\n\n")
            rq02 = self.resultados['RQ02']
            f.write(f"**Questão:** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?\n\n")
            f.write("**Resultados:**\n\n")
            f.write(f"- PRs **merged** levam em média **{rq02['merged_mean']:.2f} horas** ({rq02['merged_mean']/24:.2f} dias)\n")
            f.write(f"- PRs **closed** levam em média **{rq02['closed_mean']:.2f} horas** ({rq02['closed_mean']/24:.2f} dias)\n")
            f.write(f"- Teste Mann-Whitney U: U={rq02['u_stat']:.2f}, p={rq02['p_value']:.4f}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq02['significativo'] else '✗ Não significativo'}\n\n")
            f.write("**Interpretação:** ")
            if rq02['significativo']:
                if rq02['merged_mean'] < rq02['closed_mean']:
                    f.write("PRs que são merged tendem a ser analisados mais rapidamente.\n\n")
                else:
                    f.write("PRs que são merged tendem a levar mais tempo para serem analisados.\n\n")
            else:
                f.write("Não há evidência estatística de que o tempo de análise influencie o status final do PR.\n\n")
            
            f.write(f"![RQ02](graficos/rq02_tempo_vs_status.png)\n\n")
            f.write("---\n\n")
            
            # RQ03
            f.write("### RQ 03: Descrição dos PRs vs Feedback Final\n\n")
            rq03 = self.resultados['RQ03']
            f.write(f"**Questão:** Qual a relação entre a descrição dos PRs e o feedback final das revisões?\n\n")
            f.write("**Resultados:**\n\n")
            f.write(f"- PRs **merged** têm em média **{rq03['merged_mean']:.2f} caracteres** na descrição\n")
            f.write(f"- PRs **closed** têm em média **{rq03['closed_mean']:.2f} caracteres** na descrição\n")
            f.write(f"- Teste Mann-Whitney U: U={rq03['u_stat']:.2f}, p={rq03['p_value']:.4f}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq03['significativo'] else '✗ Não significativo'}\n\n")
            f.write("**Interpretação:** ")
            if rq03['significativo']:
                if rq03['merged_mean'] > rq03['closed_mean']:
                    f.write("Descrições mais detalhadas estão associadas a maior probabilidade de merge.\n\n")
                else:
                    f.write("Descrições mais curtas estão associadas a maior probabilidade de merge.\n\n")
            else:
                f.write("Não há evidência estatística de que o tamanho da descrição influencie o status final do PR.\n\n")
            
            f.write(f"![RQ03](graficos/rq03_descricao_vs_status.png)\n\n")
            f.write("---\n\n")
            
            # RQ04
            f.write("### RQ 04: Interações nos PRs vs Feedback Final\n\n")
            rq04 = self.resultados['RQ04']
            f.write(f"**Questão:** Qual a relação entre as interações nos PRs e o feedback final das revisões?\n\n")
            f.write("**Resultados - Comentários:**\n\n")
            f.write(f"- PRs **merged** têm em média **{rq04['merged_mean_comments']:.2f} comentários**\n")
            f.write(f"- PRs **closed** têm em média **{rq04['closed_mean_comments']:.2f} comentários**\n")
            f.write(f"- Teste Mann-Whitney U: U={rq04['u_stat_comments']:.2f}, p={rq04['p_value_comments']:.4f}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq04['significativo_comments'] else '✗ Não significativo'}\n\n")
            
            f.write("**Resultados - Participantes:**\n\n")
            f.write(f"- PRs **merged** têm em média **{rq04['merged_mean_participants']:.2f} participantes**\n")
            f.write(f"- PRs **closed** têm em média **{rq04['closed_mean_participants']:.2f} participantes**\n")
            f.write(f"- Teste Mann-Whitney U: U={rq04['u_stat_participants']:.2f}, p={rq04['p_value_participants']:.4f}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq04['significativo_participants'] else '✗ Não significativo'}\n\n")
            
            f.write("**Interpretação:** ")
            if rq04['significativo_comments'] or rq04['significativo_participants']:
                f.write("O nível de interação (comentários e/ou participantes) influencia o status final do PR.\n\n")
            else:
                f.write("Não há evidência estatística de que o nível de interação influencie o status final do PR.\n\n")
            
            f.write(f"![RQ04](graficos/rq04_interacoes_vs_status.png)\n\n")
            f.write("---\n\n")
            
            # Dimensão B: Número de Revisões
            f.write("## Dimensão B: Número de Revisões Realizadas\n\n")
            f.write("*Nota: O número de participantes é usado como proxy para o número de revisões.*\n\n")
            
            # RQ05
            f.write("### RQ 05: Tamanho dos PRs vs Número de Revisões\n\n")
            rq05 = self.resultados['RQ05']
            f.write(f"**Questão:** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?\n\n")
            f.write("**Resultados:**\n\n")
            f.write(f"- Correlação de Spearman: ρ={rq05['correlacao']:.4f}\n")
            f.write(f"- P-valor: p={rq05['p_value']:.4f}\n")
            f.write(f"- Interpretação: Correlação {rq05['interpretacao']}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq05['significativo'] else '✗ Não significativo'}\n\n")
            f.write("**Interpretação:** ")
            if rq05['significativo']:
                if rq05['correlacao'] > 0:
                    f.write("PRs maiores tendem a ter mais revisores participando.\n\n")
                else:
                    f.write("PRs menores tendem a ter mais revisores participando.\n\n")
            else:
                f.write("Não há evidência estatística de correlação entre o tamanho do PR e o número de revisões.\n\n")
            
            f.write(f"![RQ05](graficos/rq05_tamanho_vs_revisoes.png)\n\n")
            f.write("---\n\n")
            
            # RQ06
            f.write("### RQ 06: Tempo de Análise vs Número de Revisões\n\n")
            rq06 = self.resultados['RQ06']
            f.write(f"**Questão:** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?\n\n")
            f.write("**Resultados:**\n\n")
            f.write(f"- Correlação de Spearman: ρ={rq06['correlacao']:.4f}\n")
            f.write(f"- P-valor: p={rq06['p_value']:.4f}\n")
            f.write(f"- Interpretação: Correlação {rq06['interpretacao']}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq06['significativo'] else '✗ Não significativo'}\n\n")
            f.write("**Interpretação:** ")
            if rq06['significativo']:
                if rq06['correlacao'] > 0:
                    f.write("PRs que levam mais tempo tendem a ter mais revisores participando.\n\n")
                else:
                    f.write("PRs mais rápidos tendem a ter mais revisores participando.\n\n")
            else:
                f.write("Não há evidência estatística de correlação entre o tempo de análise e o número de revisões.\n\n")
            
            f.write(f"![RQ06](graficos/rq06_tempo_vs_revisoes.png)\n\n")
            f.write("---\n\n")
            
            # RQ07
            f.write("### RQ 07: Descrição dos PRs vs Número de Revisões\n\n")
            rq07 = self.resultados['RQ07']
            f.write(f"**Questão:** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?\n\n")
            f.write("**Resultados:**\n\n")
            f.write(f"- Correlação de Spearman: ρ={rq07['correlacao']:.4f}\n")
            f.write(f"- P-valor: p={rq07['p_value']:.4f}\n")
            f.write(f"- Interpretação: Correlação {rq07['interpretacao']}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq07['significativo'] else '✗ Não significativo'}\n\n")
            f.write("**Interpretação:** ")
            if rq07['significativo']:
                if rq07['correlacao'] > 0:
                    f.write("PRs com descrições mais detalhadas tendem a ter mais revisores participando.\n\n")
                else:
                    f.write("PRs com descrições mais curtas tendem a ter mais revisores participando.\n\n")
            else:
                f.write("Não há evidência estatística de correlação entre o tamanho da descrição e o número de revisões.\n\n")
            
            f.write(f"![RQ07](graficos/rq07_descricao_vs_revisoes.png)\n\n")
            f.write("---\n\n")
            
            # RQ08
            f.write("### RQ 08: Interações vs Número de Revisões\n\n")
            rq08 = self.resultados['RQ08']
            f.write(f"**Questão:** Qual a relação entre as interações nos PRs e o número de revisões realizadas?\n\n")
            f.write("**Resultados:**\n\n")
            f.write(f"- Correlação de Spearman: ρ={rq08['correlacao']:.4f}\n")
            f.write(f"- P-valor: p={rq08['p_value']:.4f}\n")
            f.write(f"- Interpretação: Correlação {rq08['interpretacao']}\n")
            f.write(f"- **Significância:** {'✓ Significativo' if rq08['significativo'] else '✗ Não significativo'}\n\n")
            f.write("**Interpretação:** ")
            if rq08['significativo']:
                if rq08['correlacao'] > 0:
                    f.write("PRs com mais comentários tendem a ter mais revisores participando (esperado).\n\n")
                else:
                    f.write("PRs com menos comentários tendem a ter mais revisores participando (contra-intuitivo).\n\n")
            else:
                f.write("Não há evidência estatística de correlação entre comentários e participantes.\n\n")
            
            f.write(f"![RQ08](graficos/rq08_interacoes_vs_revisoes.png)\n\n")
            f.write("---\n\n")
            
            # Conclusões
            f.write("## Conclusões Gerais\n\n")
            
            # Contar quantas RQs foram significativas
            sig_count = sum([
                self.resultados[f'RQ0{i}']['significativo'] for i in range(1, 5)
            ] + [
                self.resultados[f'RQ0{i}']['significativo'] for i in range(5, 9)
            ])
            
            f.write(f"Das 8 questões de pesquisa analisadas, **{sig_count} apresentaram resultados estatisticamente significativos** (p < 0.05).\n\n")
            
            f.write("### Principais Achados:\n\n")
            f.write("**Dimensão A - Feedback Final:**\n\n")
            
            for i in range(1, 5):
                rq = self.resultados[f'RQ0{i}']
                if rq['significativo']:
                    f.write(f"- ✓ **RQ0{i}:** {rq['titulo']} - Relação significativa encontrada\n")
                else:
                    f.write(f"- ✗ **RQ0{i}:** {rq['titulo']} - Sem relação significativa\n")
            
            f.write("\n**Dimensão B - Número de Revisões:**\n\n")
            
            for i in range(5, 9):
                rq = self.resultados[f'RQ0{i}']
                if rq['significativo']:
                    f.write(f"- ✓ **RQ0{i}:** {rq['titulo']} - Relação significativa encontrada\n")
                else:
                    f.write(f"- ✗ **RQ0{i}:** {rq['titulo']} - Sem relação significativa\n")
            
            f.write("\n---\n\n")
            
            # Metodologia
            f.write("## Metodologia\n\n")
            f.write("### Testes Estatísticos Utilizados:\n\n")
            f.write("1. **Teste de Mann-Whitney U:** Para comparar duas grupos independentes (PRs merged vs closed)\n")
            f.write("   - Não paramétrico, não assume distribuição normal\n")
            f.write("   - Apropriado para dados com outliers\n\n")
            f.write("2. **Correlação de Spearman:** Para medir a associação entre duas variáveis contínuas\n")
            f.write("   - Não paramétrica, baseada em ranks\n")
            f.write("   - Detecta relações monotônicas (não apenas lineares)\n\n")
            f.write("### Nível de Significância:\n\n")
            f.write("- α = 0.05 (5%)\n")
            f.write("- Resultados com p < 0.05 são considerados estatisticamente significativos\n\n")
            f.write("### Tratamento de Outliers:\n\n")
            f.write("- Outliers extremos foram tratados usando clipping nos percentis 1% e 99%\n")
            f.write("- Dados originais preservados para análises robustas\n\n")
            
            f.write("---\n\n")
            f.write(f"*Relatório gerado automaticamente pela Sprint 2 em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*\n")
        
        print(f"✓ Relatório salvo: relatorio_sprint2.md")
        print()
    
    def executar_analise_completa(self):
        """
        Executa a análise completa de todas as RQs
        """
        # Carregar dados
        if not self.carregar_dados():
            return False
        
        # Preparar dados
        self.preparar_dados()
        
        # Dimensão A: Feedback Final
        self.rq01_tamanho_vs_status()
        self.rq02_tempo_vs_status()
        self.rq03_descricao_vs_status()
        self.rq04_interacoes_vs_status()
        
        # Dimensão B: Número de Revisões
        self.rq05_tamanho_vs_revisoes()
        self.rq06_tempo_vs_revisoes()
        self.rq07_descricao_vs_revisoes()
        self.rq08_interacoes_vs_revisoes()
        
        # Gerar relatório final
        self.gerar_relatorio_final()
        
        print("=" * 80)
        print("✓ SPRINT 2 CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        print()
        print(f"📊 Gráficos salvos em: {self.caminho_graficos}")
        print(f"📄 Relatório completo: relatorio_sprint2.md")
        print()
        
        return True

def main():
    """
    Função principal para executar a Sprint 2
    """
    analisador = AnalisadorPRs()
    analisador.executar_analise_completa()

if __name__ == "__main__":
    main()

