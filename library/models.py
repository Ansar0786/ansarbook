from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta




class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ]
    name=models.CharField(max_length=30)
    author=models.CharField(max_length=40)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    pages = models.PositiveIntegerField()
    def __str__(self):
        return str(self.name)+"["+str(self.pages)+']'


def get_expiry():
    return datetime.today() + timedelta(days=5)

