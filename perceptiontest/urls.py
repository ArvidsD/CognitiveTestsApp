from django.urls import path
from . import views

urlpatterns = [
    path("testtaker/", views.TestTakerList.as_view(), name="testtaker"),
    path('imageobjects/', views.ImageObjectList.as_view(), name='imageobject'),
    path('question/', views.QuestionList.as_view(), name='questionlist'),
    path('next_question/', views.NextQuestionView.as_view(), name='next_question'),
    path('next_question/<int:last_answered_question_id>/', views.NextQuestionView.as_view(),
         name='next_question_with_id'),
    path('submit_answer/', views.SubmitAnswerView.as_view(), name='submit_answer'),
    path('submitdemographic/', views.SubmitDemographicView.as_view(), name='submitdemographic'),
    path('submitdemographic/<int:test_taker_id>/', views.SubmitDemographicView.as_view(), name='update_demographic'),


]
