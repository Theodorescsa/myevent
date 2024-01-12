from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.
def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    next = request.GET.get("next")
    is_auth = authenticate(request,username=username,password=password)
    if request.method == "POST":
        login(request,is_auth)
        if next:
            return redirect(next)
        return redirect("home:main")

    context = {
        
    }
    return render(request,'signin/signin.html',context)
