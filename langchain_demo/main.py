from typing import List
from ChatGLM3 import ChatGLM3

from langchain.agents import load_tools
from Tool.Weather import Weather
from Tool.Calculator import Calculator
from Tool.Music import Music

from langchain.agents import initialize_agent
from langchain.agents import AgentType


def run_tool(tools, llm, prompt_chain: List[str]):
    loaded_tolls = []
    for tool in tools:
        if isinstance(tool, str):
            loaded_tolls.append(load_tools([tool], llm=llm)[0])
        else:
            loaded_tolls.append(tool)
    agent = initialize_agent(
        loaded_tolls, llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    for prompt in prompt_chain:
        agent.run(prompt)


if __name__ == "__main__":
    model_path = "THUDM/chatglm3-6b"
    llm = ChatGLM3()
    llm.load_model(model_name_or_path=model_path)

    # calculator: 单个工具调用示例 3
    run_tool([Calculator(),Music()], llm, [
        "请推荐两首爱国的，钢琴的，激昂的乐曲"
    ]),
