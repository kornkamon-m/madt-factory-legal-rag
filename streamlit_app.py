import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# เริ่มต้น UI
st.title("AI Advisory for Food Factory Setup")
st.write("ระบบแนะนำข้อกำหนดทางกฎหมายและขั้นตอนการจัดตั้งโรงงานอาหาร")

# ฟังก์ชันดึงข้อมูลจาก Vector DB
@st.cache_resource
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    vector_store = FAISS.load_local("vector_db", embeddings)
    return vector_store

# โหลด Vector Store
vector_db = load_vector_store()

# Prompt Template สำหรับ Generative AI
prompt_template = """
คุณเป็น AI ที่ช่วยแนะนำกฎหมายและขั้นตอนการจัดตั้งโรงงานในประเทศไทย
ใช้ข้อมูลที่มีบริบทเกี่ยวข้องจาก Vector Database ในการสร้างคำตอบที่ชัดเจนและเข้าใจง่าย:

คำถาม: {question}
ข้อมูลที่เกี่ยวข้อง: {context}

คำตอบที่ชัดเจน:
"""

# ฟังก์ชัน Q&A โดยใช้ Retrieval + Generative AI
def retrieve_and_generate(query):
    retriever = vector_db.as_retriever()
    llm = OpenAI(model="gpt-3.5-turbo")
    prompt = PromptTemplate(template=prompt_template, input_variables=["question", "context"])
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain.run(query)

# Input Form สำหรับข้อมูลโรงงาน
with st.form("factory_input"):
    st.subheader("กรอกข้อมูลโรงงาน")
    factory_type = st.selectbox("ประเภทอาหาร", ["ผลไม้แปรรูป", "น้ำดื่มบรรจุขวด", "ผลิตภัณฑ์นม", "อื่นๆ"])
    production_capacity = st.number_input("กำลังการผลิต (ตัน/วัน)", min_value=1)
    horsepower = st.number_input("ขนาดแรงม้า (HP)", min_value=1)
    workers = st.number_input("จำนวนแรงงาน", min_value=1)
    location = st.text_input("ที่ตั้งโรงงาน (จังหวัด)")

    submit_button = st.form_submit_button("ค้นหาข้อกำหนด")

if submit_button:
    st.success("ข้อมูลถูกบันทึก! คุณสามารถถามคำถามเพิ่มเติมเกี่ยวกับกฎหมายได้")

# Conversation Q&A
st.subheader("ถามคำถามเกี่ยวกับการจัดตั้งโรงงาน")
query = st.text_input("ป้อนคำถามที่นี่:", placeholder="เช่น โรงงานผลิตน้ำดื่มต้องทำ EIA ไหม?")
if st.button("ถาม"):
    if query:
        with st.spinner("กำลังประมวลผล..."):
            response = retrieve_and_generate(query)
            st.write("**คำตอบ:**")
            st.write(response)
    else:
        st.warning("กรุณาป้อนคำถาม")

# ส่วนแสดงประวัติการถาม-ตอบ
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if query:
    st.session_state.conversation_history.append({"question": query, "answer": response})

st.subheader("ประวัติการสนทนา")
for i, qa in enumerate(st.session_state.conversation_history):
    st.write(f"**คำถาม {i+1}:** {qa['question']}")
    st.write(f"**คำตอบ:** {qa['answer']}")
