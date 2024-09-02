from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('scrape/', views.scrape_data_view, name='scrape_data'),
    path('top_six_players/', views.top_six_player_view, name='top_six_players'),
]