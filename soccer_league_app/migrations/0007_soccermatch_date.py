# Generated by Django 4.2.3 on 2023-07-22 13:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer_league_app', '0006_soccermatch_soccermatch_unique_soccer_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='soccermatch',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
    ]
