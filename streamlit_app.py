import streamlit as st
from functions import load_data, search_similarity, generate_response, generate_legal_steps

# Path to Preprocessed Data
DATA_PATH = "embedded_chunks.csv"

# Load Data
df_chunks = load_data(DATA_PATH)

# Streamlit UI
def main():
    st.title("Legal Advisory System")
    st.write("ระบบแนะนำและตอบคำถามด้านกฎหมายสำหรับโรงงานอาหาร")

    # Feature 1: ระบบแสดงคำแนะนำการขออนุญาต
    st.header("1. ระบบแสดงคำแนะนำการขออนุญาต")
    with st.form("legal_form"):
        food_type = st.text_input("ประเภทอาหาร:")
        production_capacity = st.number_input("กำลังการผลิต (ตัน/วัน):", min_value=0.0, step=0.1)
        machine_power = st.number_input("ขนาดแรงม้า (HP):", min_value=0, step=1)
        submitted = st.form_submit_button("แสดงคำแนะนำ")
        
        if submitted:
            steps = generate_legal_steps(food_type, production_capacity, machine_power)
            st.subheader("คำแนะนำ:")
            st.write(steps)

    # Feature 2: ระบบ Q&A
    st.header("2. ระบบ Q&A")
    query = st.text_input("ป้อนคำถามที่ต้องการค้นหา:")
    if query:
        results = search_similarity(query, df_chunks)
        top_context = "\n".join(results['content'].values)
        
        # Generate Answer
        answer = generate_response(top_context, query)
        
        st.subheader("คำตอบ:")
        st.write(answer)
        
        st.subheader("บริบทที่เกี่ยวข้อง:")
        for _, row in results.iterrows():
            st.write(f"- {row['content'][:300]}...")

if __name__ == "__main__":
    main()
