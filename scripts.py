import requests
from bs4 import BeautifulSoup

def scrape_service_status(service_name):
    url = f"https://istheservicedown.com.br/status/{service_name}"
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the relevant information
        status_div = soup.find('div', class_='service-status-alert-box')
        
        if status_div:
            p_tags = status_div.find_all('p')
            for p in p_tags:
                status_text = p.get_text(strip=True)
                print(f"Status: {status_text}")
        else:
            print("Could not find the service status on the page.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    # Example: 'vivo-brasil', 'tiktok', etc.
    service_name = "tinder"  # Replace with the desired service name
    scrape_service_status(service_name)
