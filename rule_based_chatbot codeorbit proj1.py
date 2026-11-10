"""
Rule-Based Chatbot
==================
A simple chatbot that chooses its reply by matching patterns
in the user's message. ML is not used. Every response comes from
a rule that a human wrote.

Run this using :   python rule_based_chatbot.py
Run tests:     python rule_based_chatbot.py --test
"""

import random
import re
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# 1. HELPER REPLY FUNCTIONS

def reply_with_name(match):
    """Uses word like 'my name is <name>'."""
    name = match.group(1).title()
    return f"Nice to meet you, {name}!"


def reply_with_time(_match):
    """Returns the current time."""
    return f"It's currently {datetime.now().strftime('%I:%M %p')}."


def reply_with_date(_match):
    """Returns today's date."""
    return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."


# ---------------------------------------------------------------------------
# 2. RULES

RULES = [
    {
        "name": "goodbye",
        "patterns": [r"\b(bye|goodbye|see you|exit|quit)\b"],
        "responses": [
            "Goodbye! Have a great day.",
            "See you later!",
            "Bye! Come back anytime.",
        ],
    },
    {
        "name": "introduce_user",
        # "my name is"  the bot can use it.
        "patterns": [r"\bmy name is (\w+)"],
        "responses": [reply_with_name],
    },
    {
        "name": "bot_identity",
        "patterns": [r"\b(your name|who are you|what are you)\b"],
        "responses": [
            "I'm SimpleBot, a rule-based chatbot built for this intern project.",
        ],
    },
    {
        "name": "thanks",
        "patterns": [r"\b(thanks|thank you|thx|cheers)\b"],
        "responses": [
            "You're welcome!",
            "Glad I could help.",
            "Anytime!",
        ],
    },
    {
        "name": "time",
        "patterns": [r"\b(time|clock)\b"],
        "responses": [reply_with_time],
    },
    {
        "name": "date",
        "patterns": [r"\b(date|what day|today)\b"],
        "responses": [reply_with_date],
    },
    {
        "name": "help",
        "patterns": [r"\b(help|what can you do|options|commands)\b"],
        "responses": [
            "I can chat with you about: greetings, my name, the time, the date, "
            "jokes, and how I'm doing. Say 'bye' to exit.",
        ],
    },
    {
        "name": "joke",
        "patterns": [r"\bjoke\b", r"\bmake me laugh\b"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why did the function break up with the variable? It felt unappreciated.",
            "There are 10 kinds of people: those who understand binary and those who don't.",
        ],
    },
    {
        "name": "how_are_you",
        "patterns": [r"\bhow are you\b", r"\bhow's it going\b", r"\bwhat's up\b"],
        "responses": [
            "I'm just a bunch of if-statements, but I'm doing great. How about you?",
            "All systems running smoothly. How are you?",
        ],
    },
    {
        "name": "greeting",
        "patterns": [r"\b(hello|hi|hey|howdy|good (morning|afternoon|evening))\b"],
        "responses": [
            "Hello! How can I help you today?",
            "Hi there! What's on your mind?",
            "Hey! Nice to see you.",
        ],
    },
]

# Used when no rule matches user input.
FALLBACK_RESPONSES = [
    "Sorry, I didn't understand that. Type 'help' to see what I can do.",
    "Hmm, I'm not sure about that one. Try asking something else, or type 'help'.",
]


# ---------------------------------------------------------------------------
# 3. CORE LOGIC

def normalize(text):
    """
    Prepares the user's text for matching:
      - converts to lowercase
      - replaces punctuation with spaces (keeps apostrophes so "what's" works)
      - collapses extra spaces
    """
    text = text.lower()
    text = re.sub(r"[^\w\s']", " ", text)
    return " ".join(text.split())


def get_reply(user_input):
    """
    Returns a tuple: (rule_name, reply_text).
    rule_name is "fallback" when no rule matched.
    """
    text = normalize(user_input)

    # Check rules in order. The first pattern that matches wins.
    for rule in RULES:
        for pattern in rule["patterns"]:
            match = re.search(pattern, text)
            if match:
                response = random.choice(rule["responses"])
                # If the response is a function, call it with the match object.
                if callable(response):
                    return rule["name"], response(match)
                return rule["name"], response

    # No rule matched, so use the fallback.
    return "fallback", random.choice(FALLBACK_RESPONSES)


# ---------------------------------------------------------------------------
# 4. CHAT LOOP

def chat():
    """Runs the interactive chat loop until the user says goodbye."""
    print("SimpleBot: Hi! I'm SimpleBot. Type 'help' to see what I can do.")

    while True:
        user_input = input("You: ").strip()

        # Ignore empty lines instead of sending them to the rules.
        if not user_input:
            print("SimpleBot: Please type something.")
            continue

        rule_name, reply = get_reply(user_input)
        print(f"SimpleBot: {reply}")

        # Stop the loop when the goodbye rule fires.
        if rule_name == "goodbye":
            break


# ---------------------------------------------------------------------------
# 5. SIMPLE TESTS
# Run with: python rule_based_chatbot.py --test
# These check that each rule fires for the input it is meant to handle.

def run_tests():
    test_cases = [
        ("Hello!", "greeting"),
        ("hi there", "greeting"),
        ("Good morning", "greeting"),
        ("bye", "goodbye"),
        ("My name is Priya", "introduce_user"),
        ("What is your name?", "bot_identity"),
        ("thank you so much", "thanks"),
        ("what time is it", "time"),
        ("what's today's date", "date"),
        ("help", "help"),
        ("tell me a joke", "joke"),
        ("how are you doing", "how_are_you"),
        ("hi, what time is it", "time"),   # specific rule beats greeting
        ("this is xyz nonsense", "fallback"),  # "hi" must not match inside "this"
    ]

    passed = 0
    for message, expected_rule in test_cases:
        actual_rule, _ = get_reply(message)
        status = "PASS" if actual_rule == expected_rule else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"[{status}] '{message}' -> {actual_rule} (expected {expected_rule})")

    print(f"\n{passed}/{len(test_cases)} tests passed.")


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        chat()
