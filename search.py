# -*- coding: utf-8 -*-

import os
import csv
import json
import argparse
import datetime

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyBxBcaYRKKjwMb3RqNi4gi5Up5OvRlThUY"

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
        if 'title' in dic['snippet']:
            title =  dic['snippet']['title']
        else:
            title = " "
        if 'publishedAt' in dic['snippet']:
            upload_time = dic['snippet']['publishedAt']
        else:
            upload_time = " "
        if 'channelId' in dic['snippet']:
            uploader = dic['snippet']['channelId']
        else:
            uploader = " "
        if 'viewCount' in stat['statistics']:
            view_count = stat['statistics']['viewCount']
        else:
            view_count = " "
        writer.writerow([title, upload_time, uploader, view_count])
    csv_file.close()



def main():
    parser = argparse.ArgumentParser(description="arguments description")
    parser.add_argument('--query','-q',help='query', default='tenet')
    args = parser.parse_args()
    
    start_time = datetime.datetime.now()
    
    # get related videos
    try:
        videos = get_related_videos(args.query)
    except Exception as e:
        print("error occurs, you should probably change another api_key" + str(e))
        return
        
    # get video stats
    video_ids = list(map(lambda x:x['id']['videoId'], videos))
    try:
        stats = get_videos_stats(video_ids)
    except Exception as e:
        print("error occurs, you should probably change another api_key" + str(e))
        return 
    
    # write result into csv file
    try: 
        write_json_into_csv(videos, stats)
    except Exception as e:
        print("error happens while writing results into csv: " + str(e))
        return
    
    # output time
    end_time = datetime.datetime.now()
    duration = (end_time-start_time).seconds
    days = int(duration/86400)
    hours = int(duration/3600)-24*days
    minutes = int(duration % 3600 /60)
    seconds = int(duration % 60)
    print("time passed: " + str(days) + "days " + str(hours) + "hours " + str(minutes) +"minutes " + str(seconds)+"seconds")
    
    
if __name__ == "__main__":
    main()
