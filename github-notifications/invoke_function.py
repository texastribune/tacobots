import requests
import json_payloads

# http  unauthenticated  endpoint to call
url = "http://localhost:8080"

# post your response
r = requests.post(url, json=json_payloads.test_branch)
r = requests.post(url, json=json_payloads.test_PR)

# print results
print(r.content)