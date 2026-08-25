import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Mauro Maia | Dashboard Profissional - Java Dev",
    page_icon="☕",
    layout="wide",
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FULL_CSV = os.path.join(DATA_DIR, "vagas_java.csv")
SAMPLE_CSV = os.path.join(DATA_DIR, "vagas_java_sample.csv")


@st.cache_data
def carregar_dados():
    caminho = FULL_CSV if os.path.exists(FULL_CSV) else SAMPLE_CSV
    df = pd.read_csv(caminho)
    df["data_criacao"] = pd.to_datetime(df["data_criacao"])
    return df, caminho


df, fonte_usada = carregar_dados()

# ---------- Sidebar ----------
with st.sidebar:
    st.title("☕ Mauro Maia")
    st.caption("Estudante de Engenharia de Software | FIAP")
    st.markdown("---")
    st.markdown("**GitHub:** [DevMauroMaia](https://github.com/DevMauroMaia)")
    st.markdown("---")
    if fonte_usada == SAMPLE_CSV:
        st.warning(
            "Exibindo dados de amostra. Rode `python fetch_data.py` para "
            "coletar o histórico completo de vagas antes da entrega."
        )
    else:
        st.success(f"{len(df)} vagas carregadas de vagas_java.csv")

tab1, tab2, tab3, tab4 = st.tabs(
        ["👋 Quem sou eu", "🎓 Minhas Qualificações", "🛠️ Skills", "📊 Análise de Dados"]
)

# ---------- Aba 1: Quem sou eu ----------
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://github.com/DevMauroMaia.png", width=220)
    with col2:
        st.header("Mauro Carlos Maia Neto")
        st.subheader("Estudante de Engenharia de Software | Foco em Back-end Java")
        st.write(
            """
            Sou Mauro Carlos Maia Neto, estudante de Engenharia de Software na FIAP
            (2º ano), com foco em desenvolvimento back-end em Java. Trabalho
            principalmente com Spring Boot, Spring Data JPA/Hibernate, PostgreSQL
            e construção de APIs REST, sempre buscando aplicar boas práticas de
            arquitetura em camadas (Controller → Service → Repository) e
            modelagem de dados.

            Já desenvolvi projetos que vão de APIs REST completas a sistemas
            acadêmicos com regras de negócio mais complexas, e uso este próprio
            dashboard como exercício de análise de dados aplicada ao mercado de
            trabalho que pretendo entrar: vagas para desenvolvedores Java.

            Atualmente estou em busca de uma oportunidade de estágio ou posição
            júnior em back-end para colocar esse conhecimento em prática em um
            time de verdade.
            """
        )
        st.caption("💡 Se quiser, ajuste o tom — deixei o texto direto e técnico, mas é seu espaço pra imprimir sua voz.")

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Vagas Java analisadas", len(df))
    df_senioridade_informada = df[df["senioridade"] != "Não informado"]
    pct_senior_pleno = (
        df_senioridade_informada["senioridade"].isin(["Pleno", "Sênior", "Staff"]).mean() * 100
        if not df_senioridade_informada.empty else 0
    )
    c2.metric("% Pleno/Sênior+ (entre as informadas)", f"{pct_senior_pleno:.0f}%")
    c3.metric("Empresas distintas identificadas", df[df["empresa"] != "Não informado"]["empresa"].nunique())

