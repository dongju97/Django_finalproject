from django.shortcuts import render, redirect

# Create your views here.
def main(request):
    return render(request, "main.html")

def login(request):
    return render(request, "login.html")