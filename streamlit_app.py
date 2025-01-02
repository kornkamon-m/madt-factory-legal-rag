import streamlit as st

st.title("Legal Advisory System")
    st.write("ระบบแนะนำและตอบคำถามเกี่ยวกับการขออนุญาตสำหรับโรงงานอาหาร")

    # Feature 1: ระบบแสดงคำแนะนำ
    st.header("แสดงคำแนะนำ")
    food_type = st.selectbox("เลือกประเภทอาหาร", metadata["food_types"])
    production_capacity = st.number_input("กำลังการผลิต (ตัน/วัน):", min_value=0.1, step=0.1)
    machine_power = st.number_input("ขนาดแรงม้า (HP):", min_value=1, step=1)
    if st.button("แสดงคำแนะนำ"):
        guidelines = get_guidelines(food_type, production_capacity, machine_power)
        if guidelines:
            st.success("คำแนะนำที่เหมาะสม:")
            for guideline in guidelines:
                st.write(f"- {guideline}")
        else:
            st.warning("ไม่พบคำแนะนำสำหรับข้อมูลที่ป้อน")

    # Feature 2: ระบบ Q&A
    st.header("ระบบ Q&A")
    query = st.text_input("ป้อนคำถาม:")
    if st.button("ค้นหา"):
        results = search_query(query, model, index, metadata)
        if results:
            st.success("คำตอบที่พบ:")
            top_context = "\n".join([result["content"] for result in results])
            response = generate_response(top_context, query)
            st.write("**คำตอบ:**")
            st.write(response)

            st.write("**บริบทที่เกี่ยวข้อง:**")
            for result in results:
                st.write(f"- {result['content'][:300]}...")
        else:
            st.warning("ไม่พบข้อมูลที่เกี่ยวข้อง")
