# Dockerfile
FROM python:3.10-slim

# Define o diretório de trabalho no contêiner
RUN mkdir /app
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt /app/

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia toda a estrutura do projeto para o contêiner
COPY . /app

# Define a porta exposta para o Flask
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["python", "src/app.py"]
