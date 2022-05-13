from pymongo import MongoClient
import pymongo

client = MongoClient(host='localhost', port=27017)

#새로운 db생성
db = client['drug_information']

#새 collection 생성
db_drugs = db['drugs']

def insert_data(dict):
    db_drugs.insert_one(dict)

print(db_drugs)
print(client.list_database_names())