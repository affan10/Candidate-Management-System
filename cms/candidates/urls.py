from django.urls import path, include

from . import views

app_name = 'candidates'

urlpatterns = [
    path('', views.candidates_list_view, name='candidate-list-view'),
    path('create/', views.candidate_create_view, name='candidate-create-view'),
    path('search/', views.search_view, name='search-results'),
    path('<int:candId>/', views.candidate_detail_view, name='candidate-detail-view'),
    path('update/<int:candId>/', views.candidate_update_view, name='candidate-update-view'),
    path('delete/<int:candId>/', views.candidate_delete_view, name='candidate-delete-view'),
    path('download/<int:candId>/', views.resume_download_view, name='resume-download-view'),
]
