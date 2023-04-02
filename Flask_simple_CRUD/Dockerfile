FROM python:latest
WORKDIR /server
COPY requirements.txt /server
RUN pip install -r requirements.txt
COPY . /server
EXPOSE 5000
CMD python /server/main.py
