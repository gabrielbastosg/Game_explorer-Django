from django.db import models

# Create your models here.
class FavoriteGame(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    game_id = models.IntegerField()
    name = models.CharField(max_length=255)
    background_image = models.URLField(max_length=200, blank=True, null=True)
    released = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class GameStatus(models.Model):
    STATUS_CHOICES = [
        ('quero',   'Quero jogar'),
        ('jogando', 'Jogando'),
        ('zerei',   'Zerei'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    game_id = models.IntegerField()
    name = models.CharField(max_length=255)
    background_image = models.URLField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    nota = models.PositiveSmallIntegerField(null=True, blank=True)
    review = models.TextField(blank=True)


    def __str__(self):
        return f"{self.name} - {self.status}"
        
