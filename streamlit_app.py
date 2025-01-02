import streamlit as st
from google.generativeai import generate_text

# Set up the page title
st.title("AI Advisory for Food Factory Setup")
st.subheader("ระบบแนะนำข้อกำหนดทางกฎหมายและขั้นตอนการขออนุญาตจัดตั้งโรงงานอาหารในประเทศไทย")

# Gemini API Key Input Section
if "api_key" not in st.session_state:
    st.session_state["api_key"] = None

if not st.session_state["api_key"]:
    st.warning("กรุณาใส่ API Key ของ Gemini ก่อนดำเนินการต่อ")
    api_key_input = st.text_input("กรอก Gemini API Key:", type="password")
    if st.button("ยืนยัน API Key"):
        if api_key_input:
            st.session_state["api_key"] = api_key_input
            st.success("API Key ถูกบันทึกแล้ว")
        else:
            st.error("กรุณากรอก API Key")
else:
    # Input form for user data
    st.header("กรอกข้อมูลโรงงาน")
    with st.form("factory_form"):
        factory_type = st.selectbox("เลือกประเภทอาหาร", ["ผลไม้แปรรูป", "น้ำดื่มบรรจุขวด", "ผลิตภัณฑ์นม", "อื่นๆ"])
        production_capacity = st.number_input("กำลังการผลิต (ตัน/วัน)", min_value=0, step=1)
        machine_power = st.number_input("ขนาดแรงม้า (HP)", min_value=0, step=1)

        submit_button = st.form_submit_button("ยืนยันข้อมูล")

    # Context generation and API interaction
    if submit_button:
        st.write("ข้อมูลที่ได้รับ:")
        st.write(f"- ประเภทโรงงาน: {factory_type}")
        st.write(f"- กำลังการผลิต: {production_capacity} ตัน/วัน")
        st.write(f"- ขนาดแรงม้า: {machine_power} HP")

        # Prompt structure
        input_query = st.text_input("ระบุคำถามเกี่ยวกับโรงงาน:", "")
        if input_query:
            context = "ข้อมูลบริบทอื่นๆ ที่เกี่ยวข้องกับกฎหมายโรงงานและอาหาร"  # Adjust with dynamic context if available
            prompt = f"""
            คุณคือที่ปรึกษาด้านกฎหมายและระเบียบข้อบังคับสำหรับโรงงานอาหารในประเทศไทย 
            ระบบนี้ต้องให้คำแนะนำที่ถูกต้อง ครบถ้วน และชัดเจน โดยอิงจากข้อมูลที่ได้รับและบริบทที่เกี่ยวข้อง

            **คำถาม**:
            {input_query}

            **ข้อมูลที่ได้รับจากผู้ใช้งาน**:
            - ประเภทโรงงาน: {factory_type}
            - กำลังการผลิต: {production_capacity} ตัน/วัน
            - ขนาดแรงม้าเครื่องจักร: {machine_power} HP

            **บริบท**:
            {context}

            **คำแนะนำที่ต้องการ**:
            1. สรุปข้อกำหนดทางกฎหมายและข้อบังคับที่เกี่ยวข้องกับประเภทโรงงานดังกล่าว.
            2. ระบุใบอนุญาตและเอกสารที่จำเป็น รวมถึงหน่วยงานที่เกี่ยวข้อง.
            3. จัดทำขั้นตอนการดำเนินการเพื่อขออนุญาตและการปฏิบัติตามข้อกำหนด.
            4. ให้คำแนะนำเพิ่มเติมเกี่ยวกับแนวทางปฏิบัติที่ช่วยเพิ่มความสอดคล้องและประสิทธิภาพ.

            **คำตอบที่คาดหวัง**:
            - ใช้ภาษาที่กระชับและเข้าใจง่าย.
            - ระบุข้อกำหนดหรือมาตราที่เกี่ยวข้องในกฎหมาย (ถ้ามี).
            - แนะนำขั้นตอนการดำเนินการและเอกสารที่จำเป็น.
            - เพิ่มคำแนะนำเพิ่มเติมที่ช่วยให้โรงงานดำเนินการได้อย่างราบรื่น.

            คำตอบ:
            """

            # Send the prompt to the generative AI model
            try:
                response = generate_text(prompt, api_key=st.session_state["api_key"])

                # Display the response
                if response:
                    st.subheader("คำแนะนำ:")
                    st.write(response.get("text", "ไม่สามารถให้คำแนะนำได้ในขณะนี้"))
                else:
                    st.error("ไม่สามารถเชื่อมต่อกับระบบ AI ได้ กรุณาลองใหม่อีกครั้ง")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
