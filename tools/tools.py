from ddgs import DDGS 
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

def post_playlist_tool():
    pass