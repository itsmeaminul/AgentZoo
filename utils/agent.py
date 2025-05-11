from typing import List, Dict
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_agent():
    groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    def agent(messages: List[Dict[str, str]]) -> str:
        # 1) Validate
        for m in messages:
            if not ("role" in m and "content" in m):
                raise ValueError(f"Each message must have 'role' and 'content', got {m!r}")

        # 2) Retrieve additional context
        user_msgs = [m["content"] for m in messages if m["role"] == "user"]
        if user_msgs:
            last_query = user_msgs[-1]
            results = tavily_client.search(query=last_query)
            snippets = [r["content"] for r in results.get("results", [])][:3]
            if snippets:
                messages.insert(
                    0,
                    {
                        "role": "system",
                        "content": "Additional context:\n\n" + "\n\n".join(snippets)
                    }
                )

        # 3) Call Groq chat completion
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.3
        )
        return completion.choices[0].message.content

    return agent
