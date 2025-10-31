# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files and buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Streamlit will use this config by default
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the app
CMD ["streamlit", "run", "app.py"]
