from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def calculate():
    x = 1
    y = 2
    c = x + y
    return c

def say_hello(request):
    x = calculate()
    return render(request,'hello.html', {'name' :'Subhi'})

