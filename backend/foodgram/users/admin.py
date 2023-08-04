from django.contrib.admin import ModelAdmin, site
from recipes.models import Recipe, Ingredient, Tag, Favorite
from users.models import User, Subscription
from django.contrib.auth.models import Group


class UserAdmin(ModelAdmin):

    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    list_display = ('username', 'email', 'first_name', 'last_name')

    def save_model(self, request, obj, form, change):
        '''
        Правильно захеширует пароль при его смене через админку
        '''
        obj.set_password(form.cleaned_data('password'))
        obj.save()


class SubscriptionAdmin(ModelAdmin):
    list_filter = ('author__username', 'user__username')
    list_display = ('user', 'author')
    search_fields = (
        'author__username',
        'author__email',

    )


class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    search_fields = ('name',)


class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', )


class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'name', 'author', 'in_favorites')
    search_fields = ('name', 'author__username')
    list_filter = ('tags__name', 'author__username', 'name')

    def in_favorites(self, obj):
        '''
        Количество добавлений в избранное рецепта
        '''
        return len(Favorite.objects.filter(recipe=obj))


site.unregister(Group)
site.register(Recipe, RecipeAdmin)
site.register(Ingredient, IngredientAdmin)
site.register(Tag, TagAdmin)
site.register(Subscription, SubscriptionAdmin)
site.register(User, UserAdmin)
