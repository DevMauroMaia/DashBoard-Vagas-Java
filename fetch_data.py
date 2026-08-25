"""
fetch_data.py
--------------
Coleta as vagas de Java publicadas como Issues no repositório público
soujava/vagas-java (https://github.com/soujava/vagas-java) usando a
API REST do GitHub, e transforma em um CSV estruturado para o dashboard.

Por que essa fonte?
- É uma base real e viva, mantida pela comunidade Java Brasil/Portugal.
- Cada vaga é uma Issue com labels padronizadas: senioridade, modalidade
  (Remoto/Híbrido/Presencial), tipo de contrato (CLT/PJ) e tecnologias
  (Spring, Quarkus, Kafka, Jakarta EE, PostgreSQL, etc).
- Está diretamente ligada ao seu nicho profissional (vagas Java júnior).

Como rodar:
    python fetch_data.py
    (opcional, recomendado) defina um token para evitar rate limit:
    GITHUB_TOKEN=seu_token python fetch_data.py

O script salva o resultado em data/vagas_java.csv. Se a API estiver
indisponível ou o rate limit for atingido, o app.py cai automaticamente
para data/vagas_java_sample.csv (uma amostra já incluída no projeto).
"""

import os
import re
import time
import csv
import requests

REPO = "soujava/vagas-java"
API_URL = f"https://api.github.com/repos/{REPO}/issues"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "vagas_java.csv")

# Listas de controle para classificar as labels de cada issue
SENIORIDADES = ["Estágio", "Estagio", "Trainee", "Júnior", "Junior", "Pleno", "Sênior", "Senior", "Staff", "Especialista"]
MODALIDADES = ["Remoto", "Híbrido", "Hibrido", "Presencial"]
CONTRATOS = ["CLT", "PJ", "Cooperado", "Freelance"]
PAISES_LABEL = ["Portugal"]  # se não tiver essa label, assumimos Brasil

# Labels de bot/meta e categorias que não são tecnologia (cidade, requisito de idioma,
# modelo de contratação etc.) — não entram na análise de "tecnologias mais pedidas"
RUIDO_TECNOLOGIA = {
    "no-issue-activity", "Stale", "bug", "good first issue",
    "Porto Alegre", "Território Nacional", "Florianópolis", "Curitiba - PR",
    "São Paulo - SP", "Belo Horizonte - MG", "RJ", "Semi-presencial",
    "Consultoria", "Alocado", "Internacional", "Inglês Avançado", "Fintech",
    "Startup", "Superior Completo", "Test Analyst", "Talent Group",
    "Stefanini", "Arquiteto",
}


def normaliza_senioridade(nome):
    n = nome.replace("Junior", "Júnior").replace("Senior", "Sênior").replace("Hibrido", "Híbrido")
    return n


def extrai_empresa(titulo):
    """Tenta extrair o nome da empresa do título da vaga. O padrão mudou ao
    longo dos anos nesse repositório, então isso é best-effort — nem toda
    vaga vai ter empresa identificada."""
    t = re.sub(r"^\[.*?\]\s*", "", titulo)  # remove [Modalidade] do início
    m = re.search(r"@\s*([A-Za-zÀ-ÿ0-9 .&\-]+)$", t)
    if m:
        return m.group(1).strip()
    if " na " in t:
        return t.split(" na ")[-1].strip("[]")
    m = re.search(r"-\s*([A-Za-zÀ-ÿ0-9 .&]+)$", t)
    if m and len(m.group(1).strip()) > 2:
        return m.group(1).strip()
    m = re.search(r"\[([A-Za-zÀ-ÿ0-9 .&\-]+)\]\s*$", t)
    if m:
        return m.group(1).strip()
    return "Não informado"


def parse_issue(issue):
    labels = [l["name"] for l in issue.get("labels", [])]

    senioridade = next((normaliza_senioridade(l) for l in labels if l in SENIORIDADES), "Não informado")
    modalidade = next((normaliza_senioridade(l) for l in labels if l in MODALIDADES), "Não informado")
    contrato = next((l for l in labels if l in CONTRATOS), "Não informado")
    pais = "Portugal" if any(l in PAISES_LABEL for l in labels) else "Brasil"

    excluir = set(SENIORIDADES + MODALIDADES + CONTRATOS + PAISES_LABEL + ["job opportunity", "Job opportunity"]) | RUIDO_TECNOLOGIA
    tecnologias = [l for l in labels if l not in excluir]

    titulo = issue["title"]
    empresa = extrai_empresa(titulo)

    return {
        "id": issue["number"],
        "titulo": titulo,
        "empresa": empresa,
        "senioridade": senioridade,
        "modalidade": modalidade,
        "contrato": contrato,
        "pais": pais,
        "tecnologias": ";".join(tecnologias),
        "estado": issue["state"],  # open = vaga em aberto, closed = encerrada/preenchida
        "data_criacao": issue["created_at"][:10],
        "url": issue["html_url"],
    }


def fetch_all_issues(max_pages=10, per_page=100):
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    todas = []
    for page in range(1, max_pages + 1):
        resp = requests.get(
            API_URL,
            headers=headers,
            params={"state": "all", "per_page": per_page, "page": page},
            timeout=30,
        )
        if resp.status_code == 403:
            print("Rate limit atingido. Use um GITHUB_TOKEN para coletar mais dados.")
            break
        resp.raise_for_status()
        dados = resp.json()
        if not dados:
            break
        # Issues de verdade não têm "pull_request"; filtra PRs fora
        todas.extend([i for i in dados if "pull_request" not in i])
        print(f"Página {page}: {len(dados)} itens coletados")
        time.sleep(0.5)

    return todas


def main():
    issues = fetch_all_issues()
    if not issues:
        print("Nenhum dado coletado. Verifique sua conexão ou rate limit da API do GitHub.")
        return

    linhas = [parse_issue(i) for i in issues]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        writer.writeheader()
        writer.writerows(linhas)

    print(f"{len(linhas)} vagas salvas em {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
