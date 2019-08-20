import pymongo

myclient = pymongo.MongoClient("mongodb+srv://andrea9888:andrea9888@cluster0-t8pwd.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["Realitica"]
if not "Accomodation" in mydb.list_collection_names():
    mycol = mydb.create_collection("Accomodation")
    mycol.create_index("oglas broj", unique=True)
    mycol.create_index("zadnja promjena", unique=False)
else:
    mycol = mydb["Accomodation"]


