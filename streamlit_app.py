import streamlit as st

# หน้า Landing Page
st.title("AI Advisory for Food Factory Setup")
st.write("ระบบแนะนำข้อกำหนดทางกฎหมายและขั้นตอนการขออนุญาตจัดตั้งโรงงานอาหารในประเทศไทย")
if st.button("เริ่มต้นใช้งาน"):
    st.session_state.page = "input"

# หน้า Input ข้อมูล
if st.session_state.get('page') == "input":
    st.header("กรอกข้อมูลโรงงาน")
    factory_type = st.selectbox("เลือกประเภทอาหาร", ["ผลไม้แปรรูป", "น้ำดื่มบรรจุขวด", "ผลิตภัณฑ์นม", "อื่นๆ"])
    production_capacity = st.number_input("กำลังการผลิต (ตัน/วัน)", min_value=0)
    horsepower = st.number_input("ขนาดแรงม้า (HP)", min_value=0)
    workers = st.number_input("จำนวนแรงงาน", min_value=0)
    location = st.selectbox("จังหวัดที่ตั้งโรงงาน", ["กรุงเทพฯ", "ชลบุรี", "สมุทรสาคร", "อื่นๆ"])

    if st.button("ค้นหาข้อกำหนดทางกฎหมาย"):
        st.session_state.page = "output"

# หน้า Output
if st.session_state.get('page') == "output":
    st.header("ผลลัพธ์การวิเคราะห์")
    st.subheader("ข้อกำหนดทางกฎหมาย")
    st.write("- พระราชบัญญัติโรงงาน พ.ศ. 2535")
    st.write("- มาตรฐาน GMP/HACCP")
    st.write("- ต้องทำ EIA: **ไม่จำเป็น** (ขึ้นกับกำลังการผลิต)")

    st.subheader("ขั้นตอนการขอใบอนุญาต")
    st.write("1. เตรียมเอกสารแบบ รง.4")
    st.write("2. ยื่นต่อกรมโรงงานอุตสาหกรรม")

    # Q&A Bot
    st.subheader("มีคำถามเพิ่มเติมหรือไม่?")
    user_question = st.text_input("ป้อนคำถามที่นี่")
    if st.button("ถาม"):
        st.write(f"คำตอบสำหรับ: {user_question}")  # เชื่อมต่อกับ RAG ได้ที่นี่

    # Feedback
    st.subheader("ให้ความคิดเห็น")
    feedback = st.text_area("ความคิดเห็น")
    if st.button("ส่งความคิดเห็น"):
        st.success("ขอบคุณสำหรับความคิดเห็น!")
