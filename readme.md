# 📦 vector_database_microservice

A lightweight, file-based Python microservice for storing and searching text embeddings using FAISS. Designed for fast nearest neighbor search via a simple API—perfect for hackathon-scale semantic search and prototype deployments.

---

## 🚀 Features

- 🔍 Nearest neighbor search over text embeddings
- 🧠 Uses `all-MiniLM` for embedding generation
- 🗃️ File-based vector storage (no external DB required)
- 🧵 Batch and streaming support
- 🛠️ Built with Python + FAISS
- 📡 Simple Python API (no auth, no multi-tenancy)

---

## 🧰 Tech Stack

| Component        | Details                          |
|------------------|----------------------------------|
| Embedding Model  | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Index     | FAISS (flat index)               |
| Storage          | Local file-based                 |
| API Framework    | FastAPI or Flask (assumed)       |
| Search Type      | Approximate Nearest Neighbor     |

---

## 📦 Installation

using docker
```bash
git clone https://github.com/NagiEight/vector_database_microservice.git
docker-compose up
```

---

## 🔌 API Usage

### ➕ Add Vectors

`POST http://localhost:8000/vectors/add`

```json
{
  "texts": [
    "The sky is a beautiful blue today.",
    "The latest iPhone has a stunning new camera.",
    "Classical music is a timeless art form.",
    "The financial markets are showing signs of recovery.",
    "Python is a versatile programming language."
  ],
  "metadata": [
    { "source": "weather", "topic": "colors" },
    { "source": "tech review", "topic": "smartphones" },
    { "source": "art history", "topic": "music" },
    { "source": "business news", "topic": "economics" },
    { "source": "programming blog", "topic": "software" }
  ]
}
```

### 🔍 Search Vectors

`POST http://localhost:8000/vectors/search`

```json
{
  "query": "What's the weather like?",
  "k": 3
}
```

> 🧠 The query is embedded using the same model and matched against stored vectors using FAISS.

---

## ✅ Recommended Usage

- Use the API endpoints for all interactions—this ensures consistent embedding and indexing.
- Batch your `add` requests for better performance.
- For streaming use cases, consider wrapping the API with a queue or event-driven trigger.

---

## 📌 Notes

- No authentication or access control is implemented—use in trusted environments only.
- Not optimized for large-scale datasets yet (no sharding, GPU, or distributed indexing).
- Ideal for prototyping, demos, and small-scale semantic search.

---

## 🧪 Future Improvements

- Add support for persistent metadata indexing
- Benchmark performance on larger datasets
- Add optional authentication and multi-tenant support
- Explore GPU acceleration and HNSW indexing

---

Want me to help you write inline docstrings or modularize the backend next?
