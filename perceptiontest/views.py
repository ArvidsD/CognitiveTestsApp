from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Question, TestTaker, ImageObject, Demographics
from rest_framework import generics, status
from .serializers import TestTakerSerializer, ImageObjectSerializer, QuestionSerializer, AnswerSerializer, \
    DemographicsSerializer, QuestionIDSerializer
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
        return Response({"message": "finished"})


class SubmitAnswerView(APIView):
    def post(self, request, format=None):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmitDemographicView(APIView):
    def post(self, request, format=None):
        test_taker_id = request.data.get('test_taker')

        # Izmantojiet 'select_for_update' lai bloķētu rindu, kamēr transakcija notiek
        with transaction.atomic():
            test_taker, _ = TestTaker.objects.select_for_update().get_or_create(id=test_taker_id)
            demographic, created = Demographics.objects.select_for_update().get_or_create(test_taker=test_taker)

            # Ja ieraksts jau eksistēja un nav jaunu datu, atgriežam esošo ierakstu
            if not created and not request.data:
                return Response(DemographicsSerializer(demographic).data)

            if created or request.data:
                serializer = DemographicsSerializer(demographic, data=request.data or None)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
                    return Response(serializer.data, status=status_code)

            # Ja dati nav derīgi un ieraksts tika tikko izveidots, izdzēsiet to
            if created:
                demographic.delete()
                raise ValidationError(serializer.errors)

    def put(self, request, test_taker_id, format=None):
        try:
            demographic = Demographics.objects.get(test_taker=test_taker_id)
        except Demographics.DoesNotExist:
            # Ja neeksistē, varat izveidot jaunu ierakstu, nevis atgriezt kļūdu
            demographic = Demographics(test_taker_id=test_taker_id)
            # Vai atgriezt kļūdu, ja jūsu biznesa loģika to pieprasa
            # return Response({'message': 'Demographic data not found'}, status=status.HTTP_404_NOT_FOUND)

        # Pievienojam `test_taker_id` datus pieprasījuma bodijā, ja tas jau nav iekļauts
        request.data['test_taker'] = test_taker_id

        serializer = DemographicsSerializer(demographic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionIDList(generics.ListAPIView):
    queryset = Question.objects.all().order_by('?')  # Sakārto nejaušā secībā
    serializer_class = QuestionIDSerializer


class SpecificQuestionView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'
