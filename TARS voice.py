import speech_recognition as sr
import pyttsx3
import openai
import cv2

# Initialize text-to-speech engine
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # You can change the index to try different voices
engine.setProperty('rate', 150)  # Adjust the speaking rate
engine.setProperty('volume', 1.0)  # Adjust the volume (0.0 to 1.0)

# Modify the pitch to create a robotic effect
engine.setProperty('pitch', 70)  # Lower pitch values sound more robotic

# Set up speech recognition
r = sr.Recognizer()
mic = sr.Microphone()

# OpenAI API key (replace with your own)
openai.api_key = "YOUR_API_KEY"

def listen_for_trigger_phrase():
    with mic as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
        if "Hey tars" in text:
            return True
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return False

def capture_image():
    cap = cv2.VideoCapture(0)  # Use 0 for default camera

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save the image (you can choose a specific format and path)
    cv2.imwrite('captured_image.jpg', frame)

def send_to_chatgpt(text, image_path):
    prompt = f"Here's what the user said: {text}\nHere's an image: {image_path}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )

    response_text = response.choices[0].text.strip()
    print("ChatGPT:", response_text)
    engine.say(response_text)
    engine.runAndWait()

while True:
    if listen_for_trigger_phrase():
        capture_image()
        with mic as source:
            print("Say something...")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            send_to_chatgpt(text, "captured_image.jpg")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
