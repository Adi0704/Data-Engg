import requests,json
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY=os.getenv("API_KEY")
channel_name='Sidemen'
url=f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_name}&key={API_KEY}'
def get_channel_id():
    response=requests.get(url)
    data=response.json()
    # print(json.dumps(data,indent=4))
    # print(data)
    print(data['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
if __name__ == '__main__':
    get_channel_id()