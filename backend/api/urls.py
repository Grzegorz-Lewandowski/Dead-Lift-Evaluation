from django.urls import path

from .views import hello_world, create_analysis, get_analysis


urlpatterns = [
    path('hello/', hello_world, name='hello_world'),

    path('analyses/', create_analysis, name='create_analysis'),
    path('analyses/<int:analysis_id>/', get_analysis, name='get_analysis'),
]