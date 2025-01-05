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

#+++This needs to return an array of all of tool calling instances
def extract_thing_in_exclamation_marks(text):
    """
    Extract the text surrounded by '!!'.

    Args:
        text (str): The input text.

    Returns:
        str: The extracted text.
    """
    pattern = r'!!(.+)!!'
    match = re.search(pattern, text)
    
    if match:
        return match.group(1)
    else:
        return ""

def main():
    print("Welcome to the Chatbot! Type 'quit' to exit.")

    tool_list = {"updateMem"}

    memory_title = "Tools: Call tools by putting the tool name between two exclamation marks. Ex: !!updateMem!!"
    memory_format = "Current tools are: " + tool_list
    old_memory = ""
    new_memory = "This is your memory"

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        total_mem = memory_title + memory_format + "Old tasks: " + old_memory + "\n    Current memory: " + new_memory

        response = send_request(total_mem + "User: " + user_input)
        bot_response = response.get("choices")[0].get("message").get("content") if response.get("choices") else "Sorry, I couldn't get a response."

        #Printed to user
        print("Bot:" + total_mem + "\n")

        #This is bad code, this needs to detect the tool name and call the appropriate script
        if(extract_thing_in_exclamation_marks(bot_response) == "updateMem"):
            old_memory = old_memory + ". " + new_memory
            new_memory = extract_string(bot_response)
            print("--updatemem trigger")

        #Or we have another one just for appropriate scripts and leave some hard coded stuff in main
        # :/

        print(bot_response)

if __name__ == "__main__":
    main()