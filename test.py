import openai

API_KEY = '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'
openai.api_key = API_KEY
x ='hello'
conversation = [
    # {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"{chat_history_text}\nUser:{x}\nChatbot:"}
]

chatbot = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=conversation,
    max_tokens=100
)

answer = chatbot.choices[0]['message']['content']
print(answer)
