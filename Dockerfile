# -----------------------------
# 1. Builder Stage
# -----------------------------
    FROM ghcr.io/astral-sh/uv:python3.14-bookworm AS builder

    WORKDIR /app
    
    # Copy project metadata
    COPY pyproject.toml uv.lock ./
    
    # Install dependencies into .venv (prod only)
    RUN uv sync --frozen --no-dev
    
    # Copy project source last (better layer caching)
    COPY . .
    
    # -----------------------------
    # 2. Runtime Stage
    # -----------------------------
    FROM python:3.14-slim-bookworm AS runtime
    
    # No .pyc files + unbuffered logs
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        PATH="/opt/venv/bin:${PATH}"
    
    # Create non-root user
    RUN groupadd --system appuser && \
        useradd --system --gid appuser appuser
    
    WORKDIR /app
    
    # Copy venv
    COPY --from=builder /app/.venv /opt/venv
    
    # Copy actual application source
    COPY . .
    
    RUN chown -R appuser:appuser /app
    
    USER appuser
    
    EXPOSE 8000
    
    # Use uv run instead of python (2025 best practice)
    CMD ["uv", "run", "--no-sync", "app/main.py"]
    