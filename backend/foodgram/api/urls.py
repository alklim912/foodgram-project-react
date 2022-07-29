from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register('ingredients', views.IngredientViewSet,
                   basename='ingredients')
router_v1.register('tags', views.TagViewSet, basename='tags')
router_v1.register('recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('auth/token/login/', views.APIToken.as_view(), name='login'),
    path('auth/token/logout/', views.APILogout.as_view(), name='loguot'),
    path('', include(router_v1.urls))
]
