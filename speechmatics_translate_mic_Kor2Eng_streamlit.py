# Use Python 3.9.13 (Isung)
# Use Python 3.9.0 (home)
# Reference: https://shelwyncorte.medium.com/translate-speech-to-any-language-google-supported-with-python-and-google-translate-api-14673747acb7
# Reference: https://py-googletrans.readthedocs.io/en/latest/
# Reference: https://medium.com/@taja.kuzman/use-google-translate-opus-mt-and-facebook-mt-models-with-just-a-few-lines-in-python-45ada098c4e9
# Reference: https://stackoverflow.com/questions/65641455/how-do-i-give-the-time-duration-of-listening-to-python-speech-recognition-librar
# Reference (Different microphone; recognize_sphinx() works offline with the CMU Sphinx engine): https://realpython.com/python-speech-recognition/
# Reference: https://github.com/Uberi/speech_recognition/blob/master/examples/write_audio.py

"""
Installation (Linux):
— pip install SpeechRecognition
— pip install googletrans
— pip install gTTS
— pip install playsound

Installation (Windows):
— pip install SpeechRecognition
— pip install gTTS
— pip install pipwin
— pipwin install pyaudio
— pip install playsound==1.2.2
— pip install googletrans==4.0.0-rc1
"""
import speech_recognition as sr # pip install SpeechRecognition; but import speech_recognition as sr; check if installed well: python -m speech_recognition
from googletrans import Translator
from gtts import gTTS # Google Text-To-Speech (gTTS)
from playsound import playsound
from datetime import datetime
import asyncio

async def translate_text(msg,srcs,dests): # https://pypi.org/project/googletrans/
     async with Translator() as translator:
          result = await translator.translate(msg,src=srcs,dest=dests)
          #print(result)
          return result
     
from_lang = "en"
to_lang = 'ko'

cc=0
while True:
    cc=cc+1
    r =sr.Recognizer()
    with sr.Microphone() as source:
        #print("Speak Now:")
        r.adjust_for_ambient_noise(source) # to auto adjust to the environment.
        audio_data = r.listen(source)
        #print("RECOGNIZING your sound now ...")
        # AND YOU CAN USE CUSTOM LANGUAGE CODE          
        try:        
            transcript = r.recognize_google(audio_data)
            translations = asyncio.run(translate_text(transcript,from_lang,to_lang))
                
            print(translations.origin)
            #print(translations2.origin)

            print(translations.text)

            """
            # AND SHOW THE RESULT TO TEXT WIDGET IN FLET APP
            #output.value = transcript
            #newText1=ft.Text(f"{transcript}")
            #newText=ft.Text(f"{translations.text}")

            newText1=Text(f"{transcript}")
            newText=Text(f"{translations.text}")

            input.controls.append(newText1)
            output.controls.append(newText)
            page.update()
            #print(transcript)
            time.sleep(1)  # Simulate work being done, adjust as needed
            if(cc % 10==0):
                input.controls.clear()
                output.controls.clear()
                page.update()
                #page.clean() #ft.Column() # Jide added this
                #page.add(ft.Text("Cleared Screen."),output)
            """
        except Exception as e:
            print(e)
