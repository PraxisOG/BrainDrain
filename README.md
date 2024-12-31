# BrainDrain
This is a general purpose agent layer for LLMs, written in python.
Prompts are tuned for Llama 3.1 family

Current goals:

[y]: Make a simple dialogue setup in python

[y]: Make LLMs work through their problems through multiple prompts

[y]: Function calling with llama 3.1 8b

[n]: Web search access w/list of trustworthy websites

[y]: Short term memory at the start of each prompt

[n]: Give access to create/write simple python scripts

[n]: Give access to call simple python scripts

[n]: Give access to debug simple python scripts

[n]: Provide a dumping ground for old context and prompts for summarization

[n]: Oh, and a nice ui. Maybe. I'm only so good at this.

[n]: Maybe, just maybe, LLM backend integration too.

And thats it! Once its up any new functions can be set to short term memory,
and written by the llm. 

What does this solve: 
Current simple LLM frontends don't support web browsing and other features, 
which is weird since these models are more useful than just as chatbots.
This project is an extension of LMStudio or similar local HTTP server LLM frontends.
