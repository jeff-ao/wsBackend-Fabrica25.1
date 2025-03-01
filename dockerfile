FROM python:3.12-slim  

WORKDIR /starWarsTranslate


RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*


COPY . /starWarsTranslate/
COPY ./requirements.txt /starWarsTranslate/requirements.txt


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]