FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install fastapi uvicorn WeasyPrint

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]