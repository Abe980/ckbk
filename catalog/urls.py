from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe_add/', views.recipe_add, name='recipe_add'),
    path('recipe_edit/<int:recipe_id>/', views.recipe_edit, name='recipe_edit'),
    path('recipe_view/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('user/registration/', views.registration, name='registration'),
    path('user/logout/', views.logout_view, name='logout_view'),
]

