# DisasterWatch — Disaster Reporting & Verification Platform

A real-time disaster reporting and verification platform built as a set of independent microservices. Users can submit disaster reports with images and location data, get them automatically classified and verified using a CNN model, and chat with a multi-agent AI assistant that gives location-aware safety guidance using live weather and report data.

## Features

- User registration and authentication using JWT
- Google OAuth 2.0 login integration
- Role-Based Access Control (RBAC) for secured API access
- Upload disaster reports with images and location details
- AI-based disaster image classification using a CNN model
- Fake/screenshot report detection to improve report authenticity
- Real-time disaster feed updates using WebSockets (Socket.IO)
- Multi-agent AI chatbot (Gemini + RAG) with ChromaDB, combining live weather data and report history to give location-aware precautions and safety guidance
- User reactions and feedback on reports
- Report validation through community feedback
- Image storage using AWS S3
- Redis caching for faster feed loading
- MySQL database for persistent user and report data
- Automated integration testing with pytest, run in isolated Docker containers
- CI/CD pipeline with GitHub Actions

## Tech Stack

### Backend
- Python
- FastAPI
- REST APIs
- WebSockets
- JWT Authentication
- OAuth 2.0 / RBAC

### Frontend
- React
- TypeScript
- Socket.IO Client

### Database
- MySQL
- Redis (Caching)
- ChromaDB (Vector store for RAG)

### Machine Learning / AI
- TensorFlow
- Keras
- CNN Model (disaster classification + fake-report detection)
- OpenCV
- Gemini LLM
- Retrieval-Augmented Generation (RAG) — multi-agent chatbot

### Cloud & DevOps
- AWS EC2
- AWS S3
- Docker
- GitHub Actions (CI/CD)
- pytest (integration testing in isolated Docker environments)

## Architecture

The platform is split into independent, containerized microservices rather than a single monolith:

```
                        React + TypeScript Frontend
                                   |
                          API Gateway / FastAPI
                                   |
   ---------------------------------------------------------------
   |              |                |                  |
Auth Service   Reporting        CNN Inference     Chatbot Service
(JWT/OAuth,     Service         Service           (Gemini + RAG
 RBAC)          (MySQL, S3)     (TensorFlow/      + ChromaDB)
                                 Keras, OpenCV)
   |              |                |                  |
   -------------------------------------------------------
                                   |
                        Redis (cache) + Socket.IO
                           (real-time feed)
```

Each service is containerized with Docker and can be built, tested, and deployed independently through the GitHub Actions CI/CD pipeline, with pytest integration tests running in isolated containers before deployment to AWS EC2.

## Installation

### Clone Repository

```bash
git clone https://github.com/abhijith87x/disaster-detection-and-real-time-monitoring.git

cd disaster-detection-and-real-time-monitoring
```

### Backend Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

## Environment Variables

Create a `.env` file:

```
DATABASE_HOST=mysql
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=disaster_db

SECRET_KEY=your_secret_key

AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket

GEMINI_API_KEY=your_gemini_api_key
CHROMADB_PATH=your_chromadb_path

GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret
```

## Running the Application

Start backend:

```bash
uvicorn main:app --reload
```

Start frontend:

```bash
cd frontend
npm run dev
```

API documentation:

```
http://localhost:8000/docs
```

## Running Tests

```bash
pytest
```

Integration tests run against isolated Docker containers as part of the CI/CD pipeline.

## Docker Setup

Build and run all services:

```bash
docker compose up --build
```

## Screenshots

<img width="1917" height="1028" alt="Screenshot 2026-07-16 154209" src="https://github.com/user-attachments/assets/63c86ed9-6d1e-4620-9327-cee673e8b5a3" />
<img width="1920" height="1080" alt="Screenshot (11)" src="https://github.com/user-attachments/assets/cef3170d-6059-4dbd-a500-d5fefec2dc92" />
<img width="1600" height="900" alt="WhatsApp Image 2026-07-16 at 3 41 01 PM" src="https://github.com/user-attachments/assets/9b468894-691b-401e-bea1-6ed0490ebced" />
<img width="1600" height="900" alt="WhatsApp Image 2026-07-16 at 3 41 01 PM (1)" src="https://github.com/user-attachments/assets/6e130589-16c3-40b6-a667-771070fd1d79" />
<img width="1920" height="1080" alt="Screenshot (10)" src="https://github.com/user-attachments/assets/59378ad4-683b-495b-a4da-00da22be8355" />
<img width="1920" height="1080" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/7d80a0d2-e1ab-476f-b255-513e5593e179" />

## Live Demo

https://disaster-watch.duckdns.org/

## Future Improvements

- Improve AI model accuracy
- Add emergency notification system
- Add live disaster map visualization
- Expand multi-agent chatbot with more data sources
- Add rate limiting and API gateway-level monitoring

## Author

Abhijith B

GitHub: https://github.com/abhijith87x
LinkedIn: https://linkedin.com/in/abhijith87b
