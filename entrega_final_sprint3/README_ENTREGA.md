# ENTREGA FINAL - LAB 03

## Caracterizando a atividade de code review no GitHub

**Aluno:** Pedro Afonso  
**Data:** 20/10/2025  
**Disciplina:** Laboratório de Experimentação de Software

---

## 📋 ARQUIVOS ENTREGUES

### 📄 Relatórios (OBRIGATÓRIOS)

- `relatorio_final.md` - **Relatório acadêmico completo**
- `resumo_executivo.md` - Resumo executivo
- `analises_estatisticas.md` - Análises estatísticas avançadas

### 📊 Dados e Resultados

- `dataset_prs.csv` - Dataset principal (500 PRs)
- `graficos/` - Gráficos das 8 questões de pesquisa
- `slides/` - Slides de apresentação (7 slides)

### 🐍 Código Fonte

- `coletor_prs.py` - Script de coleta de dados
- `analisador_prs.py` - Script de análise estatística
- `gerador_relatorio.py` - Script de geração de relatórios

---

## 🎯 RESUMO DOS RESULTADOS

### Principais Descobertas

1. **PRs menores** têm maior chance de merge (80.8 vs 167.2 linhas)
2. **PRs merged** são analisados mais rapidamente (63.2 vs 156.7 horas)
3. **Descrições detalhadas** aumentam chance de merge (399.3 vs 229.8 caracteres)
4. **Nível de interação** influencia o status final

### Testes Estatísticos

- **8 questões de pesquisa** analisadas
- **Todas as 4 hipóteses** confirmadas (p < 0.001)
- **Mann-Whitney U** e **Correlação de Spearman** utilizados
- **Nível de significância:** α = 0.05

### Dataset

- **500 Pull Requests** analisados
- **343 PRs merged** (68.6%) vs **157 PRs closed** (31.4%)
- **10 repositórios** únicos

---

## 🚀 COMO EXECUTAR

```bash
# 1. Coletar dados (se necessário)
python3 coletor_prs.py

# 2. Executar análise estatística
python3 analisador_prs.py

# 3. Gerar relatórios
python3 gerador_relatorio.py
```

---

## 📈 CRITÉRIOS ATENDIDOS

### Lab03S01 (5 pontos) ✅

- [x] Lista de repositórios selecionados
- [x] Script de coleta de PRs e métricas
- [x] Dataset com dados coletados

### Lab03S02 (5 pontos) ✅

- [x] Dataset completo com todas as métricas
- [x] Primeira versão do relatório com hipóteses
- [x] Análise estatística das 8 RQs

### Lab03S03 (10 pontos) ✅

- [x] Análise e visualização de dados completa
- [x] Relatório final elaborado com discussão
- [x] Testes estatísticos apropriados
- [x] Limitações e trabalhos futuros documentados

**TOTAL: 20 pontos** 🎉

---

_Entrega final do Lab 03 - Sprint 3 completa_
