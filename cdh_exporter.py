import prometheus_client
from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
from requests_kerberos import HTTPKerberosAuth
import sys
import time
import os

class JsonCollector(object):
	def __init__(self):
		pass
	def collect(self):
		json_urls = ["https://mgt2.hpe-project.com:9871/jmx", "https://mgt3.hpe-project.com:9871/jmx", "https://mgt2.hpe-project.com:8090/jmx", "https://mgt3.hpe-project.com:8090/jmx"]
		kerberos_auth = HTTPKerberosAuth(delegate=True)
		# Fetch the JSON
		for url in json_urls:
			response = (requests.get(url, auth=(kerberos_auth), verify=False)).json()
			data = response["beans"]
	
			for i in data:
				if i.get("CorruptBlocks") != None:
					metric = Metric("num_of_corrupted_blocks", "Number of Corrupted Blocks", "gauge")
					metric.add_sample("num_of_corrupted_blocks", value=i.get("CorruptBlocks"), labels={"target": url})
					yield metric
	
				if i.get("CorruptReplicatedBlocks") != None:
					metric = Metric("num_of_corrupted_replicated_blocks", "Number of Corrupt Replicated Blocks", "gauge")
					metric.add_sample("num_of_corrupted_replicated_blocks", value=i.get("CorruptReplicatedBlocks"), labels={"target": url})
					yield metric
	
				if i.get("MissingReplicatedBlocks") != None:
					metric = Metric("num_of_missing_replicated_blocks", "Number of Missing Replicated Blocks", "gauge")
					metric.add_sample("num_of_missing_replicated_blocks", value=i.get("MissingReplicatedBlocks"), labels={"target": url})
					yield metric
	
				if i.get("NumLiveDataNodes") != None:
					metric = Metric("num_of_live_data_nodes", "Number of Live Data Nodes", "gauge")
					metric.add_sample("num_of_live_data_nodes", value=i.get("NumLiveDataNodes"), labels={"target": url})
					yield metric
	
				if i.get("NumDeadDataNodes") != None:
					metric = Metric("num_of_dead_data_nodes", "Number of Live Data Nodes", "gauge")
					metric.add_sample("num_of_dead_data_nodes", value=i.get("NumDeadDataNodes"), labels={"target": url})
					yield metric
	
				if i.get("tag.HAState") != None:
					if i.get("tag.HAState") == "active":
						metric = Metric("tag_ha_state", "Current HA State: active=1, standby=2, others=0", "summary")
						metric.add_sample("tag_ha_state", value=1, labels={"target": url})
						yield metric
					elif i.get("tag.HAState") == "standby":
						metric = Metric("tag_ha_state", "Current HA State: active=1, standby=2, others=0", "summary")
						metric.add_sample("tag_ha_state", value=2, labels={"target": url})
						yield metric
					else:
						metric = Metric("tag_ha_state", "Current HA State: active=1, standby=2, others=0", "summary")
						metric.add_sample("tag_ha_state", value=0, labels={"target": url})
						yield metric

				if i.get("RegisterNodeManagerNumOps") != None:
					metric = Metric("num_ops_node_manager", "Number of Registered Node Manager Ops ", "gauge")
					metric.add_sample("num_ops_node_manager", value=i.get("RegisterNodeManagerNumOps"), labels={"target": url})
					yield metric

				if i.get("LiveNodeManagers") != None:
					string=i.get("LiveNodeManagers")
					substring = "RUNNING"

					count = string.count(substring)
					metric = Metric("num_live_node_managers", "Number of Live Node Managers Running", "gauge")
					metric.add_sample("num_live_node_managers", value=count, labels={"target": url})
					yield metric

if __name__ == '__main__':
	# Usage: json_exporter.py port endpoint
	start_http_server(19090)
	REGISTRY.register(JsonCollector())
	
	while True: time.sleep(1)