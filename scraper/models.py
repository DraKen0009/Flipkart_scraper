from django.db import models

from users.models import User


# Create your models here.

class Data(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    num_reviews = models.PositiveIntegerField(default=0)
    num_ratings = models.PositiveIntegerField(default=0)
    ratings = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    num_media = models.PositiveIntegerField(default=0)
    url = models.URLField(max_length=500, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
