
# AI Code Assistant

An AI-powered intelligent code analysis and chat system that integrates code analysis capabilities with smart conversation features.

## 🚀 Project Features

### Frontend Features
- 💻 **Code Analysis Mode** - Real-time code complexity, quality, and optimization suggestions analysis
- 💬 **Smart Chat Mode** - Intelligent Q&A based on knowledge base
- 🎨 **Modern UI Design** - Responsive layout supporting multiple screen sizes
- ⚡ **Real-time Response** - Fast response to user input and interactions

### Backend Features
- 🤖 **GPT-powered Intelligent Conversation** - Natural language processing based on OpenAI GPT model
- 📚 **RAG Technology** - Retrieval-Augmented Generation for more accurate responses
- 💾 **Vector Database Storage** - Efficient knowledge retrieval using ChromaDB
- 🔄 **Conversation History Memory** - Support for multi-turn conversation context management

## 🛠️ Technology Stack

### Frontend Technologies
- **React 18** - Modern frontend framework
- **TypeScript** - Type-safe JavaScript superset
- **Vite** - Fast build tool
- **Modern CSS3** - Responsive design and animations

### Backend Technologies
- **FastAPI** - High-performance Python web framework
- **LangChain** - AI application development framework
- **OpenAI GPT** - Advanced natural language processing model
- **ChromaDB** - Vector database for semantic search

## 📋 System Requirements

- **Node.js** >= 16.0.0
- **Python** >= 3.8
- **OpenAI API Key** - Required for AI functionality

## 🚀 Quick Start

### 1. Clone the Project
```bash
git clone [project-url]
cd RAG_model-dev
```

### 2. Environment Setup

#### Backend Environment Setup
```bash
# Navigate to backend directory
cd python-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

#### Frontend Environment Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 3. Start Services

#### Method 1: Using Startup Scripts (Recommended)

**Linux/macOS Users:**
```bash
# Start backend service
./start-backend.sh

# Start frontend service (new terminal)
./start-frontend.sh
```

**Windows Users:**
```cmd
# Start backend service
start-backend.bat

# Start frontend service (new terminal)
start-frontend.bat
```

#### Method 2: Manual Startup
```bash
# Start backend
cd python-backend
python main.py

# Start frontend (new terminal)
cd frontend
npm run dev
```

### 4. Access the Application
- **Frontend Interface**: http://localhost:5173
- **Backend API**: http://localhost:3000

## 📖 User Guide

### Code Analysis Mode
1. Check the **"Code Analysis Mode"** checkbox
2. Paste the code you want to analyze in the input box
3. Click send button or press Enter
4. The system will return a detailed code analysis report including:
   - **Code Complexity Evaluation** - Time and space complexity analysis
   - **Completion Assessment** - Functionality completeness and error handling
   - **Code Quality Checks** - Readability, naming conventions, and comments
   - **Optimization Suggestions** - Performance, structure, and security improvements

### Normal Chat Mode
1. Uncheck the **"Code Analysis Mode"** checkbox
2. Input your question or chat message
3. The system will provide intelligent responses based on the built-in knowledge base

## 🔧 API Documentation

### POST /chat
Send a chat message or code analysis request

**Request Format**:
```json
{
  "message": "string",
  "isCodeMode": boolean
}
```

**Response Format**:
```json
{
  "response": "string"
}
```

### GET /health
Health check endpoint

**Response**:
```json
{
  "status": "OK"
}
```

## 📁 Project Structure

```
RAG_model-dev/
├── frontend/                 # Frontend project
│   ├── src/
│   │   ├── components/      # React components
│   │   │   └── Chat.tsx    # Chat component
│   │   ├── App.tsx         # Main application component
│   │   ├── main.tsx        # Application entry point
│   │   └── index.css       # Global styles
│   ├── package.json        # Frontend dependency configuration
│   └── vite.config.ts      # Vite configuration
├── python-backend/          # Backend project
│   ├── main.py             # Main server file
│   ├── requirements.txt    # Python dependencies
│   ├── chroma_db/         # Vector database storage
│   └── .env               # Environment variable configuration
├── start-backend.sh        # Backend startup script (Linux/macOS)
├── start-frontend.sh       # Frontend startup script (Linux/macOS)
├── start-backend.bat       # Backend startup script (Windows)
├── start-frontend.bat      # Frontend startup script (Windows)
└── readme.md              # Project documentation
```

## 🛠️ Development Guidelines

### Frontend Development
- Use TypeScript for type safety
- Adopt component-based development for maintainability
- Responsive design for multi-device support
- Modern UI/UX design principles

### Backend Development
- Use FastAPI for high-performance APIs
- Integrate LangChain for AI capabilities
- Use ChromaDB for vector storage
- Support conversation context management

## 🚀 Startup Script Features

### Intelligent Environment Checking
Startup scripts automatically check:
- Python/Node.js version requirements
- Virtual environment status
- Dependency package installation
- Port availability
- Environment variable configuration

### Automated Installation
- Automatically create Python virtual environment
- Automatically install required dependencies
- Automatically create configuration file templates

### Cross-Platform Support
- **Linux/macOS**: Use `.sh` scripts
- **Windows**: Use `.bat` scripts

### Advanced Features
```bash
# Check environment only (without starting service)
./start-frontend.sh --check-only

# Show help information
./start-frontend.sh --help
```

## 🔧 Troubleshooting

### Common Issues

1. **Backend Startup Failure**
   - Check if Python version >= 3.8
   - Confirm virtual environment is activated
   - Verify OpenAI API key configuration

2. **Frontend Startup Failure**
   - Check if Node.js version >= 16
   - Confirm dependencies are installed
   - Check if port 5173 is occupied

3. **API Call Failures**
   - Confirm backend service is running
   - Check CORS configuration
   - Verify API key validity

## 📝 Changelog

### v1.0.0
- Initial version release
- Support for code analysis and intelligent conversation
- RAG technology integration
- Modern UI design

## 👥 Maintainers

- **Name**: Zane Wang
- **Email**: 5finoilheater@gmail.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ If this project helps you, please give us a star!

