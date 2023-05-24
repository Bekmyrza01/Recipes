from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Дополнительные действия после успешной регистрации
            return redirect('index')  # Перенаправляем на вашу домашнюю страницу
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Перенаправляем на вашу домашнюю страницу
        else:
            # Обработка неправильных учетных данных или других ошибок
            return render(request, 'login.html', {'error': 'Неправильные учетные данные'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def first_page(request):

    selected_menu = request.GET.get('menu')
    selected_cuisine = request.GET.get('cuisine')
    selected_bludo = request.GET.get('bludo')
    selected_category = request.GET.get('category')
    categories = Category.objects.all()
    object_list = Dishes.objects.all()
    bludos = Bludo.objects.filter(category__name=selected_category)
    cuisines =Nationality.objects.all()
    menus = Menu.objects.all()
    random_obj = random.choice(object_list)
    request.session['my_object_id'] = random_obj.id
    if request.user.is_authenticated:
        favorite_recipes = FavoriteRecipe.objects.filter(user=request.user).values_list('recipe', flat=True)

        # Добавить флаг is_favorite для каждого рецепта
        for recipe in object_list:
            recipe.is_favorite = recipe.id in favorite_recipes

    return render(request, './index.html', {'object_list': object_list,
                                            'categories': categories,
                                                'bludos': bludos,
                                            'selected_category': selected_category,
                                            'selected_bludo': selected_bludo,
                                            'cuisines': cuisines,
                                            'selected_cuisine': selected_cuisine,
                                            'menus': menus,
                                            'selected_menu': selected_menu,
                                            'random_obj': random_obj,

                                            })

#
# def mineFilter(selected_category, selected_bludo, selected_cuisine, selected_menu):
#     if

def dishes_page(request):
    selected_category = request.GET.get('category')
    objects_list = Dishes.objects.order_by('dish_name')
    selected_bludo = request.GET.get('bludo')
    selected_cuisine = request.GET.get('cuisine')
    selected_menu = request.GET.get('menu')
    object_list = Dishes.objects.order_by('dish_name')
    if request.user.is_authenticated:
        favorite_recipes = FavoriteRecipe.objects.filter(user=request.user).values_list('recipe', flat=True)
        for recipe in object_list:
            recipe.is_favorite = recipe.id in favorite_recipes

    # Если необходимо, преобразовать обратно в QuerySet
    # object_list = Dishes.objects.filter(pk__in=[obj.pk for obj in object_list])

    if selected_category !=None and selected_category != 'all':
        objects_list = object_list.filter(category__name=selected_category)

    if selected_bludo != None and selected_bludo != 'all':
        objects_list = object_list.filter(bludo__name=selected_bludo)
    #
    if selected_cuisine and selected_cuisine != 'all':
        objects_list = object_list.filter(nationality__name=selected_cuisine)

    if selected_menu and selected_menu != 'all':
        objects_list = object_list.filter(menu__name=selected_menu)

    categories = Category.objects.all()
    bludos = Bludo.objects.filter(category__name=selected_category)
    cuisines = Nationality.objects.all()
    menus = Menu.objects.all()

    return render(request, './pick_up.html', {
        'object_list': object_list,
        'categories': categories,
        'bludos': bludos,
        'selected_category': selected_category,
        'selected_bludo': selected_bludo,
        'cuisines': cuisines,
        'selected_cuisine': selected_cuisine,
        'objects_list': objects_list,
        'menus': menus,
        'selected_menu': selected_menu,
    })


def categories(request):
    cats = Category.objects.all()
    return render(request, './dishes.html', {'cats': cats})

def detail(request):
    my_object_id = request.session.get('my_object_id')
    if my_object_id:
        my_object = Dishes.objects.get(pk=my_object_id)

    return render(request, './detail.html', {'my_object': my_object})

def detail2(request, object_id):
    object = get_object_or_404(Dishes, id=object_id)
    return render(request, 'detail2.html', {'object': object})

def search_view(request):
    query = request.GET.get('query')
    query = query.title()
    recipes = Dishes.objects.filter(dish_name__icontains=query) if query else []
    # if request.user.is_authenticated:
    #     favorite_recipes = FavoriteRecipe.objects.filter(user=request.user).values_list('recipe', flat=True)
    #     for recipe in object_list:
    #         recipe.is_favorite = recipe.id in favorite_recipes

    return render(request, 'search.html', {'query': query, 'recipes': recipes})

def pick_up(request):
    selected_category = request.GET.get('category')
    selected_bludo = request.GET.get('bludo')
    selected_cuisine = request.GET.get('cuisine')
    selected_menu = request.GET.get('menu')

    object_list = Dishes.objects.all()
    object_list = list(object_list)
    k = random.choice(list(range(6,15)))
    random.shuffle(object_list)
    object_list = object_list[:k]
    if request.user.is_authenticated:
        favorite_recipes = FavoriteRecipe.objects.filter(user=request.user).values_list('recipe', flat=True)
        for recipe in object_list:
            recipe.is_favorite = recipe.id in favorite_recipes


    categories = Category.objects.all()
    bludos = Bludo.objects.filter(category__name=selected_category)
    cuisines = Nationality.objects.all()
    menus = Menu.objects.all()

    return render(request, './dishes.html', {
        'object_list': object_list,
        'categories': categories,
        'bludos': bludos,
        'selected_category': selected_category,
        'selected_bludo': selected_bludo,
        'cuisines': cuisines,
        'selected_cuisine': selected_cuisine,
        'menus': menus,
        'selected_menu': selected_menu,
    })


@login_required
def add_to_favorites(request, recipe_id):
    if request.user.is_authenticated:
        recipe = Dishes.objects.get(id=recipe_id)
        favorite_recipe = FavoriteRecipe(user=request.user, recipe=recipe)
        favorite_recipe.save()
        return redirect('favorite_recipes')
    else:
        return redirect('login')

@login_required
def remove_from_favorites(request, recipe_id):
    if request.user.is_authenticated:
        favorite_recipes = FavoriteRecipe.objects.filter(user=request.user, recipe=recipe_id)
        favorite_recipes.delete()

    return redirect('favorite_recipes')

def favorite_recipes(request):

    user = request.user
    favorite_recipes = FavoriteRecipe.objects.filter(user=user)

    return render(request, 'favorite_recipes.html', {'favorite_recipes': favorite_recipes})


