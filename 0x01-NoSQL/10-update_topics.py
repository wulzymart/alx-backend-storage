#!/usr/bin/env python3
"""update a collection"""


def update_topics(mongo_collection, name, topics):
    """set new  topic for a document in collection"""
    return mongo_collection.update_many({"name": name},
                                        {"$set": {"topics": topics}})
