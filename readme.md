
# AI Code Assistant

An AI-based intelligent code analysis and chat system, integrating code analysis and smart conversation features.

## Features

### Frontend Features
- 💻 **Code Analysis Mode**
  - Toggle between code analysis and normal chat modes
  - Real-time responsive UI
  - Beautiful message bubble design
  - Responsive layout for various screen sizes
  
### Backend Features
- 🤖 **GPT-based intelligent conversation**
- 📚 **RAG (Retrieval-Augmented Generation) technology**
- 💾 **Vector database storage**
- 🔄 **Conversation history support**

## Technology Stack

### Frontend
- React 18
- TypeScript
- Vite
- Modern CSS3

### Backend
- FastAPI
- LangChain
- OpenAI GPT
- ChromaDB

## Quick Start

### Prerequisites
- Node.js >= 16
- Python >= 3.8
- OpenAI API key

### Installation Steps

1. **Clone the project**:
   ```bash
   cd [project directory]
   ```

2. **Backend setup**:
   ```bash
   cd python-backend
   python -m venv venv
   .\venv\Scripts\python.exe -m pip install -r requirements.txt
   echo "OPENAI_API_KEY=your_openai_key" > .env
   ```

3. **Frontend setup**:
   ```bash
   cd frontend
   npm install
   ```

### Start Services

1. **Start backend**:
   ```bash
   ./start-backend.sh
   ```

2. **Start frontend**:
   ```bash
   ./start-frontend.sh
   ```

## User Guide

### Code Analysis Mode
1. Check the **"Code Analysis Mode"** checkbox.
2. Paste the code you want to analyze in the input box.
3. Click **send** or press **Enter**.
4. The system will return a detailed code analysis, including:
   - Code complexity evaluation
   - Completion assessment
   - Code quality checks
   - Optimization suggestions

### Normal Chat Mode
1. Uncheck the **"Code Analysis Mode"** checkbox.
2. Input your question or chat message.
3. The system will respond based on the built-in knowledge base.

## API Documentation

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

## Project Structure

```
frontend/                # Frontend project
├── src/
│   ├── components/     # React components
│   ├── App.tsx        
│   ├── main.tsx       
│   └── index.css      
├── package.json       
└── vite.config.ts     

python-backend/         # Backend project
├── main.py            # Main server file
├── requirements.txt   # Python dependencies
└── .env              # Environment variable configuration
```

## Development Guidelines

### Frontend Development
- Use TypeScript for type safety.
- Component-based development for maintainability.
- Responsive design for multi-device support.
- Modern UI/UX design.

### Backend Development
- FastAPI for high-performance APIs.
- LangChain integration for AI capabilities.
- ChromaDB for vector storage.
- Supports conversation context management.


## Maintainers
name: Zane Wang 
email:5finoilheater@gmail.com

