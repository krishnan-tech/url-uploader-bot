import os
import re
import glob
import instaloader

import siaskynet as skynet
from config import Config as SETTING

client = skynet.SkynetClient()

def download_post(_id):
	os.system(f"instaloader --dirname-pattern=./uploads/{_id} -- -{_id}")

def get_ids(url):
	all_match = re.findall( r'^(?:https?:\/\/)?(?:www\.)?(?:instagram\.com(?:\/\w+)?\/p\/)([\w-]+)(?:\/)?(\?.*)?$', url)
	arr = []
	for each_match in all_match:
		short_code = each_match[0]
		arr.append((short_code))
	return arr


def upload_siasky(file_path):
    skylink = client.upload_file(file_path)
    return SETTING.SIASKY_CLIENT + skylink[6:]


def all_post_ids(url):
	all_short_codes = get_ids(url)

	links = []
	for each_short_code in all_short_codes:
		download_post(each_short_code)
		all_paths = glob.glob(f"./uploads/{each_short_code}/*.jpg")
		for path in all_paths:
			x = upload_siasky(path)
			links.append(x)
		
	return links

all_post_ids("https://www.instagram.com/p/CSN8kIwKI0L/")