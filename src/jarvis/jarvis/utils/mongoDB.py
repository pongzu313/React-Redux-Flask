# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import logging
from pymongo import MongoClient, DESCENDING


def start_mongoDB_server():
    stopMongoServerCommand = "sudo service mongod start"
    process = subprocess.Popen(stopMongoServerCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    logging.info(output)


def stop_mongoDB_server():
    stopMongoServerCommand = "sudo service mongod stop"
    process = subprocess.Popen(stopMongoServerCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    logging.info(output)


class MongoDB:
    """
    This class encapsulates methods related to MongoDB 
    """

    def __init__(self, host='localhost', port=27017):
        self.client = MongoClient(host, port)
        self.database = self.client['jarvis']

    def get_documents(self, collection, key=None, limit=None):
        collection_obj = self.database[collection]
        try:
            result = collection_obj.find(key).sort('_id', DESCENDING)
            return list(result.limit(limit) if limit else result)
        except Exception as e:
            logging.error(e)

    def insert_many_documents(self, collection, documents):
        collection_obj = self.database[collection]
        try:
            collection_obj.insert_many(documents)
        except Exception as e:
            logging.error(e)

    def drop_collection(self, collection):
        collection_obj = self.database[collection]
        try:
            collection_obj.drop()
        except Exception as e:
            logging.error(e)

    def update_collection(self, collection, documents):
        self.drop_collection(collection)
        self.insert_many_documents(collection, documents)

    def update_document(self, collection, filter_document, new_value, upsert=True):
        collection_obj = self.database[collection]
        try:
            collection_obj.update(filter_document, new_value, upsert)
        except Exception as e:
            logging.error(e)

    def is_collection_empty(self, collection):
        collection_obj = self.database[collection]
        try:
            return collection_obj.count() == 0
        except Exception as e:
            logging.error(e)


# ----------------------------------------------------------------------------------------------------------------------
# Start MongoDB Service
# ----------------------------------------------------------------------------------------------------------------------
start_mongoDB_server()
db = MongoDB()
