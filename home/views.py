from django.shortcuts import render, redirect, HttpResponse
from .models import EventModel
from .forms import EventForm, EventFormModel
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.conf import settings
from subcribe2.models import SubcribeModel
from datetime import datetime
# Create your views here.

def list_events(request):
    keyword = request.GET.get("keyword")
    events = EventModel.objects.all()
    today = datetime.now()
    current_time = today.time()
    current_date = today.date()

    for item in events:
        if item.deadlinedate == current_date and item.deadlinetime < current_time:
            print(item.name)
            item.is_completed = True
            item.save()
        print(item.deadlinedate)
    if keyword:
        events = EventModel.objects.filter(
            Q(name__icontains = keyword)
            | Q(description__icontains = keyword)
            | Q(leader__icontains = keyword)
            )
    else:
        keyword = ""
    context = {
        'keyword':keyword,
        'events':events,
    }
    return render(request,'home/list_events.html',context)
@login_required(login_url=settings.LOGIN_URL)
def detail(request, id):
    user = User.objects.get(username=request.user.username)
    event = EventModel.objects.get(id=id)
    try:
        sub = SubcribeModel.objects.get(event=event, user=user,status = 1)
    except SubcribeModel.DoesNotExist:
        # Handle the case where the subscription does not exist
        sub = None
    
    context = {
        'event': event,
        'sub': sub,
    }
    return render(request, 'home/detail.html', context)
def main(request):
    events = EventModel.objects.all()
    context = {
        'events':events,
    }
    return render(request,'home/main_page.html',context)
@login_required(login_url=settings.LOGIN_URL)
def add(request):
    user = User.objects.get(username=request.user.username)
    form = EventFormModel(initial={"user":user})
    if request.method == "POST":
        form = EventFormModel(initial={"user":user})
        
        form = EventFormModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home:list_events")
    context  = {
        'form':form
    }
    return render(request,'home/add.html',context)
@login_required(login_url=settings.LOGIN_URL)
def edit(request,id):
    model = EventModel.objects.get(id=id)
    form = EventFormModel(instance=model)
    if request.method == "POST":
        form = EventFormModel(request.POST, request.FILES,instance=model)
        if form.is_valid():
            form.save()
            return HttpResponse("Dang ki thanh cong")

    context = {
        'form':form,
    }
    return render(request,"home/edit.html",context)
@login_required(login_url=settings.LOGIN_URL)
def delete(request,id):
    model = EventModel.objects.get(id=id)
    model.delete()
    return redirect("home:list_events")

def test(request):
    return render(request,"home/test.html")
@login_required(login_url=settings.LOGIN_URL)
def subcribe2(request,id):
    user = User.objects.get(username=request.user.username)
    event = EventModel.objects.get(id=id)
    if request.method == "POST":
        model, created = SubcribeModel.objects.get_or_create(
            user=user,
            event=event,
            status=1,
            
        )
    return redirect("home:subcribed")
@login_required(login_url=settings.LOGIN_URL)
def didsubcribed(request):
    user = User.objects.get(username=request.user.username)
    events = SubcribeModel.objects.filter(
        user=user,
        status=1,
    )
    context = {
        'events':events
    }
    return render(request,"home/didsubcribed.html",context)
@login_required(login_url=settings.LOGIN_URL)
def unsubcribe(request, id):
    user = User.objects.get(username=request.user.username)
    event = EventModel.objects.get(id=id)
    if request.method == "POST":
        status = False
        model, created = SubcribeModel.objects.get_or_create(
            user=user,
            event=event,
            defaults={'status': status}
        )
        if not created:
            model.status = status
            model.save()
        return redirect("home:subcribed")

