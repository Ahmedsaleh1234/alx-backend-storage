#!/usr/bin/env python3
"""main"""
from pymongo import MongoClient
import pprint
list_all = __import__("8-all").list_all
insert_school = __import__('9-insert_school').insert_school

clint = MongoClient()
school_collection = clint.my_db.school
insert_document_id = insert_school(school_collection, name="UCSF", address="505 Parnassus Ave")
print("New school created: {}".format(insert_document_id))
schools = list_all(school_collection)
for school in schools:
    pprint.pprint(school)
