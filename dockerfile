FROM python:3.13.2

WORKDIR /starWarsTranslate

COPY . /starWarsTranslate/
COPY ./requirements.txt /starWarsTranslate/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0:8000"]

