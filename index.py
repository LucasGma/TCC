import streamlit as st


def sidebar():
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
            background-color: #DCDCDC; 
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


def mostrar_titulo():
    st.title("Bem-vindo ao chatbot, programador")


if __name__ == '__main__':
    sidebar()
    mostrar_titulo()
