from django.shortcuts import render
from django.contrib.auth.models import User
from .models import ChatbotModel,ChatbotItemModel
from home.models import EventModel
import openai
# Create your views here.
from django.shortcuts import render
from .models import User, EventModel, ChatbotModel
import openai

def chatbot(request):
    API_KEY = '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'
    openai.api_key = API_KEY
    user = User.objects.get(username=request.user.username)
    events = EventModel.objects.all()
    question = request.POST.get('question', '')
    list_events = []
    if not question:
        question = 'Can you help me with something?'

    chat_history = ChatbotModel.objects.filter(user=user)
    
    chat_history_text = '\n'.join([f"Q: {item.question}\nA: {item.answer}\n" for item in chat_history])
    for item in events:
        list_events.append(item.leader)
        list_events.append(item.name)
        list_events.append(item.description)
        list_events.append(item.date)
        list_events.append(item.time)
        list_events.append(item.totalpeople)
        list_events.append(item.deadlinedate)
        list_events.append(item.deadlinetime)
        list_events.append(item.address)
        list_events.append(item.topic)
        list_events.append(item.is_completed)
    list_events_converted = [str(x) if x is not None else '' for x in list_events]
        
        
        
    conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"List events:{list_events_converted}\n{chat_history_text}\nUser:{question}\nChatbot:"}
    ]

    chatbot = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation,
        max_tokens=100
    )
    answer = chatbot.choices[0]['message']['content']


    # Lưu trữ câu hỏi mới và câu trả lời vào cơ sở dữ liệu
    output, created = ChatbotModel.objects.get_or_create(
        user=user,
        question=question,
        answer=answer
    )

    chatbot_list = ChatbotModel.objects.filter(user=user)
    chat_history_text = '\n'.join([f"Q: {item.question}\nA: {item.answer}\n" for item in chat_history])
    context = {
        'output': chatbot_list,
        'answer': answer
    }


    return render(request, 'chatbot/chatbot.html', context)


def chatbotitem(request,id):
    API_KEY = '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'
    user = User.objects.get(username=request.user.username)
    event = EventModel.objects.get(id=id)
    date = str(event.date)
    time = str(event.time)
    deadlinedate = str(event.deadlinedate)
    deadlinetime = str(event.deadlinetime)
    list_content = [f"Tên người dùng:{request.user.username}\n",f"Tên sự kiện:{event.name}\n",f"Mô tả:{event.description}\n",f"Thời gian bắt đầu:{date},{time}\n",f"Thời gian kết thúc:{deadlinedate},{deadlinetime}\n",f"Địa chỉ:{event.address}\n",f"Chủ đề:{event.topic}\n",f"Người chủ trì:{event.leader}\n",f"Số lượng người tham gia:{event.totalpeople}\n"]
    list_content = [str(x) if x is not None else '' for x in list_content]
    order = "-".join(list_content)
    openai.api_key = API_KEY
    question = order
    
    if request.method == "POST":    
        question = request.POST.get('question')
    chatbot_list = ChatbotItemModel.objects.filter(
        user=user,
        event=event
    )
    chat_history_text = "/n".join([f"Q:{item.question}\nA:{item.answer}" for item in chatbot_list])
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{chat_history_text}\nUser:{question}\nChatbot:"}
    ]

    chat_ai = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation,
        max_tokens=100
    )
    answer = chat_ai.choices[0]['message']['content']
    model, created = ChatbotItemModel.objects.get_or_create(
        order = order,
        user=user,
        event = event,
        question = question,
        answer = answer
    )
    chatbot_list = ChatbotItemModel.objects.filter(
        user=user,
        event=event
    )
    chat_history_text = "/n".join([f"Q:{item.question}\nA:{item.answer}" for item in chatbot_list])
    
    context = {
        'chatbot_list':chatbot_list,
    }
    
    return render(request,'chatbot/chatbotitem.html',context)