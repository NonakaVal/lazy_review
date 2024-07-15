from crewai import Crew, Process
from langchain_openai import ChatOpenAI

# crew_pt for Portuguese and crew_en for English
from crew_pt import (
    topic_researcher, academic_reviewer, ref_specialist, prof, research_writer,
    list_topics_task, academic_review_task, website_list_task, tutorial_write_task, research_write_task,
    pdf_path
)

# SET THE LLM MODEL
llm = ChatOpenAI(model='gpt-3.5-turbo')

# EQUIPE
crew = Crew(
    agents=[topic_researcher, academic_reviewer, ref_specialist, prof, research_writer ],
    tasks=[list_topics_task, academic_review_task, website_list_task, tutorial_write_task, research_write_task ],
    process=Process.sequential,
    manager_llm=llm
)

result = crew.kickoff(inputs={'transcript_path': pdf_path})
print(result)
