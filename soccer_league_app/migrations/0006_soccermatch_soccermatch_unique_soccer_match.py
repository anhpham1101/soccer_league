# Generated by Django 4.2.3 on 2023-07-22 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soccer_league_app', '0005_alter_club_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoccerMatch',
            fields=[
                ('round', models.IntegerField()),
                ('match_number', models.AutoField(primary_key=True, serialize=False)),
                ('home_goal', models.IntegerField()),
                ('guess_goal', models.ImageField(upload_to='')),
                ('guess_club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guess_club', to='soccer_league_app.club')),
                ('home_club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='home_club', to='soccer_league_app.club')),
            ],
        ),
        migrations.AddConstraint(
            model_name='soccermatch',
            constraint=models.UniqueConstraint(fields=('round', 'home_club', 'guess_club'), name='unique_soccer_match'),
        ),
    ]