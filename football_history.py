import gradio as gr
import openai, subprocess
import json

with open("key.json") as file:
  data  = json.load(file)
  openai.api_key = data['key']


messages = [{"role": "system", 
             "content": 'You are an expert about football history who has a deep knowledge about the games played in the past.You can even speak up stats from the past expertly.'}]

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    #subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe,title="FOOTBALL HISTORY EXPERT",description= "I AM A FOOTBALL EXPERT, ASK ME ANYTHING!", inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch(share=True)
_, _, public = ui.launch(share=True)
print(public)