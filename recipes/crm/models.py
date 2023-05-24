from django.db import models
from django.contrib.auth.models import User





class Category(models.Model):
    name = models.CharField("Категория", max_length=200)

    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField("Нация", max_length=200)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField("Menu", max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("products", max_length=200)

    def __str__(self):
        return self.name

class Bludo(models.Model):
    name = models.CharField("products", max_length=200)
    category = models.ManyToManyField(Category,verbose_name="Блюдо")

    def __str__(self):
        return self.name


class Dishes(models.Model):
    dish_dt = models.DateTimeField(auto_now=True)
    dish_name = models.CharField(max_length=200, verbose_name="Name of dish")
    dish_info = models.TextField(verbose_name="Information")
    dish_image = models.ImageField(upload_to="templates/media/", default='templates/static/image/image4.jpg')
    nationality = models.ManyToManyField(Nationality ,verbose_name='Nationality')
    category = models.ManyToManyField(Category, verbose_name='Category of dish')
    menu = models.ManyToManyField(Menu, verbose_name="Menu")
    products = models.CharField(max_length=200,verbose_name="Products",default='Ech balya')
    bludo = models.ManyToManyField(Bludo)


    def __str__(self):
        return self.dish_name


    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    favorite_recipes = models.ManyToManyField(Dishes)

    # Добавьте другие поля, связа

    def __str__(self):
        return self.user.username


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Dishes, on_delete=models.CASCADE)