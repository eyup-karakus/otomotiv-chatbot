# 🚗 Otomotiv Süreçleri Chatbot Geliştirme Projesi

Bu proje, otomotiv sektöründe yaygın olarak kullanılan PPAP, APQP, Homologasyon gibi süreçlerle ilgili sık sorulan sorulara yapay zekâ destekli yanıtlar verebilen bir chatbot sisteminin geliştirilmesini kapsamaktadır. Projede intent (niyet) türlerine dayalı bir veri seti kullanılmış, iki farklı LLM (Large Language Model) modeline dayalı RAG (Retrieval-Augmented Generation) yapısı uygulanmış ve arayüz olarak Streamlit tercih edilmiştir.

---

## 👥 Hedef Kitle

* Otomotiv üretim ve kalite kontrol ekipleri
* Tedarikçi geliştirme uzmanları
* Homologasyon süreçleriyle ilgilenen AR-GE çalışanları
* Otomotiv için dijitalleşme projeleri yürüten danışman ekipler

---

## 👩‍💻 Proje Sahibi

* **Adı Soyadı:** Eyüp Ensari Karakuş
* **Okul:** Marmara Üniversitesi
* **Bölüm:** Bilgisayar Mühendisliği
* **Ders:** Üretken Yapay Zekâ Chatbot Geliştirme Temelleri
* **Dönem:** Bahar 2025

---

## 📂 Proje Yapısı

```bash
.
├── data/
│   └── otomotiv_chatbot_dataset.xlsx   # Intent verileri
├── models/
│   └── capybarahermes-2.5-mistral-7b.Q4_K_M.gguf  # LLaMA modeli
├── app/
│   └── streamlit_app.py                # Chatbot arayüzü
├── requirements.txt                    # Gerekli kütüpaneler
└── README.md                           # Tanıtım dosyası
```

---

## 🤔 Intent ve Veri Seti Yapısı

* Dataset: `otomotiv_chatbot_dataset.xlsx`
* Format: `.xlsx`, iki sütun: `intent`, `user_message`
* Satır sayısı: 1000+

### Örnek Satır:

| Intent      | user\_message                            |
| ----------- | ---------------------------------------- |
| selamlama   | Merhaba, bana yardımcı olabilir misiniz? |
| ppap\_sorgu | PPAP hangi seviyelerde yapılır?          |

---

## 🧠 LLM Model Seçimi ve Entegrasyonu

### 🔹 Gemini 1.5 Flash (Google)

* **Neden Seçildi?**

  * Hızlı yanıt verme
  * Güvenilir API altyapısı
  * Uzun kontekste başarılı doğrulama

* **Entegrasyon:**

  * `langchain_google_genai.ChatGoogleGenerativeAI` kullanıldı.
  * API key `.env` dosyasından yüklenerek bağlandı.

### 💡 LLaMA (lokal - GGUF format)

* **Neden Seçildi?**

  * Tamamen yerel çalışabilir
  * Özelleştirilebilir çıktılar

* **Entegrasyon:**

  * `llama-cpp-python` kütüphanesi ile entegre edildi
  * Model `.gguf` formatında `models/` klasörüne yerleştirildi

---

## 🔍 Embed + FAISS + RAG Yapısı

* Embed modeli: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
* FAISS: `faiss.IndexFlatL2`
* Veri embed edildikten sonra FAISS index'e eklendi
* Kullanıcı sorusu embed edilerek en yakın cümle ile eşleştirildi
* LLM, bu eşleşmeden üretilen prompt ile yanıt verdi

---

## 📝 Prompt ve Yanıt Üretimi

```text
Sen otomotiv sektöründe çalışanlara bilgi veren teknik bir asistansın.
Kullanıcı sana şunu sordu:
"{kullanıcı sorusu}"

Aşağıda sistemde buna en yakın eşleşen veri var:
"{closest_q}"

Bu kaynağa dayanarak açık ve doğru bir cevap üret.
```

* Gemini: `ChatGoogleGenerativeAI` ile prompt üzerinden yanıt verir
* LLaMA: `llama(prompt)` ile doğrudan çıktı verir

---

## 📱 Uygulama Arayüzü (Streamlit)

* Sidebar'dan model seçimi
* Intent, benzerlik skoru, eşleşen soru gösterimi
* Sohbet geçmişi destekli ekran
* Kullanıcı dostu, sade arayüz

> Ekran görüntüsü örnekleri README'nin altına eklenebilir

---

## 📊 Performans Karşılaştırması

Intent sınıflandırma için Logistic Regression modelinde aşağıdaki skorlar elde edilmiştir:

| Model               | Precision | Recall | F1 Score | Accuracy |
| ------------------- | --------- | ------ | -------- | -------- |
| Logistic Regression | 0.96      | 0.97   | 0.965    | 0.97     |

> Not: LLM modelleri subjektif çıktılara dayandığından metrikler ayrıca test edilmiştir.

---

## ⚙️ Kurulum ve Çalıştırma

```bash
# Ortamı kur
python -m venv venv
venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# FAISS index inşa et (gerekiyorsa)
python app/build_faiss_index.py

# Chatbot arayüzünü başlat
streamlit run app/streamlit_app.py
```

> ⚠️ `models/`, `data/` ve `.env` dosyası proje dizininde yer almalıdır.

---
