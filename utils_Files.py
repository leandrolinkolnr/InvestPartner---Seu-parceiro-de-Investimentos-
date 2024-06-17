import pickle
from pathlib import Path
from unidecode import unidecode
import re


PASTA_MENSAGENS = Path(__file__).parent / 'mensagens'    # Pegando o caminho atual e salvando na pasta 'mensagens'
PASTA_MENSAGENS.mkdir(exist_ok=True)                    # Criando a pasta
CACHE_DESCONVERTE = {}



def converte_nome_mensagem(nome_mensagem):
    nome_arquivo = unidecode(nome_mensagem)
    nome_arquivo = re.sub('\\W+', '', nome_arquivo).lower()
    return nome_arquivo



def desconverte_nome_mensagem(nome_arquivo):    # Recolocando acentos, caracteres, etc
    if not nome_arquivo in CACHE_DESCONVERTE:    
        nome_mensagem = ler_mensagem_por_nome_arquivo(nome_arquivo, key='nome_mensagem')
        CACHE_DESCONVERTE[nome_arquivo] = nome_mensagem
    return CACHE_DESCONVERTE[nome_arquivo]



def retorna_nome_da_mensagem(mensagens):
    nome_mensagem = ''
    for mensagem in mensagens:
        if mensagem['role'] == 'user':
            nome_mensagem = mensagem['content'][:30]
            break
    return nome_mensagem



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




def ler_mensagem_por_nome_arquivo(nome_arquivo, key='mensagem'):
    with open(PASTA_MENSAGENS / nome_arquivo, 'rb') as f:
        mensagens = pickle.load(f)
    return mensagens[key]




def ler_mensagens(mensagens, key='mensagem'):
    if len(mensagens) == 0:
        return []
    nome_mensagem = retorna_nome_da_mensagem(mensagens)
    nome_arquivo = converte_nome_mensagem(nome_mensagem)
    with open(PASTA_MENSAGENS / nome_arquivo, 'rb') as f:
        mensagens = pickle.load(f)
    return mensagens[key]




def listar_conversas():             # Listar todas as conversas salvas no diretorio
    conversas = list(PASTA_MENSAGENS.glob('*'))  
    conversas = sorted(conversas, key=lambda item: item.stat().st_mtime_ns, reverse=True)   # Sort por mais recentes
    return [c.stem for c in conversas]










