import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Backend Data
def load_faiss_index():
    # โหลด FAISS Index และ Metadata
    index = faiss.read_index("vector_database.index")
    metadata = np.load("metadata.npy", allow_pickle=True).item()  # Metadata เช่นประเภทอาหาร, กำลังการผลิต
    return index, metadata

# Feature 1: ระบบแสดงคำแนะนำ
def get_guidelines(food_type, production_capacity, machine_power):
    # ค้นหาข้อมูลคำแนะนำที่เหมาะสมใน Metadata
    guidelines = []
    for item in metadata["guidelines"]:
        if (food_type in item["food_type"]) and \
           (production_capacity <= item["max_capacity"]) and \
           (machine_power <= item["max_machine_power"]):
            guidelines.append(item["description"])
    return guidelines

# Feature 2: ระบบ Q&A
def search_query(query, model, index, metadata, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=False)
    _, indices = index.search(np.array([query_embedding], dtype="float32"), top_k)
    results = [metadata["documents"][i] for i in indices[0]]
    return results

def generate_response(context, query, model_name="OpenThaiGPT-1.5"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)
    prompt = f"บริบท: {context}\n\nคำถาม: {query}\n\nตอบ:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(model.device)
    outputs = model.generate(inputs.input_ids, max_length=512, temperature=0.7, do_sample=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Load Preprocessed Backend Data
index, metadata = load_faiss_index()
model = SentenceTransformer("intfloat/multilingual-e5-small")
