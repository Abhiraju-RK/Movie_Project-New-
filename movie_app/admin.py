from django.contrib import admin
from .models import Category,Movie,Review,Favorite
# Register your models here.
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Favorite)