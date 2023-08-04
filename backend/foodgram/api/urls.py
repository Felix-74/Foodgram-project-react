from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CheckSubscribeAPIView, SubscribeAPIView
from recipes.views import (TagViewSet, RecipeViewSet,
                           FavoriteAPIView, ShopCartAPIView,
                           IngredientViewSet, DownloadFilesAPIView)

default_urls = DefaultRouter()

default_urls.register('ingredients', IngredientViewSet)
default_urls.register('tags', TagViewSet)
default_urls.register('recipes', RecipeViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'recipes/download_shopping_cart/',
        DownloadFilesAPIView.as_view()
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShopCartAPIView.as_view()
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscribeAPIView.as_view()
    ),
    path(
        'users/subscriptions/',
        CheckSubscribeAPIView.as_view()
    ),

    path(
        'recipes/<int:id>/favorite/',
        FavoriteAPIView.as_view()
    ),
    path('', include(default_urls.urls)),
    path('', include('djoser.urls')),
]
