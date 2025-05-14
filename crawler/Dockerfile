FROM python:3.10-slim

WORKDIR /app

RUN pip install uv

COPY . .
# COPY ./data/**/* ./data

RUN uv venv
RUN uv sync

RUN apt-get update -y
RUN apt install curl -y
RUN chmod +x run_all.sh

ENTRYPOINT ["./run_all.sh"]
