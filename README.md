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
├── requirements.txt         # Dependências Python
├── env_example.txt         # Exemplo de configuração de token
├── README.md              # Este arquivo
└── data/                  # Diretório para dados coletados (criado automaticamente)
    ├── repositorios_selecionados.json
    ├── dataset_prs.json
    └── dataset_prs.csv
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

## Exemplo de Uso

```python
from coletor_repositorios import ColetorRepositorios
from coletor_prs import ColetorPRs

# Coletar repositórios
coletor_repos = ColetorRepositorios()
repositorios = coletor_repos.obter_repositorios_populares(limite=200)
repos_filtrados = coletor_repos.filtrar_repositorios_por_prs(repositorios, min_prs=100)

# Coletar PRs
coletor_prs = ColetorPRs()
todos_prs = coletor_prs.coletar_todos_prs("repositorios_selecionados.json")
```

O script coleta apenas repositórios públicos. Repositórios privados são automaticamente ignorados.
