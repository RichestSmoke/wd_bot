FROM python:3.9-alpine
USER root
WORKDIR /bot
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt && chmod 755 .
COPY . .
VOLUME /bot/database/base
ENV TZ=Europe/Kiev
CMD ["python3", "-u", "main.py"]