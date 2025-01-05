from bs4 import BeautifulSoup
import requests

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
