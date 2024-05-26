from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    steps = models.TextField()
    cooking_time = models.PositiveIntegerField()
    img = models.ImageField(default='нет_изображения.webp')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name