import os

from langchain_openai import ChatOpenAI
import openai
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from tools.PDFSelector import select_pdf, select_output_directory
from tools.create_agents import create_agent
from tools.create_tasks import create_task


# CONFIGURAÇÕES DE API
openai.api_key = os.getenv('OPENAI_API_KEY')
os.environ["BROWSERLESS_API_KEY"] = os.getenv('BROWSERLESS_API_KEY')
llm = ChatOpenAI(model='gpt-3.5-turbo')

# ARQUIVOS
pdf_path = select_pdf()
if not pdf_path:
    print("Nenhum PDF selecionado. Encerrando o programa.")
    exit()
context_topic = input("Digite o contexto da aula: \n")
output_directory = select_output_directory()

"""AGENTES

Um agente é uma unidade autônoma programada para:

Executar tarefas
Tomar decisões
Comunique-se com outros agentes

Pense em um agente como um membro de uma equipe, com habilidades específicas e um trabalho particular a fazer. 
Os agentes podem ter diferentes papéis, como 'Pesquisador', 'Escritor' ou 'Suporte ao Cliente', 
cada um contribuindo para o objetivo geral da equipe.

SABER MAIS : https://docs.crewai.com/core-concepts/Agents/
"""

"""FERRAMENTAS
As ferramentas CrewAI capacitam agentes com capacidades que vão desde pesquisa na web e análise de dados até colaboração e delegação de tarefas entre colegas de trabalho. 
Esta documentação descreve como criar, integrar e alavancar essas ferramentas dentro da estrutura CrewAI, incluindo um novo foco em ferramentas de colaboração.

Principais características das ferramentas¶
Utilitário : criado para tarefas como pesquisa na web, análise de dados, geração de conteúdo e colaboração de agentes.
Integração : aumenta as capacidades dos agentes integrando perfeitamente ferramentas ao seu fluxo de trabalho.
Personalização : Oferece flexibilidade para desenvolver ferramentas personalizadas ou utilizar ferramentas existentes, atendendo às necessidades específicas dos agentes.
Tratamento de erros : incorpora mecanismos robustos de tratamento de erros para garantir uma operação suave.
Mecanismo de cache : possui cache inteligente para otimizar o desempenho e reduzir operações redundantes.

SABER MAIS : https://docs.crewai.com/core-concepts/Tools/
"""

"""TEREFAS
No framework crewAI, tarefas são atribuições específicas concluídas por agentes. Elas fornecem todos os detalhes necessários para execução, 
como uma descrição, o agente responsável, ferramentas necessárias e mais, facilitando uma ampla gama de complexidades de ação.
"""

# AGENTES
topic_researcher = create_agent(
    role='Especialista em Revisão e resumos',
    goal='Listar todos os tópicos abordados sobre',
    backstory="Você é especializado em extrair informações relevantes de aulas e palestras.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path,
    tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website]
)

academic_reviewer = create_agent(
    role='Revisor Acadêmico',
    goal='Identificar as técnicas e métodos nos topicos listados sobre',
    backstory="Especializado em revisar e identificar métodos específicos apresentados em contextos acadêmicos.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path,
    tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website]
)

ref_specialist = create_agent(
    role='Especialista em documentar Websites',
    goal='Listar sites presentes no texto sobre',
    backstory="Especializado em identificar e descrever websites e referências mencionadas.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path
)

prof = create_agent(
    role='Escritor de Tutoriais',
    goal='Escrever um tutorial passo a passo detalhado para o projeto apresentado na aula',
    backstory="Especializado em criar tutoriais claros e detalhados, transformando informações complexas em instruções acessíveis.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path,
    tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website]
)

research_writer = create_agent(
    role='Escritor senior',
    goal='Pesquisar, analisar e escrever um documento estruturado sobre',
    backstory="Capaz de realizar pesquisas detalhadas e escrever documentos estruturados sobre métodos acadêmicos.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path,
    tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website]
)


# TARÉFAS

list_topics_task = create_task(
    description=f"Liste todos os tópicos abordados sobre '{context_topic}' presente no texto.",
    expected_output='Lista detalhada e enumerada de todos os tópicos abordados no texto.',
    agent=topic_researcher,
    output_file=os.path.join(output_directory, "lista_de_topicos.md")
)

academic_review_task = create_task(
    description=f"Identificar as técnicas e métodos apresentados na aula de '{context_topic}'.",
    expected_output=f"Todos os tópicos listados com seus métodos utilizados e seus objetivos sobre '{context_topic}' devidamente descritos e revisados.",
    agent=academic_reviewer,
    output_file=os.path.join(output_directory, "descricao_topicos.md"),
    context=[list_topics_task]
)

website_list_task = create_task(
    description=(
        f"Listar sites mencionados na aula '{context_topic}' e suas funções específicas."
    ),
    expected_output='Lista de todos os sites mencionados no texto e suas funções.',
    agent=ref_specialist,
    output_file=os.path.join(output_directory, "referencias.md")
)

tutorial_write_task = create_task(
    description=(
        f"Produzir um guia completo que descreva de maneira clara e detalhada como executar o projeto baseado na aula '{context_topic}'."
    ),
    expected_output=f"Tutorial Passo a Passo\n\n"
                    f"**Tutorial para Executar o Projeto: \"{context_topic}\"**\n\n"
                    "Este tutorial detalha todas as etapas necessárias para executar o projeto apresentado na aula. "
                    "Siga as instruções passo a passo para garantir que todas as técnicas e métodos sejam aplicados corretamente.\n\n"
                    "**Passo 1:** [Descrição do Passo 1]\n"
                    "**Passo 2:** [Descrição do Passo 2]\n"
                    "...",
    agent=prof,
    async_execution=False,
    context=[list_topics_task, academic_review_task, website_list_task],
    output_file=os.path.join(output_directory, "tutorial.md")
)

research_write_task = create_task(
    description=(
        "Com base nos materiais fornecidos pelos outros agentes, escreva um relatório estruturado com as seguintes seções:"
        "\n- **Tópicos:** a lista dos tópicos definidos"
        "\n- **Objetivos:** Descreva os objetivos do estudo."
        "\n- **Lacuna de pesquisa:** Identifique a lacuna de pesquisa que o estudo pretende preencher."
        "\n- **Metodologia:** Detalhe os métodos utilizados no estudo."
        "\n- **Conjunto de dados:** Descreva o conjunto de dados usado no estudo."
        "\n- **Resultados:** Resuma as principais descobertas do estudo."
        "\n- **Limitações:** Discuta as limitações do estudo."
        "\n- **Conclusão:** Forneça a conclusão do estudo."
        "\n- **Direções Futuras:** Sugira possíveis direções para pesquisas futuras."
        "\n- **Avaliações:** Inclua quaisquer avaliações ou estimativas feitas no estudo."
    ),
    expected_output=f"Relatório completo profissionalmente estruturado sobre '{context_topic}' produzido com base no texto fornecido e no gerado nas tarefas anteriores.",
    agent=research_writer,
    async_execution=False,
    context=[list_topics_task, academic_review_task, website_list_task, tutorial_write_task],
    output_file=os.path.join(output_directory, "resumo.md")
)
