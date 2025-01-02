import streamlit as st
import google.generativeai as genai

# Set up the page title
st.title("AI Advisory for Food Factory Setup")
st.subheader("ระบบแนะนำข้อกำหนดทางกฎหมายและขั้นตอนการขออนุญาตจัดตั้งโรงงานอาหารในประเทศไทย")

# Capture Gemini API Key 
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password") 

# Define a persona and instructions to guide the AI's behavior as a coffee expert
coffee_expert_persona = """
คุณคือที่ปรึกษาด้านกฎหมายและระเบียบข้อบังคับสำหรับโรงงานอาหารในประเทศไทย 
ระบบนี้ต้องให้คำแนะนำที่ถูกต้อง ครบถ้วน และชัดเจน โดยอิงจากข้อมูลที่ได้รับและบริบทที่เกี่ยวข้อง

**คำตอบที่คาดหวัง**:
- ใช้ภาษาที่กระชับและเข้าใจง่าย.
- ระบุข้อกำหนดหรือมาตราที่เกี่ยวข้องในกฎหมาย และเนื้อหาในข้อกำหนดนั้น
"""

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize the Gemini Model 
if gemini_api_key: 
    try: 
        # Configure Gemini with the provided API Key 
        genai.configure(api_key=gemini_api_key) 
        model = genai.GenerativeModel("gemini-pro") 
        st.success("Gemini API Key successfully configured.") 
        
    except Exception as e: 
        st.error(f"An error occurred while setting up the Gemini model: {e}") 

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    avatar = "🏭" if role == "assistant" else "👤"  # Coffee cup emoji for assistant, person emoji for user
    st.chat_message(role, avatar=avatar).markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("สอบถามข้อมูลที่เกี่ยวข้องกับข้อกำหนดโรงงานอาหาร......."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user", avatar="👤").markdown(user_input)

    # Use Gemini AI to generate a bot response with a coffee expert persona
    if model: 
        try: 
            # Send the persona and user input to the model
            response = model.generate_content(f"{coffee_expert_persona}\nUser: {user_input}") 
            bot_response = response.text

            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response)) 
            st.chat_message("assistant", avatar="🏭").markdown(bot_response) 
        except Exception as e: 
            st.error(f"An error occurred while generating the response: {e}")
