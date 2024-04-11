from rest_framework import serializers
from .models import TestTaker, ImageObject, Question, Answer

class TestTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTaker
        fields = '__all__'

class ImageObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageObject
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    object1 = ImageObjectSerializer(read_only=True)
    object2 = ImageObjectSerializer(read_only=True)
    object3 = ImageObjectSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'test_taker', 'time_taken', 'user_angle', 'correct_angle']