# TROUBLESHOOT: If streamlit displays comments quoted under triple quotation marks, then visit this website for some suggestions: https://github.com/streamlit/streamlit/issues/533
# First suggestion is to set a "dead" variable equal to the quoted text; 2nd suggestion provides a global solution: open or create the config.toml in the HomeDirectory/.streamlit
# Edit the config.toml with
# [runner]
# magicEnabled = false

# Run with Python 3.8
#https://docs.speechmatics.com/tutorials/using-mic
import speechmatics
from httpx import HTTPStatusError
import asyncio
import pyaudio

ccc="""
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
#import speech_recognition as sr # pip install SpeechRecognition; but import speech_recognition as sr; check if installed well: python -m speech_recognition
#from googletrans import Translator
#from gtts import gTTS # Google Text-To-Speech (gTTS)
#from playsound import playsound
from datetime import datetime
import streamlit as st
import numpy as np


API_Lang=np.loadtxt('API_n_Lang.txt')

API_Num=API_Lang[0]
Langu=API_Lang[1]

if(API_Num==1):
    API_KEY = "Fp2YIyJcpkpfp6kX6ag5a3dw9Uq2FBZl" # nosajide@yahoo.com (JesusisLord1@); 3rd February 2025
elif(API_Num==2):
    API_KEY = "hutriRTWUfp5Txr4t8KI7RbvnPH7wAVE" # bovoexclusive@gmail.com (Godisgood1@); 6th February 2025
# API_KEY = "7O9WkDz5dUugMUfebw3aZa4R1MgdC3Au" # bovoexclusive@gmail.com (Godisgood1@); 9th February 2025
elif(API_Num==3):
    API_KEY = "WV6HboE14HRlYiDKw0oFDN8mo35kd1OW" # bovoogunbo@gmail.com (Godisgood1@); 9th February 2025

if(Langu==1):
    LANGUAGE = 'en'
    DESTINATION_LANG ='ko'
else:
    LANGUAGE = 'ko'
    DESTINATION_LANG ='en'

TRANSLATION_LANGUAGES = [DESTINATION_LANG] #["ko","de"]
CONNECTION_URL = f"wss://eu2.rt.speechmatics.com/v2/{LANGUAGE}"
DEVICE_INDEX = -1
CHUNK_SIZE = 1024

output="English_"
current_date = datetime.now().strftime("%Y-%m-%d")

class AudioProcessor:
    def __init__(self):
        self.wave_data = bytearray()
        self.read_offset = 0

    async def read(self, chunk_size):
        while self.read_offset + chunk_size > len(self.wave_data):
            await asyncio.sleep(0.001)
        new_offset = self.read_offset + chunk_size
        data = self.wave_data[self.read_offset:new_offset]
        self.read_offset = new_offset
        return data

    def write_audio(self, data):
        self.wave_data.extend(data)
        return


audio_processor = AudioProcessor()
# PyAudio callback
def stream_callback(in_data, frame_count, time_info, status):
    audio_processor.write_audio(in_data)
    return in_data, pyaudio.paContinue

# Set up PyAudio
p = pyaudio.PyAudio()
if DEVICE_INDEX == -1:
    DEVICE_INDEX = p.get_default_input_device_info()['index']
    device_name = p.get_default_input_device_info()['name']
    DEF_SAMPLE_RATE = int(p.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'])
    print(f"***\nIf you want to use a different microphone, update DEVICE_INDEX at the start of the code to one of the following:")
    # Filter out duplicates that are reported on some systems
    device_seen = set()
    for i in range(p.get_device_count()):
        if p.get_device_info_by_index(i)['name'] not in device_seen:
            device_seen.add(p.get_device_info_by_index(i)['name'])
            try:
                supports_input = p.is_format_supported(DEF_SAMPLE_RATE, input_device=i, input_channels=1, input_format=pyaudio.paFloat32)
            except Exception:
                supports_input = False
            if supports_input:
                print(f"-- To use << {p.get_device_info_by_index(i)['name']} >>, set DEVICE_INDEX to {i}")
    print("***\n")

SAMPLE_RATE = int(p.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'])
device_name = p.get_device_info_by_index(DEVICE_INDEX)['name']

print(f"\nUsing << {device_name} >> which is DEVICE_INDEX {DEVICE_INDEX}")
print("Starting transcription (type Ctrl-C to stop):")

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                input_device_index=DEVICE_INDEX,
                stream_callback=stream_callback
)

# Define connection parameters
conn = speechmatics.models.ConnectionSettings(
    url=CONNECTION_URL,
    auth_token=API_KEY,
)

# Create a transcription client
ws = speechmatics.client.WebsocketClient(conn)

# Define transcription parameters
# Full list of parameters described here: https://speechmatics.github.io/speechmatics-python/models
conf = speechmatics.models.TranscriptionConfig(
    language=LANGUAGE,
    enable_partials=True,
    max_delay=5,
)




ccc="""
# Define transcription parameters (.json file or config file for control of sequential functions: transcription and translation)
conf = {
    "type": "transcription",
    "transcription_config": {
        "language": LANGUAGE
    },
    "translation_config": {
        "target_languages":TRANSLATION_LANGUAGES
    }
}
"""



st.header("SKORE AI Translator: English to Korean", divider="gray")
st.title("Jesus is LORD")
txt_file = "translation.txt"



# Define an event handler to print the partial transcript
def print_partial_transcript(msg):
    print(f"[partial] {msg['metadata']['transcript']}")

# Define an event handler to print the full transcript
def print_transcript(msg):
    print(f"[  FINAL] {msg['metadata']['transcript']}")

# Define an event handler to print the translations
def print_translation(msg):
    msg_type="Final"
    if msg['message'] == "AddPartialTranslation":
        msg_type="Partial"

    language = msg['language'] # language for translation message
    translations = []
    for translation_segment in msg['results']:
        translations.append(translation_segment['content'])

    translation = " ".join(translations).strip()
    print(f"{msg_type} translation for {language}: {translation}")
    #current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') #https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time-in-python
    #myobj  = gTTS(text=translation, lang=DESTINATION_LANG)
    #myobj.save(output + current_time + ".mp3")
    #playsound(output + current_time + ".mp3") # play it using the playsound library
    #st.write(translation)
    st.write(f"## {translation}")
    ccc="""
    # Initialize session state for download confirmation
    if "downloaded" not in st.session_state:
        st.session_state.downloaded = False

        # Download button
    if st.download_button(
        label="Download Translation",
        file_name="translation.txt",data=translation,
    ):
        st.session_state.downloaded = True

    # Show success message after download
    if st.session_state.downloaded:
        st.success("Translation file downloaded successfully!")
    """

ccc="""
# Register the event handler for partial transcript
ws.add_event_handler(
    event_name=speechmatics.models.ServerMessageType.AddPartialTranscript,
    event_handler=print_partial_transcript,
)

