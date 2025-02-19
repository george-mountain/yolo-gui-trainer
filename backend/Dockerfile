

FROM ultralytics/ultralytics:8.1.1


ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
