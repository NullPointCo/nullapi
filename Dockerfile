# NullAPI - Free Developer APIs
# Ready for Render/Fly.io free tier deployment

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]