# Register the event handler for full transcript
ws.add_event_handler(
    event_name=speechmatics.models.ServerMessageType.AddTranscript,
    event_handler=print_transcript,
)
"""


# Register the event handler for partial transcript

ws.add_event_handler(
    event_name=speechmatics.models.ServerMessageType.AddPartialTranslation,    
    event_handler=print_translation,

)

# Register the event handler for full transcript
ws.add_event_handler(
    event_name=speechmatics.models.ServerMessageType.AddTranslation,
    event_handler=print_translation,
)


ccc="""
settings = speechmatics.models.AudioSettings()
settings.encoding = "pcm_f32le"
settings.sample_rate = SAMPLE_RATE
settings.chunk_size = CHUNK_SIZE

print("Starting transcription (type Ctrl-C to stop):")
try:
    ws.run_synchronously(audio_processor, conf, settings)
except KeyboardInterrupt:
    print("\nTranscription stopped.")
except HTTPStatusError as e:
    if e.response.status_code == 401:
        print('Invalid API key - Check your API_KEY at the top of the code!')
    else:
        raise e
"""

settings = speechmatics.models.AudioSettings()
settings.encoding = "pcm_f32le"
settings.sample_rate = SAMPLE_RATE
settings.chunk_size = CHUNK_SIZE
# Define transcription parameters with translation
# Full list of parameters described here: https://speechmatics.github.io/speechmatics-python/models

translation_config = speechmatics.models.RTTranslationConfig(
    target_languages=TRANSLATION_LANGUAGES,
    #enable_partials=True # Optional argument to provide translation of partial sentences
)

transcription_config = speechmatics.models.TranscriptionConfig(
    language=LANGUAGE,
    translation_config=translation_config
)

#print("Starting transcription (type Ctrl-C to stop):")
try:
    ws.run_synchronously(audio_processor, transcription_config, settings)
except KeyboardInterrupt:
    print("\nTranscription stopped.")
except HTTPStatusError as e:
    if e.response.status_code == 401:
        print('Invalid API key - Check your API_KEY at the top of the code!')
    else:
        raise e
