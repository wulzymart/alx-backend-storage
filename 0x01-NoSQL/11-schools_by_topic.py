#!/usr/bin/env python3
"""finds a list of documents with specific topic"""


def schools_by_topic(mongo_collection, topic):
    """returns list of documents with topic"""
    return mongo_collection.find({"topics": topic})
