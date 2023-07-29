import logging
import datetime
import collections
import operator

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic import CreateView

from .models import Club, Player, Stadium, SoccerMatch

WIN_SCORE = 3
DRAW_SCORE = 1


def soccer_club_view(request):
    clubs = Club.objects.all()
    context = dict(clubs=clubs)
    return render(request, 'soccer_league_app/soccer_club.html', context)


def soccer_club_add_view(request):
    # TODO LATER
    return redirect('/')


def soccer_club_delete_view(request, club_id):
    Club.objects.filter(id=club_id).delete()
    return redirect('/clubs')


def soccer_player_view(request):
    players = Player.objects.all()
    context = dict(players=players)
    return render(request, 'soccer_league_app/soccer_player.html', context)


def soccer_player_delete_view(request, player_id):
    Player.objects.filter(id=player_id).delete()
    return redirect('/players')


def soccer_stadium_view(request):
    stadiums = Stadium.objects.all()
    context = dict(stadiums=stadiums)
    return render(request, 'soccer_league_app/soccer_stadium.html', context)


def soccer_match_view(request):
    matches = SoccerMatch.objects.all()
    context = dict(matches=matches)
    return render(request, 'soccer_league_app/soccer_match.html', context)


def soccer_match_by_club_view(request, club_id):
    matches = SoccerMatch.objects.filter(Q(home_club_id=club_id) | Q(away_club_id=club_id))
    context = dict(matches=matches)
    return render(request, 'soccer_league_app/soccer_match.html', context)


def upload_match_csv_view(request):
    data = dict()
    if request.method == "GET":
        return render(request, "soccer_league_app/upload_match_result.html", data)
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_csv_view"))

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:
            fields = line.split(",")
            try:
                HomeClub = Club.objects.filter(Q(name=fields[3]) | Q(short_name=fields[3]))[0]
                AwayClub = Club.objects.filter(Q(name=fields[4]) | Q(short_name=fields[4]))[0]
                date = datetime.datetime.strptime(fields[1], '%d/%m/%Y').strftime('%Y-%m-%d')
                SoccerMatch(
                    round=int(fields[0]),
                    date=date,
                    time=fields[2],
                    home_club=HomeClub,
                    away_club=AwayClub,
                    ft_home_goal=int(fields[5]),
                    ft_away_goal=int(fields[6]),
                    ft_result=fields[7],
                    ht_home_goal=int(fields[8]),
                    ht_away_goal=int(fields[9]),
                    ht_result=fields[10]
                ).save()
            except Exception as e:
                logging.getLogger("error_logger").error("Unable to create data. " + repr(e))
                messages.error(request, "Unable to create data. " + repr(e))
        return redirect('/')
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("upload_csv_view"))


def soccer_ranking_view(request):
    rankings = prepare_ranking_data()
    context = dict(rankings=rankings)
    return render(request, 'soccer_league_app/soccer_ranking.html', context)


def prepare_ranking_data():
    def get_ranking_key(ranking_data):
        ig = operator.itemgetter(1)(ranking_data)
        return (ig['point']), (ig['num_goal_diff'])

    def add_ranking_data(data):
        result = ranking_data[data['club']]
        result['num_match_played'] += 1
        result['num_match_won'] += data.get('match_won', 0)
        result['num_match_drawn'] += data.get('match_drawn', 0)
        result['num_match_lost'] += data.get('match_lost', 0)
        result['num_goal_for'] += data.get('num_goal_for', 0)
        result['num_goal_against'] += data.get('num_goal_against', 0)
        result['history'] += [data.get('result')]

    ranking_data = collections.defaultdict(_get_ranking_data_template)
    for home_team_data, away_team_data in extract_match_data():
        add_ranking_data(home_team_data)
        add_ranking_data(away_team_data)
    ranking_data = post_process_ranking_data(ranking_data)

    return [
        {
            **{'club': club},
            **club_data
        } for club, club_data in sorted(ranking_data.items(), key=get_ranking_key, reverse=True)
    ]


def extract_match_data():
    matches = SoccerMatch.objects.all()
    for match in matches:
        home_team = dict(
            club=match.home_club,
            num_goal_for=match.ft_home_goal,
            num_goal_against=match.ft_away_goal
        )
        away_team = dict(
            club=match.away_club,
            num_goal_for=match.ft_away_goal,
            num_goal_against=match.ft_home_goal
        )
        if match.ft_result == 'H':
            home_team['match_won'] = away_team['match_lost'] = 1
            home_team['result'] = 'W'
            away_team['result'] = 'L'
        elif match.ft_result == 'A':
            home_team['match_lost'] = away_team['match_won'] = 1
            home_team['result'] = 'L'
            away_team['result'] = 'W'
        else:
            home_team['match_drawn'] = away_team['match_drawn'] = 1
            home_team['result'] = 'D'
            away_team['result'] = 'D'
        yield home_team, away_team


def _get_ranking_data_template():
    return {
        'num_match_played': 0,
        'num_match_won': 0,
        'num_match_drawn': 0,
        'num_match_lost': 0,
        'num_goal_for': 0,
        'num_goal_against': 0,
        'history': []
    }


def post_process_ranking_data(ranking_data):
    for club, club_data in ranking_data.items():
        ranking_data[club]['num_goal_diff'] = club_data['num_goal_for'] - club_data['num_goal_against']
        ranking_data[club]['point'] = club_data['num_match_won'] * WIN_SCORE + club_data['num_match_drawn'] * DRAW_SCORE
        ranking_data[club]['short_history'] = club_data['history'][-5:]
    return ranking_data


class PlayerCreate(CreateView):
    model = Player
    fields = ["name", "position", "date_of_birth", "avatar", "club", "nationality", "clothers_number", "height"]

    def get_success_url(self):
        return reverse('players_view')


class ClubCreate(CreateView):
    model = Club
    fields = ["name", "logo", "stadium", "short_name"]

    def get_success_url(self):
        return reverse('clubs_view')
