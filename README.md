# ☕ Dashboard Profissional — Mercado de Vagas Java

Dashboard interativo construído em **Python + Streamlit** que analisa o
mercado de vagas para desenvolvedores Java, a partir de dados reais
coletados via API do GitHub.

🔗 **[Acessar o dashboard](#)** <!-- troque pelo link do Streamlit Cloud -->

## Sobre o projeto

Além de servir como portfólio profissional, este dashboard aplica
conceitos de análise e visualização de dados sobre uma base real: mais
de 800 vagas de Java publicadas entre 2021 e 2026 no mural da
comunidade [soujava/vagas-java](https://github.com/soujava/vagas-java).

**O que o dashboard mostra:**
- Apresentação profissional, formação e projetos de portfólio
- Competências técnicas e soft skills
- Análise interativa do mercado de vagas Java: distribuição por
  senioridade, modalidade de trabalho, tipo de contrato, tecnologias
  mais demandadas e evolução do volume de vagas ao longo do tempo

## Stack

- **Python** — coleta e tratamento de dados (`pandas`, `requests`)
- **Streamlit** — interface do dashboard
- **Plotly** — visualizações interativas

## Rodando localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Fonte dos dados

Os dados são coletados via API pública do GitHub a partir das *Issues*
do repositório [soujava/vagas-java](https://github.com/soujava/vagas-java),
um mural de vagas mantido pela comunidade Java Brasil/Portugal.

---

Desenvolvido por **Mauro Carlos Maia Neto** — Estudante de Engenharia de
Software (FIAP), com foco em back-end Java.
[GitHub](https://github.com/DevMauroMaia)
