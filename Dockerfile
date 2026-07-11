FROM python:3.10.1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8000

CMD ["uvicorn", "main1:socket_app", "--host", "0.0.0.0", "--port", "8000"]
# docker build -t disaster-app . , docker build --no-cache -t disaster-app .
#docker build -t disaster-app .
#docker run -d --name disaster-container -p 8000:8000 disaster-app
#docker logs -f disaster-container
#docker rm -f disaster-container
#docker rmi disaster-app
#docker build --no-cache -t disaster-app .
#docker run --name disaster-container -p 8000:8000 disaster-app