from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
import bcrypt
from .models import User, Group
from django.contrib import messages

# Create your views here.
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
    try:
        request.session['logged_in']
        context = {
        "loggedin": User.objects.get(id=id),
        "groups": Group.objects.all()
        }
        return render(request, 'lefestin/home.html', context)
    except KeyError:
        return redirect(reverse('index'))

def addgroup(request):
    return render(request, 'lefestin/create_group.html')

def process_addgroup(request):
    if request.method == "POST":
        results = Group.groupManager.isValidGroup(request.POST, request.FILES)
        if results[0]:
            print request.POST
            return redirect(reverse('home', kwargs={'id':request.session['logged_in']}))
        else:
            errors = results[1]
            for error in errors:
                messages.error(request, error)
                return redirect(reverse('addgrouptemp'))

def deletegroup(request, id):
    this = Group.objects.get(id=id)
    this.delete()
    return redirect(reverse('home', kwargs={'id':request.session['logged_in']}))

def logout(request):
    request.session.clear()
    return redirect (reverse('index'))

from .models import Recipe, Step, Ingredient

# Create your views here.
def create_recipe(request):
    return render(request, 'lefestin/create_recipe.html')

def create_recipe_process(request):
    recipe = Recipe.objects.create(name=request.POST['recipeName'], user_id=request.session['logged_in'])
    for i in range(0,100):
        if 'igdName{}'.format(i) in request.POST:
            Ingredient.objects.create(name=request.POST['igdName{}'.format(i)], quantity=request.POST['quantity{}'.format(i)], recipe_id=recipe.id)
        else:
            break
    for j in range(1,100):
        if 'stepPic{}'.format(j) in request.POST:
            Step.objects.create(step_number=request.POST['step_number{}'.format(i)], direction=request.POST['step{}'.format(j)], recipe_id=recipe.id)
        else:
            break
    ingredients = Ingredient.objects.filter(recipe_id=recipe.id)
    steps = Step.objects.filter(recipe_id=recipe.id)
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'steps': steps
    }
    return render(request, 'lefestin/show_recipe.html', context)

def delete_recipe(request):
    recipes = Recipe.objects.all()
    recipes.delete()
    return redirect('create_recipe')
