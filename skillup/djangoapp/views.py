from django.shortcuts import render
from django.http import HttpResponse
import pymongo

client = pymongo.MongoClient('mongodb+srv://hurrivan:pCowJ3o9lke1fRIO@cluster0.fq0iqud.mongodb.net/')


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

        type = request.POST.get('type')
        link = request.POST.get('link')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        

        dbname = client['skillupdb']
        collection = dbname['resources']
        resource = {
            "subject": subject,
            "type": type,
            "link": link,
            "description": description,
            stars: 0, 
            ratings: 0
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
            return HttpResponse("<h1>Login successful!</h1>")
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
        subject = request.POST.get('search')
        type = request.POST.get('type')
        dbname = client['skillupdb']
        collection = dbname['resources']
        resources = collection.find({'type': type, '$text': {'$search': subject}})
        if resources:
            return render(request, 'results.html', {'resources': resources})
        else:
            return render(request, 'results.html', {'resources': None})
    if request.method == 'GET':
        return render(request, 'search.html')
    
def get_resources(request):
    dbname = client['skillupdb']
    collection = dbname['resources']
    resources = collection.find({'type': "video"})
    
    for resource in resources:
        print(resource)     
    return HttpResponse("<h1>Resources fetched successfully!</h1>")


#Text index for search based on description and subject
def create_text_index():
    dbname = client['skillupdb']
    collection = dbname['resources']
    collection.create_index([('description', 'text'), ('subject', 'text')])

create_text_index()












