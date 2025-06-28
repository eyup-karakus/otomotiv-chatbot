import streamlit as st
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from llama_cpp import Llama

# .env'den API anahtarını al
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Gemini modeli tanımla
llm_gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key)

# LLaMA modelini başlat (lokalde)
llama_model = Llama(
    model_path="models/llama/capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4,
    verbose=False
)

def ask_llama(prompt: str) -> str:
    response = llama_model(prompt, max_tokens=512, stop=["</s>"])
    return response["choices"][0]["text"].strip()

# FAISS + model yükleme
@st.cache_resource
def load_model_and_data():
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    index = faiss.read_index("data/faq_index.faiss")
    mapping = pd.read_csv("data/faq_mapping.csv")
    return model, index, mapping

model, index, mapping = load_model_and_data()

# Geçmişi saklamak için session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.markdown("# 🚗 Otomotiv Asistanı")
    st.markdown("### ⚙️ Ayarlar")
    model_choice = st.selectbox("Modelinizi Seçiniz:", ["Gemini", "LLaMA (local)"])
    if st.button("🧹 Geçmişi Temizle"):
        st.session_state.chat_history = []

# Ana Başlık
st.title("🚗 Otomotiv Süreçleri Chatbot")
st.markdown("PPAP, APQP, Homologasyon ve benzeri otomotiv süreçleri hakkında sorularınızı sorun.")

# Kullanıcı girişi
user_input = st.text_input("✏️ Soru sorun", placeholder="Otomotiv süreçleri hakkında her şey :)")
if st.button("Gönder ➤") and user_input:
    # Embed ve FAISS arama
    embedded = model.encode([user_input])
    D, I = index.search(np.array(embedded), k=1)
    matched_row = mapping.iloc[I[0][0]]
    closest_q = matched_row["user_message"]
    intent = matched_row["intent"]
    similarity_score = 100 - round(D[0][0], 2)  # Küçük mesafe = yüksek benzerlik

    # Ortak prompt
    prompt_text = f"""
    Sen otomotiv sektöründe çalışanlara bilgi veren teknik bir asistansın.
    Kullanıcı sana şunu sordu:
    "{user_input}"

    Aşağıda sistemde buna en yakın eşleşen veri var:
    "{closest_q}"

    Bu kaynağa dayanarak açık ve doğru bir cevap üret.
    """

    # Yanıt üretimi
    if model_choice == "Gemini":
        prompt = ChatPromptTemplate.from_template(prompt_text)
        final_prompt = prompt.format_messages()
        response = llm_gemini.invoke(final_prompt)
        answer = response.content
    else:
        answer = ask_llama(prompt_text)

    # Geçmişe ekle
    st.session_state.chat_history.append({
        "soru": user_input,
        "cevap": answer,
        "intent": intent,
        "eslesen_soru": closest_q,
        "benzerlik": similarity_score
    })

# Sohbet geçmişi
for idx, chat in enumerate(reversed(st.session_state.chat_history)):
    with st.expander(f"🗨️ {chat['soru']}", expanded=False):
        st.markdown(f"**🔍 Eşleşen Soru:** {chat['eslesen_soru']}")
        st.markdown(f"**🎯 Intent:** {chat['intent']}")
        st.markdown(f"**📊 Benzerlik Skoru:** %{chat['benzerlik']}")
        st.markdown(f"**🤖 Yanıt:** {chat['cevap']}")