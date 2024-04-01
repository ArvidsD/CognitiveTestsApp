from rest_framework import serializers
from .models import TestTaker

class TestTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTaker
        fields = '__all__'

