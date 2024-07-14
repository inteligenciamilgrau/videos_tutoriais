from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults # pip install -U duckduckgo-search
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os

def funcao_posterior(contexto):
    # salvar um arquivo
    # enviar_email(contexto)
    # enviar um email
    # atualizar um banco de dados
    # enviar uma mensagem de whats
    print("Terminei de rodar tudo!")

def funcao_segunda(contexto):
    ## fazer outra atividade
    print("Atividade 1")

modo = "noticia"

if modo == "busca":
    search_tool = DuckDuckGoSearchRun()  # busca
elif modo == "noticia":
    search_tool = DuckDuckGoSearchResults(backend="news")


joao_pesquisador = Agent(
    role='O seu papel é fazer pesquisas excelentes sobre tecnologia ',
    goal='Encontrar as melhores notícias que falam sobre IA',
    backstory="""
    Você trabalha em uma agência de marketing e deve fazer a newsletter
    diária das tendencias atuais de tecnologia
""",
    verbose=False,
    allow_delegation=False,
    tools=[search_tool],
    max_iter=10,
    # llm=ChatOpenAI(model_name="llama2", temperature=0.7)
    llm=ChatOpenAI(model_name="gpt-4o", temperature=0.1, verbose=True)
)


maria_escritora = Agent(
    role='O seu papel é fazer fazer textos sobre tecnologia',
    goal='Escrever textos chamativos que falam sobre IA',
    backstory="""
    Você trabalha em uma agência de marketing e deve fazer a newsletter
    diária com textos sobre tecnologia que chamem a atenção do público
""",
    verbose=False,
    allow_delegation=False,
    tools=[search_tool],
    max_iter=10,
    # llm=ChatOpenAI(model_name="llama2", temperature=0.7)
    # llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1, verbose=True)
    llm=ChatOpenAI(model_name="gpt-4o", temperature=0.1)
)

task1 = Task(
    description="""
    Pesquisar notícias de IA. Não esqueça de fornecer a URL dos sites encontrados. 
    """,
    agent=joao_pesquisador,
    expected_output="""
        Sua resposta precisa ser em português no seguinte formato:

        Noticia 1: A tendencia encontrada é que a Ia vai se tornar cada...
        Link: https://www.site.com.br

        Noticia 2: Há um crescimento de interesse...
        Link: https://www.site2.com.br
    """,
    callback=funcao_segunda,
)

task2 = Task(
    description="""
    Escrever sobre as tendencias de IA em 2024.
    """,
    agent=maria_escritora,
    expected_output="""
        Sua resposta precisa ser em português no seguinte formato:

        Título: Tendencias em 2024 são ...
        Texto: As novidades não param de chegar....
    """,
    callback=funcao_posterior,
)

crew = Crew(
    agents=[joao_pesquisador, maria_escritora],
    tasks=[task1, task2],
    verbose=2,
    process=Process.sequential,
)

result = crew.kickoff()
print("Resultado Final", result)
