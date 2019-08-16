FROM python:3.6.9-slim

RUN mkdir -p /app/namenode_exporter

WORKDIR /app/namenode_exporter

COPY requirements.txt /app/namenode_exporter
RUN pip install --no-cache -r requirements.txt

COPY namenode_exporter.py /app/namenode_exporter

EXPOSE 19090

ENTRYPOINT ["python", "-u", "./namenode_exporter.py"]
