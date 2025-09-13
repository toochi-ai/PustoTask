# Дано несколько моделей
# Написать два метода:
# 1. Присвоение игроку приза за прохождение уровня.
# 2. Выгрузку в csv следующих данных: id игрока, название уровня, пройден ли уровень,
# полученный приз за уровень. Учесть, что записей может быть 100 000 и более.

import csv
from django.db import models
from django.http import HttpResponse

class Player(models.Model):
    player_id = models.CharField(max_length=100)

class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

class Prize(models.Model):
    title = models.CharField(max_length=100)

class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()

class GameService:
    @staticmethod
    def assign_prize_to_player(player_id, level_id, prize_id):
        try:
            player_level = PlayerLevel.objects.get(
                player_id=player_id,
                level_id=level_id,
                is_completed=True
            )

            LevelPrize.objects.create(
                level_id=level_id,
                prize_id=prize_id,
                received=player_level.completed
            )

            return True, "Приз присвоен."

        except PlayerLevel.DoesNotExist:
            return False, "Уровень не пройден."
        except Exception as e:
            return False, f"Ошибка: {str(e)}"

    @staticmethod
    def export_player_levels_to_csv():
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="player_levels.csv"'

        writer = csv.writer(response)
        writer.writerow(['id игрока', 'название уровня', 'пройден ли уровень', 'полученный приз за уровень'])

        player_levels = PlayerLevel.objects.select_related('player', 'level').iterator(chunk_size=10000)

        for player_level in player_levels:
            prize_titles = []
            if player_level.is_completed:
                prizes = LevelPrize.objects.filter(level=player_level.level).select_related('prize')
                prize_titles = [prize.prize.title for prize in prizes]

            writer.writerow([
                player_level.player.player_id,
                player_level.level.title,
                'Да' if player_level.is_completed else 'Нет',
                ', '.join(prize_titles)
            ])

        return response
