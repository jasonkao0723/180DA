import random
import time
from gtts import gTTS 
import os 
import speech_recognition as sr
from pygame import mixer
import paho.mqtt.publish as publish
from avg_filter import filtered_word
from Kmean_filter import Kmean_filtered_word_use
import Kmean_filter
language = 'en'

# MQTT_SERVER = "192.168.1.19" # same mosquitto server ip. 
# MQTT_PATH = "hello/world" # same topic


def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["start", "fire""armor", "explode", "antibiotic", "surrender"]
    NUM_GUESSES = 4
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    word = random.choice(WORDS)

    while (True):

        for j in range(PROMPT_LIMIT):
            print('Please order')

            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break       
            print("I didn't catch that. What did you say?\n")
         

        # show the user the transcription
        print("Your order is: {}".format(guess["transcription"]))
        w_order = ("Your order is: {}".format(guess["transcription"]))
        w_order_obj = gTTS(text=w_order, lang=language, slow=False)
        w_order_obj.save("w_order.mp3") 
        os.system("w_order.mp3")
        time.sleep(3)

        
        print("After applying average filter: {}".format(filtered_word(guess["transcription"].lower())))
        filtered_order = ("After applying average filter: {}".format(filtered_word(guess["transcription"].lower())))
        filtered_order_obj = gTTS(text=filtered_order, lang=language, slow=False)
        filtered_order_obj.save("filtered_order.mp3") 
        os.system("filtered_order.mp3")

        time.sleep(6)
        
        print("After applying K-mean filter: {}".format(Kmean_filtered_word_use(guess["transcription"].lower())))
        filtered_order = ("After applying K-mean filter: {}".format(Kmean_filtered_word_use(guess["transcription"].lower())))
        filtered_order_obj = gTTS(text=filtered_order, lang=language, slow=False)
        filtered_order_obj.save("Kmean_filtered_word_order.mp3") 
        os.system("Kmean_filtered_word_order.mp3")

        time.sleep(6)

        # if guess["transcription"].lower() == "apple":
        #     publish.single(MQTT_PATH, "A", hostname=MQTT_SERVER)

        # if guess["transcription"].lower() == "banana":
        #     publish.single(MQTT_PATH, "B", hostname=MQTT_SERVER)
      
        # if guess["transcription"].lower() == "armor":
        #     publish.single(MQTT_PATH, "4", hostname=MQTT_SERVER)

        # if guess["transcription"].lower() == "explode":
        #     publish.single(MQTT_PATH, "5", hostname=MQTT_SERVER)
 
        # if guess["transcription"].lower() == "antibiotic":
        #     publish.single(MQTT_PATH, "6", hostname=MQTT_SERVER)

        # if guess["transcription"].lower() == "surrender":
        #     publish.single(MQTT_PATH, "7", hostname=MQTT_SERVER)



        