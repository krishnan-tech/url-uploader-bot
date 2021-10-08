from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
from urllib.parse import parse_qs, urlparse
from telegram import update

def extract_youtube_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
        # optional for playlists
        # if query.path[:9] == '/playlist': return parse_qs(query.query)['list'][0]
    return None


def yt_download(youtube_link):
    ydl_opts = {
        'format': "22/18/best",
        'outtmpl': f"uploads/{extract_youtube_id(youtube_link)}.mp4"
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([youtube_link])
        except DownloadError:
            # print("requested format not available")
            update.message.reply_text("Something went wrong, try again after some time :)")
        except Exception as e:
            # print("errr")
            print(e)
            update.message.reply_text("Ohh...\nContact Admin\nI'm Sick 🤒")