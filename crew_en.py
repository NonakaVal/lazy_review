import os

from langchain_openai import ChatOpenAI
import openai
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from tools.PDFSelector import select_pdf, select_output_directory
from tools.create_agents import create_agent
from tools.create_tasks import create_task


# API CONFIGURATIONS
openai.api_key = os.getenv('OPENAI_API_KEY')
os.environ["BROWSERLESS_API_KEY"] = os.getenv('BROWSERLESS_API_KEY')
llm = ChatOpenAI(model='gpt-3.5-turbo')

# FILES
pdf_path = select_pdf()
if not pdf_path:
    print("No PDF selected. Exiting the program.")
    exit()
context_topic = input("Enter the lecture context: \n")
output_directory = select_output_directory()

"""AGENTS

An agent is an autonomous unit programmed to:

Execute tasks
Make decisions
Communicate with other agents

Think of an agent as a team member with specific skills and a particular job to do. 
Agents can have different roles, such as 'Researcher', 'Writer', or 'Customer Support', 
each contributing to the team's overall goal.

LEARN MORE: https://docs.crewai.com/core-concepts/Agents/
"""

"""TOOLS
CrewAI tools empower agents with capabilities ranging from web research and data analysis to collaboration and task delegation among coworkers. 
This documentation describes how to create, integrate, and leverage these tools within the CrewAI framework, including a new focus on collaboration tools.

Key features of tools:
Utility: Built for tasks such as web research, data analysis, content generation, and agent collaboration.
Integration: Enhances agent capabilities by seamlessly integrating tools into their workflow.
Customization: Offers flexibility to develop custom tools or utilize existing ones, meeting specific agent needs.
Error handling: Incorporates robust error handling mechanisms to ensure smooth operation.
Cache mechanism: Features intelligent caching to optimize performance and reduce redundant operations.

LEARN MORE: https://docs.crewai.com/core-concepts/Tools/
"""

"""TASKS
In the crewAI framework, tasks are specific assignments completed by agents. They provide all necessary details for execution, 
such as a description, responsible agent, required tools, and more, facilitating a wide range of action complexities.
"""

# AGENTS
topic_researcher = create_agent(
    role='Specialist in Review and Summaries',
    goal='List all topics covered about',
    backstory="You specialize in extracting relevant information from lectures and presentations.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path,
    tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website]
)

academic_reviewer = create_agent(
    role='Academic Reviewer',
    goal='Identify the techniques and methods in the listed topics about',
    backstory="Specializes in reviewing and identifying specific methods presented in academic contexts.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path,
    tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website]
)

ref_specialist = create_agent(
    role='Website Documentation Specialist',
    goal='List sites mentioned in the text about',
    backstory="Specializes in identifying and describing websites and references mentioned.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path
)

prof = create_agent(
    role='Tutorial Writer',
    goal='Write a detailed step-by-step tutorial for the project presented in the lecture',
    backstory="Specializes in creating clear and detailed tutorials, transforming complex information into accessible instructions.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path,
    tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website]
)

research_writer = create_agent(
    role='Senior Writer',
    goal='Research, analyze, and write a structured document on',
    backstory="Capable of conducting detailed research and writing structured documents on academic methods.",
    context_topic=context_topic,
    llm=llm,
    pdf_path=pdf_path,
    tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website]
)


# TASKS
list_topics_task = create_task(
    description=f"List all topics covered about '{context_topic}' in the text.",
    expected_output='Detailed and enumerated list of all topics covered in the text.',
    agent=topic_researcher,
    output_file=os.path.join(output_directory, "topics.md")
)

academic_review_task = create_task(
    description=f"Identify the techniques and methods presented in the lecture '{context_topic}'.",
    expected_output=f"All topics listed with their methods used and their goals about '{context_topic}' properly described and reviewed.",
    agent=academic_reviewer,
    output_file=os.path.join(output_directory, "techniques.md"),
    context=[list_topics_task]
)

website_list_task = create_task(
    description=(
        f"List websites mentioned in the lecture '{context_topic}' and their specific functions."
    ),
    expected_output='List of all websites mentioned in the text and their functions.',
    agent=ref_specialist,
    output_file=os.path.join(output_directory, "websites_list.md")
)

tutorial_write_task = create_task(
    description=(
        f"Write a comprehensive guide that clearly and detailed describes how to execute the project based on the lecture '{context_topic}'."
    ),
    expected_output=f"Step-by-Step Tutorial\n\n"
                    f"**Tutorial for Executing the Project: \"{context_topic}\"**\n\n"
                    "This tutorial details all necessary steps to execute the project presented in the lecture. "
                    "Follow the step-by-step instructions to ensure all techniques and methods are correctly applied.\n\n"
                    "**Step 1:** [Description of Step 1]\n"
                    "**Step 2:** [Description of Step 2]\n"
                    "...",
    agent=prof,
    async_execution=False,
    context=[list_topics_task, academic_review_task, website_list_task],
    output_file=os.path.join(output_directory, "tutorial.md")
)

research_write_task = create_task(
    description=(
        "Based on materials provided by other agents, write a professionally structured report with the following sections:"
        "\n- **Topics:** List of defined topics"
        "\n- **Objectives:** Describe the study objectives."
        "\n- **Research Gap:** Identify the research gap the study aims to fill."
        "\n- **Methodology:** Detail the methods used in the study."
        "\n- **Data Set:** Describe the dataset used in the study."
        "\n- **Results:** Summarize the main findings of the study."
        "\n- **Limitations:** Discuss the limitations of the study."
        "\n- **Conclusion:** Provide the study conclusion."
        "\n- **Future Directions:** Suggest possible directions for future research."
        "\n- **Assessments:** Include any assessments or estimates made in the study."
    ),
    expected_output=f"Comprehensive professionally structured report on '{context_topic}' produced based on provided text and generated from previous tasks.",
    agent=research_writer,
    async_execution=False,
    context=[list_topics_task, academic_review_task, website_list_task, tutorial_write_task],
    output_file=os.path.join(output_directory, "review.md")
)
