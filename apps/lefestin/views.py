from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
import bcrypt
from .models import User, Group, Recipe, Step, Ingredient
from django.contrib import messages
from .forms import UploadFileForm, UploadGroupImg
import json


def index(request):
    try:
        request.session['logged_in']
        return redirect(reverse('home', kwargs={'id':request.session['logged_in']}))
    except KeyError:
        return render(request, 'lefestin/index.html')

def login(request):
    if request.method == "POST":
        results = User.userManager.ValidLogin(request.POST)
        if results[0]:
            passFlag = True
            if 'logged_in' not in request.session:
                email = request.POST['email']
                request.session['logged_in'] = User.objects.get(email=email).id
                request.session['fname'] = User.objects.get(email=email).first_name
                return redirect(reverse('home', kwargs={'id':request.session['logged_in']}))
        else:
            passFlag = False
            errors = results[1]
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))

# this part routes the user to a registration page
def register(request):
    try:
        request.session['logged_in']
        return redirect(reverse('home', kwargs={'id':request.session['logged_in']}))
    except KeyError:
        return render(request, 'lefestin/register.html')

# this part processes the submitted registration
def registration(request):
    if request.method == "POST":
        results = User.userManager.isValidRegistration(request.POST)
        if results[0]:
            return redirect(reverse('index'))
        else:
            errors = results[1]
            for error in errors:
                messages.error(request, error)
                return redirect(reverse('register'))
    else:
        return redirect(reverse('register'))

def home(request, id):
    if request.method == 'POST':
        formGroup = UploadGroupImg(request.POST, request.FILES)
    else:
        formGroup = UploadGroupImg()
    try:
        request.session['logged_in']
    except KeyError:
        return redirect(reverse('index'))
    userRecipes = Recipe.objects.filter(user_id=request.session['logged_in'])
    userGroups = Group.objects.filter(creator_id=request.session['logged_in'])
    context = {
        "loggedin": User.objects.get(id=id),
        'formGroup': formGroup,
        'userRecipes': userRecipes,
        'userGroups': userGroups
    }
    return render(request, 'lefestin/home.html', context)

def addgroup(request):
    return render(request, 'lefestin/create_group.html')

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def getAllGroups(request):
    stringResult = ""
    # keys = ["group_name", "description", "creator", "photo", "grouped_users_id", "created_at", "updated_at"]
    for group in Group.objects.all():
        stringResult += "{} | {} \n".format(group.group_name, group.creator_id) 
    return HttpResponse(stringResult);

def process_addgroup(request):
    if request.method == "POST":
        results = Group.groupManager.isValidGroup(request.POST, request.FILES, request.session['logged_in'])
        if results[0]:
            latestGroup = Group.objects.get(group_name=request.POST['group_name'])
            earlyGroups = Group.objects.filter(creator_id=request.session['logged_in']).exclude(group_name=request.POST['group_name']).order_by('created_at')
            otherGroups = Group.objects.exclude(creator_id=request.session['logged_in'])
            context = {
                'latestGroup': latestGroup,
                'earlyGroups': earlyGroups,
                'otherGroups': otherGroups,
            }
            return render(request, 'lefestin/show_group.html', context)
        else:
            errors = results[1]
            for error in errors:
                messages.error(request, error)
                return redirect('home', request.session['logged_in'])
def showgroups(request):
    earlyGroups = Group.objects.filter(creator_id=request.session['logged_in'])
    otherGroups = Group.objects.exclude(creator_id=request.session['logged_in'])
    context = {
        'earlyGroups': earlyGroups,
        'otherGroups': otherGroups,
    }
    return render(request, 'lefestin/show_group.html', context)
def showgroup(request):
    this = Group.objects.get(id=request.POST['hiddenGroupId'])
    context = {
        'this': this
    }
    return render(request, 'lefestin/show_group_ind.html', context)
def searchGroup(request):
    pattern = request.POST['search_group']
    result = Group.objects.filter(group_name__contains=pattern)
    context = {
        'result': result,
        'count': len(result)
    }
    return render(request, 'lefestin/search.html', context)
def deletegroup(request, id):
    this = Group.objects.get(id=id)
    this.delete()
    return redirect(reverse('home', kwargs={'id':request.session['logged_in']}))

def logout(request):
    request.session.clear()
    return redirect (reverse('index'))

def create_recipe(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
    else:
        form = UploadFileForm()
    context = {
        'form': form
    }
    return render(request, 'lefestin/create_recipe.html', context)

def create_recipe_process(request):
    recipe = Recipe.objects.create(name=request.POST['recipeName'], user_id=request.session['logged_in'], product_pic=request.FILES['image'])
    for i in range(0,100):
        if 'igdName{}'.format(i) in request.POST:
            Ingredient.objects.create(name=request.POST['igdName{}'.format(i)], quantity=request.POST['quantity{}'.format(i)], recipe_id=recipe.id)
        else:
            break
    for j in range(1,100):
        if 'step_number{}'.format(j) in request.POST:
            Step.objects.create(step_number=request.POST['step_number{}'.format(i)], direction=request.POST['step{}'.format(j)], recipe_id=recipe.id)
        else:
            break
    return redirect('show_recipe', recipe.id)
def show_recipe(request, recipe_id):
    context = {
        'recipe': Recipe.objects.get(id=recipe_id),
        'ingredients': Ingredient.objects.filter(recipe_id=recipe_id),
        'steps': Step.objects.filter(recipe_id=recipe_id),
    }
    return render(request, 'lefestin/show_recipe.html', context)
def showrecipes(request):
    idList = []
    recipes = Recipe.objects.filter(user_id=request.session['logged_in'])
    for recipe in recipes:
        idList.append(recipe.id)
    ingredients = Ingredient.objects.filter(recipe_id__in=idList)
    steps = Step.objects.filter(recipe_id__in=idList)
    context = {
        'recipes': Recipe.objects.filter(user_id=request.session['logged_in']),
        'ingredients':ingredients,
        'steps':steps
    }
    return render (request, 'lefestin/show_recipes.html', context)
def deleterecipe(request, id):
    this = Recipe.objects.get(id=id)
    this.delete()
    return redirect(reverse('home', kwargs={'id':request.session['logged_in']}))

def delete_recipe(request):
    recipes = Recipe.objects.all()
    recipes.delete()
    return redirect('create_recipe')

def delete_all_group(request):
    Group.objects.all().delete()
    return HttpResponse('deleted')