FROM python:3.6.9

RUN mkdir -p /app/cdh_exporter

WORKDIR /app/cdh_exporter

COPY requirements.txt /app/cdh_exporter
RUN pip install --no-cache -r requirements.txt

COPY cdh_exporter.py /app/cdh_exporter

EXPOSE 19090

ENTRYPOINT ["python", "-u", "./cdh_exporter.py"]
