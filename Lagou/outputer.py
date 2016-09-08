# -*- coding: utf-8 -*-
import csv
from pymongo import MongoClient

class CsvOutPuter(object):
    def outputtocsv(self, data, filename):
        fobj = file(filename, "a")
        writer = csv.writer(fobj)
        writer.writerow(data)
        fobj.close()



class MongodbPipe(object):
    def __init__(self, db_name, collection_name, host='localhost', port='27017'):
        try:
            self.URI = 'mongodb://{host}:{port}'.format(host=host, port=port)
        except Exception, e:
            print e
        # self.URI = 'mongodb://{username}:{password}@{host}:{port}'
        self.db = db_name
        self.col = collection_name

    def insert_data(self, data):
        # data is in json format
        try:
            client = MongoClient(self.URI)
            db_name = self.db
            collection_name = self.col
            db = client[db_name]
            col = db[collection_name]
            id = col.insert(data)
            # print id
        except Exception, e:
            print e