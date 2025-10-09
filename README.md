# Lab 03 - Caracterizando a atividade de code review no GitHub

Este projeto implementa a coleta e análise de dados de Pull Requests (PRs) do GitHub para estudar a atividade de code review em repositórios populares.

## Objetivo

Analisar a atividade de code review desenvolvida em repositórios populares do GitHub, identificando variáveis que influenciam no merge de um PR, sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados.

## Estrutura do Projeto

```
lab3/
├── coletor_repositorios.py   # Script para coletar repositórios populares
├── coletor_prs.py           # Script para coletar PRs e métricas
├── executar_sprint1.py      # Script principal para executar a Sprint 1
├── executar_sprint2.py      # Script principal para executar a Sprint 2
├── requirements.txt         # Dependências Python
├── env_example.txt         # Exemplo de configuração de token
├── README.md              # Este arquivo
├── data/                  # Diretório para dados coletados (criado automaticamente)
│   ├── repositorios_selecionados.json
│   ├── dataset_prs.json
│   └── dataset_prs.csv
├── graficos/              # Diretório para gráficos da Sprint 2 (criado automaticamente)
│   ├── rq01_tamanho_vs_status.png
│   ├── rq02_tempo_vs_status.png
│   ├── rq03_descricao_vs_status.png
│   ├── rq04_interacoes_vs_status.png
│   ├── rq05_tamanho_vs_revisoes.png
│   ├── rq06_tempo_vs_revisoes.png
│   ├── rq07_descricao_vs_revisoes.png
│   └── rq08_interacoes_vs_revisoes.png
└── relatorio_sprint2.md   # Relatório completo da Sprint 2
```

## Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar token do GitHub (recomendado)

1. Crie um token pessoal no GitHub: https://github.com/settings/tokens
2. Permissões necessárias: `public_repo`
3. Crie um arquivo `.env` baseado no `env_example.txt`:

```bash
cp env_example.txt .env
```

4. Edite o arquivo `.env` e adicione seu token:

```
GITHUB_TOKEN=seu_token_aqui
```

**Nota:** O token é opcional, mas altamente recomendado para evitar rate limiting da API do GitHub.

## Uso

### Sprint 1: Coleta de repositórios e PRs

#### Opção 1: Script automático (recomendado)

```bash
cd /Users/pedroafonso/lab3
python executar_sprint1.py
```

#### Opção 2: Scripts individuais

```bash
# 1. Coletar repositórios
python coletor_repositorios.py

# 2. Coletar PRs
python coletor_prs.py
```

### Sprint 2: Análise de dados e resposta às RQs

Após coletar os dados na Sprint 1, execute a análise estatística:

```bash
python executar_sprint2.py
```

Este script irá:

1. Carregar o dataset de PRs coletados
2. Realizar análises estatísticas para todas as 8 questões de pesquisa
3. Gerar gráficos e visualizações (salvos em `graficos/`)
4. Criar um relatório completo em Markdown (`relatorio_sprint2.md`)

**Outputs da Sprint 2:**

- `graficos/rq01_tamanho_vs_status.png` - Relação entre tamanho e status
- `graficos/rq02_tempo_vs_status.png` - Relação entre tempo e status
- `graficos/rq03_descricao_vs_status.png` - Relação entre descrição e status
- `graficos/rq04_interacoes_vs_status.png` - Relação entre interações e status
- `graficos/rq05_tamanho_vs_revisoes.png` - Relação entre tamanho e revisões
- `graficos/rq06_tempo_vs_revisoes.png` - Relação entre tempo e revisões
- `graficos/rq07_descricao_vs_revisoes.png` - Relação entre descrição e revisões
- `graficos/rq08_interacoes_vs_revisoes.png` - Relação entre interações e revisões
- `relatorio_sprint2.md` - Relatório completo com todos os resultados

### Critérios de Filtragem

Os PRs coletados devem atender aos seguintes critérios:

1. **Repositórios:** 200 mais populares do GitHub
2. **Volume de PRs:** pelo menos 100 PRs fechados por repositório
3. **Status:** MERGED ou CLOSED
4. **Revisões:** pelo menos uma revisão
5. **Tempo:** mais de 1 hora entre criação e fechamento

## Questões de Pesquisa

### Dimensão A: Feedback Final das Revisões (Status do PR)

- RQ 01: Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
- RQ 02: Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
- RQ 03: Qual a relação entre a descrição dos PRs e o feedback final das revisões?
- RQ 04: Qual a relação entre as interações nos PRs e o feedback final das revisões?

### Dimensão B: Número de Revisões

- RQ 05: Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
- RQ 06: Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
- RQ 07: Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
- RQ 08: Qual a relação entre as interações nos PRs e o número de revisões realizadas?

## Métricas Coletadas

Para cada PR, as seguintes métricas são coletadas:

### Tamanho

- `num_files`: Número de arquivos modificados
- `total_additions`: Total de linhas adicionadas
- `total_deletions`: Total de linhas removidas

### Tempo de Análise

- `time_analysis_hours`: Horas entre criação e fechamento
- `created_at`: Data de criação
- `closed_at`: Data de fechamento
- `merged_at`: Data de merge (se aplicável)

### Descrição

- `description_chars`: Número de caracteres na descrição
- `description`: Texto da descrição (truncado)

### Interações

- `num_comments`: Número de comentários
- `num_participants`: Número de participantes únicos

## Testes Estatísticos (Sprint 2)

A Sprint 2 utiliza testes estatísticos não-paramétricos para responder às questões de pesquisa:

### Testes Utilizados

1. **Teste de Mann-Whitney U**
   - Compara duas grupos independentes (PRs merged vs closed)
   - Não assume distribuição normal dos dados
   - Apropriado para dados com outliers
   - Usado nas RQs 01-04 (Dimensão A)

2. **Correlação de Spearman (ρ)**
   - Mede associação monotônica entre duas variáveis
   - Baseada em ranks, não nos valores absolutos
   - Detecta relações não-lineares
   - Usado nas RQs 05-08 (Dimensão B)

### Interpretação dos Resultados

- **Nível de significância:** α = 0.05
- **P-valor < 0.05:** Resultado estatisticamente significativo
- **Correlação:**
  - |ρ| < 0.3: Fraca
  - 0.3 ≤ |ρ| < 0.5: Moderada
  - 0.5 ≤ |ρ| < 0.7: Forte
  - |ρ| ≥ 0.7: Muito forte

## Exemplo de Uso

```python
from coletor_repositorios import ColetorRepositorios
from coletor_prs import ColetorPRs

# Sprint 1: Coletar repositórios
coletor_repos = ColetorRepositorios()
repositorios = coletor_repos.obter_repositorios_populares(limite=200)
repos_filtrados = coletor_repos.filtrar_repositorios_por_prs(repositorios, min_prs=100)

# Sprint 1: Coletar PRs
coletor_prs = ColetorPRs()
todos_prs = coletor_prs.coletar_todos_prs("repositorios_selecionados.json")

# Sprint 2: Analisar dados
from executar_sprint2 import AnalisadorPRs

analisador = AnalisadorPRs()
analisador.executar_analise_completa()
```

O script coleta apenas repositórios públicos. Repositórios privados são automaticamente ignorados.
