from django.contrib import admin
from perceptiontest.models import TestTaker
from perceptiontest.models import ImageObject
from perceptiontest.models import Question
from perceptiontest.models import Answer
# Register your models here.

admin.site.register(TestTaker)
admin.site.register(ImageObject)
admin.site.register(Question)
admin.site.register(Answer)

