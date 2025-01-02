import streamlit as st
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI

# Load FAISS database
def load_faiss():
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["openai"]["api_key"])
    vector_store = FAISS.load_local("path_to_faiss", embeddings)
    return vector_store

vector_db = load_faiss()

# Build conversational interface
st.title("Legal Advisory for Factory Setup")
query = st.text_input("Ask your legal question:")
if st.button("Submit"):
    retriever = vector_db.as_retriever()
    llm = OpenAI(model="gpt-3.5-turbo", api_key=st.secrets["openai"]["api_key"])
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    response = qa_chain.run(query)
    st.write(f"**Answer:** {response}")
