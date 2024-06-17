
from utils_Files import *
from utils_OpenAI import *
from utils_Tools import *



# =========================== Inicialização ===========================


@st.cache_resource
def inicializacao():

    _ = yf.Ticker("ABEV3.SA").history(period='1d')['Close']  # Iniciando API

    if not 'mensagens' in st.session_state:
        st.session_state.mensagens = []
    if not 'conversa_atual' in st.session_state:
        st.session_state.conversa_atual = ''
    if not 'modelo' in st.session_state:
        st.session_state.modelo = 'gpt-3.5-turbo'





# =========================== TABS ===========================


def tab_conversas(tab):
    tab.button('➕ Nova conversa',                  # Iniciando nova conversa
                on_click=seleciona_conversa,
                args=('', ),
                use_container_width=True)
    tab.markdown('')

    conversas = listar_conversas()                  # Listando conversas existentes

    for nome_arquivo in conversas:
        nome_mensagem = desconverte_nome_mensagem(nome_arquivo).capitalize()
        if len(nome_mensagem) == 30:
            nome_mensagem += '...'
        tab.button(nome_mensagem,
            on_click=seleciona_conversa,
            args=(nome_arquivo, ),
            disabled=nome_arquivo==st.session_state['conversa_atual'],
            use_container_width=True)



def seleciona_conversa(nome_arquivo):
    if nome_arquivo == '':
        st.session_state['mensagens'] = []
    else:
        mensagem = ler_mensagem_por_nome_arquivo(nome_arquivo)
        st.session_state['mensagens'] = mensagem
    st.session_state['conversa_atual'] = nome_arquivo




def tab_configuracoes(tab):
    
    modelo_escolhido = tab.selectbox('Selecione o modelo',
                                     ['gpt-3.5-turbo', 'gpt-4'])
    st.session_state['modelo'] = modelo_escolhido

    if (modelo_escolhido == "gpt-3.5-turbo"):
        st.session_state.id_assistant = "asst_zH3fnRmniBiWJkzLiu3sTplM"
    elif (modelo_escolhido == "gpt-4"):
        st.session_state.id_assistant = "asst_VTWGUwSpjMaLV3XDHgb61Gk7"






# ===========================  PAgina Inicial ===========================



def pagina_principal():
    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

    mensagens = ler_mensagens(st.session_state['mensagens'])
    if 'header' not in st.session_state:
        st.session_state.header = []
        st.header('🤖  InvestPartner', divider=True)

    for mensagem in mensagens:
        chat = st.chat_message(mensagem['role'])
        chat.markdown(mensagem['content'])


    st.session_state.prompt = []
    prompt = st.chat_input('Pergunte ao seu parceiro de investimentos! :)')
    if prompt:
        chat = st.chat_message('user')
        chat.markdown(prompt)
        asyncio.run(processa_mensagens(prompt))





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





# ===========================  Main  ===========================


def main():
    inicializacao()
    pagina_principal()
    tab1, tab2 = st.sidebar.tabs(['Conversas', 'Configurações'])   # Adiciondo SideBar
    tab_conversas(tab1)
    tab_configuracoes(tab2)



if __name__ == '__main__':
    main()
