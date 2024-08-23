from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.get("/check-status/{service_name}")
async def check_service_status(service_name: str):
    url = f"https://istheservicedown.com.br/status/{service_name}"
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the service logo
        logo_container = soup.find('div', class_='service-logo-container')
        logo_img = logo_container.find('img') if logo_container else None
        logo_url = logo_img['src'] if logo_img else None
        
        # Extract the relevant status information
        status_div = soup.find('div', class_='service-status-alert-box')
        
        if status_div:
            status_texts = [p.get_text(strip=True) for p in status_div.find_all('p')]
            
            # Determine if the service is stable or unstable based on the status text
            status = "estável" if any("nenhum problema" in text.lower() for text in status_texts) else "instável"
            
            return {
                "service_name": service_name,
                "status": status,
                "logo_url": logo_url,
                "details": status_texts
            }
        else:
            raise HTTPException(status_code=404, detail="Service status not found on the page.")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve the page.")

