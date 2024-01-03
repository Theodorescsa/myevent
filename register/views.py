from django.shortcuts import render, HttpResponse
from .forms import RegisterForm
# Create your views here.
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Dang ki thanh cong")
    context = {
        'form':form
    }
    return render(request,"register/register.html",context)