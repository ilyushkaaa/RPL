import hashlib
import time
from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


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
    STATUS_CHOICES = [
        ('Защитник', 'Защитник'),
        ('Вратарь', 'Вратарь'),
        ('Нападающий', 'Нападающий'),
        ('Полузащитник', 'Полузащитник')
    ]

    id = models.BigIntegerField(primary_key=True)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    birthday = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    photo_path = models.TextField(default='qwerty')
    position = models.CharField(max_length=30, default='qwerty', choices=STATUS_CHOICES)

    def __str__(self):
        return self.name + ' ' + self.surname

    def get_absolute_url(self):
        return reverse('list_footballer')

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

    def get_absolute_url(self):
        return reverse('list_match')

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
    success_url = ''

    def get_absolute_url(self):
        return reverse('list_goal')

    def __str__(self):
        return str(self.footballer) + str(self.match) + str(self.minute)

    class Meta:
        managed = False
        db_table = 'goal'


class FanManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Fan(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=False)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    favourite_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    password = models.CharField(max_length=70)
    email = models.EmailField(max_length=50, primary_key=True, unique=True)
    last_login = models.DateTimeField(auto_now=True)  # Добавляем last_login
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = FanManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday', 'favourite_team']

    def get_absolute_url(self):
        return reverse('main')
    def save(self, *args, **kwargs):
        # Перед сохранением, установите username равным email
        self.username = self.email
        if len(self.password) != 64:
            sha256_hash = hashlib.sha256()

            # Обновите хэш с байтами строки (преобразованными в байты)
            sha256_hash.update(self.password.encode('utf-8'))

            # Получите SHA-256 хэш в виде шестнадцатеричной строки
            self.password = sha256_hash.hexdigest()
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        sha256_hash = hashlib.sha256()

        # Обновите хэш с байтами строки (преобразованными в байты)
        sha256_hash.update(raw_password.encode('utf-8'))

        # Получите SHA-256 хэш в виде шестнадцатеричной строки
        hash_password = sha256_hash.hexdigest()
        print(hash_password)

        # Реализация проверки совпадения паролей
        return hash_password == self.password  # П

    def __str__(self):
        return str(self.email)

    class Meta:
        managed = False
        db_table = 'fan'


class Ticket(models.Model):
    id = models.BigIntegerField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    sector = models.BigIntegerField()
    row = models.BigIntegerField()
    place = models.BigIntegerField()

    def __str__(self):
        return str(self.sector) + str(self.row) + str(self.place)

    class Meta:
        managed = False
        db_table = 'ticket'


class TicketSales(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'ticket_sales'
