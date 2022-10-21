from django.shortcuts import render, redirect

# Create your views here.
def main(request):
    return render(request, "main.html")


def login(request):
    return render(request, "login.html")


def graph(request):
    return render(request, "graph.html")


def feed(request):
    return render(request, "feed.html")


def point(request):
    return render(request, "point.html")


def write(request):
    return render(request, "write.html")
    