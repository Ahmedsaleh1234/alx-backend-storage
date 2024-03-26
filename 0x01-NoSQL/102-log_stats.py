#!/usr/bin/env python3
"""
Log stats - new version
"""
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient()
    mongo_collection = client.logs.nginx
    logs = mongo_collection.count_documents({})
    print(f"{logs} logs")
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        method_count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
    path = mongo_collection.count_documents(
        {'method': 'GET', 'path': '/status'})
    print(f"{path} status check")
    print("IPs:")
    top_ips = mongo_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for ip in top_ips:
        print(f"\t{ip.get('ip')}: {ip.get('count')}")
