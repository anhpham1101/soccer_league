import datetime

from django.db import models


class Stadium(models.Model):
    name = models.TextField()
    city = models.TextField()
    establish_year = models.IntegerField()


class Nationality(models.Model):
    name = models.TextField()
    telephone_code = models.TextField()
    iso_2_code = models.TextField()
    iso_3_code = models.TextField()
    ensign = models.BinaryField(null=True)


class Club(models.Model):
    name = models.TextField()
    short_name = models.TextField()
    logo = models.ImageField(null=True, blank=True, upload_to='images/clubs/')
    stadium = models.ForeignKey("Stadium", on_delete=models.SET_NULL, null=True)


class Player(models.Model):
    name = models.TextField()
    club = models.ForeignKey("Club", on_delete=models.SET_NULL, null=True)
    position = models.TextField()
    nationality = models.ForeignKey("Nationality", on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField()
    height = models.IntegerField()
    clothers_number = models.IntegerField()
    avatar = models.ImageField(null=True, blank=True, upload_to='images/players/')


class SoccerMatch(models.Model):
    round = models.IntegerField()
    match_number = models.AutoField(primary_key=True)
    home_club = models.ForeignKey("Club", on_delete=models.SET_NULL, null=True, related_name="home_club")
    away_club = models.ForeignKey("Club", on_delete=models.SET_NULL, null=True, related_name="away_club")
    ft_home_goal = models.IntegerField(default=0)
    ft_away_goal = models.IntegerField(default=0)
    ft_result = models.TextField(default='D')
    ht_home_goal = models.IntegerField(default=0)
    ht_away_goal = models.IntegerField(default=0)
    ht_result = models.TextField(default='D')
    date = models.DateField(default=datetime.date.today, blank=True)
    time = models.TimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['round', 'home_club', 'away_club'],
                name='unique_soccer_match'
            ),
        ]
