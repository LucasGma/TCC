import streamlit as st
import openai
from index import sidebar

sidebar()


# Chave da API da OpenAI
openai_api_key = "chave"

# Definindo a chave da API da OpenAI
openai.api_key = openai_api_key

st.title("Chatbot")

# Inicialização do histórico de mensagens no estado da sessão
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Como posso lhe ajudar com desenvolvimento de software?"}]

# Exibição das mensagens do histórico
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Captura da entrada do usuário
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    if not openai_api_key:
        st.stop()  # Interrompe a execução se a chave da API não estiver definida

    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Criação da mensagem de controle para envio à API
    chat = (
        "Eu sou um assistente especializado em desenvolvimento de software. "
        "Eu respondo a perguntas sobre programação, sistemas de informação, engenharia de software, design de software,"
        " arquitetura de software, "
        "testes de software, metodologias ágeis, DevOps, segurança de software, bancos de dados, integração de sistemas, "
        "gerenciamento de projetos de software e qualquer outro tópico relacionado ao desenvolvimento de software. "
        "Por favor, me faça perguntas apenas sobre esses tópicos. Se sua pergunta não estiver relacionada a esses tópicos, "
        "eu responderei com: 'Me faça uma pergunta relacionada ao desenvolvimento de software.'"
    )
    messages_to_send = st.session_state.messages + [{"role": "user", "content": chat + "\n" + prompt}]

    # Faz a solicitação à API da OpenAI para gerar uma resposta
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_to_send
    )

    # Obtém o conteúdo da resposta
    msg = response.choices[0].message["content"]

    # Adiciona a resposta do assistente ao histórico de mensagens
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)