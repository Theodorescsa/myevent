from django.shortcuts import render
from django.contrib.auth.models import User
from .models import ChatbotModel,ChatbotItemModel
from home.models import EventModel
import openai
# Create your views here.
def chatbot(request):
    API_KEY = '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'
    openai.api_key = API_KEY
    user = User.objects.get(username = request.user.username)
    events = EventModel.objects.all()
    question = request.POST.get('question')
    if not question:
        question='Can you help me somethings? '
    chatbot = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = question,
        max_tokens = 100
    )
    answer = chatbot.choices[0]['text']
    output, created = ChatbotModel.objects.get_or_create(
        user=user,
        question=question,
        answer=answer
    )
    chatbot_list = ChatbotModel.objects.filter(user=user)
    context = {
        'output':chatbot_list,
        'answer':answer
    }
    return render(request,'chatbot/chatbot.html',context)

def chatbotitem(request,id):
    API_KEY = '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'
    user = User.objects.get(username=request.user.username)
    event = EventModel.objects.get(id=id)
    date = str(event.date)
    time = str(event.time)
    deadlinedate = str(event.deadlinedate)
    deadlinetime = str(event.deadlinetime)
    list_content = [request.user.username,event.name,event.description,date,time,deadlinedate,deadlinetime,event.address,event.topic,event.leader]
    list_content = [str(x) if x is not None else '' for x in list_content]
    question = "-".join(list_content)
    openai.api_key = API_KEY
    chat_ai = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = question,
        max_tokens = 100
    )
    answer = chat_ai.choices[0]['text']
    model, created = ChatbotItemModel.objects.get_or_create(
        user=user,
        event = event,
        question = question,
        answer = answer
    )
    chatbot_list = ChatbotItemModel.objects.filter(
        user=user,
        event=event
    )
    context = {
        'chatbot_list':chatbot_list,
    }
    return render(request,'chatbot/chatbotitem.html',context)