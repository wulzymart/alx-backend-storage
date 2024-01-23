#!/usr/bin/env python3
""" provides some stats about Nginx logs stored in MongoDB"""


import pymongo
from pymongo import MongoClient


def nginx_log_printer(mongo_collection):
    """provides some stats about Nginx logs"""
    print(f"{mongo_collection.estimated_document_count()} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    gets_count = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{gets_count} status check")


def nginx_top_ips_prnter(mongo_collection):
    '''prints to ips in requests'''
    print('IPs:')
    requests = mongo_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for log in requests:
        ip = log['_id']
        count = log['totalRequests']
        print('\t{}: {}'.format(ip, count))


if __name__ == "__main__":
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    nginx_log_printer(mongo_collection)
    nginx_top_ips_prnter(mongo_collection)
