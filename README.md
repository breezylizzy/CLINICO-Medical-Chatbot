<<<<<<< HEAD
# Medical Chatbot RAG System

Sistem chatbot medis berbasis RAG (Retrieval-Augmented Generation) dengan agentic AI menggunakan LangChain, LangGraph, Pinecone, dan HuggingFace.

## 🌟 Fitur

- ✅ **Dual Agentic AI**: 
  - Agent 1: Retrieval agent untuk mengambil dokumen relevan
  - Agent 2: Answer agent untuk menjawab pertanyaan
- ✅ **RAG System**: Retrieval-Augmented Generation dengan Pinecone vector database
- ✅ **HuggingFace Embeddings**: Model embedding gratis dari HuggingFace
- ✅ **Groq LLM**: Model bahasa gratis untuk reasoning
- ✅ **Memory System**: Menyimpan konteks percakapan (5 pesan terakhir)
- ✅ **Reranker**: BM25 reranking untuk hasil pencarian lebih akurat
- ✅ **Streamlit UI**: Antarmuka web yang user-friendly

## 📋 Prerequisites

1. **Pinecone Account**
   - Daftar gratis di [pinecone.io](https://www.pinecone.io/)
   - Dapatkan API key dan environment

2. **Groq Account**
   - Daftar gratis di [console.groq.com](https://console.groq.com/)
   - Dapatkan API key gratis

3. **Python 3.8+**

## 🚀 Instalasi

### 1. Clone atau Download Project

```bash
# Buat folder project
mkdir medical-chatbot-rag
cd medical-chatbot-rag
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Buat file `.env` dan isi dengan credentials Anda:

```env
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=medical-chatbot

GROQ_API_KEY=your_groq_api_key_here
```

**Cara mendapatkan credentials:**

#### Pinecone:
1. Login ke [pinecone.io](https://www.pinecone.io/)
2. Buat project baru
3. Salin API Key dari dashboard
4. Environment biasanya seperti: `us-west1-gcp`, `us-east-1-aws`, dll

#### Groq:
1. Login ke [console.groq.com](https://console.groq.com/)
2. Buat API key baru
3. Salin API key

### 4. Struktur Project

```
medical-chatbot-rag/
├── app.py                                  # Aplikasi Streamlit (Chat Only)
├── process_pdf.py                          # Script untuk process PDF
├── agents.py                               # Implementasi agentic AI
├── utils.py                                # Utility functions
├── requirements.txt                        # Dependencies
├── .env                                    # Environment variables
├── The_GALE_ENCYCLOPEDIA_of_MEDICINE.pdf  # File PDF (letakkan di sini)
└── README.md                              # Dokumentasi
```

## 🎯 Cara Penggunaan

### 1. Siapkan File PDF

Letakkan file `The_GALE_ENCYCLOPEDIA_of_MEDICINE.pdf` di folder yang sama dengan script.

### 2. Process PDF (Hanya Sekali)

```bash
python process_pdf.py
```

Script ini akan:
- Membaca PDF
- Memecah menjadi chunks
- Membuat embeddings
- Menyimpan ke Pinecone

⏱️ Proses ini memakan waktu sekitar **5-15 menit** tergantung ukuran PDF.

### 3. Jalankan Aplikasi Chat

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

### 4. Mulai Bertanya

- Ketik pertanyaan Anda di kolom input
- Klik **"📨 Kirim"**
- Chatbot akan menjawab berdasarkan The GALE Encyclopedia

### 5. Contoh Pertanyaan

```
- Apa itu hipertensi?
- Bagaimana cara mengobati diabetes?
- Apa saja gejala pneumonia?
- Jelaskan tentang penyakit jantung koroner
- Apa itu anemia dan cara mengatasinya?
```

## 🏗️ Arsitektur Sistem

```
User Input → Streamlit UI
    ↓
LangGraph Workflow
    ↓
┌─────────────────────┐
│ Retriever Agent     │
│ - Query improvement │
│ - Vector search     │
│ - BM25 reranking    │
└─────────────────────┘
    ↓
Pinecone Vector DB
    ↓
┌─────────────────────┐
│ Answer Agent        │
│ - Context analysis  │
│ - Memory integration│
│ - Answer generation │
└─────────────────────┘
    ↓
Response → User
```

## 🔧 Komponen Teknis

### 1. Embeddings
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensi**: 384
- **Sumber**: HuggingFace (gratis)

### 2. Vector Database
- **Platform**: Pinecone
- **Metric**: Cosine similarity
- **Index**: Auto-created

### 3. LLM
- **Provider**: Groq
- **Model**: Mixtral-8x7b-32768
- **Gratis**: Ya (dengan rate limit)

### 4. Reranker
- **Algorithm**: BM25 (Okapi)
- **Kombinasi**: 50% vector similarity + 50% BM25 score

### 5. Memory
- **Type**: Conversation buffer
- **Window**: 5 pesan terakhir
- **Storage**: Session state

## 📊 Versi Library

Library menggunakan versi lama yang **stabil dan kompatibel**:

- Streamlit: 1.28.0
- LangChain: 0.0.350
- LangGraph: 0.0.20
- Pinecone: 2.2.4
- Sentence-transformers: 2.2.2

## ⚙️ Customization

### Mengubah Ukuran Chunk

Di `app.py`, fungsi `process_pdf()`:

```python
documents = split_text(text, chunk_size=500, chunk_overlap=50)
```

### Mengubah Jumlah Dokumen Retrieved

Di `agents.py`, class `RetrieverAgent`:

```python
retrieved_docs = retrieve_documents(
    self.index, 
    improved_query, 
    self.embeddings_model, 
    top_k=10  # Ubah angka ini
)
```

### Mengubah Memory Window

Di `agents.py`, inisialisasi `AnswerAgent`:

```python
answer_agent = AnswerAgent(memory_window=5)  # Ubah angka ini
```

### Mengubah Model Embedding

Di `app.py`, fungsi `initialize_system()`:

```python
st.session_state.embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
```

**Model alternatif:**
- `all-mpnet-base-v2` (lebih akurat, lebih lambat)
- `paraphrase-multilingual-MiniLM-L12-v2` (mendukung bahasa Indonesia lebih baik)

### Mengubah Model LLM

Di `agents.py`, class `GroqLLM`:

```python
def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
```

**Model Groq gratis:**
- `mixtral-8x7b-32768` (default, balanced)
- `llama-3.1-70b-versatile` (lebih pintar)
- `gemma-7b-it` (lebih cepat)

## 🐛 Troubleshooting

### Error: "Pinecone index not found"
- Anda belum menjalankan `process_pdf.py`
- Jalankan: `python process_pdf.py` terlebih dahulu

### Error: "File 'The_GALE_ENCYCLOPEDIA_of_MEDICINE.pdf' tidak ditemukan"
- Pastikan file PDF ada di folder yang sama
- Atau edit nama file di `process_pdf.py` line 27

### Error: "Rate limit exceeded" (Groq)
- Groq free tier memiliki rate limit
- Tunggu beberapa menit sebelum mencoba lagi
- Atau upgrade ke Groq Pro

### Error: "Invalid API key"
- Periksa kembali API key di file `.env`
- Pastikan tidak ada spasi tambahan

### Process PDF terlalu lama
- PDF besar membutuhkan waktu lebih lama
- The GALE Encyclopedia sekitar 10-15 menit
- Biarkan proses berjalan sampai selesai

### Jawaban tidak relevan
- Pastikan PDF sudah terproses dengan benar
- Cek di Pinecone dashboard apakah vectors tersimpan
- Tingkatkan `top_k` di `agents.py` line 77
- Perbaiki query dengan lebih spesifik

## 💡 Tips Penggunaan

1. **Upload dokumen berkualitas**: Dokumen yang well-structured akan memberikan hasil lebih baik
2. **Pertanyaan spesifik**: Semakin spesifik pertanyaan, semakin baik jawabannya
3. **Gunakan bahasa Indonesia**: System prompt sudah dioptimasi untuk bahasa Indonesia
4. **Review jawaban**: Selalu verifikasi informasi medis dengan profesional kesehatan

## 🔒 Security & Privacy

- ⚠️ **PENTING**: Jangan upload dokumen yang mengandung data pasien pribadi
- API keys tersimpan lokal di `.env` (jangan commit ke Git)
- Data hanya tersimpan selama session (tidak persistent)
- Pinecone menyimpan embeddings, bukan teks asli lengkap

## 📝 Catatan Penting

1. **Bukan Pengganti Dokter**: Chatbot ini adalah alat bantu informasi, bukan diagnosis medis
2. **Akurasi**: Jawaban bergantung pada kualitas dokumen yang diupload
3. **Rate Limits**: Groq free tier memiliki batasan request per menit
4. **Pinecone Free Tier**: Terbatas pada 1 index dan 100K vectors

## 🤝 Kontribusi

Untuk improvement atau bug report, silakan buat issue atau pull request.

## 📄 License

MIT License - bebas digunakan untuk project pribadi maupun komersial.

## 🙏 Credits

- LangChain & LangGraph: Framework orchestration
- Pinecone: Vector database
- HuggingFace: Embedding models
- Groq: Free LLM inference
- Streamlit: Web framework

---

**Happy Coding! 🚀**

Jika ada pertanyaan, silakan hubungi atau buat issue di repository.
=======
# CLINICO-Medical-Chatbot
>>>>>>> abeaf1e21ebddae7d7b66025d04f37e62f2f6987
