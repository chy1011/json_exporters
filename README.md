# json_exporters
Prometheus Exporters for NameNode and Yarn

# Build the docker image
Run "docker build -t cdh_exporter ."

# Spin up the container
Run "docker run -d -p HOST_PORT:19090 -e NAMENODE_URL="NAMENODE_JSON_URL" -e YARN_URL="YARN_JSON_URL" --name cdh_exporter cdh_exporter:latest"
