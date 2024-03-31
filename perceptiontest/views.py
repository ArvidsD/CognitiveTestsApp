from django.shortcuts import render
from django.http import HttpResponse
import json
import perceptiontest.models


# Create your views here.

def perceptiontest_form(request):
    print(request.method)
    if request.method == 'POST':
        TestTaker_name = request.POST.get('name')
        TestTaker_age = request.POST.get('age')
        TestTaker_email = request.POST.get('email')
        TestTaker_test = "perspective test"

        TestTaker = perceptiontest.models.TestTaker(first_name=TestTaker_name, age=TestTaker_age, email=TestTaker_email,
                                                    takenTest=TestTaker_test)
        TestTaker.save()

    return render(request, 'perceptiontest/perceptiontest_form.html')


def image_canvas(request):
    images = list(perceptiontest.models.ImageObject.objects.values('name', 'image_url', 'x_coordinate', 'y_coordinate'))
    # Pārvērst Python sarakstu uz JSON
    images_json = json.dumps(images)

    return render(request, 'perceptiontest/perceptiontest_image.html', {'images_json': images_json})
