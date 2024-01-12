from django.shortcuts import render

# Create your views here.

def sociallogin(request):
    return render(request,'loginapp/sociallogin.html')