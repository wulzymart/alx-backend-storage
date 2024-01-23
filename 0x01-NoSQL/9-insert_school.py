#!/usr/bin/env python3
"""Inserts into a collection"""


def insert_school(mongo_collection, **kwargs):
    """insertes a new document"""
    return mongo_collection.insert_one(kwargs)
