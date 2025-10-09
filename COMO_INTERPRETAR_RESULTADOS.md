# Como Interpretar os Resultados da Sprint 2

Este guia ajuda você a entender e interpretar os resultados das análises estatísticas realizadas na Sprint 2.

## Conceitos Básicos

### P-valor

O **p-valor** indica a probabilidade de observar os dados (ou mais extremos) assumindo que não há relação entre as variáveis (hipótese nula).

- **p < 0.05**: Resultado **estatisticamente significativo** ✓
  - Há evidência suficiente de que existe uma relação
  - Podemos rejeitar a hipótese nula com 95% de confiança
  
- **p ≥ 0.05**: Resultado **não significativo** ✗
  - Não há evidência estatística suficiente de uma relação
  - Não podemos descartar o acaso

### Correlação de Spearman (ρ)

Mede a força e direção da associação entre duas variáveis:

**Intensidade:**
- |ρ| < 0.10: Muito fraca (praticamente nenhuma correlação)
- 0.10 ≤ |ρ| < 0.30: Fraca
- 0.30 ≤ |ρ| < 0.50: Moderada
- 0.50 ≤ |ρ| < 0.70: Forte
- |ρ| ≥ 0.70: Muito forte

**Direção:**
- ρ > 0: Correlação **positiva** (quando uma variável aumenta, a outra tende a aumentar)
- ρ < 0: Correlação **negativa** (quando uma variável aumenta, a outra tende a diminuir)

**Exemplo:**
```
ρ = 0.45, p = 0.001
```
Interpretação: Há uma correlação **moderada positiva** e **estatisticamente significativa** entre as variáveis.

### Teste de Mann-Whitney U

Compara se dois grupos independentes têm distribuições diferentes.

- **U grande, p pequeno**: Os grupos são significativamente diferentes
- **U pequeno, p grande**: Os grupos não diferem significativamente

**Exemplo:**
```
PRs MERGED: média = 150 linhas
PRs CLOSED: média = 300 linhas
U = 15000, p = 0.003
```
Interpretação: PRs merged têm **significativamente menos** linhas que PRs closed.

## Interpretando Cada Questão de Pesquisa

### RQ 01: Tamanho dos PRs vs Feedback Final

**O que estamos testando:**
- PRs merged têm tamanho diferente de PRs closed?

**Como interpretar:**
- Se p < 0.05 E média(merged) < média(closed):
  - ✓ PRs menores têm maior chance de serem aceitos
  
- Se p < 0.05 E média(merged) > média(closed):
  - ✓ PRs maiores têm maior chance de serem aceitos (improvável)
  
- Se p ≥ 0.05:
  - ✗ O tamanho não influencia significativamente a aceitação

### RQ 02: Tempo de Análise vs Feedback Final

**O que estamos testando:**
- PRs merged levam tempo diferente para análise que PRs closed?

**Como interpretar:**
- Se p < 0.05 E média(merged) < média(closed):
  - ✓ PRs aceitos são analisados mais rapidamente
  
- Se p < 0.05 E média(merged) > média(closed):
  - ✓ PRs aceitos levam mais tempo (mais cuidado na análise?)
  
- Se p ≥ 0.05:
  - ✗ O tempo não influencia significativamente a aceitação

### RQ 03: Descrição dos PRs vs Feedback Final

**O que estamos testando:**
- PRs com descrições mais longas têm maior chance de serem aceitos?

**Como interpretar:**
- Se p < 0.05 E média(merged) > média(closed):
  - ✓ Descrições mais detalhadas aumentam a chance de aceitação
  
- Se p < 0.05 E média(merged) < média(closed):
  - ✓ Descrições mais curtas são melhores (improvável)
  
- Se p ≥ 0.05:
  - ✗ O tamanho da descrição não influencia a aceitação

### RQ 04: Interações nos PRs vs Feedback Final

**O que estamos testando:**
- PRs com mais comentários/participantes têm maior chance de serem aceitos?

**Como interpretar:**
- Se p < 0.05 para comentários:
  - ✓ O nível de discussão influencia o resultado
  
- Se p < 0.05 para participantes:
  - ✓ O engajamento da comunidade influencia o resultado
  
- Se p ≥ 0.05:
  - ✗ As interações não influenciam significativamente

### RQ 05: Tamanho dos PRs vs Número de Revisões

**O que estamos testando:**
- PRs maiores atraem mais revisores?

**Como interpretar:**
- Se p < 0.05 E ρ > 0:
  - ✓ PRs maiores atraem mais revisores (precisam de mais olhos)
  
- Se p < 0.05 E ρ < 0:
  - ✓ PRs menores atraem mais revisores (improvável)
  
- Se p ≥ 0.05:
  - ✗ O tamanho não afeta o número de revisores

### RQ 06: Tempo de Análise vs Número de Revisões

**O que estamos testando:**
- Mais revisores fazem o PR levar mais tempo?

