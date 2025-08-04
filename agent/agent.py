import os 
from openai import OpenAI
from tools.tools import search_tool, post_playlist_tool

SILLICONFLOW_API_KEY = os.getenv('SILLICONFLOW_API_KEY')

class AIAgent:
    def __init__(self, system_prompt, playlist_id, max_retries=3):
        self.system_prompt = system_prompt
        self.playlist_id = playlist_id
        self.max_retries = max_retries
        self.client = OpenAI(
                              api_key=SILLICONFLOW_API_KEY, 
                              base_url="https://api.siliconflow.cn/v1")
        self.tools = {
            "search_tool": search_tool,
            "post_playlist_tool": post_playlist_tool
        }

    def _call_llm(self, prompt, max_tokens=50, temperature=0.2):
        """A helper function to make calls to the LLM API."""
        try:
            response = self.client.chat.completions.create(
                model="Pro/deepseek-ai/DeepSeek-V3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Agent: An error occurred with the LLM API: {e}")
            return None

    def refine_query_with_llm(self, user_prompt):
        """Uses the LLM to refine a user prompt into an effective search query."""
        print("Agent: Refining query with LLM...")
        refinement_prompt = f"""
        Your task is to take a user's request for a song and turn it into a concise, effective search query for finding a YouTube video.
        The query should be optimized to find content suitable for the described context (e.g., for a baby).
        Do not add any extra text or explanation, just the search query.

        User request: "{user_prompt}"
        
        Refined search query:
        """
        refined_query = self._call_llm(refinement_prompt)
        if refined_query:
            print(f"Agent: LLM refined query to: '{refined_query}'")
            return refined_query
        return user_prompt # Fallback to original prompt

    def judge_video_relevance(self, user_prompt, title, description):
        """Uses the LLM to judge if a video is relevant to the user's prompt."""
        print("Agent: Judging video relevance with LLM...")
        judgment_prompt = f"""
        A user wants to find a video based on this request: "{user_prompt}"
        We found a video with the following details:
        Title: "{title}"
        Description: "{description}"

        Does this video seem like a good match for the user's request? Please answer with only "Yes" or "No".
        """
        response = self._call_llm(judgment_prompt, max_tokens=5)
        if response and response.lower().startswith("yes"):
            print("Agent: Video judged as RELEVANT.")
            return True
        print("Agent: Video judged as NOT RELEVANT.")
        return False

    def get_new_search_query(self, user_prompt, failed_query, failed_title):
        """Asks the LLM for a new search query if the previous one failed."""
        print("Agent: Getting a new search query from LLM...")
        new_query_prompt = f"""
        A user wants to find a video based on this request: "{user_prompt}"
        Our previous search query, "{failed_query}", returned a video titled "{failed_title}" which was not a good match.
        Please provide a new, different search query to try and find a better result.
        Do not add any extra text or explanation, just the new search query.
        """
        new_query = self._call_llm(new_query_prompt)
        if new_query:
            print(f"Agent: New query from LLM: '{new_query}'")
            return new_query
        return failed_query # Fallback to the failed query if API fails

    def process_prompt(self, user_prompt):
        print(f"Agent: Received prompt: '{user_prompt}'")
        
        current_query = self.refine_query_with_llm(user_prompt)
        
        for attempt in range(self.max_retries):
            print(f"\n--- Attempt {attempt + 1} of {self.max_retries} ---")
            
            video_info = self.tools["search_tool"](current_query)
            
            if video_info and video_info.get("id"):
                is_relevant = self.judge_video_relevance(user_prompt, video_info['title'], video_info['description'])
                
                if is_relevant:
                    print(f"\nAgent: Found relevant video: {video_info['title']}")
                    result = self.tools["post_playlist"](self.playlist_id, video_info['id'])
                    print(f"Agent: {result}")
                    return # Success, exit the function
                else:
                    # If not relevant, get a new query for the next loop iteration
                    current_query = self.get_new_search_query(user_prompt, current_query, video_info['title'])
            else:
                print("Agent: Search returned no results. Trying a different query.")
                current_query = self.get_new_search_query(user_prompt, current_query, "No video found")

        print(f"\nAgent: Could not find a suitable video after {self.max_retries} attempts.")


def main():
    system_prompt = "You are an AI agent that finds and saves YouTube videos to a playlist, with self-correction capabilities."
    playlist_id = "PL-your-playlist-id" 
    
    try:
        agent = AIAgent(system_prompt, playlist_id)
        user_prompt = "I want to find a song about spring for a 7-month old baby"
        agent.process_prompt(user_prompt)
    except ValueError as e:
        print(f"Error: {e}")
        print("Please make sure you have set the SILICONFLOW_API_KEY environment variable.")

if __name__ == "__main__":
    main()