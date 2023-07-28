from django.db import models


# Create your models here.


class Genres(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Games(models.Model):
    title = models.CharField(max_length=32, null=False)
    description = models.CharField(max_length=256, null=False)
    players = models.CharField(max_length=8, null=False)
    age_category = models.CharField(max_length=4, null=False)
    video_link = models.URLField()
    image = models.ImageField(upload_to="games/")
    genre = models.ManyToManyField(Genres)
    game_mode = models.CharField(
        choices=[
            ("single", "Single Player"),
            ("multiplayer", "Multiplayer"),
            ("both", "Both (Single & Multiplayer)"),
        ],
        max_length=12,
    )

    def str(self):
        return self.title + self.age_category
