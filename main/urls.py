from django.urls import path
from . import views
urlpatterns = [
   path('', views.index, name='home'),
   path('main', views.index, name='main'),
   path('next', views.next, name='next'),
   path('team/<int:team_id>/', views.team_detail, name='team_detail'),
   path('footballer/<int:foot_id>/', views.footballer_detail, name='footballer_detail'),
   path('show_team_players/<int:current_team_id>/', views.show_team_players, name='show_team_players'),
   path('show_stadium/<int:stadium_id>/', views.show_stadium, name='show_stadium'),
   path('match/<int:match_id>/', views.match, name='match'),
   path('referee_detail/<int:referee_id>/', views.referee_detail, name='referee_detail'),
   path('results', views.results, name='results'),
   path('timetable', views.timetable, name='timetable'),
   path('table', views.table, name='table'),
   path('bombardirs', views.bombardirs, name='bombardirs'),
   path('stadiums', views.stadiums, name='stadiums'),
   path('referee', views.referee_all, name='referee')
]