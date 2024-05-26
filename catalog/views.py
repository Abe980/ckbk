from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from .forms import RecipeForm
from .models import Recipe
from random import sample
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'catalog/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


# def login_view(request):
#     user = authenticate(username=username, password=password)
#     login(request, user)
#     return redirect('/')


def index(request):
    context = {
        'title': '5 случайных рецептов',
        'rec': sample(list(Recipe.objects.all()), 5)
    }
    return render(request, 'catalog/index.html', context=context)


@login_required
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        message = 'Data ERROR'
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            steps = form.cleaned_data['steps']
            cooking_time = form.cleaned_data['cooking_time']
            img = form.cleaned_data['img']
            author = request.user
            recipe = Recipe(name=name, description=description, steps=steps, cooking_time=cooking_time, img=img, author=author)
            recipe.save()
            message = 'Recipe ADD'
    else:
        form = RecipeForm()
        message = 'Create Recipe'
    return render(request, 'catalog/recipe_add.html', {'form': form, 'message': message})


@login_required
def recipe_edit(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.author != request.user:
        raise Http404
    if request.method == 'POST':
        print(request.FILES.get('img'))
        recipe.name = request.POST.get('name')
        recipe.description = request.POST.get('description')
        recipe.steps = request.POST.get('steps')
        recipe.cooking_time = request.POST.get('cooking_time')
        if request.FILES.get('img'):
            recipe.img = request.FILES.get('img')
        recipe.save()
        return HttpResponseRedirect(f'/recipe_edit/{recipe.id}')
    else:
        form = RecipeForm(initial={
            'name': recipe.name,
            'description': recipe.description,
            'steps': recipe.steps,
            'cooking_time': recipe.cooking_time,
            'img': recipe.img,
            })
        return render(request, 'catalog/recipe_edit.html', {'form': form})
    

def recipe_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'catalog/recipe_view.html', {'recipe': recipe})