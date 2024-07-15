from typing import List, Optional
from crewai import Agent
from crewai_tools import PDFSearchTool

def create_agent(
    role: str,
    goal: str,
    backstory: str,
    context_topic: str,
    llm: str,
    pdf_path: Optional[str] = None,
    verbose: bool = True,
    tools: Optional[List[str]] = None
):
    agent_tools = tools if tools else []
    if pdf_path:
        agent_tools.append(PDFSearchTool(pdf=pdf_path))
    
    return Agent(
        role=role,
        goal=f'{goal} "{context_topic}"',
        verbose=verbose,
        backstory=backstory,
        llm=llm,
        tools=agent_tools
    )