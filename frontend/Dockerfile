FROM python
WORKDIR /app

# install requirements before the rest
COPY reuirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]
CMD ["app.py"]
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]
