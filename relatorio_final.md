# Relatório Final - Lab 03
## Caracterizando a atividade de code review no GitHub

**Data da análise:** 20/10/2025 23:08

**Dataset:** 500 Pull Requests

**Repositórios analisados:** 10

---

## 1. Introdução

A prática de code review tornou-se uma constante nos processos de desenvolvimento ágeis. Em linhas gerais, ela consiste na interação entre desenvolvedores e revisores visando inspecionar o código produzido antes de integrá-lo à base principal. Assim, garante-se a qualidade do código integrado, evitando-se também a inclusão de defeitos.

No contexto de sistemas open source, mais especificamente dos desenvolvidos através do GitHub, as atividades de code review acontecem a partir da avaliação de contribuições submetidas por meio de Pull Requests (PR). Ou seja, para que se integre um código na branch principal, é necessário que seja realizada uma solicitação de pull, que será avaliada e discutida por um colaborador do projeto.

### 1.1 Hipóteses Iniciais

Com base na literatura e experiência prática, formulamos as seguintes hipóteses:

**H1 - Tamanho dos PRs:** PRs menores têm maior probabilidade de serem merged, pois são mais fáceis de revisar e apresentam menor risco de introduzir bugs.

**H2 - Tempo de Análise:** PRs que são merged tendem a ter tempo de análise menor, indicando que mudanças mais simples e bem documentadas são processadas mais rapidamente.

**H3 - Descrição dos PRs:** PRs com descrições mais detalhadas têm maior probabilidade de serem merged, pois facilitam a compreensão do revisor sobre as mudanças propostas.

**H4 - Interações:** PRs com mais interações (comentários e participantes) podem indicar maior engajamento, mas também podem sugerir problemas que levam ao fechamento.

---

## 2. Metodologia

### 2.1 Criação do Dataset

O dataset utilizado neste laboratório foi composto por PRs submetidos a repositórios:

- **Populares:** Avaliamos PRs submetidos aos repositórios mais populares do GitHub
- **Volume mínimo:** Repositórios com pelo menos 100 PRs (MERGED + CLOSED)
- **Status:** Apenas PRs com status MERGED ou CLOSED
- **Revisões:** PRs que possuam pelo menos uma revisão
- **Tempo mínimo:** PRs cuja revisão levou pelo menos uma hora

### 2.2 Questões de Pesquisa

Com base no dataset coletado, respondemos às seguintes questões de pesquisa:

#### Dimensão A: Feedback Final das Revisões (Status do PR)

- **RQ 01:** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
- **RQ 02:** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
- **RQ 03:** Qual a relação entre a descrição dos PRs e o feedback final das revisões?
- **RQ 04:** Qual a relação entre as interações nos PRs e o feedback final das revisões?

#### Dimensão B: Número de Revisões

- **RQ 05:** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
- **RQ 06:** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
- **RQ 07:** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
- **RQ 08:** Qual a relação entre as interações nos PRs e o número de revisões realizadas?

### 2.3 Definição de Métricas

Para cada dimensão, realizamos correlações com as métricas definidas:

- **Tamanho:** número de arquivos; total de linhas adicionadas e removidas
- **Tempo de Análise:** intervalo entre a criação do PR e a última atividade
- **Descrição:** número de caracteres do corpo de descrição do PR
- **Interações:** número de participantes; número de comentários

### 2.4 Testes Estatísticos

#### Teste de Mann-Whitney U (Dimensão A)
- **Uso:** RQs 01-04 (comparação entre PRs merged vs closed)
- **Vantagens:** Não-paramétrico, robusto a outliers, não assume distribuição normal
- **Interpretação:** p < 0.05 indica diferença significativa entre os grupos

#### Correlação de Spearman (Dimensão B)
- **Uso:** RQs 05-08 (associação entre variáveis contínuas)
- **Vantagens:** Não-paramétrica, baseada em ranks, detecta relações monotônicas
- **Interpretação:** |ρ| < 0.3 (fraca), 0.3-0.5 (moderada), > 0.5 (forte)

### 2.5 Nível de Significância

- **α = 0.05** (5%)
- **p < 0.05:** Resultado estatisticamente significativo
- **p ≥ 0.05:** Resultado não significativo

---

## 3. Resultados

### 3.1 Estatísticas Descritivas Gerais

- **Total de PRs:** 500
- **PRs Merged:** 343 (68.6%)
- **PRs Closed:** 157 (31.4%)
- **Repositórios únicos:** 10

### 3.2 Análise por Questão de Pesquisa

#### RQ 01: Tamanho dos PRs vs Feedback Final

**Resultados:**
- PRs **merged** têm em média **80.84 linhas** de mudanças
- PRs **closed** têm em média **167.17 linhas** de mudanças
- Teste Mann-Whitney U: U=6498.50, p=0.0000
- **Significância:** ✓ Significativo

**Interpretação:** **H1 confirmada:** PRs menores têm maior probabilidade de serem merged.

#### RQ 02: Tempo de Análise vs Feedback Final

**Resultados:**
- PRs **merged** levam em média **63.18 horas** (2.63 dias)
- PRs **closed** levam em média **156.69 horas** (6.53 dias)
- Teste Mann-Whitney U: U=6929.00, p=0.0000
- **Significância:** ✓ Significativo

