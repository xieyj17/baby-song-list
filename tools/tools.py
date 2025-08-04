from ddgs import DDGS
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time

def search_tool(query: str):
    """
    Searches for a YouTube video using the DDGS video search.
    """
    print(f"Tool: Searching for YouTube video with query: '{query}'")
    
    try:
        with DDGS() as ddgs:
            cleaned_query = query.strip().strip('"\'')
            
            # Add "site:youtube.com" to the query to filter results
            youtube_query = f"{cleaned_query} site:youtube.com"
            print(f"Tool: Executing text search with: '{youtube_query}'")

            # Search for videos using the text search function
            # We'll take the first result.
            text_results = list(ddgs.text(
                query=youtube_query,
                region="wt-wt",
                safesearch="off",
                timelimit=None,
                max_results=1
            ))

            if not text_results:
                print("Tool: No results found on DuckDuckGo.")
                return None
            
            video = text_results[0]
            # Ensure the result is a YouTube link
            if "youtube.com/watch" not in video.get('href', ''):
                print(f"Tool: First result is not a YouTube video: {video.get('href')}")
                return None

            print(f"Tool: Found video: {video['title']}")
            
            # The ddgs.text() function returns a dictionary with 'title', 'href', and 'body'
            return {
                "id": video['href'].split("v=")[-1],
                "title": video['title'],
                "url": video['href'],
                "description": video.get('body', '')
            }

    except Exception as e:
        print(f"Tool: An error occurred during video search: {e}")
        return None

def post_playlist_tool(video_url, playlist_id, credentials_file="credentials.json", token_file="token.json"):
    """
    添加YouTube视频到指定的playlist
    
    Args:
        video_url (str): YouTube视频URL
        playlist_id (str): 目标playlist的ID
        credentials_file (str): OAuth凭据文件路径
        token_file (str): token文件路径
    
    Returns:
        dict: 操作结果
    """
    
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    
    # 从URL提取video ID
    if "youtube.com/watch" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
    else:
        return {"success": False, "error": "无效的YouTube URL"}
    
    try:
        # OAuth认证
        creds = None
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=8080)
            
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        # 建立YouTube API连接
        youtube = build('youtube', 'v3', credentials=creds)
        
        # 添加视频到playlist
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        
        response = request.execute()
        
        return {
            "success": True,
            "video_id": video_id,
            "title": response['snippet']['title'],
            "message": f"✅ 已为Aaron添加: {response['snippet']['title']}"
        }
        
    except HttpError as e:
        return {
            "success": False,
            "error": f"YouTube API错误: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"未知错误: {str(e)}"
        }