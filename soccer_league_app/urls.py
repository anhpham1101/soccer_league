from django.urls import path

from .views import soccer_club_view, soccer_player_view, soccer_stadium_view, upload_match_csv_view, soccer_match_view, soccer_ranking_view, soccer_match_by_club_view
from .views import PlayerCreate, ClubCreate
from .views import soccer_club_delete_view, soccer_player_delete_view

urlpatterns = [
    path('', soccer_ranking_view, name='ranking_view'),
    path('matches', soccer_match_view, name='matches_view'),
    path('matches/<int:club_id>', soccer_match_by_club_view, name='matches_by_club_view'),

    path('clubs', soccer_club_view, name='clubs_view'),
    path('clubs/add', ClubCreate.as_view(), name="clubs_add_view"),
    path('clubs/<int:club_id>/delete/', soccer_club_delete_view, name="clubs_delete_view"),

    path('players', soccer_player_view, name='players_view'),
    path('players/add', PlayerCreate.as_view(), name="players_add_view"),
    path('players/<int:player_id>/delete/', soccer_player_delete_view, name="players_delete_view"),

    path('stadiums', soccer_stadium_view, name='stadiums_view'),
    path('upload/match/csv', upload_match_csv_view, name='upload_csv_view'),
]
