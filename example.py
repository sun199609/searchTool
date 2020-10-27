# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import csv
import json
import argparse

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret_463048915584-qrp7qtk37bo3m9gvm5qboho7jb6hhku5.apps.googleusercontent.com.json"
api_key = "AIzaSyBxBcaYRKKjwMb3RqNi4gi5Up5OvRlThUY"


# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key) #credentials=credentials)



def get_related_videos(query):
    videos = []
    next_page_token = None
    
    while 1:
        res = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=10,
            pageToken=next_page_token
        ).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        if next_page_token is None or len(videos) >= 10:
            break
     
    videos = sorted(videos, key=lambda x:x['snippet']['publishedAt'])
    
    return videos


def get_videos_stats(video_ids):
    stats = []
    for i in range(0, len(video_ids), 50):
        res = youtube.videos().list(id=','.join(video_ids[i:i+50]),
                                 part='statistics').execute()
        stats += res['items']
    return stats  


def write_json_into_csv(videos, stats):
    csv_file = open("results.csv", "w", newline='')
    writer = csv.writer(csv_file,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    keys = ['title','upload_time','uploader','view_count']
    writer.writerow(keys)
    
    for dic, stat in zip(videos, stats):
        title = dic['snippet']['title']
        upload_time = dic['snippet']['publishedAt']
        uploader = dic['snippet']['channelId']
        view_count = stat['statistics']['viewCount']
        writer.writerow([title, upload_time, uploader, view_count])
    csv_file.close()



def main():
    parser = argparse.ArgumentParser(description="arguments description")
    parser.add_argument('--query','-q',help='query', default='tenet')
    args = parser.parse_args()
    
    # get related videos
    videos = get_related_videos(args.query)
    print(len(videos))
    with open("data.json","a") as f:
        f.write(videos)
        
    # get video stats
    video_ids = list(map(lambda x:x['id']['videoId'], videos))
    stats = get_videos_stats(video_ids)
    print(len(stats))
    
    # write result into csv file
    write_json_into_csv(videos, stats)
    
    
if __name__ == "__main__":
    main()
