from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from provider import model
from tools import get_products, generate_products

agent = create_agent(
    model=model,
    tools=[get_products, generate_products],
    system_prompt="You are a helpful assistant and should only focus on products",
)


# response = agent.invoke({
#     "messages" : [
#         HumanMessage("find the products added after 20th march 2026")
#     ]
# })

for chunk in agent.stream(
    {
        "messages": [
            {"role": "user", "content": "find the products added after 20th march 2026"}
        ]
    },
    stream_mode="updates",
    version="v2",
):
    if chunk["type"] == "updates":
        for step, data in chunk["data"].items():
            print(f"step: {step}")
            print(f"content: {data['messages'][-1].content_blocks}")

# print(response)
