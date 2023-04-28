from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password,  **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    is_admin = models.BooleanField(
        default=False, verbose_name='Admin'
    )

    def __str__(self):
        return self.username

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Flow(models.Model):
    title = models.CharField(
        max_length=60, 
        verbose_name='Заголовок'
        )

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'

    def __str__(self):
        return self.title


class Direction(models.Model):
    title = models.CharField(
        max_length=60, 
        verbose_name='Заголовок'
        )
    flow = models.ForeignKey(
        Flow, on_delete=models.CASCADE,
        related_name='directions',
        verbose_name='Поток'
        )

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return self.title


class Student(models.Model):
    first_name = models.CharField(
        max_length=60, 
        verbose_name='Имя'
        )
    last_name = models.CharField(
        max_length=60, 
        verbose_name='Фамилия'
        )
    age = models.PositiveIntegerField(verbose_name='Возраст')
    direction = models.ForeignKey(
        Direction, 
        on_delete=models.CASCADE, 
        verbose_name='Направление', 
        related_name='directions'
        )
    # flow = models.ForeignKey(Flow, 
    #     on_delete=models.CASCADE, 
    #     verbose_name='Поток', 
    #     related_name='flows'
    #     )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

