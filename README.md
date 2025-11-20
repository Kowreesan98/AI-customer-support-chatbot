# 🤖 AI Customer Support Chatbot

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3.8+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-005571?style=for-the-badge)

**An intelligent customer support chatbot powered by AI, built with FastAPI and LangChain**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Deployment](#-deployment)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

This AI-powered customer support chatbot leverages advanced language models and vector search to provide intelligent, context-aware responses to customer queries. Upload your knowledge base documents (PDFs), and the chatbot will use RAG (Retrieval-Augmented Generation) to answer questions based on your content.

### Key Capabilities

- 📄 **PDF Document Processing**: Upload and process PDF documents to build your knowledge base
- 🔍 **Semantic Search**: Uses FAISS vector store for efficient similarity search
- 💬 **Intelligent Responses**: Powered by OpenAI GPT models with context-aware answers
- 📊 **Chat Logging**: Tracks all conversations in SQLite database
- 🚀 **RESTful API**: Clean FastAPI endpoints for easy integration
- 🔄 **Multi-Provider Support**: Supports OpenAI and Ollama LLM providers

## ✨ Features

- ✅ **RAG (Retrieval-Augmented Generation)** - Answers questions using uploaded documents
- ✅ **PDF Document Upload** - Process and index PDF files automatically
- ✅ **Vector Similarity Search** - Fast and accurate document retrieval using FAISS
- ✅ **Chat History** - Persistent conversation logging
- ✅ **Health Monitoring** - Built-in health check endpoints
- ✅ **CORS Support** - Ready for frontend integration
- ✅ **Environment-based Configuration** - Easy setup with `.env` file
- ✅ **Production Ready** - Includes deployment configuration for Render

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI |
| **LLM Framework** | LangChain |
| **LLM Provider** | OpenAI (GPT-4o-mini) |
| **Vector Store** | FAISS |
| **Database** | SQLite |
| **PDF Processing** | PyPDF |
| **Server** | Uvicorn |

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (or Ollama for local LLM)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Kowreesan98/AI-customer-support-chatbot.git
cd AI-customer-support-chatbot
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# LLM Settings
LLM_PROVIDER=openai
LLM_MODEL_NAME=gpt-4o-mini
EMBEDDING_MODEL_NAME=text-embedding-3-small

# Optional: For local LLM (Ollama)
# LLM_PROVIDER=ollama
# LLM_MODEL_NAME=llama2
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `LLM_PROVIDER` | LLM provider (`openai` or `ollama`) | `openai` |
| `LLM_MODEL_NAME` | Model name to use | `gpt-4o-mini` |
| `EMBEDDING_MODEL_NAME` | Embedding model name | `text-embedding-3-small` |

## 🚀 Usage

### Start the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Quick Start Example

#### 1. Upload a PDF Document

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"
```

#### 2. Ask a Question

```bash
curl -X POST "http://localhost:8000/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is your return policy?"}'
```

#### 3. View Chat Logs

```bash
curl -X GET "http://localhost:8000/logs"
```

## 📚 API Documentation

### Endpoints

#### `POST /upload`
Upload a PDF document to the knowledge base.

**Request:**
- Content-Type: `multipart/form-data`
- Body: PDF file

**Response:**
```json
{
  "status": "processed",
  "chunks_added": 15,
  "filename": "document.pdf"
}
```

#### `POST /`
Chat with the AI assistant.

**Request:**
```json
{
  "question": "What is your return policy?"
}
```

**Response:**
```json
{
  "answer": "Our return policy allows returns within 30 days...",
  "context": [
    {
      "content": "Return Policy: Customers can return items...",
      "source": "document.pdf"
    }
  ]
}
```

#### `GET /logs`
Retrieve chat conversation history.

**Response:**
```json
[
  {
    "id": 1,
    "question": "What is your return policy?",
    "response": "Our return policy allows...",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## 📁 Project Structure

```
AI-customer-support-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Application configuration
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── session.py          # Database session management
│   │   └── crud.py             # Database operations
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py             # Chat endpoint
│   │   ├── upload.py           # PDF upload endpoint
│   │   ├── logs.py             # Chat logs endpoint
│   │   └── health.py           # Health check endpoint
│   │
│   └── services/
│       ├── __init__.py
│       ├── llm.py              # LLM service (LangChain)
│       ├── pdf.py              # PDF text extraction
│       └── vectorstore.py      # FAISS vector store service
│
├── data/                       # Data directory (FAISS index, SQLite DB)
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment configuration
└── README.md                   # This file
```

## 🌐 Deployment

### Deploy to Render

This project includes a `render.yaml` configuration file for easy deployment on Render.

1. **Fork/Clone** this repository
2. **Connect** your GitHub account to Render
3. **Create** a new Web Service from the repository
4. **Set Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `LLM_PROVIDER`: `openai`
   - `LLM_MODEL_NAME`: `gpt-4o-mini`
   - `EMBEDDING_MODEL_NAME`: `text-embedding-3-small`

5. **Deploy** - Render will automatically detect the `render.yaml` file

### Manual Deployment

For other platforms (Heroku, AWS, etc.):

1. Set the required environment variables
2. Run: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [LangChain](https://www.langchain.com/) - LLM application framework
- [OpenAI](https://openai.com/) - Language models and embeddings
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search

---

<div align="center">

**Made with ❤️ by [Kowreesan98](https://github.com/Kowreesan98)**

⭐ Star this repo if you find it helpful!

</div>

