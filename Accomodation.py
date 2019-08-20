import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Realitica"]
if not "Accomodation" in mydb.list_collection_names():
    mycol = mydb.create_collection("Accomodation")
    mycol.create_index("oglas broj", unique=True)
    mycol.create_index("zadnja promjena", unique=False)
else:
    mycol = mydb["Accomodation"]


