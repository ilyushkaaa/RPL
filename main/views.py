from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import connection
from .models import Referee
from .models import Stadium
from .models import Team
from .models import Footballer
from .models import Match
from .models import Goal


def index(request):
    teams = Team.objects.all()
    return render(request, 'main/index.html', {"teams": teams})


def next(request):
    return render(request, 'main/next.html')


def footballer_detail(request, foot_id):
    footballer = get_object_or_404(Footballer, id=foot_id)
    with connection.cursor() as cursor1:
        query = "SELECT * from rpl.team where id = %s"
        cursor1.execute(query, [footballer.team_id])
        footballer_team = cursor1.fetchall()

    return render(request, 'main/footballer_detail.html',
                  {'footballer': footballer, 'footballer_team': footballer_team})


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    stadium = team.stadium
    return render(request, 'main/team_detail.html', {'team': team, 'stadium': stadium})


def show_team_players(request, current_team_id):
    with connection.cursor() as cursor1:
        query = "SELECT * from rpl.footballer where %s = rpl.footballer.team_id"
        cursor1.execute(query, [current_team_id])
        current_players = cursor1.fetchall()
    team = get_object_or_404(Team, id=current_team_id)
    return render(request, 'main/show_team_players.html', {'current_players': current_players, 'team': team})


def show_stadium(request, stadium_id):
    st = get_object_or_404(Stadium, id=stadium_id)
    return render(request, 'main/show_stadium.html', {'st': st})


def match(request, match_id):
    with connection.cursor() as cursor:
        query = "select sel.id, sel.footballer_id, sel.minute, rpl.footballer.name, rpl.footballer.surname, rpl.footballer.team_id from (SELECT goal.id,goal.footballer_id,goal.minute FROM rpl.goal WHERE %s = goal.match_id) as sel join rpl.footballer on rpl.footballer.id = sel.footballer_id"
        cursor.execute(query, [match_id])
        goal_info = cursor.fetchall()
    with connection.cursor() as cursor1:
        query = "SELECT * from rpl.results_view where %s = id"
        cursor1.execute(query, [match_id])
        result = cursor1.fetchall()

    with connection.cursor() as cursor3:
        query = "select sel.home as home_id, sel.guest as guest_id, sel.id as match_id, t1.name as home_name, t2.name as guest_name, t1.emblem_path as home_emblem, t2.emblem_path as guest_emblem, rpl.match.referee_id, t1.stadium_id, rpl.stadium.name as st_name, rpl.referee.name as ref_name, rpl.referee.surname as ref_surname from (select * from rpl.results_view where id = %s) as sel join rpl.team t1 on t1.id = sel.home join rpl.team t2 on t2.id = sel.guest join rpl.match on rpl.match.id = sel.id join rpl.stadium on rpl.stadium.id = t1.stadium_id join rpl.referee on rpl.referee.id = rpl.match.referee_id"
        cursor3.execute(query, [match_id])
        match_info = cursor3.fetchall()

    return render(request, 'main/match.html', {'match_info': match_info, 'result': result, 'goal_info': goal_info})


def referee_detail(request, referee_id):
    ref = get_object_or_404(Referee, id=referee_id)
    return render(request, 'main/referee_detail.html', {'ref': ref})


def results(request):
    with connection.cursor() as cursor2:
        cursor2.execute("SELECT * from rpl.full_results_view order by date")
        results = cursor2.fetchall()
    return render(request, 'main/results.html', {'results': results})


def timetable(request):
    with connection.cursor() as cursor3:
        cursor3.execute(
            "select t1.name,t2.name, sel.date from (select * from rpl.match where is_over = false) as sel join rpl.team t1 on t1.id = sel.team_home_id join rpl.team t2 on t2.id = sel.team_guest_id")
        future_matches = cursor3.fetchall()
    return render(request, 'main/timetable.html', {'future_matches': future_matches})


def table(request):
    with connection.cursor() as cursor1:
        cursor1.execute("SELECT * from rpl.full_table_view")
        tournament_table = cursor1.fetchall()
    return render(request, 'main/table.html', {'tournament_table': tournament_table})


def bombardirs(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from rpl.bombardir_view")
        bombardirs = cursor.fetchall()
    return render(request, 'main/bombardirs.html', {'bombardirs': bombardirs})


def stadiums(request):
    stadiums = Stadium.objects.all()
    return render(request, 'main/stadiums.html', {'stadiums': stadiums})


def referee_all(request):
    referee = Referee.objects.all()
    return render(request, 'main/referee.html', {'referee': referee})