# ---------- Aba 2: Minhas Qualificações ----------
with tab2:
    st.header("Formação e Experiência")

    st.subheader("🎓 Formação acadêmica")
    st.write("- Engenharia de Software — FIAP, São Paulo (cursando, 2º ano)")

    st.subheader("📌 Projetos de portfólio")
    st.write(
        """
        - **[ShelfAPI](https://github.com/DevMauroMaia/ShelfApi)** — API REST em Spring Boot para gestão de produtos e categorias,
          com PostgreSQL, DTOs de request/response, tratamento de exceções
          customizado (GlobalExceptionHandler) e relacionamentos JPA
          (@ManyToOne/@OneToMany).
        - **InsightFlow** — Analisador de transcrições de reunião, desenvolvido em
          equipe para um desafio da FIAP com a TOTVS; começou como CLI em Java e
          foi migrado para uma API REST em Spring Boot com JPA/Hibernate e H2.
        - **[AprendendoJpa](https://github.com/DevMauroMaia/AprendendoJpa)** — Sistema de gestão de academia explorando relacionamentos
          JPA mais avançados (@OneToOne, @ManyToMany), Projections e tratamento de
          erros com @ControllerAdvice.
        - **SAFS** — Aplicação console em Java aplicando DDD, tema de Economia
          Espacial.
        - **Dashboard CP1 (este projeto)** — dashboard de análise de dados em
          Python/Streamlit sobre o mercado de vagas Java, aplicando conceitos de
          Data Science.
        """
    )

    st.subheader("📜 Trilha de autoestudo")
    st.write(
        """
        Ainda não tenho certificações formais concluídas, mas mantenho uma
        rotina própria de estudo em back-end Java:

        - Acompanhamento prático de conteúdo de Java/Spring Boot no YouTube,
          sempre praticando o conceito logo após assistir, antes de avançar
          para o próximo tópico.
        - Roteiro de estudo autoguiado cobrindo Spring Boot, microsserviços,
          Kafka/RabbitMQ, PostgreSQL, MongoDB, Redis, REST, GraphQL,
          OAuth2/JWT, Docker, Kubernetes, CI/CD e observabilidade.
        - Base de estudos própria documentando cada tópico estudado.
        """
    )

# ---------- Aba 3: Skills ----------
with tab3:
    st.header("Competências técnicas")

    skills = {
        "Java": 80,
        "Spring Boot": 75,
        "Spring Data JPA / Hibernate": 70,
        "PostgreSQL": 65,
        "REST APIs": 75,
        "Git / GitHub": 80,
        "Maven": 60,
        "Lombok": 65,
        "Python (conhecimento secundário)": 45,
        "JavaScript (conhecimento secundário)": 35,
    }

    for skill, nivel in skills.items():
        st.write(skill)
        st.progress(nivel / 100)

    st.subheader("🤝 Soft skills")
    st.write(
        """
        - **Trabalho em equipe** — desenvolvimento do InsightFlow em grupo para um
          desafio da FIAP com a TOTVS, incluindo apresentação de pitch para
          público não técnico.
        - **Aprendizado autônomo** — estudo estruturado de tópicos de back-end
          (Spring Boot, mensageria, bancos de dados, cloud) fora da grade da
          faculdade, documentando o progresso em uma base de estudos própria.
        - **Resolução de problemas** — depuração e correção de parsing não
          padronizado de dados (encoding, registros multilinha) em um projeto de
          análise de transcrições.
        - **Atenção a boas práticas de código** — refatoração de anotações Lombok
          genéricas para anotações granulares mais explícitas no ShelfAPI.
        """
    )

