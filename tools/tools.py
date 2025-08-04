from duckduckgo_search import DDGS


def search_tool(query: str) -> dict:
    """
    Search for a youtube video based on the provided query.

    Args:
    - query: The search query.

    Returns:
    - A dictionary containing the search results.
    """
    print(f"Tool: search youtube for: {query}")

    search_query = f"{query} site:youtube.com"

    try:
        with DDGS() as ddgs:
            result = list(ddgs.text(search_query), max_results=1)
            if not result:
                print("Tool: No resutls found on DuckDuckGo.")
                return None
            video = result[0]
            print(f"Tool: Found video: {video['title']}")

            return {
                "id": video['href'].split("v=")[-1],
                "title": video['title'],
                "url": video['href'],
                "description": video.get('body', '')
            }
    except Exception as e:
        print(f"Tool: An error occured during search: {e}")
        return None

