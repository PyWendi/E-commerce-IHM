FROM python:3.11.8-slim-bullseye

# Variable environment settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Setting working directory
WORKDIR /app

# Create a virtual environment
RUN python -m venv /opt/venv

# Setting path to venv activate script
ENV PATH="/opt/venv/bin:$PATH"

# Regrouping dependances
COPY requirements.txt /app/

# Setting privileges to execute file
RUN chmod 777 .

# Installing all dependances
RUN pip install --no-cache-dir -r requirements.txt

# Setting all files into the app directory
COPY . /app/

# Setting database and static files configuration
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Exposing the app to port 8000
EXPOSE 8000

#Final running command
#python -m gunicorn Ecommerce.asgi:application -k uvicorn.workers.UvicornWorker
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "Ecommerce.asgi.application", "-k", "uvicorn.workers.UvicornWorker"]
