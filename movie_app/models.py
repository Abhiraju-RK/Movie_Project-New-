from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    poster=models.ImageField()
    description=models.TextField()
    release_date=models.DateField()
    actors=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='movies')
    youtube_trailer=models.URLField()

    def __str__(self):
        return f"{self.user}-{self.title}"

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    text=models.TextField()
    rating=models.IntegerField()

    def __str__(self):
        return f"{self.user.username}--{self.movie.title}"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.movie.title}"
