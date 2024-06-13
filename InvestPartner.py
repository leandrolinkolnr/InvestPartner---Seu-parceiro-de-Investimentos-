import streamlit as st
import openai
from dotenv import load_dotenv, find_dotenv
import time
import yfinance as yf
import json
from unidecode import unidecode
import re
import pickle
from pathlib import Path
import asyncio
import concurrent.futures

PASTA_MENSAGENS = Path(__file__).parent / 'mensagens'    # Pegando o caminho atual e salvando na pasta 'mensagens'
PASTA_MENSAGENS.mkdir(exist_ok=True)                    # Criando a pasta

@st.cache_resource
def iniciaClient():
    _ = load_dotenv(find_dotenv())
    client = openai.Client()
    return client

client = iniciaClient()

@st.cache_data
def retorna_cotacao_acao_historica(ticker, periodo='1mo'):
    ticker = yf.Ticker(ticker)
    hist = ticker.history(period=periodo)['Close']
    #hist.index = hist.index.strftime('%Y-%m-%d')
    #hist = round(hist, 2)

    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]

    return hist.to_json()

@st.cache_data
def retorna_info(ticker):
    ticker = yf.Ticker(ticker)
    info = str(ticker.info)
    return info

@st.cache_data
def retorna_metadados(ticker, periodo):
    ticker = yf.Ticker(ticker)
    #hist = ticker.history(period=periodo)
    metadados = str(ticker.history_metadata)
    return metadados

@st.cache_data
def retorna_noticias(ticker):
    ticker = yf.Ticker(ticker)
    noticias = str(ticker.news)
    return noticias

@st.cache_data
def retorna_desdobramentos(ticker):
    ticker = yf.Ticker(ticker)
    desdobramentos = ticker.splits
    return desdobramentos.to_json()

funcoes_disponiveis = {
    'retorna_cotacao_acao_historica': retorna_cotacao_acao_historica,
    'retorna_info': retorna_info,
    'retorna_metadados': retorna_metadados,
    'retorna_noticias': retorna_noticias,
    'retorna_desdobramentos': retorna_desdobramentos
}


# def dispoe_tools():
#     tools = [
#         {
#             'type': 'function',
#             'function': {
#                 'name': 'retorna_cotacao_acao_historica',
#                 'description': 'Retorna a cotação diária histórica para uma ação da bovespa',
#                 'parameters': {
#                     'type': 'object',
#                     'properties': {
#                         'ticker': {
#                             'type': 'string',
#                             'description': 'O ticker da ação. Exemplo: "ABEV3.SA" para ambev, "PETR4.SA" para petrobras, etc'
#                         },
#                         'periodo': {
#                             'type': 'string',
#                             'description': 'O período que será retornado de dados históriocos \
#                                             sendo "1mo" equivalente a um mês de dados, "1d" a \
#                                             1 dia e "1y" a 1 ano',
#                             'enum': ["1d","5d","1mo","6mo","1y","5y","10y","ytd","max"]  # API so aceita esses dias
#                         }
#                     }
#                 }
#             }
#         },
        
        
        
        
        
#         {
#             'type': 'function',
#             'function': {
#                 'name': 'retorna_info',
#                 'description': 'Retorna informações gerais sobre uma ação, incluindo uma variedade de dados, \
#                 como o nome da empresa, setor da indústria, descrição da empresa, país de origem, e mais. É útil para obter \
#                 uma visão geral rápida e detalhes básicos sobre a empresa associada ao ticker fornecido.',
#                 'parameters': {
#                     'type': 'object',
#                     'properties': {
#                         'ticker': {
#                             'type': 'string',
#                             'description': 'O ticker da ação. Exemplo: "ABEV3.SA" para ambev, "PETR4.SA" para petrobras, etc'
#                         }
#                     }
#                 }
#             }
#         },
        
        
#         {
#             'type': 'function',
#             'function': {
#                 'name': 'retorna_metadados',
#                 'description': 'Fornece informações, de acordo com a data fornecida, sobre os dados históricos disponíveis para \
#                 uma ação, incluindo o intervalo de datas disponíveis, os tipos de preços incluídos  (como abertura, fechamento, \
#                 máximos, mínimos e volume), divisões de ações, ajustes de dividendos e outros eventos corporativos relevantes. \
#                 Essas informações são úteis para entender a qualidade e o escopo dos dados históricos disponíveis.',
#                 'parameters': {
#                     'type': 'object',
#                     'properties': {
#                         'ticker': {
#                             'type': 'string',
#                             'description': 'O ticker da ação. Exemplo: "ABEV3.SA" para ambev, "PETR4.SA" para petrobras, etc'
#                         },
#                         'periodo': {
#                             'type': 'string',
#                             'description': 'O período que será retornado de dados históriocos \
#                                             sendo "1mo" equivalente a um mês de dados, "1d" a \
#                                             1 dia e "1y" a 1 ano',
#                             'enum': ["1d","5d","1mo","6mo","1y","5y","10y","ytd","max"]  # API so aceita esses dias
#                         }
#                     }
#                 }
#             }
#         },
        
