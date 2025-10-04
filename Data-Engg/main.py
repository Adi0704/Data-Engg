import requests,json
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY=os.getenv("API_KEY")
channel_name='Sidemen'
MAX_RESULTS=50
url=f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_name}&key={API_KEY}'

def get_playlist_id():
    response=requests.get(url)
    data=response.json()
    playlist_id=data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return playlist_id


def get_video_ids(playlist_id):
    video_ids=[]
    next_page_token=None
    try:
        while True:
            playlist_url=f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&maxResults={MAX_RESULTS}&key={API_KEY}'
            if next_page_token:
                playlist_url+=f'&pageToken={next_page_token}'
            response=requests.get(playlist_url)
            data=response.json()
            for item in data['items']:
                video_ids.append(item['contentDetails']['videoId'])
            next_page_token=data.get('nextPageToken')
            if not next_page_token:
                break
        return video_ids # All video IDs collected
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
    

def extract_video_data(video_id):
    extracted_data=[]
    def batch_list(video_id_lst,batch_size):
        for i in range(0,len(video_id_lst),batch_size):
            yield video_id_lst[i:i+batch_size]
    try:
        for batch in batch_list(video_id,MAX_RESULTS):
            video_ids_str=','.join(batch)
            url=f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_ids_str}&key={API_KEY}'
            response=requests.get(url)
            data=response.json()
            for item in data['items']:
                video_data={
                    'video_id':item['id'],
                    'title':item['snippet']['title'],
                    'publishedAt':item['snippet']['publishedAt'],
                    'viewCount':int(item['statistics'].get('viewCount',0)),
                    'likeCount':int(item['statistics'].get('likeCount',0)),
                    'duration':item['contentDetails']['duration']
                }
                extracted_data.append(video_data)
        return extracted_data # All video data collected
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    playlist_id=get_playlist_id()
    video_ids=get_video_ids(playlist_id) # List of all video IDs
    print(extract_video_data(video_ids)) # List of all video data