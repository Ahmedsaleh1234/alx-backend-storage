#!/usr/bin/env python3
"""main"""

import pprint
from pymongo import MongoClient
list_all = __import__('8-all').list_all
if __name__ == '__main__':
    clint = MongoClient()
    school_collection = clint.my_db.school
    schools = list_all(school_collection)
    for school in schools:
        pprint.pprint(school)
