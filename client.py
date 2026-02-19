print("AI MCP CLIENT STARTED")

import asyncio
import json
import requests
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
from config import OLLAMA_URL, MODEL_NAME


async def run_agent():
    server = StdioServerParameters(
        command="python3",
        args=["db_mcp_server.py"]
    )

    async with stdio_client(server) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()

            print("\nType 'exit' to stop.\n")

            while True:
                user_input = input(">>> ")

                if user_input.lower() == "exit":
                    print("Exiting...")
                    break

                payload = {
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "user", "content": user_input}
                    ],
                    "stream": False
                }

                try:
                    response = requests.post(OLLAMA_URL, json=payload)

                    # Check HTTP status
                    if response.status_code != 200:
                        print("HTTP Error:", response.status_code)
                        print("Response:", response.text)
                        continue

                    response_json = response.json()

                    # If normal chat response
                    if "message" in response_json:
                        message = response_json["message"]
                        print("\nLLM Response:\n")
                        print(message.get("content", "No content returned"))

                    # If Ollama returned error
                    elif "error" in response_json:
                        print("Ollama API Error:", response_json["error"])

                    else:
                        print("Unexpected Response Format:")
                        print(json.dumps(response_json, indent=2))

                except Exception as e:
                    print("Request Failed:", str(e))


asyncio.run(run_agent())

