from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time

class JsonCollector(object):
	def __init__(self, endpoint):
		self._endpoint = endpoint
	def collect(self):
		# Fetch the JSON
		response = json.loads(requests.get(self._endpoint).content.decode('UTF-8'))
		data = response["beans"]

		for i in data:
			if i.get("RegisterNodeManagerNumOps") != None:
				metric = Metric("num_ops_node_manager", "Number of Registered Node Manager Ops ", "counter")
				metric.add_sample("num_ops_node_manager", value=i.get("RegisterNodeManagerNumOps"), labels={"name": i.get("name")})
				yield metric

			if i.get("LiveNodeManagers") != None:
				string=i.get("LiveNodeManagers")
				substring = "RUNNING"

				count = string.count(substring)
				metric = Metric("num_live_node_managers", "Number of Live Node Managers Running", "counter")
				metric.add_sample("num_live_node_managers", value=3, labels={"name": i.get("name")})
				yield metric

if __name__ == '__main__':
	# Usage: json_exporter.py port endpoint
	start_http_server(int(sys.argv[1]))
	REGISTRY.register(JsonCollector(sys.argv[2]))

	while True: time.sleep(1)