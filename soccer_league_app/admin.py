from django.contrib import admin
from .models import Stadium, Nationality, Club, Player, SoccerMatch


admin.site.register(Stadium)
admin.site.register(Nationality)
admin.site.register(Club)
admin.site.register(Player)
admin.site.register(SoccerMatch)
