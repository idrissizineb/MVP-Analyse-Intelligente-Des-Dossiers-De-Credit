# ==========================================
# Stage 1: Build Dependencies
# ==========================================
FROM python:3.10-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# THE MAGIC TRICK:
# 1. Pre-install CPU PaddlePaddle
# 2. Append the PyTorch CPU index URL so `torch` installs without CUDA bloat
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/packages/stable/cpu/ && \
    pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# ==========================================
# Stage 2: Final Runtime Image
# ==========================================
FROM python:3.10-slim AS runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    PADDLE_HOME="/app/.paddleocr"

WORKDIR /app

# We MUST include libgl1 and libglib2.0-0 because your original file uses 
# standard opencv-python (which requires these Linux GUI libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libquadmath0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

RUN mkdir -p /app/data/input \
             /app/data/processed \
             /app/data/output \
             /app/data/database \
             /app/.paddleocr

COPY ./app ./app

# Expose both API (8000) and Streamlit (8501) ports
EXPOSE 8000
EXPOSE 8501

CMD ["streamlit", "run", "app/ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]