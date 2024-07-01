import streamlit as st
import openai
from index import sidebar

def java_file():

    sidebar()




    st.title("Quiz de Java")

    # Configurar a chave de API da OpenAI
    openai.api_key = "chave"

    # Inicializando variáveis no estado da sessão
    if 'perguntas' not in st.session_state:
        st.session_state['perguntas'] = []
    if 'alternativas' not in st.session_state:
        st.session_state['alternativas'] = []
    if 'respostas' not in st.session_state:
        st.session_state['respostas'] = []
    if 'pontuacao' not in st.session_state:
        st.session_state['pontuacao'] = 0
    if 'perguntas_respondidas' not in st.session_state:
        st.session_state['perguntas_respondidas'] = 0
    if 'resposta_selecionada' not in st.session_state:
        st.session_state['resposta_selecionada'] = None
    if 'mostrar_resposta' not in st.session_state:
        st.session_state['mostrar_resposta'] = False

    # Função para enviar a pergunta para a OpenAI e exibir resposta
    def enviar_pergunta_para_openai(pergunta):
        retorno_openai = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pergunta}],
            max_tokens=150,
            n=1
        )
        resposta = retorno_openai['choices'][0]['message']['content']
        return resposta

    # Função para gerar uma nova pergunta
    def gerar_pergunta():
        pergunta = ("Crie uma pergunta sobre Java com 4 alternativas, identificando qual é a correta. Formato: "
                    "Pergunta: ... A: ... B: ... C: ... D: ... Resposta: ...")
        pergunta_gerada = enviar_pergunta_para_openai(pergunta)

        # Extrair pergunta, alternativas e resposta correta da string gerada
        linhas = pergunta_gerada.split('\n')
        pergunta_texto = ""
        alternativa_a = ""
        alternativa_b = ""
        alternativa_c = ""
        alternativa_d = ""
        resposta_correta = ""

        for linha in linhas:
            if linha.startswith("Pergunta:"):
                pergunta_texto = linha.replace("Pergunta: ", "").strip()
            elif linha.startswith("A:"):
                alternativa_a = linha.replace("A: ", "A: ").strip()
            elif linha.startswith("B:"):
                alternativa_b = linha.replace("B: ", "B: ").strip()
            elif linha.startswith("C:"):
                alternativa_c = linha.replace("C: ", "C: ").strip()
            elif linha.startswith("D:"):
                alternativa_d = linha.replace("D: ", "D: ").strip()
            elif linha.startswith("Resposta:"):
                resposta_correta = linha.replace("Resposta: ", "").strip()

        # Adicionar a pergunta gerada e as alternativas à lista de perguntas
        st.session_state['perguntas'].append(pergunta_texto)
        st.session_state['alternativas'].append([alternativa_a, alternativa_b, alternativa_c, alternativa_d])
        st.session_state['respostas'].append(resposta_correta)

    # Verificar se precisamos gerar uma nova pergunta (apenas se ainda não tivermos 5 perguntas)
    if len(st.session_state['perguntas']) < 5:
        gerar_pergunta()

    # Exibir a pergunta atual
    pergunta_atual_index = st.session_state['perguntas_respondidas']
    if pergunta_atual_index < len(st.session_state['perguntas']):
        st.subheader("Pergunta gerada")
        st.write(st.session_state['perguntas'][pergunta_atual_index])
        alternativas = st.session_state['alternativas'][pergunta_atual_index]

        if not st.session_state['mostrar_resposta']:
            resposta_selecionada = st.radio(
                "Selecione a sua resposta:",
                alternativas,
                key=f"radio_{pergunta_atual_index}"
            )
            if st.button("Enviar Resposta"):
                st.session_state['resposta_selecionada'] = resposta_selecionada
                resposta_correta = st.session_state['respostas'][pergunta_atual_index]
                if resposta_selecionada.strip() == resposta_correta.strip():
                    st.session_state['pontuacao'] += 1
                st.session_state['mostrar_resposta'] = True
                st.experimental_rerun()
        else:
            st.write("Você selecionou: ", st.session_state['resposta_selecionada'])
            st.write("A resposta correta é: ", st.session_state['respostas'][pergunta_atual_index])
            if st.button("Próxima Pergunta"):
                st.session_state['mostrar_resposta'] = False
                st.session_state['perguntas_respondidas'] += 1
                st.experimental_rerun()
    else:
        st.write(f"Quiz terminado! Sua pontuação final é: {st.session_state['pontuacao']} de 5.")
        if st.session_state['pontuacao'] >= 3:
            st.success("Parabéns, você teve sucesso!")
        else:
            st.error("Você não obteve sucesso, estude mais.")
        if st.button("Refazer Quiz"):
            st.session_state.clear()
            st.experimental_rerun()
java_file()