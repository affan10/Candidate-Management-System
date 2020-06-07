from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    path('', views.CandidateAPIView.as_view(), name='candidates-list-and-post-apiurl'),
    path('<int:id>/', views.CandidateAPIView.as_view(), name='get-apiurl'),
    path('<int:id>/update/', views.CandidateAPIView.as_view(), name='update-apiurl'),
    path('<int:id>/delete/', views.CandidateAPIView.as_view(), name='delete-apiurl'),
    #path('list/', views.CandidatePaginationView.as_view(), name='pagination-url'),
]