**Como interpretar:**
- Se p < 0.05 E ρ > 0:
  - ✓ Mais revisores = mais tempo (mais discussões)
  
- Se p < 0.05 E ρ < 0:
  - ✓ Mais revisores = menos tempo (análise paralela?)
  
- Se p ≥ 0.05:
  - ✗ O número de revisores não afeta o tempo

### RQ 07: Descrição dos PRs vs Número de Revisões

**O que estamos testando:**
- Descrições mais longas atraem mais revisores?

**Como interpretar:**
- Se p < 0.05 E ρ > 0:
  - ✓ Descrições detalhadas atraem mais revisores
  
- Se p < 0.05 E ρ < 0:
  - ✓ Descrições curtas atraem mais revisores (improvável)
  
- Se p ≥ 0.05:
  - ✗ A descrição não afeta o número de revisores

### RQ 08: Interações vs Número de Revisões

**O que estamos testando:**
- Mais comentários indicam mais revisores participando?

**Como interpretar:**
- Se p < 0.05 E ρ > 0 (forte):
  - ✓ Há uma relação clara: mais revisores = mais discussão
  
- Esta RQ geralmente deve mostrar correlação positiva forte, pois mais participantes naturalmente levam a mais comentários.

## Exemplos Práticos de Interpretação

### Exemplo 1: Resultado Significativo

```
RQ 01: Tamanho dos PRs vs Feedback Final

Estatísticas:
- PRs MERGED: média = 156.43 linhas
- PRs CLOSED: média = 287.92 linhas
- Teste Mann-Whitney U: U=125847.50, p=0.0001

Interpretação:
✓ Resultado estatisticamente significativo
✓ PRs merged têm em média 131 linhas a menos que PRs closed
✓ Conclusão: PRs menores têm MAIOR PROBABILIDADE de serem aceitos
```

### Exemplo 2: Resultado Não Significativo

```
RQ 03: Descrição dos PRs vs Feedback Final

Estatísticas:
- PRs MERGED: média = 423.15 caracteres
- PRs CLOSED: média = 398.72 caracteres
- Teste Mann-Whitney U: U=89234.00, p=0.1245

Interpretação:
✗ Resultado NÃO estatisticamente significativo (p > 0.05)
✗ Não há evidência de que o tamanho da descrição influencie o status
✗ Conclusão: A extensão da descrição NÃO afeta a aceitação do PR
```

### Exemplo 3: Correlação Moderada

```
RQ 05: Tamanho dos PRs vs Número de Revisões

Estatísticas:
- Correlação de Spearman: ρ=0.38
- P-valor: p=0.0003

Interpretação:
✓ Correlação moderada positiva
✓ Estatisticamente significativa
✓ Conclusão: PRs maiores tendem a ter MAIS revisores, mas a relação não é muito forte
```

## Dicas de Análise

### 1. Sempre olhe p-valor primeiro
Se p ≥ 0.05, a correlação/diferença pode ser apenas acaso.

### 2. Magnitude importa
Um resultado pode ser significativo (p < 0.05) mas ter efeito pequeno (ρ = 0.12).

### 3. Causalidade ≠ Correlação
- Correlação significa: "as variáveis se movem juntas"
- NÃO significa: "uma causa a outra"
- Exemplo: PRs maiores atraem mais revisores OU PRs complexos ficam maiores E precisam de mais revisores?

### 4. Contexto é importante
- Compare as médias, não apenas o p-valor
- Um PR com 100 linhas vs 105 linhas pode ser significativo, mas a diferença prática é pequena

### 5. Outliers
- Os gráficos mostram dados sem outliers extremos (1% - 99%)
- Isso ajuda a visualizar, mas os testes usam todos os dados
- Outliers são esperados em dados reais de GitHub

## Perguntas Frequentes

**P: Um p-valor de 0.051 significa que não há relação?**

R: Não. Significa que não temos evidência estatística **suficiente** ao nível de 95% de confiança. Pode haver uma relação, mas precisaríamos de mais dados.

**P: Uma correlação de 0.15 (fraca) mas significativa vale algo?**

R: Sim! Em dados do mundo real com muitas variáveis confundidoras, correlações fracas mas consistentes são importantes. Elas indicam que há uma tendência real, mesmo que pequena.

**P: Por que usar testes não-paramétricos?**

R: Porque dados de GitHub não seguem distribuição normal. Há muitos outliers (PRs gigantes, muito tempo, etc.). Testes não-paramétricos são mais robustos a outliers.

**P: O que é "Dimensão A" e "Dimensão B"?**

R: 
- **Dimensão A**: Pergunta "o que faz um PR ser aceito (merged) vs rejeitado (closed)?"
- **Dimensão B**: Pergunta "o que faz um PR ter mais revisores/revisões?"

---

**Lembre-se:** A análise estatística é uma ferramenta, não a resposta final. Sempre considere o contexto do projeto, a cultura da comunidade e outros fatores não quantificáveis.