# ---------- Aba 4: Análise de Dados ----------
with tab4:
    st.header("Análise: Mercado de Vagas Java")
    st.caption(
        "Base: Issues do repositório público [soujava/vagas-java]"
        "(https://github.com/soujava/vagas-java), mural de vagas mantido "
        "pela comunidade Java Brasil/Portugal."
    )

    colf1, colf2, colf3 = st.columns(3)
    with colf1:
        paises = st.multiselect("País", sorted(df["pais"].unique()), default=list(df["pais"].unique()))
    with colf2:
        opcoes_senioridade = sorted(df["senioridade"].unique())
        senioridades = st.multiselect(
            "Senioridade", opcoes_senioridade,
            default=[s for s in opcoes_senioridade if s != "Não informado"],
        )
    with colf3:
        estados = st.multiselect("Status da vaga", sorted(df["estado"].unique()), default=list(df["estado"].unique()))

    st.caption(
        "Por padrão, vagas sem senioridade informada ficam fora dos gráficos "
        "(muitas issues antigas do repositório não usam essa label) — "
        "selecione 'Não informado' acima se quiser incluí-las."
    )

    df_f = df[df["pais"].isin(paises) & df["senioridade"].isin(senioridades) & df["estado"].isin(estados)]

    st.markdown("### Distribuição por senioridade")
    fig_senioridade = px.bar(
        df_f["senioridade"].value_counts().reset_index(),
        x="senioridade", y="count",
        labels={"senioridade": "Senioridade", "count": "Nº de vagas"},
        color="senioridade",
    )
    st.plotly_chart(fig_senioridade, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Modalidade de trabalho")
        fig_modalidade = px.pie(df_f, names="modalidade", hole=0.4)
        st.plotly_chart(fig_modalidade, use_container_width=True)
    with col_b:
        st.markdown("### Tipo de contrato")
        fig_contrato = px.pie(df_f, names="contrato", hole=0.4)
        st.plotly_chart(fig_contrato, use_container_width=True)

    st.markdown("### Tecnologias mais pedidas junto com Java")
    tecnologias_expandidas = (
        df_f["tecnologias"].fillna("").str.split(";").explode().str.strip()
    )
    tecnologias_expandidas = tecnologias_expandidas[
        (tecnologias_expandidas != "") & (tecnologias_expandidas != "Java")
    ]
    top_tec = tecnologias_expandidas.value_counts().head(10).reset_index()
    top_tec.columns = ["tecnologia", "count"]
    fig_tec = px.bar(top_tec, x="count", y="tecnologia", orientation="h",
                      labels={"count": "Nº de vagas", "tecnologia": "Tecnologia"})
    fig_tec.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_tec, use_container_width=True)
    st.caption("Java foi excluído deste gráfico por ser o filtro base da análise (apareceria em praticamente todas as vagas).")

    st.markdown("### Volume de vagas ao longo do tempo")
    por_mes = df_f.set_index("data_criacao").resample("MS").size().reset_index(name="vagas")
    fig_tempo = px.line(por_mes, x="data_criacao", y="vagas", markers=True,
                         labels={"data_criacao": "Mês", "vagas": "Nº de vagas publicadas"})
    st.plotly_chart(fig_tempo, use_container_width=True)

    with st.expander("📋 Ver dados brutos"):
        st.dataframe(df_f, use_container_width=True)

    st.markdown("### 🔎 Principais insights")
    st.write(
        f"""
        - A base atual tem **{len(df_f)}** vagas após os filtros aplicados
          (de um total de **{len(df)}** vagas coletadas desde 2021).
        - Entre as vagas com senioridade informada, a mais comum é
          **{df_f['senioridade'].mode()[0] if not df_f.empty else '-'}**.
        - A tecnologia mais associada a vagas Java (além do próprio Java) é
          **{top_tec.iloc[0]['tecnologia'] if not top_tec.empty else '-'}**.
        - Apenas **{df["senioridade"].isin(["Júnior", "Estágio"]).sum()}** das
          {len(df)} vagas coletadas são de nível Júnior/Estágio.
        """
    )
    st.caption("Os três primeiros pontos acima respondem aos filtros selecionados; o último considera a base completa, sem filtro.")
    st.markdown(
        """
        **O que isso significa para minha estratégia de busca de vaga:**
        O dado mais forte que essa base revela é a escassez de vagas
        Júnior/Estágio: de 848 vagas coletadas em quase 5 anos de histórico,
        pouquíssimas são de entrada — a esmagadora maioria das vagas
        rotuladas por senioridade é Pleno ou Sênior. Isso muda minha
        estratégia: não posso depender só de filtrar por "vaga júnior",
        porque essas vagas são raras e disputadas; preciso também mirar
        processos seletivos de trainee/estágio fora desse mural específico,
        e usar o tempo até lá pra fechar a distância técnica. Do lado
        positivo, Spring aparece como a tecnologia mais pedida junto com
        Java disparado — confirma que meu foco de estudo atual (Spring
        Boot, Spring Data JPA) está alinhado com o que o mercado
        efetivamente pede, então vale continuar aprofundando esse
        ecossistema em vez de dispersar o estudo.
        """
    )
