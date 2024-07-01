
import streamlit as st
import whisper
from audio_recorder_streamlit import audio_recorder
from index import sidebar
import openai
import os

with st.sidebar:
    st.page_link("index.py", label="inicio", icon="🏠")
    st.page_link("pages/arquivo1.py", label="CHATBOT", icon="🤖")
    st.page_link("pages/audio.py", label="CHATBOT POR VOZ", icon="🎙️")
    st.page_link("pages/texto.py", label="ANALISE SEU PDF", icon="📋")
    st.page_link("pages/Quiz.py", label="QUIZ", icon="🕹️")

with st.sidebar:
    st.subheader("______________________________")
    st.write("Desen. por Lucas Gustavo")
    st.markdown(
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")
    st.markdown(
        """
        <a href="https://www.facebook.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" width="30" style="margin-right: 10px;">
        </a>
        <a href="https://www.instagram.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="30" style="margin-right: 10px;">
        </a>
        <a href="https://www.linkedin.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo.svg" width="80" style="margin-right: 10px;">
        </a>
        <a href="https://www.youtube.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" width="30" style="margin-right: 10px;">
        </a>
        """,
        unsafe_allow_html=True
    )


# Função para adicionar CSS personalizado
def add_custom_css():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #4F4F4F;
            color: EEE8AA;
        }
        [data-testid="stSidebar"] * {
        color: white; /* Altera a cor do texto dentro do sidebar para branco */
    }

        }
        .stTextInput > div > div > input {
            width: 100%;
            height: 50px;
            background-color: #B0C4DE;
            color: black;
        }
        .main {
            background-color: white; 
        }
        .st-emotion-cache-18ni7ap{
            background-color: #DCDCDC; 
        }
        .st-emotion-cache-uhkwx6{
             background: #DCDCDC 
        }
        p{
            font-size: 20px;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# Adicionando CSS personalizado
add_custom_css()
st.title("Chatbot por voz")
# Definindo a chave da API da OpenAI
openai.api_key = "chave"
# Inicializando a lista de conversa
if 'conversa' not in st.session_state:
    st.session_state['conversa'] = [{"role": "assistant", "content": "Fale algo no microfonee para que eu possa lhe ajudar com desenvolvimento de software."}]
# Função para enviar a pergunta para a OpenAI e exibir a resposta
def enviar_pergunta_para_openai_e_exibir_resposta(pergunta):
    # Inclui o prompt inicial no começo da conversa interna
    conversa_interna = [
        {"role": "system", "content": ("Eu sou um assistente especializado em desenvolvimento de software. "
                                       "Eu respondo a perguntas sobre programação, sistemas de informação, engenharia de software, design de software, arquitetura de software, "
                                       "testes de software, metodologias ágeis, DevOps, segurança de software, bancos de dados, integração de sistemas, "
                                       "gerenciamento de projetos de software e qualquer outro tópico relacionado ao desenvolvimento de software. "
                                       "Por favor, me faça perguntas apenas sobre esses tópicos. Se sua pergunta não estiver relacionada a esses tópicos, "
                                       "eu responderei com: 'Me faça uma pergunta relacionada ao desenvolvimento de software'")}]
    # Adiciona a conversa real
    conversa_interna.extend(st.session_state['conversa'])

    # Adiciona a nova pergunta do usuário
    conversa_interna.append({"role": "user", "content": pergunta})

    # Chamando a API da OpenAI para obter resposta
    retorno_openai = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversa_interna,
        max_tokens=150,
        n=1
    )
    resposta = retorno_openai['choices'][0]['message']['content']
    st.session_state['conversa'].append({
        "role": "assistant",
        "content": resposta
    })


# Inicializando o gravador de áudio
audio_bytes = audio_recorder()

if audio_bytes:
    # Salvar os bytes do áudio em um arquivo
    with open("audio_gravado.wav", "wb") as f:
        f.write(audio_bytes)

    # Carregar o modelo Whisper
    modelo = whisper.load_model("base")

    # Transcrever o áudio
    resposta = modelo.transcribe("audio_gravado.wav")
    text = resposta['text']

    # Adicionando a pergunta real à lista de conversa
    st.session_state['conversa'].append({"role": "user", "content": text})

    # Obtém a resposta do modelo
    enviar_pergunta_para_openai_e_exibir_resposta(text)

# Exibe o histórico de chat invertido
if 'conversa' in st.session_state:
    for chat in st.session_state['conversa'][::-1]:
        st.chat_message(chat['role']).write(chat['content'])
