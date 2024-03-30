from django.shortcuts import render
from django.http import HttpResponse

import perceptiontest.models


# Create your views here.

def perceptiontest_form(request):
    print(request.method)
    if request.method == 'POST':
        TestTaker_name = request.POST.get('name')
        TestTaker_age = request.POST.get('age')
        TestTaker_email = request.POST.get('email')
        TestTaker_test = "perspective test"

        TestTaker = perceptiontest.models.TestTaker(first_name=TestTaker_name , age=TestTaker_age, email=TestTaker_email,
                                                    takenTest=TestTaker_test)
        TestTaker.save()

    return render(request, 'perceptiontest/perceptiontest_form.html')
