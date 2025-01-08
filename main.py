import json
import requests
from bs4 import BeautifulSoup
import os
import glob
import re
import langchain

def send_request(message):
    url = "http://localhost:1234/v1/chat/completions"

    # Your request payload
    payload = {
        "messages": [
            { "role": "system", "content": "You will work through problems yourself with the tools given to you." },
            { "role": "user", "content": message }
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Send POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check for successful response
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Request failed with status code " + str(response.status_code)}

#+++This needs to take two inputs, one tool call to locate the string, and the text to locate it in
def extract_string(text):
    """
    Returns input within quotes if it matches a function call pattern.
    
    Example:
        !!updateMem!! "returned text" -> 'returned text'
    """
    match = re.search(r'\!\!(\w+)\!\!', text)
    if match:
        func_name = match.group(1)
        args_str = text[match.end():]
        return f"'{func_name}{args_str}'"
    else:
        return text

#Returns an array of tool names and corresponding strings
def extract_tools_called(text):
    """
    Extract the tools surrounded by '!!' and their corresponding arguments.

    Args:
        text (str): The input text.

    Returns:
        list: A list of tuples containing the extracted tools and their arguments.
    """
    pattern = r'!!([^!]*)!!\s*"([^"]*)"'
    matches = re.findall(pattern, text)
    
    return [(match[0].strip(), match[1].strip()) for match in matches]


def solver(directive):
    #

    #while loop
        #Send request
        #Tool calling
        #Bot def
        #
    
    #return with message
    print("returned")

def bot(input):
    response = send_request(input)
    bot_response = response.get("choices")[0].get("message").get("content") if response.get("choices") else "Sorry, I couldn't get a response."
    return bot_response

def main():
    print("Welcome to the Chatbot! Type 'quit' to exit.")

    tool_list = {"updateMem"}

    memory_title = "\nTools: Call tools by putting the tool name between two exclamation marks. Ex: !!updateMem!!\n"
    memory_format = "Current tools are: " + str(tool_list)
    old_memory = ""
    new_memory = "This is your memory"

    newmemone = ""

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("You have quit!")
            break
        
        print("one" + user_input)
        response = send_request(user_input)
        bot_response = response.get("choices")[0].get("message").get("content") if response.get("choices") else "Sorry, I couldn't get a response."

        newmemone = newmemone + bot_response

        #Printed to user
        print("Bot: " + bot_response + "\n")

if __name__ == "__main__":
    main()