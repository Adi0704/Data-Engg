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
    # print(json.dumps(data,indent=4))
    # print(data)
    playlist_id=data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return playlist_id
base_url='https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=UUDogdKl7t7NHzQ95aEwkdMw&key=AIzaSyDE39JD3yz0j9Eo10R_Cp39lK1dl5OFlE0 '
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
        return video_ids
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == '__main__':
    playlist_id=get_playlist_id()
    video_ids=get_video_ids(playlist_id)
    print(video_ids)