# Use uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo do cliente para o container
COPY Cliente.py .

# Comando para rodar o cliente
CMD ["python", "Cliente.py"]
