import hashlib
import json
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.sessions.models import Session
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.urls import reverse_lazy

from .authentication import CustomAuthBackend
from .models import Referee, Fan
from .models import Stadium
from .models import Team
from .models import Footballer
from .models import Match, Ticket, TicketSales
from .models import Goal
from django.shortcuts import render, redirect
from .forms import MatchForm, GoalForm, FootballerForm, FanRegistrationForm, FanLoginForm, UpdateProfileForm
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.hashers import make_password


def is_superuser(user):
    return user.is_superuser


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
    search_query = request.GET.get('search', None)
    print(search_query)

    if search_query:
        with connection.cursor() as cursor2:
            query = "SELECT * from rpl.full_results_view where lower(home_team) ilike lower(%s) or lower(guest_team) ilike lower(%s) order by date desc"
            cursor2.execute(query, ['%' + search_query + '%', '%' + search_query + '%'])
            res = cursor2.fetchall()
    else:
        with connection.cursor() as cursor3:
            cursor3.execute("SELECT * from rpl.full_results_view order by date desc")
            res = cursor3.fetchall()
    return render(request, 'main/results.html', {'results': res})


def timetable(request):
    search_query = request.GET.get('search', None)
    print(search_query)

    if search_query:
        with connection.cursor() as cursor2:
            query = "select t1.name,t2.name, sel.date, sel.id from (select * from rpl.match where is_over = false) as sel join rpl.team t1 on t1.id = sel.team_home_id join rpl.team t2 on t2.id = sel.team_guest_id where lower(t1.name) ilike lower(%s) or lower(t2.name) ilike lower(%s) order by date"

            cursor2.execute(query, ['%' + search_query + '%', '%' + search_query + '%'])
            future_matches = cursor2.fetchall()
    else:
        with connection.cursor() as cursor3:
            cursor3.execute(
                "select t1.name,t2.name, sel.date, sel.id from (select * from rpl.match where is_over = false) as sel join rpl.team t1 on t1.id = sel.team_home_id join rpl.team t2 on t2.id = sel.team_guest_id")
            future_matches = cursor3.fetchall()
    return render(request, 'main/timetable.html', {'future_matches': future_matches})


def table(request):
    with connection.cursor() as cursor1:
        cursor1.execute("SELECT * from rpl.full_table_view")
        tournament_table = cursor1.fetchall()
    return render(request, 'main/table.html', {'tournament_table': tournament_table})


