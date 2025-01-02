import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Embedding Model
embedding_model = SentenceTransformer('intfloat/multilingual-e5-small')

# Load LLM Model
tokenizer = AutoTokenizer.from_pretrained("OpenThaiGPT-1.5")
llm_model = AutoModelForCausalLM.from_pretrained(
    "OpenThaiGPT-1.5", 
    device_map="auto", 
    torch_dtype=torch.float16
)

# Function: Load Preprocessed Data
def load_data(data_path):
    df = pd.read_csv(data_path)
    df['embedding'] = df['embedding'].apply(eval)  # Convert stored string to list
    return df

# Function: Similarity Search
def search_similarity(query, df, top_k=5):
    query_embedding = embedding_model.encode(query, convert_to_tensor=False)
    chunk_embeddings = np.vstack(df['embedding'].values)
    similarities = np.dot(chunk_embeddings, query_embedding) / (
        np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    df['similarity'] = similarities
    return df.sort_values(by='similarity', ascending=False).head(top_k)

# Function: Generate Response
def generate_response(context, query):
    prompt = f"บริบท: {context}\n\nคำถาม: {query}\n\nตอบ:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(llm_model.device)
    outputs = llm_model.generate(inputs.input_ids, max_length=512, temperature=0.7, do_sample=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function: Generate Legal Steps
def generate_legal_steps(food_type, production_capacity, machine_power):
    prompt = f"""
    คุณคือผู้เชี่ยวชาญด้านกฎหมายโรงงานอาหารในประเทศไทย
    **ประเภทอาหาร**: {food_type}
    **กำลังการผลิต**: {production_capacity} ตัน/วัน
    **ขนาดแรงม้า**: {machine_power} HP
    กรุณาสรุปขั้นตอนการขออนุญาตและคำแนะนำที่จำเป็นในรูปแบบที่กระชับและเข้าใจง่าย:
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(llm_model.device)
    outputs = llm_model.generate(inputs.input_ids, max_length=512, temperature=0.7, do_sample=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
