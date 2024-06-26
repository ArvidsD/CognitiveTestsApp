from rest_framework import serializers
from .models import TestTaker, ImageObject, Question, Answer, Demographics, EducationLevel, Profession


class TestTakerSerializer(serializers.ModelSerializer):
    custom_id = serializers.CharField(max_length=252, allow_blank=True, required=False)

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


class QuestionIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'test_taker', 'time_taken', 'user_angle', 'correct_angle']


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['name']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['name']


class DemographicsSerializer(serializers.ModelSerializer):
    education_levels = EducationLevelSerializer(many=True, required=False)
    professions = ProfessionSerializer(many=True, required=False)

    class Meta:
        model = Demographics
        fields = ['test_taker', 'gender', 'age', 'native_language', 'education_levels', 'professions', 'dominant_hand',
                  'field_of_education', 'device_used']

    def create(self, validated_data):
        education_levels_data = validated_data.pop('education_levels', [])
        professions_data = validated_data.pop('professions', [])
        demographic = Demographics.objects.create(**validated_data)

        for level_data in education_levels_data:
            level, created = EducationLevel.objects.get_or_create(**level_data)
            demographic.education_levels.add(level)

        for profession_data in professions_data:
            profession, created = Profession.objects.get_or_create(**profession_data)
            demographic.professions.add(profession)

        return demographic

    def update(self, instance, validated_data):
        education_levels_data = validated_data.pop('education_levels', [])
        professions_data = validated_data.pop('professions', [])

        if education_levels_data:
            instance.education_levels.clear()
            for level_data in education_levels_data:
                level_obj, created = EducationLevel.objects.get_or_create(**level_data)
                instance.education_levels.add(level_obj)

        if professions_data:
            instance.professions.clear()
            for profession_data in professions_data:
                profession_obj, created = Profession.objects.get_or_create(**profession_data)
                instance.professions.add(profession_obj)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
