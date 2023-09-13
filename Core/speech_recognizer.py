import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="en-US")
        print("Recognized Text:", recognized_text)
        return recognized_text
    except sr.WaitTimeoutError:
        return "Timeout: No speech detected."
    except sr.UnknownValueError:
        return "Sorry, could not understand audio."
    except sr.RequestError as e:
        return f"Request error: {e}"

