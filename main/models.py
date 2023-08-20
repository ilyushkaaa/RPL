import time
from datetime import datetime

from django.db import models


# Create your models here.

class Stadium(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    max_people = models.BigIntegerField()
    photo_path = models.TextField(default='qwerty')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'stadium'


class Referee(models.Model):
    id = models.BigIntegerField(primary_key=True)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    birthday = models.DateField()
    city = models.CharField(max_length=30)
    photo_path = models.TextField(default='qwerty')

    def __str__(self):
        return self.name + ' ' + self.surname

    class Meta:
        managed = False
        db_table = 'referee'


class Team(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    emblem_path = models.TextField()

    def __str__(self):
        return self.name + ' ' + self.city

    class Meta:
        managed = False
        db_table = 'team'


class Footballer(models.Model):
    id = models.BigIntegerField(primary_key=True)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    birthday = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    photo_path = models.TextField(default='qwerty')
    position = models.CharField(max_length=30, default='qwerty')

    def __str__(self):
        return self.name + ' ' +  self.surname

    class Meta:
        managed = False
        db_table = 'footballer'


class Match(models.Model):
    id = models.BigIntegerField(primary_key=True)
    team_home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_home')
    team_guest = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_guest')
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE)
    date = models.DateField()
    is_over = models.BooleanField()

    def __str__(self):
        return str(self.team_home) + str(self.team_guest)

    class Meta:
        managed = False
        db_table = 'match'


class Goal(models.Model):
    id = models.BigIntegerField(primary_key=True)
    footballer = models.ForeignKey(Footballer, on_delete=models.CASCADE)
    minute = models.BigIntegerField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.footballer) + str(self.match) + str(self.minute)

    class Meta:
        managed = False
        db_table = 'goal'
