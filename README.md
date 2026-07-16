# Disaster Management System

A disaster reporting and management platform that allows users to upload disaster reports with images, location details. The system uses AI-based image classification to identify disaster types and provides a real-time feed with user interactions.

## Features

- User registration and authentication using JWT
- Google OAuth login integration
- Upload disaster reports with images and location
- AI-based disaster image classification
- Real-time disaster feed updates using WebSockets
- User reactions and feedback on reports
- Report validation through user feedback
- Image storage using AWS S3
- Redis caching for faster feed loading
- MySQL database for storing user and report data

## Tech Stack

### Backend
- Python
- FastAPI
- REST APIs
- WebSockets
- JWT Authentication

### Database
- MySQL
- Redis (Caching)

### Machine Learning
- TensorFlow
- Keras
- CNN Model
- OpenCV

### Cloud & Deployment
- AWS EC2
- AWS S3
- Docker
- GitHub Actions (CI/CD)

### Frontend
- HTML
- CSS
- JavaScript

## Project Architecture

```
Frontend
    |
    |
FastAPI Backend
    |
 -------------------
 |        |         |
MySQL   Redis    ML Model
                 |
              CNN Model
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/disaster-management-system.git

cd disaster-management-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:
```bash
venv\Scripts\activate
```

Linux:
```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
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
```

## Running the Application

Start backend:

```bash
uvicorn main1:app --reload
```

API documentation:

```
http://localhost:8000/docs
```

## Docker Setup

Build image:

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



## Future Improvements

- Improve AI model accuracy
- Add emergency notification system
- Add live disaster map visualization
- Deploy frontend separately

## Author

Abhijith B

GitHub: https://github.com/abhijith87x
