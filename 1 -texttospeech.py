from gtts import gTTS
import os
import pygame
import time

# Function for Text-to-Speech Conversiona and Playback

def generate_tts_response():
    # Ask the user to input the text that they want to convert to sppech
    text = input("Enter the text you want to convert to speech:")

    # Convert the input text to speech using gTTS
    tts = gTTS(text=text, lang='en', slow=False)

    # Save the speech to an audio file. we are saving it temporarily in 'output.mp3'

    audio_file = 'output.mp3'
    tts.save(audio_file)

    # Initialize the pyame mixer to handle audio playback

    pygame.mixer.init()

    #Load the generated audio file into the pygame mixer

    pygame.mixer.music.load(audio_file)

    # Play the audio file

    pygame.mixer.music.play()

    #Wait for the audio to finsh playing before moving on

    while pygame.mixer.music.get_busy():
        time.sleep(1) # Pauses the program for 1 sec to allow the audio to continue playing.

    # Stop the mixer and unload the file

    pygame.mixer.music.stop()

    pygame.mixer.quit()
   
    # After the playback, we want to remove the audio file to clean up

    os.remove(audio_file)

    # Return the success message

    return "Audio played successfully"

# Call the function and display the return message

message = generate_tts_response()
    
print(message) #This will print "Audio Played successfully"




































    
