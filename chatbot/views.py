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

    if not question:
        question = 'Can you help me with something?'

    # Lấy lịch sử câu hỏi và câu trả lời từ cơ sở dữ liệu
    chat_history = ChatbotModel.objects.filter(user=user)
    
    chat_history_text = '\n'.join([f"Q: {item.question}\nA: {item.answer}\n" for item in chat_history])

    # Kết hợp câu hỏi mới với lịch sử chat
    prompt = f"{chat_history_text}\nUser: {question}\nChatbot:"

    chatbot = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=100
    )
    
    answer = chatbot.choices[0]['text']

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
    prompt = f"{chat_history_text}\nUser:{question}\nChatbot:"

    chat_ai = openai.Completion.create(
        model = 'text-davinci-003',     
        prompt = prompt,
        max_tokens = 1000
    )

    answer = chat_ai.choices[0]['text']
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