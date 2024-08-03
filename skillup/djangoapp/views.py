from bson.objectid import ObjectId
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from djangoapp.models import Profile
from django.shortcuts import redirect
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
            "raters": 0,
            "ratings":{},
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

        resources = list(resources)    
        if len(resources) == 0:
            messages.info(request, 'No resources matching criteria!')
            return redirect(request.META['HTTP_REFERER'])  
          
        return render(request, 'results.html', {'resources':resources, 'range': range(1,6)})

    if request.method == 'GET':
        return redirect('/')


"""
    Get a single resource by id
    Allow users to save resource
    Allow users to rate resource
    Allow users to comment on resource
    Allow users to remove resource from saved
    Allow author to delete resource
"""
def get_resource(request, id):
    if request.method == 'GET':
        dbname = client['skillupdb']
        collection = dbname['resources']
        try:
            resource = collection.find_one({'_id': ObjectId(id)})
            return render(request, 'resource.html', {'resource': resource, 'range': range(1,6)})  
        except Exception as e:
            print(e)
            return HttpResponse("<h1>Resource not found! Try again later</h1>")
    
    if request.method == 'POST':
        data = json.loads(request.body)

        if data['action'] == 'save':
            if request.user.is_authenticated:
                dbname = client['skillupdb']
                collection = dbname['resources']
                resource = collection.find_one({'_id': ObjectId(id)})
                
                # Forbid author from saving own resource
                if request.user.username == resource['author']:
                    return HttpResponse('Forbidden', status=403)
                
                profile = request.user.profile
                if id not in profile.saved_resources:
                    profile.saved_resources.append(id)
                    profile.save()
                return HttpResponse('Success')
            else:
                return HttpResponse('Unauthorized', status=401)
            
        
        if data['action'] == 'rate':
            if request.user.is_authenticated:
                dbname = client['skillupdb']
                collection = dbname['resources']

                if data['rating'] == '':
                    messages.error(request, 'Stars cannot be empty!')
                    return HttpResponse('Stars cannot be empty!', status=400)

                rating = int(data['rating'])
                resource = collection.find_one({'_id': ObjectId(id)})

                # Forbid author from rating own resource
                if request.user.username == resource['author']:
                    return HttpResponse('Forbidden', status=403)

                if request.user.username in resource['ratings']:
                    old_rating = resource['ratings'][request.user.username]
                    resource['ratings'][request.user.username] = rating
                    resource['stars_total'] = resource['stars_total'] - old_rating + rating
                else:
                    resource['ratings'][request.user.username] = rating
                    resource['stars_total'] = resource['stars_total'] + rating
                    resource['raters'] = resource['raters'] + 1
                
                resource['star_rating'] = resource['stars_total'] / resource['raters']
                collection.update_one({'_id': ObjectId(id)}, {'$set': {'ratings': resource['ratings'], 'stars_total': resource['stars_total'], 'star_rating': resource['star_rating'], 'raters': resource['raters']}})

                return HttpResponse('Success')
            else:
                return HttpResponse('Unauthorized', status=401)
        
            
        if data['action'] == 'comment':
            if request.user.is_authenticated:
                dbname = client['skillupdb']
                collection = dbname['resources']
                
                if data['comment_text'] == '':
                    messages.error(request, 'Comment cannot be empty!')
                    return HttpResponse('Comment cannot be empty!', status=400)
                
                comment_text = data['comment_text']
                comment = { 'author': request.user.username, 'date': datetime.now(), 'text': comment_text}
                resource = collection.find_one({'_id': ObjectId(id)})
                resource['comments'].append(comment)

                try:
                    collection.update_one({'_id': ObjectId(id)}, {'$set': {'comments': resource['comments']}})
                    return HttpResponse('Success')
                except Exception as e:
                    print(e)
                    return HttpResponse('Error saving comment!', status=500)    
                
            else:
                return HttpResponse('Unauthorized', status=401)
            
    if request.method == 'DELETE':
        data = json.loads(request.body)

        if data['action'] == 'delete':
            if request.user.is_authenticated:
                dbname = client['skillupdb']
                collection = dbname['resources']
                resource = collection.find_one({'_id': ObjectId(id)})

                if request.user.username == resource['author']:
                    collection.delete_one({'_id': ObjectId(id)})

                    # Remove resource from profile
                    profile = request.user.profile 
                    profile.created_resources.remove(id)
                    profile.save()

                    # Remove resource from saved resources of all users
                    users = User.objects.all()
                    
                    for user in users:
                        if id in user.profile.saved_resources:
                            user.profile.saved_resources.remove(id)
                            user.profile.save()

                    return HttpResponse('Success')
                else:
                    return HttpResponse('Forbidden', status=403)
            else:
                return HttpResponse('Unauthorized', status=401)
                   
        if data['action'] == 'remove_from_profile':
            if request.user.is_authenticated:
                profile = request.user.profile
                if id in profile.saved_resources:
                    profile.saved_resources.remove(id)
                    profile.save()
                return HttpResponse('Success')
            else:
                return HttpResponse('Unauthorized', status=401)
    
    
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















