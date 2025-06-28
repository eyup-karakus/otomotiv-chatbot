# 🚗 Otomotiv Süreçleri Chatbot Projesi

Bu proje, otomotiv sektöründeki önemli kalite süreçleri (PPAP, APQP, Homologasyon vb.) hakkında teknik soruları yanıtlayabilen yapay zekâ destekli bir chatbot sisteminin geliştirilmesini kapsamaktadır. Projede intent sınıflandırması ve RAG (Retrieval-Augmented Generation) yapısı bir arada uygulanmıştır. Gemini (Google) ve LLaMA (lokal) olmak üzere iki farklı LLM modeli karşılaştırmalı olarak kullanılmıştır.

---

## 👥 Hedef Kitle

* Otomotiv sektörü çalışanları
* Kalite güvence ve proses mühendisleri
* Homologasyon uzmanları

---

## 👨‍💻 Proje Sahibi

* **Adı Soyadı:** Eyüp Ensari Karakuş
* **Okul:** Marmara Üniversitesi
* **Bölüm:** Bilgisayar Mühendisliği
* **Ders:** Üretken Yapay Zekâ Chatbot Geliştirme Temelleri
* **Dönem:** Bahar 2025

---

## 📦 Proje Yapısı

```bash
.
├── data/
│   └── otomotiv_chatbot_dataset.xlsx   # Intent verileri
├── models/
│   └── capybarahermes-2.5-mistral-7b.Q4_K_M.gguf  # LLaMA modeli
├── app/
│   ├── streamlit_app.py                # Chatbot arayüzü
│   ├── llama_local.py                  # LLaMA için yardımcı fonksiyonlar
│   └── build_faiss_index.py            # Embed + FAISS index oluşturma
├── requirements.txt                    # Gerekli kütüphaneler
└── README.md                           # Tanıtım dosyası
```

---

## 🧠 Chatbot Intent Tasarımı

Kullanıcının mesajı embed edilerek en yakın intent eşleşmesi yapılır. Elde edilen eşleşme, yanıt üretiminde temel alınır.

### Örnek Intent Karar Akışı:

* **Selamlama** → "Merhaba, nasıl yardımcı olabilirim?"
* **Vedalaşma** → "Görüşmek üzere, iyi çalışmalar!"
* **Konu Dışı** → "Bu konuda yardımcı olamıyorum. Lütfen otomotiv süreçlerine dair bir soru sorunuz."
* **Teknik Süreç Sorgusu (RAG)** → Veri setinden embed edilen örnekler ile FAISS eşleştirmesi yapılır.

✔・Intent türleri: `selamlama`, `veda`, `konu_dışı`, `faq_sorgu`, `ppap`, `apqp`, `homologasyon`, vb.

---

## 📂 Veri Seti

### Format

* `otomotiv_chatbot_dataset.xlsx` → 1000+ satır
* İki sütun: `intent`, `user_message`

### Örnek Satır:

| intent    | user\_message                            |
| --------- | ---------------------------------------- |
| selamlama | Merhaba, bana yardımcı olabilir misiniz? |
| ppap      | PPAP dosyası nasıl hazırlanır?           |

✅ Veri, `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` modeliyle embed edilmiştir.

---

## 🤖 LLM Model Seçimi ve Entegrasyonu

### 🔷 Gemini 1.5 Flash (Google)

* **Neden seçildi?**

  * Hızlı yanıt üretimi
  * Geniş bağlamlı sorgularda başarılı
  * Ücretsiz API erişimi

* **Kullanılan araçlar:**

  * `langchain_google_genai.ChatGoogleGenerativeAI`
  * Embedding: `HuggingFaceEmbeddings`

```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
```

* **API entegrasyonu:**

  * [Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key)
  * `.env` dosyasına `GEMINI_API_KEY=xxx` olarak eklenir
  * `load_dotenv()` ile yüklenir

---

### 🦙 LLaMA (Lokal)

* **Neden seçildi?**

  * Lokal çalışabilirlik
  * Ücretsiz kullanım
  * Özelleştirme ve kontrol imkânı

* **Kullanılan araç:** `llama-cpp-python`

```python
from llama_cpp import Llama
llama = Llama(model_path="models/llama/capybarahermes-2.5-mistral-7b.Q4_K_M.gguf")
```

---

## 🧠 LLM ve RAG Yapısı

### Prompt Şablonu

Sistem promptu: "Sen otomotiv süreçleri konusunda uzman bir yardımcı botsun..."
Kullanıcı girdisi ve FAISS ile eşleşen cümle birlikte modele verilir.

### Vektör Store:

* `build_faiss_index.py` ile veri seti embed edilir ve FAISS index oluşturulur
* Kullanıcının girdisi embed edilir
* FAISS ile en yakın soru bulunur ve modele verilir

---

## 📊 Model Performansı Karşılaştırması

### Intent Sınıflandırma (Logistic Regression)

| Model               | Precision | Recall | F1 Score | Accuracy |
| ------------------- | --------- | ------ | -------- | -------- |
| Logistic Regression | 0.94      | 0.95   | 0.945    | 0.95     |

### LLM Yanıt Değerlendirmesi (Subjektif)

| Model  | Hız   | Cevap Kalitesi |
| ------ | ----- | -------------- |
| Gemini | Hızlı | ✅✅✅✅✅          |
| LLaMA  | Orta  | ✅✅✅✅           |

---

## 🖥️ Uygulama Arayüzü

* Streamlit ile geliştirildi
* Model seçimi (Gemini / LLaMA)
* Embed eşleşmesi gösterimi (intent, en yakın soru, benzerlik yüzdesi)
* Yanıt geçmişi yönetimi

---

## ⚙️ Kurulum ve Çalıştırma

```bash
# Ortamı oluştur
conda create -n otomotiv_env python=3.10
conda activate otomotiv_env

# Gerekli paketleri yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
streamlit run app/streamlit_app.py
```

> ⚠️ Not: FAISS bazı sürümlerde uyumsuzluk gösterebileceğinden Python 3.10 önerilmektedir.

---

## 📷 Arayüz Ekran Görüntüleri

![image](https://github.com/user-attachments/assets/36649391-03f5-4631-a8ea-fbf68283abc0)

---

Hazırlayan: **Eyüp Ensari Karakuş**

GitHub repo: `https://github.com/eyup-karakus/otomotiv-chatbot`
