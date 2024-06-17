import yfinance as yf
import streamlit as st

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


# @st.cache_resource
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