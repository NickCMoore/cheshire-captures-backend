from django.urls import path
from photographers import views

urlpatterns = [
    path('photographers/', views.PhotographerList.as_view()),
    path('photographers/<int:pk>/', views.PhotographerDetail.as_view()),
    path('photographers/<int:pk>/unfollow/', PhotographerDetail.as_view({'post': 'unfollow'}), name='photographer-unfollow'),
]