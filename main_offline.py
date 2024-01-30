# 08/11/2023 - Virtual assistant (Offline Using VOSK)

# https://www.youtube.com/watch?v=3Mga7_8bYpw

import speech_recognition as sr
import llama_index_interface as llama
import pyttsx3

pre_prompt = "You are a helpful virtual assistant. You must answer to any question."
recogniser = sr.Recognizer()

model = llama.Interface(pre_prompt=pre_prompt, verbose=False, temperature=0.9)

# Prompt user to say something
print("Say something...")
said_something = True

while True:
    try:
        # Capture Microphone Audio
        with sr.Microphone() as mic:
            recogniser.adjust_for_ambient_noise(mic, duration=0.2)  # Adjust for ambient noise

            if said_something:
                print("You:", end=" ")

            audio = recogniser.listen(mic)

            # speech to text
            recognised_text = recogniser.recognize_google(audio)
            print(recognised_text)

        if recognised_text is not None:
            # Process text using LLM
            response = model.chat(recognised_text)

            # Print output to terminal:
            print("AI:", response)

            # Initialise pyttsx3 lib
            r = pyttsx3.init()

            # Text to speech
            r.say(response)

            # Wait for the speech to finish before closing the engine
            r.runAndWait()

            said_something = True

    except KeyboardInterrupt:
        print("\n---------------------\nUser Ended Program.")
        exit(0)
    except sr.exceptions.UnknownValueError:  # Nothing said / Unable to understand
        said_something = False
    except sr.exceptions.RequestError as e:
        print(f"Error with the Speech Recognition request: {e}")
    except ValueError:
        llama.quit()
