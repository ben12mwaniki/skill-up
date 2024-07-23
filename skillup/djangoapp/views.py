from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import os

# Connect to MongoDB
client = pymongo.MongoClient(os.environ.get("MONGO_URI"))

# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello and welcome to <u>Skill UP</u> project!</h1>")

def create_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password') 
        dbname = client['skillupdb']
        collection = dbname['users']
        user = {
            "user_name": user_name,
            "email": email,
            "password": password
        }
        collection.insert_one(user)
        return HttpResponse("<h1>User created successfully!</h1>")
    if request.method == 'GET':
        return render(request, 'create_user.html')

def create_resource(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        type = request.POST.get('type')
        link = request.POST.get('link')
        subjects = request.POST.getlist('subjects')
        description = request.POST.get('description')

        print(' '.join(subjects))
        

        dbname = client['skillupdb']
        collection = dbname['resources']
        resource = {
            "title": title,
            "subjects": ', '.join(subjects),
            "type": type,
            "link": link,
            "description": description,
            "stars": 0, 
            "rating": 0
        }
        collection.insert_one(resource)
        return HttpResponse("<h1>Resource created successfully!</h1>")
    if request.method == 'GET':
        return render(request, 'create_resource.html')
    
    
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        dbname = client['skillupdb']
        collection = dbname['users']
        user = collection.find_one({'email': email, 'password': password})
        if user:
            return render(request, 'search.html')
        else:
            return HttpResponse("<h1>Login failed!</h1>")
    if request.method == 'GET':
        return render(request, 'login.html')
    

def get_users(request):
    dbname = client['skillupdb']
    collection = dbname['users']
    users = collection.find()
    
    for user in users:
        print(user)     
    return HttpResponse("<h1>Users fetched successfully!</h1>")

def search(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text')
        type = request.POST.get('type')
        dbname = client['skillupdb']
        collection = dbname['resources']
        
        if type == '':
            resources = collection.find({'$text': {'$search': search_text}})
        elif search_text == '':
            resources = collection.find({'type': type})
        else:
            resources = collection.find({'$text': {'$search': search_text}, 'type': type})
        
        return render(request, 'results.html', {'resources': resources})

    if request.method == 'GET':
        return render(request, 'search.html')
    
def get_resources(request):
    dbname = client['skillupdb']
    collection = dbname['resources']
    resources = collection.find({'type': "video"})
    
    for resource in resources:
        print(resource)     
    return HttpResponse("<h1>Resources fetched successfully!</h1>")


#Text index for search based on description and subjects
def create_text_index():
    dbname = client['skillupdb']
    collection = dbname['resources']
    collection.create_index([('description', 'text'), ('subjects', 'text'), ('title', 'text')]) 

create_text_index()












