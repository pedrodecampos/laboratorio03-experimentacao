"""
Coletor de repositórios populares do GitHub
Lab 03 - Sprint 1
"""

import requests
import time
import json
import pandas as pd
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class ColetorRepositorios:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Lab03-Repository-Collector'
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    def obter_repositorios_populares(self, limite: int = 200) -> List[Dict]:
        repositorios = []
        pagina = 1
        por_pagina = 100
        
        print(f"Coletando os {limite} repositórios mais populares do GitHub...")
        
        while len(repositorios) < limite:
            restantes = limite - len(repositorios)
            atual_por_pagina = min(por_pagina, restantes)
            
            url = f"https://api.github.com/search/repositories"
            params = {
                'q': 'stars:>1000',
                'sort': 'stars',
                'order': 'desc',
                'page': pagina,
                'per_page': atual_por_pagina
            }
            
            try:
                print(f"Fazendo requisição para página {pagina}...")
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    repos = data.get('items', [])
                    
                    if not repos:
                        print("Nenhum repositório encontrado. Parando a coleta.")
                        break
                    
                    repositorios.extend(repos)
                    print(f"Coletados {len(repos)} repositórios da página {pagina}. Total: {len(repositorios)}")
                    
                    time.sleep(1)
                    pagina += 1
                    
                elif response.status_code == 403:
                    print("Rate limit atingido. Aguardando 60 segundos...")
                    time.sleep(60)
                else:
                    print(f"Erro na requisição: {response.status_code}")
                    print(f"Resposta: {response.text}")
                    break
                    
            except Exception as e:
                print(f"Erro ao fazer requisição: {e}")
                break
        
        return repositorios[:limite]
    
    def filtrar_repositorios_por_prs(self, repositorios: List[Dict], min_prs: int = 100) -> List[Dict]:
        repositorios_filtrados = []
        
        print(f"Filtrando repositórios com pelo menos {min_prs} PRs...")
        
        for i, repo in enumerate(repositorios):
            nome_repo = repo.get('full_name', '')
            print(f"[{i+1}/{len(repositorios)}] Verificando {nome_repo}...")
            
            try:
                search_url = f"https://api.github.com/search/issues"
                search_params = {
                    'q': f'repo:{nome_repo} is:pr is:closed',
                    'per_page': 1
                }
                
                search_response = requests.get(search_url, headers=self.headers, params=search_params)
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    total_prs = search_data.get('total_count', 0)
                    
                    if total_prs >= min_prs:
                        repo['total_closed_prs'] = total_prs
                        repositorios_filtrados.append(repo)
                        print(f"  ✓ {nome_repo}: {total_prs} PRs fechados")
                    else:
                        print(f"  ✗ {nome_repo}: {total_prs} PRs fechados (abaixo do mínimo)")
                else:
                    print(f"  ✗ Erro ao buscar PRs para {nome_repo}: {search_response.status_code}")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ Erro ao processar {nome_repo}: {e}")
                continue
        
        print(f"\nFiltragem concluída: {len(repositorios_filtrados)} repositórios atendem aos critérios")
        return repositorios_filtrados
    
    def salvar_repositorios(self, repositorios: List[Dict], nome_arquivo: str = "repositorios_selecionados.json"):
        caminho_arquivo = f"/Users/pedroafonso/lab3/{nome_arquivo}"
        
        repos_limpos = []
        for repo in repositorios:
            repo_limpo = {
                'id': repo.get('id'),
                'name': repo.get('name'),
                'full_name': repo.get('full_name'),
                'description': repo.get('description'),
                'html_url': repo.get('html_url'),
                'stars': repo.get('stargazers_count'),
                'forks': repo.get('forks_count'),
                'language': repo.get('language'),
                'created_at': repo.get('created_at'),
                'updated_at': repo.get('updated_at'),
                'total_closed_prs': repo.get('total_closed_prs', 0)
            }
            repos_limpos.append(repo_limpo)
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(repos_limpos, f, indent=2, ensure_ascii=False)
        
        print(f"Lista de repositórios salva em: {caminho_arquivo}")
    
    def criar_relatorio_resumo(self, repositorios: List[Dict]) -> pd.DataFrame:
        dados = []
        
        for repo in repositorios:
            dados.append({
                'Nome': repo.get('full_name', ''),
                'Descrição': repo.get('description', '')[:100] + '...' if repo.get('description') and len(repo.get('description', '')) > 100 else repo.get('description', ''),
                'Linguagem': repo.get('language', 'N/A'),
                'Estrelas': repo.get('stargazers_count', 0),
                'Forks': repo.get('forks_count', 0),
                'PRs Fechados': repo.get('total_closed_prs', 0),
                'Criado em': repo.get('created_at', ''),
                'Atualizado em': repo.get('updated_at', '')
            })
        
        df = pd.DataFrame(dados)
        return df

def main():
    coletor = ColetorRepositorios()
    
    print("=== LAB 03 - SPRINT 1: COLETA DE REPOSITÓRIOS ===\n")
    
    repositorios = coletor.obter_repositorios_populares(limite=200)
    
    if not repositorios:
        print("Erro: Nenhum repositório foi coletado.")
        return
    
    print(f"\nColetados {len(repositorios)} repositórios populares.")
    
    coletor.salvar_repositorios(repositorios, "todos_repositorios_populares.json")
    
    repositorios_filtrados = coletor.filtrar_repositorios_por_prs(repositorios, min_prs=100)
    
    if not repositorios_filtrados:
        print("Erro: Nenhum repositório atende aos critérios de filtragem.")
        return
    
    coletor.salvar_repositorios(repositorios_filtrados, "repositorios_selecionados.json")
    
    resumo_df = coletor.criar_relatorio_resumo(repositorios_filtrados)
    
    resumo_df.to_csv("/Users/pedroafonso/lab3/resumo_repositorios.csv", index=False, encoding='utf-8')
    
    print(f"\n=== RESUMO DA COLETA ===")
    print(f"Total de repositórios coletados: {len(repositorios)}")
    print(f"Repositórios que atendem aos critérios: {len(repositorios_filtrados)}")
    print(f"Taxa de filtragem: {len(repositorios_filtrados)/len(repositorios)*100:.1f}%")
    
    print(f"\nTop 10 repositórios selecionados:")
    print(resumo_df[['Nome', 'Linguagem', 'Estrelas', 'PRs Fechados']].head(10).to_string(index=False))
    
    print(f"\nLinguagens mais comuns:")
    lang_counts = resumo_df['Linguagem'].value_counts().head(5)
    print(lang_counts.to_string())

if __name__ == "__main__":
    main()

