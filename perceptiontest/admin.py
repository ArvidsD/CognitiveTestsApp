from django.contrib import admin
from perceptiontest.models import TestTaker, ImageObject, Question, Answer, Demographics, EducationLevel, Profession
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin


# Resource klases
class TestTakerResource(resources.ModelResource):
    answers = fields.Field()
    demographics = fields.Field()

    class Meta:
        model = TestTaker
        fields = ('id', 'takenTest', 'session_id', 'answers', 'demographics')

    def dehydrate_answers(self, test_taker):
        answers = Answer.objects.filter(test_taker=test_taker).select_related('question')
        answer_data = []
        for answer in answers:
            question = answer.question
            answer_detail = f"Question ID {question.id}, User Angle: {answer.user_angle}, Correct Angle: {answer.correct_angle}, Time Taken: {answer.time_taken}"
            answer_data.append(answer_detail)
        return ' | '.join(answer_data)

    def dehydrate_demographics(self, test_taker):
        demographics = Demographics.objects.filter(test_taker=test_taker).first()
        if demographics:
            education_levels = ', '.join([level.name for level in demographics.education_levels.all()])
            professions = ', '.join([prof.name for prof in demographics.professions.all()])
            return f"Gender: {demographics.gender}, Age: {demographics.age}, Education Levels: {education_levels}, Professions: {professions}, Native Language: {demographics.native_language}"
        return "No demographics data"


class ImageObjectResource(resources.ModelResource):
    class Meta:
        model = ImageObject
        fields = '__all__'


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerResource(resources.ModelResource):
    class Meta:
        model = Answer
        fields = '__all__'


class EducationLevelResource(resources.ModelResource):
    class Meta:
        model = EducationLevel
        fields = '__all__'


class ProfessionResource(resources.ModelResource):
    class Meta:
        model = Profession
        fields = '__all__'


class DemographicsResource(resources.ModelResource):
    class Meta:
        model = Demographics
        fields = '__all__'


# Admin klases
class TestTakerAdmin(ImportExportModelAdmin):
    resource_class = TestTakerResource


class ImageObjectAdmin(ImportExportModelAdmin):
    resource_class = ImageObjectResource


class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource


class AnswerAdmin(ImportExportModelAdmin):
    resource_class = AnswerResource


class EducationLevelAdmin(ImportExportModelAdmin):
    resource_class = EducationLevelResource


class ProfessionAdmin(ImportExportModelAdmin):
    resource_class = ProfessionResource


class DemographicsAdmin(ImportExportModelAdmin):
    resource_class = DemographicsResource


# Reģistrē modeļus admin panelī
admin.site.register(TestTaker, TestTakerAdmin)
admin.site.register(ImageObject, ImageObjectAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(EducationLevel, EducationLevelAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Demographics, DemographicsAdmin)
