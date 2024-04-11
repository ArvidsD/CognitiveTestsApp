from django.db import models
import numpy as np
class TestTaker(models.Model):
    first_name = models.CharField(max_length=32)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    takenTest = models.CharField(max_length=32)

    def __str__(self):
        return self.email

class ImageObject(models.Model):
    name = models.CharField(max_length=32)
    image_url = models.CharField(max_length=250)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()

    def __str__(self):
        return self.name

class Question(models.Model):
    object1 = models.ForeignKey(ImageObject, related_name='question_object1', on_delete=models.CASCADE)
    object2 = models.ForeignKey(ImageObject, related_name='question_object2', on_delete=models.CASCADE)
    object3 = models.ForeignKey(ImageObject, related_name='question_object3', on_delete=models.CASCADE)
    correct_angle = models.IntegerField(blank=True, null=True)

    def calculate_correct_angle(self):
        # Pieņemam, ka ImageObject modelim ir x_coordinate un y_coordinate lauki
        b = np.array([self.object1.x_coordinate, self.object1.y_coordinate])
        a = np.array([self.object2.x_coordinate, self.object2.y_coordinate])
        c = np.array([self.object3.x_coordinate, self.object3.y_coordinate])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)

    def save(self, *args, **kwargs):
        # Automātiski aprēķināt correct_angle pirms saglabāšanas
        self.correct_angle = self.calculate_correct_angle()
        super(Question, self).save(*args, **kwargs)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test_taker = models.ForeignKey(TestTaker, on_delete=models.CASCADE)
    time_taken = models.DurationField()
    user_angle = models.IntegerField()
    correct_angle = models.IntegerField()


