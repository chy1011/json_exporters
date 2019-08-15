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
			if i.get("CorruptBlocks") != None:
				metric = Metric("num_of_corrupted_blocks", "Number of Corrupted Blocks", "counter")
				metric.add_sample("num_of_corrupted_blocks", value=i.get("CorruptBlocks"), labels={"name": i.get("name")})
				yield metric

			if i.get("CorruptReplicatedBlocks") != None:
				metric = Metric("num_of_corrupted_replicated_blocks", "Number of Corrupt Replicated Blocks", "counter")
				metric.add_sample("num_of_corrupted_replicated_blocks", value=i.get("CorruptReplicatedBlocks"), labels={"name": i.get("name")})
				yield metric

			if i.get("MissingReplicatedBlocks") != None:
				metric = Metric("num_of_missing_replicated_blocks", "Number of Missing Replicated Blocks", "counter")
				metric.add_sample("num_of_missing_replicated_blocks", value=i.get("MissingReplicatedBlocks"), labels={"name": i.get("name")})
				yield metric

			if i.get("NumLiveDataNodes") != None:
				metric = Metric("num_of_live_data_nodes", "Number of Live Data Nodes", "counter")
				metric.add_sample("num_of_live_data_nodes", value=i.get("NumLiveDataNodes"), labels={"name": i.get("name")})
				yield metric

			if i.get("NumDeadDataNodes") != None:
				metric = Metric("num_of_dead_data_nodes", "Number of Live Data Nodes", "counter")
				metric.add_sample("num_of_dead_data_nodes", value=i.get("NumDeadDataNodes"), labels={"name": i.get("name")})
				yield metric

			if i.get("tag.HAState") != None:
				if i.get("tag.HAState") == "active":
					metric = Metric("tag_ha_state", "Current HA State: active=1, standby=2, others=0", "summary")
					metric.add_sample("tag_ha_state", value=1, labels={"name": i.get("name")})
					yield metric
				elif i.get("tag.HAState") == "standby":
					metric = Metric("tag_ha_state", "Current HA State: active=1, standby=2, others=0", "summary")
					metric.add_sample("tag_ha_state", value=2, labels={"name": i.get("name")})
					yield metric
				else:
					metric = Metric("tag_ha_state", "Current HA State: active=1, standby=2, others=0", "summary")
					metric.add_sample("tag_ha_state", value=0, labels={"name": i.get("name")})
					yield metric

if __name__ == '__main__':
	# Usage: json_exporter.py port endpoint
	start_http_server(int(sys.argv[1]))
	REGISTRY.register(JsonCollector(sys.argv[2]))

	while True: time.sleep(1)