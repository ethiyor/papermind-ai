"# PaperMind AI

**Intelligent PDF Analysis and Summarization Platform**

A web application that processes academic papers and documents using natural language processing. Built with FastAPI and modern web technologies, PaperMind AI enables semantic search and AI-powered summarization using multiple transformer models.

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge)](https://papermind-ai-frontend-production.up.railway.app)

---

## Features

- **Semantic Search** - Find relevant content using AI-powered similarity matching  
- **Multi-Model Summarization** - Choose from 5 different AI models (BART, T5, Pegasus, LED, DistilBART)  
- **PDF Processing** - Extract and analyze text from academic papers and documents  
- **Modern UI** - Clean, responsive interface with dark/light theme support  
- **Fast & Scalable** - Deployed on Railway with 8GB RAM for optimal performance  

---

## Live Application

- **Frontend**: [papermind-ai-frontend-production.up.railway.app](https://papermind-ai-frontend-production.up.railway.app)
- **Backend API**: [papermind-ai-production.up.railway.app](https://papermind-ai-production.up.railway.app)
- **API Documentation**: [papermind-ai-production.up.railway.app/docs](https://papermind-ai-production.up.railway.app/docs)

---

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning framework
- **Transformers** - Hugging Face transformer models
- **Sentence Transformers** - Semantic search capabilities
- **PDFMiner** - PDF text extraction
- **Uvicorn** - ASGI server

### Frontend
- **HTML5** - Modern markup with semantic elements
- **CSS3** - Custom properties, flexbox, grid layouts
- **JavaScript** - ES6+ features, async/await, fetch API
- **FontAwesome** - Icon library
- **Inter Font** - Modern typography

### AI Models
- **BART** - General-purpose summarization
- **DistilBART** - Lightweight, fast summarization
- **T5** - Text-to-text transfer transformer
- **Pegasus** - Optimized for news and academic text
- **LED** - Long document encoder-decoder (16k+ tokens)

### Deployment
- **Railway** - Cloud platform with 8GB RAM
- **GitHub** - Version control and CI/CD
- **Python 3.11.9** - Stable runtime environment

---

## Quick Start

### Using the Live Application

1. Visit the [live application](https://papermind-ai-frontend-production.up.railway.app)
2. Upload your PDF file using drag and drop
3. Use semantic search to find relevant content
4. Choose an AI model and generate summaries

### Local Development

#### Prerequisites
- Python 3.11.9
- pip package manager
- Git

#### Backend Setup
```bash
# Clone repository
git clone https://github.com/ethiyor/papermind-ai.git
cd papermind-ai/papermind/backend

# Install dependencies
pip install -r requirements.txt

# Start development server
python start_production.py
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Serve static files (use any local server)
python -m http.server 8080
# or
npx serve .
```

#### Environment Variables
```bash
ENVIRONMENT=development
TOKENIZERS_PARALLELISM=false
```

---

## API Documentation

### Core Endpoints

#### Upload PDF
```http
POST /upload-pdf/
Content-Type: multipart/form-data
```

#### Semantic Search
```http
POST /search/
Content-Type: application/json

{
  "query": "machine learning algorithms",
  "top_k": 5
}
```

#### Generate Summary
```http
POST /summarize/
Content-Type: application/json

{
  "text": "Long document text...",
  "model": "bart",
  "max_length": 150
}
```

#### Available Models
```http
GET /models/
```

### Response Format
```json
{
  "status": "success",
  "data": {
    "results": [...],
    "summary": "Generated summary text",
    "model_used": "bart"
  },
  "message": "Operation completed successfully"
}
```

---

## Architecture

```
┌─────────────────┐    HTTP/HTTPS    ┌─────────────────┐
│   Frontend      │ ───────────────► │   Backend       │
│   (Railway)     │                  │   (Railway)     │
│                 │ ◄─────────────── │                 │
│ • HTML/CSS/JS   │    JSON API      │ • FastAPI       │
│ • File Upload   │                  │ • AI Models     │
│ • Search UI     │                  │ • PDF Parser    │
│ • Results UI    │                  │ • Vector Search │
└─────────────────┘                  └─────────────────┘
```

### Data Flow
1. **PDF Upload** → Text extraction → Embedding generation
2. **Search Query** → Vector similarity → Ranked results
3. **Summarization** → Model selection → AI-generated summary

---

## Development

### Project Structure
```
papermind-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── pdf_utils.py         # PDF processing
│   │   ├── embed_utils.py       # Semantic search
│   │   └── summarizer_utils.py  # AI models
│   ├── requirements.txt         # Dependencies
│   └── start_production.py      # Server launcher
├── frontend/
│   ├── index.html              # Main application
│   ├── style.css               # Styling
│   └── package.json            # Configuration
├── Procfile                    # Railway deployment
├── requirements.txt            # Root dependencies
└── runtime.txt                 # Python version
```

### Key Features Implementation

#### Semantic Search Engine
```python
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def search(self, query, top_k=5):
        # Vector similarity search implementation
```

#### Multi-Model Summarization
```python
class SummarizationManager:
    def __init__(self):
        self.models = {
            'bart': BartForConditionalGeneration,
            'distilbart': DistilBartForConditionalGeneration,
            't5': T5ForConditionalGeneration,
            'pegasus': PegasusForConditionalGeneration,
            'led': LEDForConditionalGeneration
        }
```

---

## AI Model Comparison

| Model | Size | Speed | Best For | Max Tokens |
|-------|------|-------|----------|------------|
| **DistilBART** | 306MB | Fast | Quick summaries | 1,024 |
| **BART** | 558MB | Fast | General purpose | 1,024 |
| **T5** | 892MB | Medium | Flexible tasks | 512 |
| **Pegasus** | 568MB | Medium | Academic papers | 1,024 |
| **LED** | 1.2GB | Slow | Long documents | 16,384 |

---

## Use Cases

- **Academic Research**: Analyze research papers and extract key findings
- **Document Review**: Quickly understand large document sets
- **Content Creation**: Generate summaries for articles and reports
- **Educational Tools**: Help students understand complex academic texts
- **Business Intelligence**: Extract insights from technical documentation

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Hugging Face** - For providing excellent transformer models
- **FastAPI** - For the amazing Python web framework
- **Railway** - For reliable cloud hosting
- **Sentence Transformers** - For semantic search capabilities

---

## Contact

- **Developer**: Yordanos Kassa
- **Email**: ytk2108@columbia.edu
- **Project Link**: [https://github.com/ethiyor/papermind-ai](https://github.com/ethiyor/papermind-ai)

---

**Star this repository if you found it helpful!**

[![GitHub stars](https://img.shields.io/github/stars/ethiyor/papermind-ai?style=social)](https://github.com/ethiyor/papermind-ai/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ethiyor/papermind-ai?style=social)](https://github.com/ethiyor/papermind-ai/network)" 
