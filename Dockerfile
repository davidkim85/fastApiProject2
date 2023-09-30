FROM python:3.10.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /fastapi_app

WORKDIR /fastapi_app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x /fastapi_app/docker/app.sh
CMD ["sh", "-c","./wait-for-it.sh db:5432"]

