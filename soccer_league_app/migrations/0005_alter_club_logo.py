# Generated by Django 4.2.3 on 2023-07-22 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer_league_app', '0004_nationality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/clubs/'),
        ),
    ]