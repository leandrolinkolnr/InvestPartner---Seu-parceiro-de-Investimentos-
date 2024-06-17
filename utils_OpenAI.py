import openai
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import asyncio
import concurrent.futures
import json

from utils_Tools import funcoes_disponiveis



@st.cache_resource
def iniciaClient():

    _ = load_dotenv(find_dotenv())
    client = openai.Client()
    return client


client = iniciaClient()


# @st.cache_resource
# def criaAssistant(modelo):
#     assistant = client.beta.assistants.create(
#         name="Assistente Financeiro",
#         instructions="Você é um assistente pessoal de investimentos especializado na área de ações da bolsa de valores do Brasil. \
#                     Sua função é responder perguntas dos usuários relacionadas ao mercado de ações brasileiro. Utilize as \
#                     ferramentas e funções disponíveis, juntamente com a API Yfinance, para fornecer respostas precisas e \
#                     relevantes. Certifique-se de oferecer informações atualizadas e insights úteis para auxiliar os usuários em \
#                     suas decisões de investimento. Priorize a clareza e a precisão em suas respostas, garantindo uma experiência \
#                     satisfatória para os usuários que buscam orientação no mercado de ações brasileiro.",
#         model = st.session_state['modelo'],
#         tools=dispoe_tools()
#         ) 
#     return assistant.id




@st.cache_resource
def criar_thread():
    thread = client.beta.threads.create()
    return thread

                                    

async def retorna_resposta_modelo(mensagens):
    
    thread = criar_thread()

    await asyncio.to_thread(client.beta.threads.messages.create,
                            thread_id=thread.id,
                            role='user',
                            content=[
                                {
                                    "type": "text",
                                    "text": mensagens
                                }
                            ])

    run = await asyncio.to_thread(client.beta.threads.runs.create,
                                  thread_id=thread.id,
                                  assistant_id=st.session_state.id_assistant,
                                  instructions='Seja breve e conciso na resposta')

    while run.status in ['queued', 'in_progress', 'cancelling']:
        #await asyncio.sleep(0.1)
        run = await asyncio.to_thread(client.beta.threads.runs.retrieve,
                                      thread_id=thread.id,
                                      run_id=run.id)

    if run.status == 'completed':
        messages = await asyncio.to_thread(client.beta.threads.messages.list,
                                           thread_id=thread.id)


    tool_outputs = []
    tool_calls = run.required_action.submit_tool_outputs.tool_calls

    if tool_calls:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for tool in tool_calls:
                func_name = tool.function.name
                function_to_call = funcoes_disponiveis[func_name]
                func_args = json.loads(tool.function.arguments)
                futures.append(executor.submit(function_to_call, **func_args))
            for future in concurrent.futures.as_completed(futures):
                try:
                    tool_output = future.result()
                    tool_outputs.append({
                        'tool_call_id': tool.id,
                        'output': tool_output
                    })
                except Exception as e:
                    print(f"Error in tool execution: {e}")

    if tool_outputs:
        try:
            run = await asyncio.to_thread(client.beta.threads.runs.submit_tool_outputs_and_poll,
                                          thread_id=thread.id,
                                          run_id=run.id,
                                          tool_outputs=tool_outputs)
        except Exception as e:
            print("Failed to submit tool outputs:", e)

    if run.status == 'completed':
        messages = await asyncio.to_thread(client.beta.threads.messages.list,
                                           thread_id=thread.id)
        resposta = messages.data[0].content[0].text.value
    else:
        print(run.status)


    return resposta