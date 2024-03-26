#!/usr/bin/env python3
""" Log stats"""

from pymongo import MongoClient

client = MongoClient()
mongo_collection = client.logs.nginx
logs = mongo_collection.count_documents({})
get = mongo_collection.count_documents({"method": "GET"})
post = mongo_collection.count_documents({"method": "POST"})
put = mongo_collection.count_documents({"method": "PUT"})
patch = mongo_collection.count_documents({"method": "PATCH"})
delete = mongo_collection.count_documents({"method": "DELETE"})
path = mongo_collection.count_documents({"method": "GET", "path": "/status"})
print(f"{logs} logs")
print("Methods:")
print(f"\tmethod GET: {get}")
print(f"\tmethod PUT: {post}")
print(f"\tmethod PATCH: {patch}")
print(f"\tmethod DELETE: {delete}")
print(f"{path} status check")