def bombardirs(request):
    search_query = request.GET.get('search', None)
    print(search_query)

    if search_query:
        with connection.cursor() as cursor2:
            query = "select * from rpl.bombardir_view where lower(name) ilike lower(%s) or lower(surname) ilike lower(%s) or lower(team) ilike lower(%s)"
            cursor2.execute(query, ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'])
            bombardirs = cursor2.fetchall()
    else:
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


@user_passes_test(is_superuser)
def my_template_view(request):
    return render(request, 'main/my_template.html')


@user_passes_test(is_superuser)
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


@user_passes_test(is_superuser)
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


@user_passes_test(is_superuser)
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


@user_passes_test(is_superuser)
def change_match(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "select t1.name, t2.name, date, rpl.match.id from rpl.match join rpl.team t1 on t1.id = rpl.match.team_home_id join rpl.team t2 on t2.id = rpl.match.team_guest_id order by date")
        matches = cursor.fetchall()
    return render(request, 'main/list_match.html', {'matches': matches})


@user_passes_test(is_superuser)
def change_footballer(request):
    footballers = Footballer.objects.all()
    return render(request, 'main/list_footballer.html', {'footballers': footballers})


@user_passes_test(is_superuser)
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
    success_url = reverse_lazy('list_footballer')


class DeleteGoal(DeleteView):
    model = Goal
    template_name = 'main/delete_goal.html'
    success_url = reverse_lazy('list_goal')


class DeleteMatch(DeleteView):
    model = Match
    template_name = 'main/delete_match.html'
    success_url = reverse_lazy('list_match')


def authorization(request):
    if request.method == 'POST':
        form = FanLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            custom_backend = CustomAuthBackend()
            user = custom_backend.authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                request.session['user_email'] = user.email
                if user.is_superuser:
                    return redirect('my_template')  # Замените на нужный URL

                else:
                    return redirect('success_authorization')  # Замените на нужный URL

                # Перенаправьте пользователя на страницу после успешной авторизации
            else:
                print("error")
    else:
        form = FanLoginForm()

    return render(request, 'main/authorization.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = FanRegistrationForm(request.POST)
        if form.is_valid():
            # Хешируем пароль
            password = form.cleaned_data['password']
            # Создаем объект Fan и устанавливаем хешированный пароль
            fan_instance = form.save(commit=False)
            fan_instance.password = password
            fan_instance.save()

            # Пользователь успешно зарегистрирован, перенаправьте его на другую страницу
            return redirect('success_registration_page')
    else:
        form = FanRegistrationForm()

    return render(request, 'main/registration.html', {'form': form})


def success_registration(request):
    return render(request, 'main/success_registration.html')


@login_required
def logoutMe(request):
    logout(request)
    return redirect('success_logout')


def success_logout(request):
    return render(request, 'main/success_logout.html')


def success_authorization(request):
    return render(request, 'main/success_authorization.html')


class UpdateProfile(UpdateView):
    model = Fan
    template_name = 'main/change_profile.html'
    form_class = UpdateProfileForm


@login_required
def favourite_team(request, email):
    if request.user.email == email:
        with connection.cursor() as cursor2:
            query = "select t1.name,t2.name, sel.date, sel.id from (select * from rpl.match where is_over = false) as sel join rpl.team t1 on t1.id = sel.team_home_id join rpl.team t2 on t2.id = sel.team_guest_id where t1.id in (select favourite_team_id from rpl.fan where email = %s) or t2.id in (select favourite_team_id from rpl.fan where email = %s)"
            cursor2.execute(query, (email, email))
            future_matches = cursor2.fetchall()

        with connection.cursor() as cursor3:
            query = "SELECT * from rpl.full_results_view where Idh in (select favourite_team_id from rpl.fan where email = %s) or Idg in (select favourite_team_id from rpl.fan where email = %s)"
            cursor3.execute(query, (email, email))
            results = cursor3.fetchall()

        with connection.cursor() as cursor4:
            query = "select * from rpl.team where id in (select favourite_team_id from rpl.fan where email = %s)"
            cursor4.execute(query, [email])
            team = cursor4.fetchall()

        return render(request, 'main/favourite_team.html',
                      {'future_matches': future_matches, 'results': results, 'team': team})


@login_required
def buy_tickets(request, id):
    with connection.cursor() as cursor3:
        query = "select sel.id, st.id, st.name, t1.name, t1.id, t1.city, t1.emblem_path, t2.name, t2.id, t2.city, t2.emblem_path,ref.id, ref.name, ref.surname from (select* from rpl.match where is_over = false and id = '%s') as sel join rpl.team t1 on t1.id = sel.team_home_id join rpl.team t2 on t2.id = sel.team_guest_id join rpl.referee ref on ref.id = sel.referee_id join rpl.stadium st on st.id = t1.stadium_id"
        cursor3.execute(query, [id])
        match_info = cursor3.fetchall()
    return render(request, 'main/buy_tickets.html', {'match_info': match_info})


@login_required
def get_places(request):
    sector_id = request.GET.get('sector_num')
    match_id = request.GET.get('match_id')

    places = Ticket.objects.filter(sector=sector_id, match_id=match_id)
    places_data = [{'row': currentPlace.row, 'place': currentPlace.place, 'placeId': currentPlace.id} for currentPlace
                   in places]

    return JsonResponse({'places': places_data})


def check_authentication(request):
    authenticated = request.user.is_authenticated
    return JsonResponse({'authenticated': authenticated})


def process_selected_places(request):
    if request.method == 'POST':
        # Получаем данные из запроса в формате JSON
        try:
            data = json.loads(request.body)

            print("good")

        except json.JSONDecodeError:
            print("error")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        return JsonResponse({'message': 'Data received successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)
