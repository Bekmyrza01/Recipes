from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.first_page, name='index'),
    path('dish/', views.dishes_page, name='dishes'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pick_up/', views.pick_up, name='pick_up'),
    path('accounts/', include('social_django.urls', namespace='social')),
    path('detail/', views.detail, name='detail'),
    path('detail2/<int:object_id>/', views.detail2, name='detail2'),
    path('search/', views.search_view, name='search'),
    path('recipe/add_to_favorites/<int:recipe_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorite_recipes/', views.favorite_recipes, name='favorite_recipes'),
    path('recipe/remove_from_favorites/<int:recipe_id>/', views.remove_from_favorites, name='remove_from_favorites'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

