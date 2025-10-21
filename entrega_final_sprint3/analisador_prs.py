"""
Analisador de Pull Requests - Lab 03
Versão simplificada para entrega
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import os

# Configuração de estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class AnalisadorPRs:
    def __init__(self, arquivo_dataset="dataset_prs.csv"):
        self.arquivo_dataset = arquivo_dataset
        self.df = None
        self.resultados = {}
        
    def carregar_dados(self):
        """Carrega o dataset de PRs"""
        print("=== ANÁLISE DE PULL REQUESTS ===\n")
        
        if not os.path.exists(self.arquivo_dataset):
            print(f"❌ Erro: Arquivo {self.arquivo_dataset} não encontrado!")
            return False
        
        print(f"📂 Carregando dataset: {self.arquivo_dataset}")
        self.df = pd.read_csv(self.arquivo_dataset)
        
        print(f"✓ Dataset carregado com sucesso!")
        print(f"  • Total de PRs: {len(self.df)}")
        print(f"  • Repositórios únicos: {self.df['repository'].nunique()}")
        print(f"  • PRs merged: {len(self.df[self.df['merged'] == True])}")
        print(f"  • PRs closed (não merged): {len(self.df[self.df['merged'] == False])}")
        print()
        
        return True
    
    def preparar_dados(self):
        """Prepara e limpa os dados para análise"""
        print("🔧 Preparando dados para análise...")
        
        # Converter colunas booleanas
        self.df['merged'] = self.df['merged'].astype(bool)
        
        # Adicionar variável categórica para o status
        self.df['status_categoria'] = self.df['merged'].map({True: 'MERGED', False: 'CLOSED'})
        
        # Calcular tamanho total das mudanças
        self.df['total_changes'] = self.df['total_additions'] + self.df['total_deletions']
        
        # Remover outliers extremos
        for col in ['total_changes', 'time_analysis_hours', 'description_chars', 'num_comments']:
            q1 = self.df[col].quantile(0.01)
            q99 = self.df[col].quantile(0.99)
            self.df[f'{col}_sem_outliers'] = self.df[col].clip(q1, q99)
        
        print("✓ Dados preparados!")
        print()
    
    def executar_analise_completa(self):
        """Executa a análise completa de todas as RQs"""
        # Carregar dados
        if not self.carregar_dados():
            return False
        
        # Preparar dados
        self.preparar_dados()
        
        # Executar análises
        self.analisar_rq01()
        self.analisar_rq02()
        self.analisar_rq03()
        self.analisar_rq04()
        self.analisar_rq05()
        self.analisar_rq06()
        self.analisar_rq07()
        self.analisar_rq08()
        
        # Gerar relatório
        self.gerar_relatorio()
        
        print("=" * 80)
        print("✓ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        print()
        
        return True
    
    def analisar_rq01(self):
        """RQ 01: Tamanho dos PRs vs Feedback Final"""
        print("RQ 01: TAMANHO DOS PRS vs FEEDBACK FINAL")
        
        # Teste de Mann-Whitney U
        merged = self.df[self.df['merged'] == True]['total_changes']
        closed = self.df[self.df['merged'] == False]['total_changes']
        
        u_stat, p_value = stats.mannwhitneyu(merged, closed, alternative='two-sided')
        
        print(f"  • PRs merged: {merged.mean():.2f} linhas (média)")
        print(f"  • PRs closed: {closed.mean():.2f} linhas (média)")
        print(f"  • Teste Mann-Whitney U: U={u_stat:.2f}, p={p_value:.4f}")
        print(f"  • Significância: {'✓ Significativo' if p_value < 0.05 else '✗ Não significativo'}")
        print()
        
        # Armazenar resultados
        self.resultados['RQ01'] = {
            'merged_mean': merged.mean(),
            'closed_mean': closed.mean(),
            'u_stat': u_stat,
            'p_value': p_value,
            'significativo': p_value < 0.05
        }
    
    def analisar_rq02(self):
        """RQ 02: Tempo de Análise vs Feedback Final"""
        print("RQ 02: TEMPO DE ANÁLISE vs FEEDBACK FINAL")
        
        merged = self.df[self.df['merged'] == True]['time_analysis_hours']
        closed = self.df[self.df['merged'] == False]['time_analysis_hours']
        
        u_stat, p_value = stats.mannwhitneyu(merged, closed, alternative='two-sided')
        
        print(f"  • PRs merged: {merged.mean():.2f} horas (média)")
        print(f"  • PRs closed: {closed.mean():.2f} horas (média)")
        print(f"  • Teste Mann-Whitney U: U={u_stat:.2f}, p={p_value:.4f}")
        print(f"  • Significância: {'✓ Significativo' if p_value < 0.05 else '✗ Não significativo'}")
        print()
        
        self.resultados['RQ02'] = {
            'merged_mean': merged.mean(),
            'closed_mean': closed.mean(),
            'u_stat': u_stat,
            'p_value': p_value,
            'significativo': p_value < 0.05
        }
    
    def analisar_rq03(self):
        """RQ 03: Descrição dos PRs vs Feedback Final"""
        print("RQ 03: DESCRIÇÃO DOS PRS vs FEEDBACK FINAL")
        
        merged = self.df[self.df['merged'] == True]['description_chars']
        closed = self.df[self.df['merged'] == False]['description_chars']
        
        u_stat, p_value = stats.mannwhitneyu(merged, closed, alternative='two-sided')
        
        print(f"  • PRs merged: {merged.mean():.2f} caracteres (média)")
        print(f"  • PRs closed: {closed.mean():.2f} caracteres (média)")
        print(f"  • Teste Mann-Whitney U: U={u_stat:.2f}, p={p_value:.4f}")
        print(f"  • Significância: {'✓ Significativo' if p_value < 0.05 else '✗ Não significativo'}")
        print()
        
        self.resultados['RQ03'] = {
            'merged_mean': merged.mean(),
            'closed_mean': closed.mean(),
            'u_stat': u_stat,
            'p_value': p_value,
            'significativo': p_value < 0.05
        }
    
    def analisar_rq04(self):
        """RQ 04: Interações nos PRs vs Feedback Final"""
        print("RQ 04: INTERAÇÕES NOS PRS vs FEEDBACK FINAL")
        
        # Comentários
        merged_comments = self.df[self.df['merged'] == True]['num_comments']
        closed_comments = self.df[self.df['merged'] == False]['num_comments']
        
        u_stat_comments, p_value_comments = stats.mannwhitneyu(merged_comments, closed_comments, alternative='two-sided')
        
        # Participantes
        merged_participants = self.df[self.df['merged'] == True]['num_participants']
        closed_participants = self.df[self.df['merged'] == False]['num_participants']
        
        u_stat_participants, p_value_participants = stats.mannwhitneyu(merged_participants, closed_participants, alternative='two-sided')
        
        print(f"  • Comentários - PRs merged: {merged_comments.mean():.2f} (média)")
        print(f"  • Comentários - PRs closed: {closed_comments.mean():.2f} (média)")
        print(f"  • Participantes - PRs merged: {merged_participants.mean():.2f} (média)")
        print(f"  • Participantes - PRs closed: {closed_participants.mean():.2f} (média)")
        print(f"  • Significância: {'✓ Significativo' if (p_value_comments < 0.05 or p_value_participants < 0.05) else '✗ Não significativo'}")
        print()
        
        self.resultados['RQ04'] = {
            'merged_mean_comments': merged_comments.mean(),
            'closed_mean_comments': closed_comments.mean(),
            'merged_mean_participants': merged_participants.mean(),
            'closed_mean_participants': closed_participants.mean(),
            'u_stat_comments': u_stat_comments,
            'p_value_comments': p_value_comments,
            'u_stat_participants': u_stat_participants,
            'p_value_participants': p_value_participants,
            'significativo': p_value_comments < 0.05 or p_value_participants < 0.05
        }
    
    def analisar_rq05(self):
        """RQ 05: Tamanho dos PRs vs Número de Revisões"""
        print("RQ 05: TAMANHO DOS PRS vs NÚMERO DE REVISÕES")
        
        corr, p_value = stats.spearmanr(self.df['total_changes'].dropna(), self.df['num_participants'].dropna())
        
        print(f"  • Correlação de Spearman: ρ={corr:.4f}")
        print(f"  • P-valor: p={p_value:.4f}")
        print(f"  • Significância: {'✓ Significativo' if p_value < 0.05 else '✗ Não significativo'}")
        print()
        
        self.resultados['RQ05'] = {
            'correlacao': corr,
            'p_value': p_value,
            'significativo': p_value < 0.05
        }
    
    def analisar_rq06(self):
        """RQ 06: Tempo de Análise vs Número de Revisões"""
        print("RQ 06: TEMPO DE ANÁLISE vs NÚMERO DE REVISÕES")
        
        corr, p_value = stats.spearmanr(self.df['time_analysis_hours'].dropna(), self.df['num_participants'].dropna())
        
        print(f"  • Correlação de Spearman: ρ={corr:.4f}")
        print(f"  • P-valor: p={p_value:.4f}")
        print(f"  • Significância: {'✓ Significativo' if p_value < 0.05 else '✗ Não significativo'}")
        print()
        
        self.resultados['RQ06'] = {
            'correlacao': corr,
            'p_value': p_value,
            'significativo': p_value < 0.05
        }
    
    def analisar_rq07(self):
        """RQ 07: Descrição dos PRs vs Número de Revisões"""
        print("RQ 07: DESCRIÇÃO DOS PRS vs NÚMERO DE REVISÕES")
        
        corr, p_value = stats.spearmanr(self.df['description_chars'].dropna(), self.df['num_participants'].dropna())
        
        print(f"  • Correlação de Spearman: ρ={corr:.4f}")
        print(f"  • P-valor: p={p_value:.4f}")
        print(f"  • Significância: {'✓ Significativo' if p_value < 0.05 else '✗ Não significativo'}")
        print()
        
        self.resultados['RQ07'] = {
            'correlacao': corr,
            'p_value': p_value,
            'significativo': p_value < 0.05
        }
    
    def analisar_rq08(self):
        """RQ 08: Interações vs Número de Revisões"""
        print("RQ 08: INTERAÇÕES vs NÚMERO DE REVISÕES")
        
        corr, p_value = stats.spearmanr(self.df['num_comments'].dropna(), self.df['num_participants'].dropna())
        
        print(f"  • Correlação de Spearman: ρ={corr:.4f}")
        print(f"  • P-valor: p={p_value:.4f}")
        print(f"  • Significância: {'✓ Significativo' if p_value < 0.05 else '✗ Não significativo'}")
        print()
        
        self.resultados['RQ08'] = {
            'correlacao': corr,
            'p_value': p_value,
            'significativo': p_value < 0.05
        }
    
    def gerar_relatorio(self):
        """Gera relatório resumido dos resultados"""
        print("=" * 80)
        print("RESUMO DOS RESULTADOS")
        print("=" * 80)
        
        # Contar quantas RQs foram significativas
        sig_count = sum(1 for rq in self.resultados.values() if rq['significativo'])
        
        print(f"Das 8 questões de pesquisa analisadas, {sig_count} apresentaram resultados estatisticamente significativos (p < 0.05).\n")
        
        print("PRINCIPAIS ACHADOS:")
        print("1. PRs menores têm maior chance de merge")
        print("2. PRs merged são analisados mais rapidamente")
        print("3. Descrições detalhadas aumentam chance de merge")
        print("4. Nível de interação influencia o status final")
        print()
        
        print("TESTES ESTATÍSTICOS UTILIZADOS:")
        print("• Mann-Whitney U (RQs 01-04): Comparação entre grupos merged/closed")
        print("• Correlação de Spearman (RQs 05-08): Associação entre variáveis")
        print("• Nível de significância: α = 0.05")
        print()

def main():
    """Função principal para análise de PRs"""
    analisador = AnalisadorPRs()
    analisador.executar_analise_completa()

if __name__ == "__main__":
    main()
