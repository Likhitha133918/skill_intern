

import datetime

print("🤖 ChatBot: Hello! I am your chatbot.")
print("Type 'bye' to exit.\n")

while True:
    user_input = input("You: ").strip().lower()


    if user_input == "bye":
        print(" ChatBot: Goodbye! 👋")
        break

    
    elif "hi" in user_input or "hello" in user_input or "hey" in user_input:
        print(" ChatBot: Hello! How can I help you?")

    # Asking chatbot name
    elif "your name" in user_input:
        print(" ChatBot: I am a Python rule-based chatbot.")

    # Asking how are you
    elif "how are you" in user_input:
        print(" ChatBot: I am just code, but I'm working perfectly! 😄")

    # Time
    elif "time" in user_input:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(" ChatBot: Current time is", current_time)

    # Date
    elif "date" in user_input:
        today = datetime.date.today()
        print(" ChatBot: Today's date is", today)

    # Help
    elif "help" in user_input:
        print(" ChatBot: Try saying hello, ask my name, ask time/date, or say bye.")

    else:
        print(" ChatBot: I didn't understand that. Type 'help' to see options.")