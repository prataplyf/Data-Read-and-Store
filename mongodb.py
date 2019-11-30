import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Employee"]
mycol = mydb["data"]
name = "Ashish"

for x in mycol.find({"Name":name},{"Name":1, "Email":1, "Contact Number":1, "_id":0}):
  name = x['Name']
  email = x['Email']
  print(name, email)
