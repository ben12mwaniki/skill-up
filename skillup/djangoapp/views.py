from django.shortcuts import render
from django.http import HttpResponse
import pymongo

# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello and welcome to <u>Skill UP</u> project!</h1>")

client = pymongo.MongoClient('mongodb+srv://hurrivan:pCowJ3o9lke1fRIO@cluster0.fq0iqud.mongodb.net/')

#Define Db Name
dbname = client['skillupdb']

#Define Collection
collection = dbname['resources']

resource_1={
    "name": "python_intro",
    "type" : "video",
    "link" : "https://www.youtube.com/watch?v=rfscVS0vtbw"
}

collection.insert_one(resource_1)

resources_details = collection.find({})

for r in resources_details:
    print(r['name'])