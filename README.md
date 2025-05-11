
# ChatPDFBot 📄🤖  
[![Docker Pulls](https://img.shields.io/badge/Docker-Ready-blue)](https://hub.docker.com/r/aminulislam/chatpdfbot)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**ChatPDFBot** is an AI-powered chatbot that lets you upload a PDF file and ask questions based on its content.  
It uses **FastAPI**, **Streamlit**, and **Docker** to provide a seamless chat interface.

![alt text]([screenshot\ChatPDFBot_user_interface.png](./screenshot/ChatPDFBot_user_interface.png)

---

## 🚀 Features  
- Upload any PDF and interact with it using natural language  
- Extracts and understands content from documents  
- Chat interface built with Streamlit  
- FastAPI backend for PDF processing and AI response  
- Easy deployment using Docker  
- Environment-based configuration using `.env` file  

---

## 📁 Project Structure
```
ChatPDFBot/
├── app/
│   ├── backend.py        # FastAPI backend
│   ├── frontend.py       # Streamlit frontend
├── utils/
│   ├── agent.py          # Chat logic with AI
│   ├── pdf_processor.py  # PDF text extraction
├── .env                  # Environment config
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker container config
└── docker-compose.yml    # Multi-service deployment
```

---

## ⚡ Quick Start with Docker

1. **Clone the Repository**
```bash
git clone https://github.com/aminulislam/ChatPDFBot.git
cd ChatPDFBot
cp .env.example .env  # Add your API keys if needed
```

2. **Run the App**
```bash
docker-compose up -d --build
```

3. **Access the Services**  
- **Chat Interface:** [http://localhost:8501](http://localhost:8501)  
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧑‍💻 Local Development (without Docker)

1. **Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
.env\Scriptsctivate    # For Windows
pip install -r requirements.txt
```

2. **Run the App**
```bash
# Start backend
uvicorn app.backend:app --reload

# In another terminal, start frontend
streamlit run app/frontend.py
```

---

## 🔄 How It Works

1. Upload a PDF using the Streamlit UI  
2. The backend extracts and processes the content  
3. Chat with your document through natural language  
4. Get intelligent answers based on the file's content

---

## 📡 API Endpoints

- `POST /process_pdf` – Upload and process a PDF  
- `POST /chat` – Send a chat query  
- `GET /health` – Check if the API is running

Example:
```bash
curl -X POST "http://localhost:8000/process_pdf" \
     -F "file=@document.pdf" \
     -H "accept: application/json"
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.


---

## 📞 Contact  
**👤 Name**: MD. AMINUL ISLAM <br>
**📧 Email**: itsmeaminul@gmail.com <br>
**🔗 GitHub**: https://github.com/itsmeaminul