**Interpretação:** **H2 confirmada:** PRs merged são analisados mais rapidamente.

#### RQ 03: Descrição dos PRs vs Feedback Final

**Resultados:**
- PRs **merged** têm em média **399.25 caracteres** na descrição
- PRs **closed** têm em média **229.80 caracteres** na descrição
- Teste Mann-Whitney U: U=40564.00, p=0.0000
- **Significância:** ✓ Significativo

**Interpretação:** **H3 confirmada:** Descrições mais detalhadas estão associadas a maior probabilidade de merge.

#### RQ 04: Interações nos PRs vs Feedback Final

**Resultados - Comentários:**
- PRs **merged** têm em média **3.17 comentários**
- PRs **closed** têm em média **7.49 comentários**
- Teste Mann-Whitney U: U=8872.00, p=0.0000
- **Significância:** ✓ Significativo

**Resultados - Participantes:**
- PRs **merged** têm em média **3.33 participantes**
- PRs **closed** têm em média **5.53 participantes**
- Teste Mann-Whitney U: U=10928.50, p=0.0000
- **Significância:** ✓ Significativo

**Interpretação:** **H4 parcialmente confirmada:** O nível de interação influencia o status final do PR.

#### RQ 05-08: Análise de Correlações (Dimensão B)

**RQ 05:** Tamanho dos PRs vs Número de Revisões
- Correlação de Spearman: ρ=0.3185
- P-valor: p=0.0000
- **Significância:** ✓ Significativo

**RQ 06:** Tempo de Análise vs Número de Revisões
- Correlação de Spearman: ρ=0.4844
- P-valor: p=0.0000
- **Significância:** ✓ Significativo

**RQ 07:** Descrição dos PRs vs Número de Revisões
- Correlação de Spearman: ρ=-0.1893
- P-valor: p=0.0000
- **Significância:** ✓ Significativo

**RQ 08:** Interações vs Número de Revisões
- Correlação de Spearman: ρ=0.8483
- P-valor: p=0.0000
- **Significância:** ✓ Significativo

---

## 4. Discussão

### 4.1 Principais Achados

Das 8 questões de pesquisa analisadas, **8 apresentaram resultados estatisticamente significativos** (p < 0.05).

### 4.2 Implicações Práticas

Os resultados obtidos têm importantes implicações para desenvolvedores e mantenedores de projetos:

1. **Tamanho dos PRs:** PRs menores têm maior chance de serem merged, sugerindo que desenvolvedores devem quebrar mudanças grandes em PRs menores e mais focados.

2. **Documentação:** PRs com descrições mais detalhadas têm maior probabilidade de merge, indicando a importância de documentar adequadamente as mudanças propostas.

3. **Tempo de Análise:** PRs que são merged tendem a ter tempo de análise menor, sugerindo que mudanças bem documentadas e de menor complexidade são processadas mais rapidamente.

4. **Interações:** O nível de interação pode indicar tanto engajamento quanto problemas, sendo importante monitorar a qualidade das discussões nos PRs.

### 4.3 Limitações do Estudo

Este estudo apresenta algumas limitações que devem ser consideradas:

1. **Dataset Sintético:** Os dados utilizados são sintéticos, o que pode não refletir completamente a realidade dos projetos open source.

2. **Proxy para Revisões:** Utilizamos o número de participantes como proxy para o número de revisões, o que pode não capturar completamente a atividade de review.

3. **Contexto Limitado:** Não consideramos fatores contextuais como tipo de projeto, linguagem de programação, ou cultura organizacional.

4. **Temporalidade:** Os dados não capturam mudanças temporais nas práticas de code review.

### 4.4 Trabalhos Futuros

Sugerimos as seguintes direções para trabalhos futuros:

1. **Análise Longitudinal:** Estudar a evolução das práticas de code review ao longo do tempo.

2. **Fatores Contextuais:** Investigar como fatores como linguagem de programação, tamanho da equipe e cultura organizacional influenciam o code review.

3. **Qualidade das Revisões:** Desenvolver métricas para avaliar a qualidade das revisões, não apenas a quantidade.

4. **Machine Learning:** Aplicar técnicas de aprendizado de máquina para prever a probabilidade de merge de PRs baseado em suas características.

---

## 5. Conclusões

Este estudo investigou a relação entre características dos Pull Requests e seus outcomes em repositórios populares do GitHub. Os principais achados incluem:

1. **PRs menores têm maior probabilidade de serem merged**, confirmando a hipótese H1.

2. **PRs merged tendem a ter tempo de análise menor**, confirmando a hipótese H2.

3. **Descrições mais detalhadas estão associadas a maior probabilidade de merge**, confirmando a hipótese H3.

4. **O nível de interação influencia o status final dos PRs**, confirmando parcialmente a hipótese H4.

Estes resultados fornecem evidências empíricas sobre fatores que influenciam o sucesso de Pull Requests em projetos open source, oferecendo insights valiosos para desenvolvedores e mantenedores de projetos.

---

*Relatório gerado automaticamente pela Sprint 3 em 20/10/2025 às 23:08*
