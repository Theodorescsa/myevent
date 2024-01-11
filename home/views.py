from django.shortcuts import render, redirect, HttpResponse
from .models import EventModel
from .forms import EventForm, EventFormModel
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.conf import settings
from subcribe2.models import SubcribeModel
from datetime import datetime
from chatbot.models import ChatbotItemModel
# Create your views here.

def list_events(request):
    keyword = request.GET.get("keyword")
    events = EventModel.objects.all()
    today = datetime.now()
    current_time = today.time()
    current_date = today.date()
    subcribe = SubcribeModel.objects.all()
    list_event_id = []
    list_dict = []
    # chạy vòng lặp lấy id của các event đang có
    for item in events:
        list_event_id.append(item.id)

    # chạy vòng lặp đếm số lượng 
    for num_id in list_event_id:
        event_total = SubcribeModel.objects.filter(event__id=num_id,status = 1)
        
        total = event_total.count()
        if total == 0:
            event = EventModel.objects.get(id=num_id)
            event.totalpeople = total
            event.save()
        for item in event_total:
            item.event.totalpeople = total
            list_dict.append({item.event.id: item.event.totalpeople})

            # print(f"{item.event.name} đang có {item.event.totalpeople} đang tham gia")
            item.save()
    print(list_dict)
    if list_dict == []:
        for item in list_event_id:
            event = EventModel.objects.get(id=item)
            event.totalpeople = 0
            event.save()
    for item in list_dict:
        
        event_id = list(item.keys())[0]
        total_people = item[event_id]

        # Lấy sự kiện từ cơ sở dữ liệu và cập nhật tổng số người tham gia
        event = EventModel.objects.get(id=event_id)
        event.totalpeople = total_people
        event.save()
 

    # thời gian sự kiện kết thúc
    # for item in events:
    #     if item.deadlinedate == current_date and item.deadlinetime < current_time:
    #         item.is_completed = True
    #         item.save()
    # tìm kiếm 
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
    form = EventFormModel(initial={"user":user,"totalpeople":0})
    if request.method == "POST":
        form = EventFormModel(initial={"user":user,"totalpeople":0})
        
        form = EventFormModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # new_event = form.save(commit=False)
            # new_event.user = user
            # subscribe, created = SubcribeModel.objects.get_or_create(
            #     user=user,
            #     event=new_event,
            #     status=1,
            # )
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
            return redirect('home:detail',id)

    context = {
        'form':form,
    }
    return render(request,"home/edit.html",context)
@login_required(login_url=settings.LOGIN_URL)
def delete(request,id):
    model = EventModel.objects.get(id=id)
    chatbot = ChatbotItemModel.objects.all()
    for item in chatbot:
        if item.event.id == id:
       
            item.delete()
    model.delete()
    return redirect("home:list_events")

def test(request):
    model = SubcribeModel.objects.all()
    context = {
        'model':model,
    }
    return render(request,"home/test.html",context)
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
    total = events.count()
    print(total)
    context = {
        'events':events,
        'total':total
    }
    return render(request,"home/didsubcribed.html",context)
@login_required(login_url=settings.LOGIN_URL)
def unsubcribe(request, id):
    user = User.objects.get(username=request.user.username)
    event = EventModel.objects.get(id=id)
    if request.method == "POST":
        model = SubcribeModel.objects.get(
            user=user,
            event=event,   
            status = 1   
        )
        try:
            status = 0

            model.status = status
            model.save()
        except SubcribeModel.DoesNotExist:
            status = 0

            model, created = SubcribeModel.objects.get_or_create(
                user=user,
                event=event,      
                status=status
            )
  
        return redirect("home:subcribed")

