import TTS
from TTS.api import TTS
import soundfile as sf
import tkinter as tk
import winsound

# List available 🐸TTS models and choose the first one
model_name = TTS.list_models()[0]

# Init TTS
tts = TTS(model_name)

# Define a function to handle button click event
def play_audio():
    tts.tts_to_file(text="Hey George, how was your party yesterday?", speaker=tts.speakers[0],
                    language=tts.languages[0], file_path="output.wav")
    file_path = "output.wav"
    winsound.PlaySound(file_path, winsound.SND_FILENAME)

# Create a Tkinter window
window = tk.Tk()

# Create a button
play_button = tk.Button(window, text="Play Audio", command=play_audio)
play_button.pack()

# Start the Tkinter event loop
window.mainloop()
