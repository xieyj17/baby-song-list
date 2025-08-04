# main.py
from agent.agent import AIAgent

def main():
    """
    Main function to initialize and run the AI agent.
    """
    system_prompt = "You are an AI agent that finds and saves YouTube videos to a playlist, with self-correction capabilities."
    
    # This would typically be loaded from a config file or environment variable
    playlist_id = "PL-your-playlist-id" 
    
    # The user's request
    user_prompt = "I want to find a song about spring for a 7-month old baby"

    try:
        # Initialize the agent
        agent = AIAgent(system_prompt, playlist_id)
        
        # Start the agent's process
        agent.process_prompt(user_prompt)

    except ValueError as e:
        # Catch the error if the API key is not set
        print(f"Configuration Error: {e}")
        print("Please make sure you have set the SILICONFLOW_API_KEY environment variable.")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # This ensures the main function is called only when the script is executed directly
    main()
