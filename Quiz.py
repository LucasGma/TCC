import streamlit as st
from pages import java
from index import sidebar


sidebar()
st.title("Quiz")
def main():
    opcao = st.selectbox("Escolha uma opção:", ["Selecione uma opção", "Java", "Python", "Algoritmo"])

    # Botão para redirecionar para outra página com base na opção selecionada
    if st.button("Ir para o quiz"):
        if opcao != "Selecione uma opção":
            if opcao == "Java":
                st.page_link("pages/java.py", label="Quiz Java")
            elif opcao == "Python":
                st.page_link("pages/python.py",label="Quiz Python")
            elif opcao == "Algoritmo":
                st.page_link("pages/algoritimo.py",label="Algoritimo Quiz")

# Executa a função principal
if __name__ == "__main__":
    main()
