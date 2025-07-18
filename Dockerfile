# USE THE LATEEST PYTHON 
FROM python:3.11-slim

# SET THE WORKING DIRECTORY
WORKDIR /app

# COPY THE REQUIREMENTS FILES TO THE WORKING DIRECTORY
COPY requirements.txt .

# INSTALL DEPENDENCIES
RUN pip install --no-cache-dir -r requirements.txt

# COPY REST OF CODE
COPY . .

# EXPOSE PORTS FOR BOTH BACKEND AND FRONTEND
EXPOSE 8000 
EXPOSE 8501

# RUN BOTH THE BACKEND AND FRONTEND FILES USING A JOING SHELL COMMAND
CMD ["sh", "-c", "uvicorn backend.fastapi_backend:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_frontend.py --server.port 8501"]