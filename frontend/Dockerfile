FROM python
WORKDIR /app

# install requirements before the rest
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-m", "gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]
