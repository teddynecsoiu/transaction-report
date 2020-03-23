FROM python:3.6.9

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 5000

RUN pytest

RUN python db_init.py

CMD python app.py
