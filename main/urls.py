from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
   path('referee', views.referee_all, name='referee'),
   path('login/', auth_views.LoginView.as_view(), name='login'),
   path('my_template/', views.my_template_view, name='my_template'),
   path('add_match/', views.add_match, name='add_match'),
   path('add_footballer/', views.add_footballer, name='add_footballer'),
   path('add_goal/', views.add_goal, name='add_goal'),
   path('change_footballer/<int:pk>', views.UpdateFootballer.as_view(), name='change_footballer'),
   path('change_goal/<int:pk>', views.UpdateGoal.as_view(), name='change_goal'),
   path('change_match/<int:pk>', views.UpdateMatch.as_view(), name="change_match"),
   path('delete_footballer/<int:pk>', views.DeleteFootballer.as_view(), name='delete_footballer'),
   path('delete_goal/<int:pk>', views.DeleteGoal.as_view(), name='delete_goal'),
   path('delete_match/<int:pk>', views.DeleteMatch.as_view(), name="delete_match"),
   path('list_match/', views.change_match, name='list_match'),
   path('list_goal/', views.change_goal, name='list_goal'),
   path('list_footballer/', views.change_footballer, name='list_footballer')

]
