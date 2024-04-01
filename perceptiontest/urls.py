from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_test, name='start_test'),
    path('question/', views.question_view, name='question_view'),
    path('get_question/', views.get_question, name='get_question'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    # path('test_completed/', views.test_completed, name='test_completed'),
]
