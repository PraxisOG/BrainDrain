import requests
import json
import requests
from bs4 import BeautifulSoup
import os
import glob
import re

def send_request(message):
    url = "http://localhost:1234/v1/chat/completions"

    # Your request payload
    payload = {
        "messages": [
            { "role": "system", "content": "You will work through problems yourself with the tools given to you. " +
            "Your context is short so keep your current mission in your short term memory." },
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

def search_google(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        
        # Make a GET request to the specified URL
        response = requests.get(url)
        
        # Verify if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the title of the page
            title = soup.find('title').get_text(strip=True)
            
            # Attempt to extract a summary from the meta description or the first paragraph
            meta_description = soup.find('meta', attrs={'name': 'description'})
            if meta_description and 'content' in meta_description.attrs:
                summary = meta_description['content']
            else:
                first_paragraph = soup.find('p')
                summary = first_paragraph.get_text(strip=True) if first_paragraph else "No summary available."
            
            # Format the output
            result = {
                'title': title,
                'summary': summary
            }
            
            return result
        else:
            # Return an error message if the request was unsuccessful
            return f"Error: Request failed with status code {response.status_code}"
    except requests.RequestException as e:
        # Handle any request-related exceptions and return an error message
        return f"Error: {str(e)}"
    except Exception as e:
        # Handle any other unexpected exceptions and return an error message
        return f"Error: An unexpected error occurred - {str(e)}"




def main():
    print("Welcome to the Chatbot! Type 'quit' to exit.")

    memory_title = "Tools: Call tools by putting the tool name between two exclamation marks. Ex: !!updateMem!!"
    memory_format = """
    Current tools are:
    updateMem (use plenty of detail when using this function. Ex: !!updatemem!! "this is short term memory")
    web (ex: !!web!! "search query")
    Only use zero or one tool per response
    """
    old_memory = ""
    new_memory = "This is your memory"

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        total_mem = memory_title + memory_format + "Old tasks: " + old_memory + "\n    Current task: " + new_memory

        response = send_request(total_mem + "User: " + user_input)
        bot_response = response.get("choices")[0].get("message").get("content") if response.get("choices") else "Sorry, I couldn't get a response."

        #Printed to user
        print("Bot:" + total_mem + "\n")

        #print("Script finder found: " + extract_thing_in_exclamation_marks(bot_response) + "\n" + extract_string(bot_response) + "\n")

        if(extract_thing_in_exclamation_marks(bot_response) == "updateMem"):
            old_memory = old_memory + ". " + new_memory
            new_memory = extract_string(bot_response)
            print("--updatemem trigger")

        print(bot_response)

        if(extract_thing_in_exclamation_marks(bot_response) == "web"):
            web_results = str(search_google(extract_string(bot_response)))
            response = send_request("\n" + total_mem + "Web results for:  " + web_results)
            print(total_mem + "Web results for:  " + web_results)
            bot_response = response.get("choices")[0].get("message").get("content") if response.get("choices") else "Sorry, I couldn't get a response."
            
            print("--web trigger")
            print(bot_response)

if __name__ == "__main__":
    main()
