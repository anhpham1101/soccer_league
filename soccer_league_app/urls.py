from django.urls import path

from .views import soccer_club_view, soccer_stadium_view, upload_match_csv_view, soccer_match_view, soccer_ranking_view, soccer_match_by_club_view

urlpatterns = [
    path('', soccer_ranking_view, name='ranking_view'),
    path('matches', soccer_match_view, name='matches_view'),
    path('matches/<int:club_id>', soccer_match_by_club_view, name='matches_by_club_view'),
    path('clubs', soccer_club_view, name='clubs_view'),
    path('stadiums', soccer_stadium_view, name='stadiums_view'),
    path('upload/match/csv', upload_match_csv_view, name='upload_csv_view'),
]
