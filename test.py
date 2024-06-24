import sys
import os
import requests
import time
from tqdm import tqdm

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <base_url> <parameters_file>")
        return
    
    base_url = sys.argv[1]
    parameters_file = sys.argv[2]
    
    if not os.path.isfile(parameters_file):
        print(f"The file '{parameters_file}' does not exist.")
        return
    
    found_urls = []  # List to store URLs where keyword was found
    
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    
    payloads = [
        "nexiz%22", "nexiz%2522", 'nexiz%27', "nexiz%2527",
        "nexiz%3C", "nexiz%253C"
    ]
    
    pays = [
        'nexiz%22', "nexiz%25%32%32", "nexiz%27", "nexiz%25%32%37",
        "nexiz%3C", "nexiz%25%33%63"
    ]
    
    keywords = ["nexiz'", 'nexiz"', "nexiz<"]
    
    try:
        with open(parameters_file, 'r') as file:
            parameters = file.readlines()
        
        for param in parameters:
            param = param.strip()
            progress_bar = tqdm(payloads, desc=f"Checking {param}", unit="request", colour='green')
            found_any = False

            # Check GET requests with payloads
            for payload in progress_bar:
                url = f"{base_url}&{param}={payload}"
                response = requests.get(url, headers=header)
                
                if any(keyword in response.text for keyword in keywords):
                    found_any = True
                    found_urls.append(url)
                    progress_bar.set_postfix(found="YES", refresh=True)
                    progress_bar.set_description(f"Found {param}", refresh=True)
                time.sleep(1)
            
            # Additional checks with 'test' and 'nexiz' parameters
            test_url = f"{base_url}&{param}=test&{param}=nexiz"
            response = requests.get(test_url, headers=header)
            if "nexiz" in response.text:
                for payload in payloads:
                    url = f"{base_url}&{param}=test&{param}={payload}"
                    response = requests.get(url, headers=header)
                    
                    if any(keyword in response.text for keyword in keywords):
                        found_any = True
                        found_urls.append(url)
                        progress_bar.set_postfix(found="YES", refresh=True)
                        progress_bar.set_description(f"Found {param}", refresh=True)
                    time.sleep(1)
            
            # Check POST requests with payloads
            for payload in pays:
                data = {param: payload}
                response = requests.post(base_url, headers=headers, data=data)
                print(f"Payload '{data}' sent. Response status code: {response.status_code}")
                if any(keyword in response.text for keyword in keywords):
                    found_any = True
                    found_urls.append(f"POST: {data}")
                    progress_bar.set_postfix(found="YES", refresh=True)
                    progress_bar.set_description(f"Found {param}", refresh=True)
                time.sleep(1)
                
            datas = {param: ['test', 'nexiz']}
            response = requests.post(base_url, headers=headers, data=datas)
            print(f"Payload '{datas}' sent. Response status code: {response.status_code}")
            if "nexiz" in response.text:
                for payload in pays:
                    dataz = {param: ['test', payload]}
                    response = requests.post(base_url, headers=headers, data=dataz)
                    if any(keyword in response.text for keyword in keywords):
                        found_any = True
                        found_urls.append(f"POST: {dataz}")
                        progress_bar.set_postfix(found="YES", refresh=True)
                        progress_bar.set_description(f"Found {param}", refresh=True)
                    time.sleep(1)
                
            if found_any:
                print(f"Found: {param}")
            else:
                print(f"Not Found: {param}")
            
            time.sleep(1)  # Delay before processing next parameter
        
        # Print all found URLs
        if found_urls:
            print("\nFound URLs:")
            for url in found_urls:
                print(url)
        else:
            print("\nNo URLs found.")
    
    except requests.RequestException as e:
        print(f"A network error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
