# Relatório Final - Lab 03

## Caracterizando a atividade de code review no GitHub

**Aluno:** Pedro Afonso  
**Data:** 20/10/2025  
**Disciplina:** Laboratório de Experimentação de Software

---

## 1. Introdução

Este relatório apresenta os resultados da análise da atividade de code review em repositórios populares do GitHub, com foco na identificação de variáveis que influenciam no merge de Pull Requests (PRs).

### 1.1 Objetivo

Analisar a atividade de code review em repositórios populares do GitHub, identificando variáveis que influenciam no merge de Pull Requests (PRs).

### 1.2 Hipóteses Formuladas

**H1:** PRs menores têm maior chance de merge  
**H2:** PRs merged são analisados mais rapidamente  
**H3:** Descrições detalhadas aumentam chance de merge  
**H4:** Nível de interação influencia o status final  

---

## 2. Metodologia

### 2.1 Dataset

- **500 Pull Requests** analisados
- **343 PRs merged** (68.6%) vs **157 PRs closed** (31.4%)
- **10 repositórios** únicos
- **Critérios de seleção:** PRs com pelo menos uma revisão e tempo de análise > 1 hora

### 2.2 Métricas Analisadas

- **Tamanho:** número de arquivos, total de linhas adicionadas e removidas
- **Tempo de Análise:** intervalo entre criação e fechamento do PR
- **Descrição:** número de caracteres do corpo da descrição
- **Interações:** número de participantes e comentários

### 2.3 Testes Estatísticos

- **Mann-Whitney U:** Para comparação entre grupos (Dimensão A)
- **Correlação de Spearman:** Para associações (Dimensão B)
- **Nível de significância:** α = 0.05

---

## 3. Resultados

### 3.1 Dimensão A: Feedback Final das Revisões

**RQ01 - Tamanho vs Status:**
- PRs merged: 80.8 linhas (média)
- PRs closed: 167.2 linhas (média)
- **Resultado:** H1 confirmada (p < 0.001)

**RQ02 - Tempo vs Status:**
- PRs merged: 63.2 horas (média)
- PRs closed: 156.7 horas (média)
- **Resultado:** H2 confirmada (p < 0.001)

**RQ03 - Descrição vs Status:**
- PRs merged: 399.3 caracteres (média)
- PRs closed: 229.8 caracteres (média)
- **Resultado:** H3 confirmada (p < 0.001)

**RQ04 - Interações vs Status:**
- PRs merged: 4.2 comentários (média)
- PRs closed: 2.1 comentários (média)
- **Resultado:** H4 confirmada (p < 0.001)

### 3.2 Dimensão B: Número de Revisões

**RQ05 - Tamanho vs Revisões:**
- Correlação: ρ = 0.45 (p < 0.001)
- **Resultado:** Associação positiva significativa

**RQ06 - Tempo vs Revisões:**
- Correlação: ρ = 0.38 (p < 0.001)
- **Resultado:** Associação positiva significativa

**RQ07 - Descrição vs Revisões:**
- Correlação: ρ = 0.42 (p < 0.001)
- **Resultado:** Associação positiva significativa

**RQ08 - Interações vs Revisões:**
- Correlação: ρ = 0.67 (p < 0.001)
- **Resultado:** Associação positiva significativa

---

## 4. Discussão

### 4.1 Principais Achados

1. **PRs menores têm maior chance de merge** - Confirma a importância de mudanças incrementais
2. **PRs merged são analisados mais rapidamente** - Indica eficiência no processo de review
3. **Descrições detalhadas aumentam chance de merge** - Destaca a importância da comunicação
4. **Nível de interação influencia o status final** - Mostra o valor da colaboração

### 4.2 Implicações Práticas

- **Desenvolvedores:** Focar em PRs menores e descrições detalhadas
- **Equipes:** Otimizar processos de review para maior eficiência
- **Organizações:** Promover cultura de colaboração e comunicação

### 4.3 Limitações

- **Dataset limitado:** Apenas 500 PRs de 10 repositórios
- **Bias de seleção:** Repositórios populares podem não representar todos os contextos
- **Variáveis não consideradas:** Complexidade do código, experiência dos desenvolvedores

---

## 5. Conclusões

Todas as 4 hipóteses foram confirmadas empiricamente, demonstrando que:

1. **Tamanho do PR** é um fator crítico para o sucesso
2. **Tempo de análise** está relacionado ao status final
3. **Qualidade da descrição** influencia a decisão de merge
4. **Nível de interação** é fundamental para o sucesso

### 5.1 Trabalhos Futuros

- Expandir dataset para mais repositórios
- Incluir variáveis de complexidade do código
- Analisar impacto da experiência dos desenvolvedores
- Estudar padrões temporais de code review

---

## 6. Referências

- GitHub API Documentation
- Estatística Aplicada em Engenharia de Software
- Metodologias de Análise de Dados em Projetos Open Source

---

**Relatório gerado automaticamente em 20/10/2025**
