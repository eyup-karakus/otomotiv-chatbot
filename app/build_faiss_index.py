import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# 📄 Üst klasördeki veri dosyasını yükle
df = pd.read_excel("../data/otomotiv_chatbot_dataset.xlsx")

# 🔠 Cümleleri çek
sentences = df['user_message'].tolist()

# 🔍 Embedding modeli
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# 🔢 Embeddingleri üret
embeddings = model.encode(sentences, show_progress_bar=True)

# 🧠 FAISS index oluştur
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# 💾 FAISS index kaydet
faiss.write_index(index, "../data/faq_index.faiss")

# 🗂️ Mapping CSV'si
df[['user_message', 'intent']].to_csv("../data/faq_mapping.csv", index=False)

print("✅ FAISS index ve mapping dosyası oluşturuldu.")
