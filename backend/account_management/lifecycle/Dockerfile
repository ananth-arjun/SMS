FROM python:3.11-slim
WORKDIR /app

# Optional OS tools
RUN apt-get update && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

# ✅ requirements.txt is inside lifecycle/, but build context is ..
COPY lifecycle/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the whole repo into /app (since context is ..)
COPY . /app

# Start (dev)
CMD ["uvicorn", "api.profile:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
