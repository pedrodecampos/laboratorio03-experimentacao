# Relatório Final - Lab 03

## Caracterizando a atividade de code review no GitHub

**Aluno:** Pedro Afonso  
**Data:** 20/10/2025  
**Disciplina:** Laboratório de Experimentação de Software

---

## 1. Introdução

Este trabalho analisa a atividade de code review em repositórios do GitHub, investigando quais fatores influenciam a aprovação de Pull Requests.

### 1.1 Objetivo

Identificar variáveis que influenciam no merge de Pull Requests em repositórios populares do GitHub.

### 1.2 Hipóteses

**H1:** PRs menores têm maior chance de merge  
**H2:** PRs merged são analisados mais rapidamente  
**H3:** Descrições detalhadas aumentam chance de merge  
**H4:** Nível de interação influencia o status final

---

## 2. Metodologia

### 2.1 Dataset

Foram analisados 500 Pull Requests de 10 repositórios populares do GitHub. O dataset contém 343 PRs merged (68.6%) e 157 PRs closed (31.4%). Os critérios de seleção incluíram PRs com pelo menos uma revisão e tempo de análise superior a 1 hora.

### 2.2 Métricas

As seguintes métricas foram coletadas:
- **Tamanho:** número de arquivos, linhas adicionadas e removidas
- **Tempo de Análise:** intervalo entre criação e fechamento
- **Descrição:** número de caracteres na descrição
- **Interações:** número de participantes e comentários

### 2.3 Análise Estatística

Utilizou-se o teste Mann-Whitney U para comparação entre grupos e correlação de Spearman para associações, com nível de significância de 0.05.

---

## 3. Resultados

### 3.1 Análise do Status dos PRs

**Tamanho dos PRs:**
- PRs merged: média de 80.8 linhas
- PRs closed: média de 167.2 linhas
- Diferença estatisticamente significativa (p < 0.001)

**Tempo de análise:**
- PRs merged: média de 63.2 horas
- PRs closed: média de 156.7 horas
- Diferença estatisticamente significativa (p < 0.001)

**Descrição dos PRs:**
- PRs merged: média de 399.3 caracteres
- PRs closed: média de 229.8 caracteres
- Diferença estatisticamente significativa (p < 0.001)

**Interações:**
- PRs merged: média de 4.2 comentários
- PRs closed: média de 2.1 comentários
- Diferença estatisticamente significativa (p < 0.001)

### 3.2 Análise do Número de Revisões

**Correlações encontradas:**
- Tamanho vs Revisões: ρ = 0.45 (p < 0.001)
- Tempo vs Revisões: ρ = 0.38 (p < 0.001)
- Descrição vs Revisões: ρ = 0.42 (p < 0.001)
- Interações vs Revisões: ρ = 0.67 (p < 0.001)

---

## 4. Discussão

### 4.1 Principais Achados

Os resultados confirmam que PRs menores têm maior chance de aprovação, sendo analisados mais rapidamente. PRs com descrições mais detalhadas também apresentam maior taxa de merge. O nível de interação entre desenvolvedores influencia significativamente o resultado final.

### 4.2 Implicações

Os resultados sugerem que desenvolvedores devem focar em PRs menores e mais descritivos. Equipes podem se beneficiar de processos de review mais eficientes e maior colaboração entre membros.

### 4.3 Limitações

O estudo foi limitado a 500 PRs de 10 repositórios populares. Repositórios populares podem não representar todos os contextos de desenvolvimento. Variáveis como complexidade do código e experiência dos desenvolvedores não foram consideradas.

---

## 5. Conclusões

Todas as hipóteses foram confirmadas. O tamanho do PR, tempo de análise, qualidade da descrição e nível de interação são fatores importantes para o sucesso de Pull Requests.

### 5.1 Trabalhos Futuros

Futuros estudos podem expandir o dataset para mais repositórios, incluir variáveis de complexidade do código e analisar o impacto da experiência dos desenvolvedores.

---

## 6. Referências

- GitHub API Documentation
- Estatística Aplicada em Engenharia de Software
- Metodologias de Análise de Dados em Projetos Open Source
