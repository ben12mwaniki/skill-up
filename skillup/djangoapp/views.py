from django.shortcuts import render
from django.http import HttpResponse
import pymongo

client = pymongo.MongoClient('mongodb+srv://hurrivan:pCowJ3o9lke1fRIO@cluster0.fq0iqud.mongodb.net/')


# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello and welcome to <u>Skill UP</u> project!</h1>")

def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        dbname = client['skillupdb']
        collection = dbname['users']
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        collection.insert_one(user)
        return HttpResponse("<h1>User created successfully!</h1>")

def create_resource(request):
    if request.method == 'POST':
        type = request.POST['type']
        link = request.POST['link']
        subject = request.POST['subject']

        dbname = client['skillupdb']
        collection = dbname['resources']
        resource = {
            "subject": subject,
            "type": type,
            "link": link
        }
        collection.insert_one(resource)
        return HttpResponse("<h1>Resource created successfully!</h1>")
    


def get_users(request):
    dbname = client['skillupdb']
    collection = dbname['users']
    users = collection.find()
    
    for user in users:
        print(user)     
    return HttpResponse("<h1>Users fetched successfully!</h1>")

def get_resources(request):
    dbname = client['skillupdb']
    collection = dbname['resources']
    resources = collection.find({'type': "video"})
    
    for resource in resources:
        print(resource)     
    return HttpResponse("<h1>Resources fetched successfully!</h1>")


get_resources(None) 











