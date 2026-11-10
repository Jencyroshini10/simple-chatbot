# simple-chatbot
A simple rule-based chatbot in Python that replies to greetings, questions, and small talk using keyword and regex matching, with a fallback for unknown input and built-in tests.
# Rule-Based Chatbot

A beginner-friendly Python chatbot that chooses its responses using predefined rules instead of machine learning. Each rule matches keywords or patterns in the user’s message and returns a reply, and a fallback response handles anything it doesn’t recognize.

# Features
Responds to greetings, goodbyes, thanks, and “how are you”
Answers questions about the bot’s name, the current time, and the date
Remembers a user’s name when they say “my name is ...”
Tells jokes and shows available commands with help
Friendly fallback for unknown input
Built-in tests to check that each rule works
How It Works
The user’s message is lowercased and cleaned of punctuation.
Rules are checked from top to bottom, and the first match wins.
The matched rule returns a reply, chosen at random from its options.
If no rule matches, a fallback reply is returned.
Getting Started

Requires Python 3.6 or newer. No external libraries are needed.

# To Run
  start chat
      * python rule_based_chatbot.py   
 run the tests
       * python rule_based_chatbot.py --test   

Adding a New Rule

Add a dictionary to the RULES list with a name, a list of regex patterns, and a list of responses. Place specific rules above general ones.

# Project Structure
rule-based-chatbot/
├── rule_based_chatbot.py   # chatbot logic, rules, chat loop, and tests
└── README.md
# Possible Improvements
Load rules from a JSON file
Keep conversation history
Add a web interface with Flask or Streamlit
