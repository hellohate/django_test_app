from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    date = models.DateField(default=date.today)
    total_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_votes')
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')
