FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask flask_sqlalchemy flask_cors flask_marshmallow
CMD ["python", "app.py"]