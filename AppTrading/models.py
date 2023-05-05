from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Titre(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=255)
    difference = models.FloatField()
    graphe = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name


class Portefeuille(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.BigIntegerField()

    def __str__(self):
        return self.author.username


class Action(models.Model):
    titre_action = models.ForeignKey(Titre, on_delete=models.CASCADE)
    value = models.BigIntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    portefeuille = models.ForeignKey(Portefeuille, on_delete=models.CASCADE)
    buy = models.CharField(max_length=255)
    variation = models.FloatField()

    def __str__(self):
        return self.author.username, self.titre_action.name
