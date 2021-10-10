import requests
from bs4 import BeautifulSoup
import wget
import os
from urllib.parse import urlparse

def get_response(insta_url):
    payload={}
    headers = {
    'Host': 'www.instagram.com',
    'Sec-Ch-Ua': '";Not A Brand";v="99", "Chromium";v="94"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cookie': 'csrftoken=WkpsiMOtthFWAlNo5MySlICduSX1M7Zn; ig_did=0B172B92-F4DD-4F1F-BA7E-CAC06D92D5E1; mid=YNb1pAAEAAEGnmwyCKL7yUVIFfHk'
    }

    response = requests.request("GET", insta_url, headers=headers, data=payload)
    response = BeautifulSoup(response.content, features="html.parser")
    meta_tag = response.find("meta", {"property" : "og:image"})
    filename = wget.download(meta_tag["content"], out="./uploads/")
    filename = os.path.basename(filename)

    if response.status_code == 200:
        return filename
    else:
        return None

def extract_insta_id(link):
    query = urlparse(link)
    if query.hostname in {'www.instagram.com', 'instagram.com'}:
        if query.path[:3] == '/p/': return query.path.split('/')[2]
        if query.path[:6] == '/reel/': return query.path.split('/')[2]
    return None