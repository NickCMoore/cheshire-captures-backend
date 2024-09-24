from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to Cheshire Captures - A Platform for Photographers!")
