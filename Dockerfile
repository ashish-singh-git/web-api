FROM python:3.6.1-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV HOST=0.0.0.0
ENV PORT=5000

EXPOSE 5000
CMD ["python","./src/app.py"]