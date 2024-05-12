from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

client = MongoClient(
    "mongodb+srv://raichenstorm:Hoods2517@raichenstorm.ryfph8b.mongodb.net/",
    server_api=ServerApi('1')
)

db = client["cats_db"]
collection = db["cats_list"]

def create_cat(cat_data: str):
        collection.insert_one(cat_data)
        return ("Cat's info inserted")



def get_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)

def get_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        return None

def update_cat_age(name, new_age):
    if name in collection:
        collection.update_one({"name": name}, {"$set": {"age": new_age}})

def add_feature_to_cat(name, feature):
    if name in collection:
        collection.update_one({"name": name}, {"$push": {"features": feature}})



def delete_cat_by_name(name):
    if name in collection:
        collection.delete_one({"name": name})

def delete_all_cats():
    collection.delete_many({})


if __name__ == "__main__":
    cat_data = {
        "name": "barsik",
        "age": 3,
        "features": ["ходить в капці", "дає себе гладити", "рудий"]
    }
    create_cat(cat_data)