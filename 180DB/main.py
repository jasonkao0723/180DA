import random
import time
from gtts import gTTS 
import os 
import speech_recognition as sr
import vlc
language = 'en'


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
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
    WORDS = ["start", "fire", "armor", "explode", "antibiotic", "surrender"]
    NUM_GUESSES = 4
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    word = random.choice(WORDS)

    # format the instructions string
    instructions = (
        "The battle is ready and welcome to the weapons shop:\n"
        "Our service include: {words}\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    myobj = gTTS(text=instructions, lang=language, slow=False)
    myobj.save("welcome.mp3") 
    os.system("welcome.mp3")

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(10)

    while (True):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Please order')
            time.sleep(3)
            p_order = ('Please order')
            p_order_obj = gTTS(text=p_order, lang=language, slow=False)
            p_order_obj.save("p_order.mp3") 
            os.system("p_order.mp3")

            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            not_catch = ("I didn't catch that. What did you say?\n")
            print("I didn't catch that. What did you say?\n")
            not_catch_obj = gTTS(text=not_catch, lang=language, slow=False)
            not_catch_obj.save("not_catch.mp3") 
            os.system("not_catch.mp3")

        # show the user the transcription
        print("Your order is: {}".format(guess["transcription"]))
        w_order = ("Your order is: {}".format(guess["transcription"]))
        w_order_obj = gTTS(text=w_order, lang=language, slow=False)
        w_order_obj.save("w_order.mp3") 
        os.system("w_order.mp3")
        time.sleep(3)
        if guess["transcription"].lower() == "fire":
            p = vlc.MediaPlayer("C:/Users/guoyu/Desktop/2020 winter/180 DB/speech recognization/gun_effect.mp3")
            p.play()
        if guess["transcription"].lower() == "start":
            p = vlc.MediaPlayer("C:/Users/guoyu/Desktop/2020 winter/180 DB/speech recognization/start_effect.mp3")
            p.play()
            time.sleep(3)
        if guess["transcription"].lower() == "armor":
            p = vlc.MediaPlayer("C:/Users/guoyu/Desktop/2020 winter/180 DB/speech recognization/armor_effect.mp3")
            p.play()
        if guess["transcription"].lower() == "explode":
            p = vlc.MediaPlayer("C:/Users/guoyu/Desktop/2020 winter/180 DB/speech recognization/explode_effect.mp3")
            p.play()
        if guess["transcription"].lower() == "antibiotic":
            p = vlc.MediaPlayer("C:/Users/guoyu/Desktop/2020 winter/180 DB/speech recognization/antibiotic_effect.mp3")
            p.play()
            time.sleep(3)
        if guess["transcription"].lower() == "surrender":
            p = vlc.MediaPlayer("C:/Users/guoyu/Desktop/2020 winter/180 DB/speech recognization/surrender_effect.mp3")
            p.play()


    
        