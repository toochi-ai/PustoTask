# Приложение подразумевает ежедневный вход пользователя, начисление баллов за вход.
# Нужно отследить момент первого входа игрока для аналитики. Также у игрока имеются
# игровые бонусы в виде нескольких типов бустов. Нужно описать модели игрока и бустов с
# возможностью начислять игроку бусты за прохождение уровней или вручную. (Можно
# написать, применяя sqlachemy)

from django.db import models


class Player(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    first_login = models.DateTimeField(auto_now_add=True)
    last_daily_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} уровень {self.level}, {self.points} баллов."


class Boost(models.Model):
    SOURCE_CHOICES = [
        ('admin', 'Администратор'),
        ('daily_login', 'Ежедневный вход'),
        ('level_complete', 'Прохождение уровня')
    ]

    type = models.CharField(max_length=20)
    player = models.ForeignKey(Player, related_name='boosts', on_delete=models.CASCADE)
    level_obtained = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    