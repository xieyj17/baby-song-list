# main.py
from agent.agent import AIAgent

def main():
    """
    Main function to initialize and run the AI agent.
    """
    system_prompt = "You are an AI agent that finds and saves YouTube videos to a playlist, with self-correction capabilities."
    
    # This would typically be loaded from a config file or environment variable
    playlist_id = "PLXQTj_UselJ3ACin7QI3oKv51dYVxSm-D" 
    
    print("🎵 Aaron's Baby Songs Agent")
    print("=" * 40)
    print("为Aaron寻找适合的儿歌并添加到播放列表")
    print("输入 'quit' 或 'exit' 退出程序")
    print("=" * 40)

    try:
        # Initialize the agent
        agent = AIAgent(system_prompt, playlist_id)
        print("✅ AI Agent 初始化成功！")
        
        # Interactive loop
        while True:
            print("\n" + "-" * 30)
            user_prompt = input("请描述你想要的儿歌类型: ").strip()
            
            # Check for exit commands
            if user_prompt.lower() in ['quit', 'exit', '退出', 'q']:
                print("👋 再见！希望Aaron喜欢这些儿歌！")
                break
            
            # Skip empty inputs
            if not user_prompt:
                print("⚠️ 请输入有效的描述")
                continue
            
            print(f"\n🔍 正在处理: '{user_prompt}'")
            
            # Start the agent's process
            agent.process_prompt(user_prompt)

    except ValueError as e:
        # Catch the error if the API key is not set
        print(f"❌ 配置错误: {e}")
        print("请确保已设置 SILICONFLOW_API_KEY 环境变量")
    except KeyboardInterrupt:
        print("\n\n👋 程序被中断，再见！")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"❌ 发生意外错误: {e}")

if __name__ == "__main__":
    # This ensures the main function is called only when the script is executed directly
    main()