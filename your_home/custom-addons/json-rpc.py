# python3 /Users/emin/Desktop/odoo-deneme/your_home/custom-addons/json-rpc.py
import json
import random
import urllib.request

url = "http://localhost:8069"
username = "admin"
password = "admin"
db = "your_home"


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(a=0, b=1000000000)
    }
    headers = {
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers=headers)
    response = json.loads(urllib.request.urlopen(req).read().decode("UTF-8"))

    if response.get("error"):
        raise Exception(response("error"))
    return response["result"]


def call(url, service, method, *args):
    return json_rpc(url=f"{url}/jsonrpc", method=method, params={"service": service, "method": method, "args": args})


user_id = call(url, "common", "login", db, username, password)
print(user_id)

vals = {
    "name": "json-rpc ile oluşturuldu",
    "sales_id": 1
}

# create
# create_property = call(url, "object", "execute", db, user_id, password, "estate.property", "create", vals)
# print(create_property)

# read
read_property = call(url, "object", "execute", db, user_id, password, "estate.property", "read", [9])
print(read_property)