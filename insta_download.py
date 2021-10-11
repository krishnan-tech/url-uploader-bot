import requests
from bs4 import BeautifulSoup
import wget
import os
from urllib.parse import urlparse
import json

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
    if response.status_code == 200:
        return response
    else:
        return None


def insta_type_checker(json_response):
    with open("test.json", "w") as file:
        file.write(json.dumps(json_response))
    if "product_type" in json_response["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"] and "is_video" in json_response["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]:
        if json_response["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["is_video"]:
            return json_response["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["product_type"]
        else:
            return None

    elif "is_video" in json_response["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]:
        if json_response["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["is_video"] == False:
            return "post"
        else:
            return None
    else:
        return None

def insta_json_conveter(response):
    try:
        soup = BeautifulSoup(response.text, features="html.parser")
        with open("test.html", "w") as file:
            file.write(response.text)
        script_data = soup.find_all("script")[4]
        try:
            json_data = json.loads(script_data.contents[0][21:-1])
        except:
            json_data = json.loads(script_data.contents[0][21:-1])
        return json_data
    except:
        return None

def insta_wget(url):
    filename = wget.download(url, out="./uploads/")
    filename = os.path.basename(filename)
    return filename

def insta_post(response):
    try:
        soup = BeautifulSoup(response.content, features="html.parser")
        meta_tag = soup.find("meta", {"property" : "og:image"})
        return insta_wget(meta_tag["content"])
    except:
        return None


def insta_reel(json_data):
    try:
        reel_src = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"]
        return insta_wget(reel_src)
    except:
        return None


def insta_video(json_data):
    try:
        video_src = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"]
        return insta_wget(video_src)
    except:
        return None


def insta_igtv(json_data):
    try:
        igtv_src = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"]
        return insta_wget(igtv_src)
    except:
        return None

def extract_insta_id(link):
    query = urlparse(link)
    if query.hostname in {'www.instagram.com', 'instagram.com'}:
        if query.path[:3] == '/p/': return query.path.split('/')[2]
        if query.path[:6] == '/reel/': return query.path.split('/')[2]
    return None