# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret_463048915584-qrp7qtk37bo3m9gvm5qboho7jb6hhku5.apps.googleusercontent.com.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)



def get_related_videos(query):
    videos = []
    next_page_token = None
    
    while 1:
        res = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        if next_page_token is None:
            break
     
    videos = sorted(videos, key=lambda x:x['snippet']['publishedAt'])
    
    return videos


def get_videos_stats(video_ids):
    stats = []
    for i in range(0, len(video_ids), 50):
        res = youtube.videos.list(id=','.join(video_ids[i:i+50]),
                                 part='statistics').execute()
        stats += res['items']
    return stats


def main():
    
    # get related videos
    videos = get_related_videos("tenet")
  
    # get video stats
    video_ids = list(map(lambda x:x['id']['videoId'], videos))
    stats = get_videos_stats(video_ids)
    println(len(stats))
    
    

if __name__ == "__main__":
    main()