#         {
#             'type': 'function',
#             'function': {
#                 'name': 'retorna_noticias',
#                 'description': 'retorna uma lista de notícias recentes relacionadas à empresa. Ele fornece manchetes, datas e links para artigos sobre a empresa cujas ações são negociadas na bolsa',
#                 'parameters': {
#                     'type': 'object',
#                     'properties': {
#                         'ticker': {
#                             'type': 'string',
#                             'description': 'O ticker da ação. Exemplo: "ABEV3.SA" para ambev, "PETR4.SA" para petrobras, etc'
#                         }
#                     }
#                 }
#             }
#         },
        
        
#         {
#             'type': 'function',
#             'function': {
#                 'name': 'retorna_desdobramentos',
#                 'description': 'retorna uma série temporal contendo os históricos de desdobramentos (splits) de ações de uma empresa. Ele fornece as datas e as razões dos splits ocorridos ao longo do tempo para uma determinada ação listada na bolsa.',
#                 'parameters': {
#                     'type': 'object',
#                     'properties': {
#                         'ticker': {
#                             'type': 'string',
#                             'description': 'O ticker da ação. Exemplo: "ABEV3.SA" para ambev, "PETR4.SA" para petrobras, etc'
#                         }
#                     }
#                 }
#             }
#         },
        
        
#         {'type': 'code_interpreter'}
        
        
#         ]
    
#     return tools



# assistant = client.beta.assistants.create(
#     name="Assistente Financeiro",
#     instructions="Você é um assistente pessoal de investimentos especializado na área de ações da bolsa de valores do Brasil. \
#                   Sua função é responder perguntas dos usuários relacionadas ao mercado de ações brasileiro. Utilize as \
#                   ferramentas e funções disponíveis, juntamente com a API Yfinance, para fornecer respostas precisas e \
#                   relevantes. Certifique-se de oferecer informações atualizadas e insights úteis para auxiliar os usuários em \
#                   suas decisões de investimento. Priorize a clareza e a precisão em suas respostas, garantindo uma experiência \
#                   satisfatória para os usuários que buscam orientação no mercado de ações brasileiro.",
#     #model="gpt-4o",
#     model = "gpt-3.5-turbo-0125",
#     tools=tools
# )




assistant_id = "asst_D72a8kRFXV99YSw4x8zKxS1Z"

@st.cache_resource
def criar_thread():
    thread = client.beta.threads.create()
    return thread

async def retorna_resposta_modelo(mensagens):
    start_time = time.time()
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
                                  assistant_id=assistant_id,
                                  instructions='Seja breve e conciso na resposta')

    while run.status in ['queued', 'in_progress', 'cancelling']:
        await asyncio.sleep(0.1)
        run = await asyncio.to_thread(client.beta.threads.runs.retrieve,
                                      thread_id=thread.id,
                                      run_id=run.id)

    if run.status == 'completed':
        messages = await asyncio.to_thread(client.beta.threads.messages.list,
                                           thread_id=thread.id)
        print(messages)

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

    #print(f"Tempo total de resposta: {time.time() - start_time} segundos")
    return resposta

def salvar_mensagens(mensagens):
    if len(mensagens) == 0:
        return False
    nome_mensagem = retorna_nome_da_mensagem(mensagens)
    nome_arquivo = converte_nome_mensagem(nome_mensagem)
    arquivo_salvar = {'nome_mensagem': nome_mensagem,
                      'nome_arquivo': nome_arquivo,
                      'mensagem': mensagens}

    with open(PASTA_MENSAGENS / nome_arquivo, 'wb') as f:
        pickle.dump(arquivo_salvar, f)

def retorna_nome_da_mensagem(mensagens):
    nome_mensagem = ''
    for mensagem in mensagens:
        if mensagem['role'] == 'user':
            nome_mensagem = mensagem['content'][:30]
            break
    return nome_mensagem

def converte_nome_mensagem(nome_mensagem):
    nome_arquivo = unidecode(nome_mensagem)
    nome_arquivo = re.sub('\W+', '', nome_arquivo).lower()
    return nome_arquivo

def ler_mensagens(mensagens, key='mensagem'):
    if len(mensagens) == 0:
        return []
    nome_mensagem = retorna_nome_da_mensagem(mensagens)
    nome_arquivo = converte_nome_mensagem(nome_mensagem)
    with open(PASTA_MENSAGENS / nome_arquivo, 'rb') as f:
        mensagens = pickle.load(f)
    return mensagens[key]

async def processa_mensagens(prompt):
    nova_mensagem = {'role': 'user', 'content': prompt}
    st.session_state['mensagens'].append(nova_mensagem)

    chat = st.chat_message('assistant')
    placeholder = chat.empty()
    placeholder.markdown("▌")
    respostas = await retorna_resposta_modelo(prompt)
    placeholder.markdown(respostas)

    nova_mensagem = {'role': 'assistant', 'content': respostas}
    st.session_state['mensagens'].append(nova_mensagem)
    salvar_mensagens(st.session_state['mensagens'])

def pagina_principal():
    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

    mensagens = ler_mensagens(st.session_state['mensagens'])
    st.header('🤖  InvestPartner', divider=True)

    for mensagem in mensagens:
        chat = st.chat_message(mensagem['role'])
        chat.markdown(mensagem['content'])

    prompt = st.chat_input('Pergunte ao seu parceiro de investimentos! :)')
    if prompt:
        chat = st.chat_message('user')
        chat.markdown(prompt)
        asyncio.run(processa_mensagens(prompt))

pagina_principal()
