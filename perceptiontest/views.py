import json
from tkinter import Image

from django.shortcuts import render, redirect
from django import forms
from django.http import JsonResponse

import perceptiontest
from .models import Question, TestTaker, Answer, ImageObject
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from .serializers import TestTakerSerializer, ImageObjectSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
class TestTakerList(generics.ListCreateAPIView):
    queryset = TestTaker.objects.all()
    serializer_class = TestTakerSerializer


class ImageObjectList(generics.ListAPIView):
    queryset = ImageObject.objects.all()
    serializer_class = ImageObjectSerializer

class QuestionList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class NextQuestionView(APIView):
    def get(self, request, last_answered_question_id=None):
        if last_answered_question_id is not None:
            next_question = Question.objects.filter(id__gt=last_answered_question_id).order_by('id').first()
        else:
            next_question = Question.objects.all().order_by('id').first()

        if next_question:
            serializer = QuestionSerializer(next_question)
            return Response(serializer.data)
        return Response({"message": "No more questions available."})


class SubmitAnswerView(APIView):
    def post(self, request, format=None):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Create your views here.
# def image_canvas(request):
#     images = list(perceptiontest.models.ImageObject.objects.values('name', 'image_url', 'x_coordinate', 'y_coordinate'))
#     # Pārvērst Python sarakstu uz JSON
#     images_json = json.dumps(images)
#
#     return render(request, 'perceptiontest/perceptiontest_image.html', {'images_json': images_json})
#
# class TestTakerForm(forms.ModelForm):
#     class Meta:
#         model = TestTaker
#         fields = ['first_name', 'age', 'email']
#
#
# # Sākuma skata funkcija
# def start_test(request):
#     if request.method == 'POST':
#         form = TestTakerForm(request.POST)
#         if form.is_valid():
#             test_taker = form.save()
#             # Saglabājiet test_taker ID sesijā, lai to varētu izmantot nākamajos soļos
#             request.session['test_taker_id'] = test_taker.id
#             # Novirziet lietotāju uz nākamo skatu, kur tiks rādīts pirmais jautājums
#             return redirect(
#                 'question_view')  # Pārliecinieties, ka šis URL nosaukums atbilst jūsu urls.py konfigurācijai
#     else:
#         form = TestTakerForm()
#     return render(request, 'perceptiontest/perceptiontest_form.html', {'form': form})
#
#
# def question_view(request):
#     images = list(perceptiontest.models.ImageObject.objects.values('name', 'image_url', 'x_coordinate', 'y_coordinate'))
#     # Pārvērst Python sarakstu uz JSON
#     images_json = json.dumps(images)
#     # Šis skats tiks izsaukts pēc TestTaker formas iesniegšanas
#     return render(request, 'perceptiontest/perceptiontest_question.html', {'images_json': images_json})
#
#
# def get_question(request):
#     test_taker_id = request.session.get('test_taker_id')
#     if not test_taker_id:
#         return JsonResponse({'error': 'Test taker not identified'}, status=400)
#
#     # Pārbauda, kuri jautājumi ir jau atbildēti
#     answered_questions = TestTakerQuestion.objects.filter(
#         test_taker_id=test_taker_id,
#         answered=True
#     ).values_list('question_id', flat=True)
#
#     # Atrod nākamo neatzīmēto jautājumu
#     next_question = Question.objects.exclude(id__in=answered_questions).first()
#
#     if next_question:
#         # Sagatavo un atgriež jautājumu JSON formātā
#         data = {
#             'question_id': next_question.id,
#             'question_text': f'Iedomājies, ka esi {next_question.object1.name}, un tu skaties uz {next_question.object2.name}. Kādā leņķī atrodas {next_question.object3.name}?',
#             'image_urls': {
#                 'object1': next_question.object1.image_url,
#                 'object2': next_question.object2.image_url,
#                 'object3': next_question.object3.image_url,
#             }
#         }
#         return JsonResponse(data)
#     else:
#         # Ja vairs nav jautājumu
#         return JsonResponse({'message': 'No more questions'})
#
#
# @csrf_exempt
# def submit_answer(request):
#     if request.method == "POST":
#         test_taker_id = request.session.get('test_taker_id')
#         question_id = request.POST.get('question_id')
#         user_angle = request.POST.get('user_angle')
#
#         if not all([test_taker_id, question_id, user_angle]):
#             return JsonResponse({'error': 'Missing data'}, status=400)
#
#         # Saglabā lietotāja atbildi
#         Answer.objects.create(
#             question_id=question_id,
#             test_taker_id=test_taker_id,
#             user_angle=user_angle,
#             correct_angle=0  # Šeit varat aprēķināt vai iestatīt pareizo leņķi pēc vajadzības
#         )
#
#         # Atzīmēt jautājumu kā atbildētu
#         TestTakerQuestion.objects.create(
#             test_taker_id=test_taker_id,
#             question_id=question_id,
#             answered=True
#         )
#
#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=405)
