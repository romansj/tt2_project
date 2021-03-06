from django.urls import path

from . import views
from .views import signup_view, activation_sent_view, activate, ProfileView, report_issue

app_name = 'users'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('signup/', signup_view, name="signup"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-view'),
    path('profile/<int:pkkk>/promote/', views.user_promotion, name='user_promotion'),
    path('profile/<int:pkkk>/demote/', views.user_demotion, name='user_demotion'),
    path('report-issue/', report_issue, name='report-issue'),
    path('profile/<int:pk>/report/', views.report_profile, name='report_profile'),
    # from django tutorial
    # ex: /users/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /users/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /users/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
