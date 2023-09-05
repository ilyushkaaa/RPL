from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import connection
from .models import Referee
from .models import Stadium
from .models import Team
from .models import Footballer
from .models import Match
from .models import Goal
from django.shortcuts import render, redirect
from .forms import MatchForm, GoalForm, FootballerForm
from django.views.generic import UpdateView, DeleteView


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
        query = "select sel.id, sel.footballer_id, sel.minute, rpl.footballer.name, rpl.footballer.surname, rpl.footballer.team_id from (SELECT goal.id,goal.footballer_id,goal.minute FROM rpl.goal WHERE %s = goal.match_id) as sel join rpl.footballer on rpl.footballer.id = sel.footballer_id order by minute"
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
    with connection.cursor() as cursor2:
        query = "SELECT * from rpl.full_results_view where referee_id = %s order by date"
        cursor2.execute(query, [referee_id])
        results = cursor2.fetchall()
    ref = get_object_or_404(Referee, id=referee_id)
    return render(request, 'main/referee_detail.html', {'ref': ref, 'results': results})


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


def my_template_view(request):
    return render(request, 'main/my_template.html')


def add_match(request):
    error = ''
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()

        else:
            error = "error"
    form = MatchForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/add_match.html', data)


def add_goal(request):
    error = ''
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            form.save()

        else:
            error = "error"
    form = GoalForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/add_goal.html', data)


def add_footballer(request):
    error = ''
    if request.method == "POST":
        form = FootballerForm(request.POST)
        if form.is_valid():
            form.save()

        else:
            error = "error"
    form = FootballerForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/add_footballer.html', data)


def change_match(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "select t1.name, t2.name, date, rpl.match.id from rpl.match join rpl.team t1 on t1.id = rpl.match.team_home_id join rpl.team t2 on t2.id = rpl.match.team_guest_id order by date")
        matches = cursor.fetchall()
    return render(request, 'main/list_match.html', {'matches': matches})


def change_footballer(request):
    footballers = Footballer.objects.all()
    return render(request, 'main/list_footballer.html', {'footballers': footballers})


def change_goal(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "select t1.name, t2.name, rpl.footballer.name, rpl.footballer.surname, rpl.goal.minute, rpl.goal.id from rpl.goal join rpl.match on rpl.match.id = rpl.goal.match_id join rpl.team t1 on t1.id = rpl.match.team_home_id join rpl.team t2 on t2.id = rpl.match.team_guest_id join rpl.footballer on rpl.footballer.id = rpl.goal.footballer_id")
        goals = cursor.fetchall()
    return render(request, 'main/list_goal.html', {'goals': goals})


class UpdateMatch(UpdateView):
    model = Match
    template_name = 'main/change_match.html'
    fields = ['id', 'team_home', 'team_guest', 'referee', 'date', 'is_over']


class UpdateFootballer(UpdateView):
    model = Footballer
    template_name = 'main/change_footballer.html'
    fields = ['id', 'surname', 'name', 'patronymic', 'birthday', 'team', 'photo_path', 'position']


class UpdateGoal(UpdateView):
    model = Goal
    template_name = 'main/change_goal.html'

    fields = ['id', 'footballer', 'minute', 'match']


class DeleteFootballer(DeleteView):
    model = Footballer
    template_name = 'main/delete_footballer.html'
    success_url = ''


class DeleteGoal(DeleteView):
    model = Goal
    template_name = 'main/delete_goal.html'


class DeleteMatch(DeleteView):
    model = Match
    template_name = 'main/delete_match.html'
