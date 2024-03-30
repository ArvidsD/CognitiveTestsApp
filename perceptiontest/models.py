from django.db import models

# Create your models here.
class TestTaker(models.Model):
    first_name = models.CharField(max_length=32)
    age = models.IntegerField()
    email = models.EmailField()
    takenTest = models.CharField(max_length=32)

    def __str__(self):
        return self.email
