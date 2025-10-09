"""
Coletor de Pull Requests do GitHub
Lab 03 - Sprint 1
"""

import requests
import time
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class ColetorPRs:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Lab03-PR-Collector'
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    def obter_prs_do_repositorio(self, nome_repo: str, max_prs: int = 1000) -> List[Dict]:
        prs = []
        pagina = 1
        por_pagina = 100
        
        print(f"Coletando PRs do repositório: {nome_repo}")
        
        while len(prs) < max_prs:
            restantes = max_prs - len(prs)
            atual_por_pagina = min(por_pagina, restantes)
            
            url = f"https://api.github.com/repos/{nome_repo}/pulls"
            params = {
                'state': 'closed',
                'sort': 'updated',
                'direction': 'desc',
                'page': pagina,
                'per_page': atual_por_pagina
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    batch_prs = response.json()
                    
                    if not batch_prs:
                        print(f"  Nenhum PR encontrado na página {pagina}")
                        break
                    
                    prs_filtrados = self.filtrar_prs(batch_prs, nome_repo)
                    prs.extend(prs_filtrados)
                    
                    print(f"  Página {pagina}: {len(batch_prs)} PRs encontrados, {len(prs_filtrados)} filtrados. Total: {len(prs)}")
                    
                    if len(batch_prs) < atual_por_pagina:
                        print(f"  Última página alcançada")
                        break
                    
                    pagina += 1
                    time.sleep(1)
                    
                elif response.status_code == 403:
                    print(f"  Rate limit atingido. Aguardando 60 segundos...")
                    time.sleep(60)
                else:
                    print(f"  Erro na requisição: {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"  Erro ao coletar PRs: {e}")
                break
        
        print(f"  Coleta concluída: {len(prs)} PRs válidos coletados")
        return prs
    
    def filtrar_prs(self, prs: List[Dict], nome_repo: str) -> List[Dict]:
        prs_filtrados = []
        
        for pr in prs:
            if not self.tem_revisoes(pr, nome_repo):
                continue
            
            if not self.atende_criterio_tempo(pr):
                continue
            
            pr_com_metricas = self.adicionar_metricas_ao_pr(pr, nome_repo)
            if pr_com_metricas:
                prs_filtrados.append(pr_com_metricas)
        
        return prs_filtrados
    
    def tem_revisoes(self, pr: Dict, nome_repo: str) -> bool:
        try:
            review_count = pr.get('review_count', 0)
            
            if review_count > 0:
                return True
            
            numero_pr = pr.get('number')
            url = f"https://api.github.com/repos/{nome_repo}/pulls/{numero_pr}/reviews"
            
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                reviews = response.json()
                return len(reviews) > 0
            
            return False
            
        except Exception as e:
            print(f"    Erro ao verificar revisões: {e}")
            return False
    
    def atende_criterio_tempo(self, pr: Dict) -> bool:
        try:
            created_at = pr.get('created_at')
            closed_at = pr.get('closed_at') or pr.get('merged_at')
            
            if not created_at or not closed_at:
                return False
            
            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            closed_dt = datetime.fromisoformat(closed_at.replace('Z', '+00:00'))
            
            time_diff = closed_dt - created_dt
            
            return time_diff > timedelta(hours=1)
            
        except Exception as e:
            print(f"    Erro ao verificar critério de tempo: {e}")
            return False
    
    def adicionar_metricas_ao_pr(self, pr: Dict, nome_repo: str) -> Optional[Dict]:
        try:
            numero_pr = pr.get('number')
            
            metricas = self.coletar_metricas_pr(pr, nome_repo, numero_pr)
            
            if metricas:
                pr.update(metricas)
                return pr
            
            return None
            
        except Exception as e:
            print(f"    Erro ao adicionar métricas: {e}")
            return None
    
    def coletar_metricas_pr(self, pr: Dict, nome_repo: str, numero_pr: int) -> Optional[Dict]:
        try:
            metricas = {}
            
            metricas_arquivos = self.obter_metricas_arquivos(nome_repo, numero_pr)
            if metricas_arquivos:
                metricas.update(metricas_arquivos)
            
            metricas_tempo = self.obter_metricas_tempo(pr)
            if metricas_tempo:
                metricas.update(metricas_tempo)
            
            metricas_descricao = self.obter_metricas_descricao(pr)
            if metricas_descricao:
                metricas.update(metricas_descricao)
            
            metricas_interacao = self.obter_metricas_interacao(nome_repo, numero_pr)
            if metricas_interacao:
                metricas.update(metricas_interacao)
            
            return metricas if metricas else None
            
        except Exception as e:
            print(f"      Erro ao coletar métricas: {e}")
            return None
    
    def obter_metricas_arquivos(self, nome_repo: str, numero_pr: int) -> Optional[Dict]:
        try:
            url = f"https://api.github.com/repos/{nome_repo}/pulls/{numero_pr}/files"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                files = response.json()
                
                num_files = len(files)
                total_additions = sum(file.get('additions', 0) for file in files)
                total_deletions = sum(file.get('deletions', 0) for file in files)
                
                return {
                    'num_files': num_files,
                    'total_additions': total_additions,
                    'total_deletions': total_deletions
                }
            
            return None
            
        except Exception as e:
            print(f"        Erro ao coletar métricas de arquivos: {e}")
            return None
    
    def obter_metricas_tempo(self, pr: Dict) -> Optional[Dict]:
        try:
            created_at = pr.get('created_at')
            closed_at = pr.get('closed_at') or pr.get('merged_at')
            
            if not created_at or not closed_at:
                return None
            
            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            closed_dt = datetime.fromisoformat(closed_at.replace('Z', '+00:00'))
            
            time_diff = closed_dt - created_dt
            time_hours = time_diff.total_seconds() / 3600
            
            return {
                'time_analysis_hours': time_hours,
                'created_at': created_at,
                'closed_at': closed_at,
                'merged_at': pr.get('merged_at')
            }
            
        except Exception as e:
            print(f"        Erro ao calcular métricas de tempo: {e}")
            return None
    
    def obter_metricas_descricao(self, pr: Dict) -> Optional[Dict]:
        try:
            body = pr.get('body', '') or ''
            body_chars = len(body)
            
            return {
                'description_chars': body_chars,
                'description': body[:500] + '...' if len(body) > 500 else body
            }
            
        except Exception as e:
            print(f"        Erro ao calcular métricas da descrição: {e}")
            return None
    
    def obter_metricas_interacao(self, nome_repo: str, numero_pr: int) -> Optional[Dict]:
        try:
            comments_url = f"https://api.github.com/repos/{nome_repo}/issues/{numero_pr}/comments"
            comments_response = requests.get(comments_url, headers=self.headers)
            
            reviews_url = f"https://api.github.com/repos/{nome_repo}/pulls/{numero_pr}/reviews"
            reviews_response = requests.get(reviews_url, headers=self.headers)
            
            num_comments = 0
            participants = set()
            
            if comments_response.status_code == 200:
                comments = comments_response.json()
                num_comments = len(comments)
                for comment in comments:
                    user = comment.get('user', {})
                    if user:
                        participants.add(user.get('login', ''))
            
            if reviews_response.status_code == 200:
                reviews = reviews_response.json()
                for review in reviews:
                    user = review.get('user', {})
                    if user:
                        participants.add(user.get('login', ''))
            
            return {
                'num_comments': num_comments,
                'num_participants': len(participants)
            }
            
        except Exception as e:
            print(f"        Erro ao coletar métricas de interação: {e}")
            return None
    
    def coletar_todos_prs(self, arquivo_repositorios: str = "repositorios_selecionados.json") -> List[Dict]:
        caminho_arquivo = f"/Users/pedroafonso/lab3/{arquivo_repositorios}"
        
        if not os.path.exists(caminho_arquivo):
            print(f"Arquivo {caminho_arquivo} não encontrado!")
            return []
        
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            repositorios = json.load(f)
        
        todos_prs = []
        
        print(f"=== COLETA DE PRs DE {len(repositorios)} REPOSITÓRIOS ===\n")
        
        for i, repo in enumerate(repositorios):
            nome_repo = repo.get('full_name', '')
            print(f"[{i+1}/{len(repositorios)}] Processando repositório: {nome_repo}")
            
            try:
                prs = self.obter_prs_do_repositorio(nome_repo, max_prs=200)
                todos_prs.extend(prs)
                
                print(f"  Total de PRs coletados até agora: {len(todos_prs)}")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"  Erro ao processar {nome_repo}: {e}")
                continue
        
        print(f"\n=== COLETA CONCLUÍDA ===")
        print(f"Total de PRs coletados: {len(todos_prs)}")
        
        return todos_prs
    
    def salvar_dataset_prs(self, prs: List[Dict], nome_arquivo: str = "dataset_prs.json"):
        caminho_arquivo = f"/Users/pedroafonso/lab3/{nome_arquivo}"
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(prs, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"Dataset salvo em: {caminho_arquivo}")
    
    def criar_dataframe_prs(self, prs: List[Dict]) -> pd.DataFrame:
        if not prs:
            return pd.DataFrame()
        
        dados = []
        
        for pr in prs:
            linha = {
                'pr_id': pr.get('id'),
                'pr_number': pr.get('number'),
                'repository': pr.get('head', {}).get('repo', {}).get('full_name', ''),
                'title': pr.get('title', ''),
                'state': pr.get('state', ''),
                'merged': pr.get('merged', False),
                'user': pr.get('user', {}).get('login', ''),
                'created_at': pr.get('created_at'),
                'closed_at': pr.get('closed_at'),
                'merged_at': pr.get('merged_at'),
                'num_files': pr.get('num_files', 0),
                'total_additions': pr.get('total_additions', 0),
                'total_deletions': pr.get('total_deletions', 0),
                'time_analysis_hours': pr.get('time_analysis_hours', 0),
                'description_chars': pr.get('description_chars', 0),
                'num_comments': pr.get('num_comments', 0),
                'num_participants': pr.get('num_participants', 0)
            }
            dados.append(linha)
        
        df = pd.DataFrame(dados)
        return df
    
    def salvar_prs_csv(self, prs: List[Dict], nome_arquivo: str = "dataset_prs.csv"):
        df = self.criar_dataframe_prs(prs)
        
        if not df.empty:
            caminho_arquivo = f"/Users/pedroafonso/lab3/{nome_arquivo}"
            df.to_csv(caminho_arquivo, index=False, encoding='utf-8')
            print(f"Dataset CSV salvo em: {caminho_arquivo}")
            
            print(f"\n=== ESTATÍSTICAS DO DATASET ===")
            print(f"Total de PRs: {len(df)}")
            print(f"PRs Merged: {len(df[df['merged'] == True])}")
            print(f"PRs Closed (não merged): {len(df[df['merged'] == False])}")
            print(f"Repositórios únicos: {df['repository'].nunique()}")

def main():
    coletor = ColetorPRs()
    
    print("=== LAB 03 - SPRINT 1: COLETA DE PRs ===\n")
    
    arquivo_repos = "repositorios_selecionados.json"
    if not os.path.exists(f"/Users/pedroafonso/lab3/{arquivo_repos}"):
        print(f"Arquivo {arquivo_repos} não encontrado!")
        print("Execute primeiro o script coletor_repositorios.py para gerar a lista de repositórios.")
        return
    
    todos_prs = coletor.coletar_todos_prs(arquivo_repos)
    
    if not todos_prs:
        print("Nenhum PR foi coletado. Verifique a configuração e tente novamente.")
        return
    
    coletor.salvar_dataset_prs(todos_prs, "dataset_prs.json")
    coletor.salvar_prs_csv(todos_prs, "dataset_prs.csv")
    
    print(f"\n=== SPRINT 1 CONCLUÍDA ===")
    print(f"Dataset com {len(todos_prs)} PRs coletados e salvo com sucesso!")

if __name__ == "__main__":
    main()

