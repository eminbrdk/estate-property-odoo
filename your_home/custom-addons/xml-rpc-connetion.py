# python3 /Users/emin/Desktop/odoo-deneme/your_home/custom-addons/xml-rpc-connetion.py

import xmlrpc.client

url = "http://localhost:8069"
username = "admin"
password = "admin"
db = "your_home"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
print(common.version())
user_uid = common.authenticate(db, username, password, {})
print(user_uid)

"xmlrpc/2/object" "execute_kw"
"db, uid, password, model_name, method_name, [], {}"

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# search function
property_ids = models.execute_kw(db, user_uid, password, "estate.property", "search", [[]]) # ,{"offset": 0, "limit": 1} ekleyebilirsin
print(property_ids)

# count function
count_property_ids = models.execute_kw(db, user_uid, password, "estate.property", "search_count", [[]])
print(count_property_ids)

# read function
read_property_ids = models.execute_kw(db, user_uid, password, "estate.property", "read", [property_ids], {"fields": ["name"]})
print(read_property_ids)

# search and read function
search_read_property_ids = models.execute_kw(db, user_uid, password, "estate.property", "search_read", [[]], {"fields": ["name"]})
print(search_read_property_ids)

# create function
# create_property_ids = models.execute_kw(db, user_uid, password, "estate.property", "create", [{"name": "Property from RPC", "sales_id": 2}]) # buraya required = true olanları eklemelisin, öükü veri yaratırken zorunlu
# print(create_property_ids)

# write function
write_property_ids = models.execute_kw(db, user_uid, password, "estate.property", "write", [[1], {"name": "Property from RPC updated"}]) # buraya required = true olanları eklemelisin, öükü veri yaratırken zorunlu
print(write_property_ids)

# name get function
# unlink_property_ids = models.execute_kw(db, user_uid, password, "estate.property", "unlink", [[1]]) # buraya required = true olanları eklemelisin, öükü veri yaratırken zorunlu
# print(unlink_property_ids)

