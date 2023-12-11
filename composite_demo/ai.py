from langchain.agents import load_tools  
from langchain.agents import initialize_agent  
from langchain.agents import AgentType  
from langchain.llms import OpenAI  
  
# First, let's load the language model we're going to use to control the agent.  
llm = OpenAI(temperature=0)  
  
# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.  
tools = load_tools(["ddg-search"], llm=llm)  
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)  
  
# Now let's test it out!  
agent.run("南昌明天多少度? ")