from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
assistant_id = "ID_DO_SEU_ASSISTENTE"

assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)

conversa_thread = client.beta.threads.create()
tools = []

def get_gpt_completion(message, agent, tools_agent, thread):
    
    """ Executa uma thread com base em uma mensagem fornecida e recupera o resultado da conclusão.
    
    Esta função envia uma mensagem para uma thread específica, acionando a execução de uma matriz de funções
    definidas dentro de um parâmetro de função. Cada função na matriz deve implementar um método run() que retorna os outputs.
    
    Parâmetros:

    - message (str): A mensagem de entrada a ser processada.
    - agent (OpenAI Assistant): A instância do agente que processará a mensagem.
    - tools_agent (list): Uma lista de objetos de ferramentas, definidos com a biblioteca do instrutor.
    - thread (Thread): A thread da API do OpenAI Assistants responsável por gerenciar o fluxo de execução.
    
    Retorna:
    str: O output de conclusão como uma string, obtido do agente após a execução da mensagem de entrada e das funções. 
    """

    # create new message in the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # run this thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=agent.id,
    )

    while True:
        # wait until run completes
        while run.status in ['queued', 'in_progress']:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            # time.sleep(1)

        # function execution
        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                print(str(tool_call.function))
                # find the tool to be executed
                func = next(iter([func for func in tools_agent if func.__name__ == tool_call.function.name]))

                try:
                    # init tool
                    func = func(**eval(tool_call.function.arguments))
                    # get outputs from the tool
                    output = func.run()
                except Exception as e:
                    output = "Error: " + str(e)

                print(f"{tool_call.function.name}: ", output)
                tool_outputs.append({"tool_call_id": tool_call.id, "output": output})

            # submit tool outputs
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        # error
        elif run.status == "failed":
            raise Exception("Run Failed. Error: ", run.last_error)
        # return assistant message
        else:
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            message = messages.data[0].content[0].text.value

            return message
        

print("Chat iniciado")

while True:
    mensagem = input("Você: ")

    if mensagem.lower().startswith("sair"):
        break

    resposta = get_gpt_completion(mensagem, assistant, tools, conversa_thread)
    print("Chat:", resposta)

print("Fim do chat")
