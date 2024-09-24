# Use uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários para o container
COPY Servidor.py .
COPY cidades.txt .

# Instala as dependências necessárias
RUN pip install networkx

# Expõe a porta usada pelo servidor
EXPOSE 777

# Comando para rodar o servidor
CMD ["python", "Servidor.py"]
