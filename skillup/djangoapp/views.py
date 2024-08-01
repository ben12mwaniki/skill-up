from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from bson.objectid import ObjectId
from django.contrib.auth.models import User
from djangoapp.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
import pymongo
import os
import json
from dotenv import load_dotenv
load_dotenv()

# Connect to MongoDB
client = pymongo.MongoClient(os.getenv('MONGO_URI'))



def index(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password') 
        
        try:
            user = User.objects.create_user(user_name, email, password)
            profile = Profile(user=user)
            profile.saved_resources = []
            profile.created_resources = []
            profile.save()
            user.save()
            
            return redirect('/login')
        except IntegrityError as e:
            if "auth_user_username_key" in str(e):
                return render(request, 'create_user.html', {'error': 'Username already exists!'})
            else:
                print(e)
                return render(request, 'create_user.html', {'error': 'An error occured while creating user!'})
        

    if request.method == 'GET':
        return render(request, 'create_user.html')

@login_required
def create_resource(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        type = request.POST.get('type')
        link = request.POST.get('link')
        subjects = request.POST.getlist('subjects')
        description = request.POST.get('description') 

        resource = {
            "title": title,
            "type": type,
            "link": link,
            "author": request.user.username,
            "subjects": ', '.join(subjects),
            "description": description,
            "stars_total": 0, 
            "star_rating": 0,
            "raters":0,
            "comments": []
            
        }

        dbname = client['skillupdb']
        collection = dbname['resources']
       
        try:
            inserted_id = collection.insert_one(resource).inserted_id
            profile = request.user.profile
            profile.created_resources.append(str(inserted_id))
            profile.save()
            return redirect('/profile')   
        except Exception:
            return render(request, 'create_resource.html', {'error': 'Error creating resource!'})

    if request.method == 'GET':
        return render(request, 'create_resource.html')
    
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if request.GET.get('next') != None:
                return redirect(request.GET.get('next'))
            else: 
                return redirect('/profile',)
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    if request.method == 'GET':
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    if request.method == 'GET':
        profile = request.user.profile
        saved_resources = profile.saved_resources
        created_resources = profile.created_resources

        if saved_resources != None:
            for i in range(len(saved_resources)):
                saved_resources[i] = client['skillupdb']['resources'].find_one({'_id': ObjectId(saved_resources[i])})
        if created_resources != None:
            for i in range(len(created_resources)):
                created_resources[i] = client['skillupdb']['resources'].find_one({'_id': ObjectId(created_resources[i])})

        return render(request, 'profile.html', {'saved_resources': saved_resources, 'created_resources': created_resources})
         

    if request.method == 'POST':
        pass

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
          
        return render(request, 'results.html', {'resources':list(resources)})

    if request.method == 'GET':
        return redirect('/')

def get_resource(request, id):
    if request.method == 'GET':
        dbname = client['skillupdb']
        collection = dbname['resources']
        try:
            resource = collection.find_one({'_id': ObjectId(id)})
            return render(request, 'resource.html', {'resource': resource})  
        except Exception as e:
            print(e)
            return HttpResponse("<h1>Resource not found! Try again later</h1>")
    
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['action'] == 'save':
            if request.user.is_authenticated:
                profile = request.user.profile
                if id not in profile.saved_resources:
                    profile.saved_resources.append(id)
                    profile.save()
                return HttpResponse('Success')
            else:
                return HttpResponse('Unauthorized', status=401)
            
        # To be tested
        if data['action'] == 'rate':
            data = json.loads(request.body)
            if request.user.is_authenticated:
                rating = int(request.POST.get('rating'))
                resource = collection.find_one({'_id': ObjectId(id)})
                stars_total = resource['stars_total'] + rating
                raters = resource['raters'] + 1
                star_rating = stars_total / raters
                collection.update_one({'_id': ObjectId(id)}, {'$set': {'stars_total': stars_total, 'star_rating': star_rating, 'raters': raters}})
                return redirect('/resource/'+id)
            else:
                return redirect('/login?next=/resource/'+id)
        
        # To be tested    
        if data['action'] == 'comment':
            data = json.loads(request.body)
            if request.user.is_authenticated:
                comment = request.POST.get('comment')
                resource = collection.find_one({'_id': ObjectId(id)})
                comments = resource['comments']
                comments.append({'author': request.user.username, 'comment': comment})
                collection.update_one({'_id': ObjectId(id)}, {'$set': {'comments': comments}})
                return redirect('/resource/'+id)
            else:
                return redirect('/login?next=/resource/'+id)
    
    
def get_resources(request):
    dbname = client['skillupdb']
    collection = dbname['resources']
    resources = collection.find()
    
    for resource in resources:
        print(resource)     
    return HttpResponse("<h1>Resources fetched successfully!</h1>")

# Text index for search based on description and subjects
def create_text_index():
    dbname = client['skillupdb']
    collection = dbname['resources']
    collection.create_index([('description', 'text'), ('subjects', 'text'), ('title', 'text')]) 
    

create_text_index()















