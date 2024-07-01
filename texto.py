import streamlit as st
import PyPDF2
import openai
from index import sidebar

# Função para ler o conteúdo de um arquivo PDF
def ler_pdf(arquivo):
    leitor_pdf = PyPDF2.PdfReader(arquivo)
    texto = ''
    for pagina in leitor_pdf.pages:
        texto += pagina.extract_text()
    return texto

def perguntar(conteudo, pergunta, chave_api):
    openai.api_key = chave_api

    # Limita o conteúdo do PDF a ser enviado para a API
    tamanho_maximo_conteudo = 2000  # Ajuste conforme necessário
    conteudo_truncado = conteudo[:tamanho_maximo_conteudo]

    mensagens = [
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": f"O seguinte é o conteúdo de um documento:\n\n{conteudo_truncado}"},
        {"role": "user", "content": pergunta},
    ]

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mensagens,
        max_tokens=150,
        temperature=0.7,
    )

    resposta_final = resposta.choices[0].message['content'].strip()
    return resposta_final

# Inicializa o histórico de chat na sessão
if 'historico_chat' not in st.session_state:
    st.session_state.historico_chat = []

st.title('Analise seu PDF')

arquivo_enviado = st.file_uploader("Faça o upload do seu PDF", type=["pdf"])

if arquivo_enviado is not None:
    # Leitura do conteúdo do PDF
    conteudo_pdf = ler_pdf(arquivo_enviado)
    st.text_area("Seu PDF", conteudo_pdf, height=300)

    chave_api = "chave"

    if entrada_pergunta := st.chat_input("Digite sua pergunta aqui"):
        # Adiciona a pergunta ao histórico de chat
        st.session_state.historico_chat.append({"role": "user", "content": entrada_pergunta})

        # Obtém a resposta do modelo
        resposta = perguntar(conteudo_pdf, entrada_pergunta, chave_api)

        # Adiciona a resposta ao histórico de chat
        st.session_state.historico_chat.append({"role": "assistant", "content": resposta})

# Exibe o histórico de chat
if st.session_state.historico_chat:
    for chat in st.session_state.historico_chat:
        st.chat_message(chat['role']).write(chat['content'])

# Chamando a função sidebar
sidebar()

