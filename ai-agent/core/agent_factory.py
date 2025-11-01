from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

import config
from tools.student_tools import (
    get_student_schedule,
    get_student_enrollments,
    get_student_placements
)
from tools.professor_tools import (
    get_professor_classes,
    get_professor_schedule,
    get_students_in_class
)
from tools.general_tools import (
    search_courses,
    get_course_details,
    get_class_schedule,
    get_current_semester
)



def create_agent_executor():
    """
    This factory function builds and returns the complete agent executor.
    It assembles the LLM, the tools, and the prompt.
    """
    
   
    llm = AzureChatOpenAI(
        azure_deployment=config.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version="2024-02-01",
        temperature=0, 
    )

    # 2. Collect all available tools
    tools = [
        get_student_schedule,
        get_student_enrollments,
        get_student_placements,
        get_professor_classes,
        get_professor_schedule,
        get_students_in_class,
        search_courses,
        get_course_details,
        get_class_schedule,
        get_current_semester
    ]


    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a helpful and professional Campus Copilot."
            "Your job is to answer the user's questions about the university."
            "You must use the available tools to find the information."
            "You have the following context about the user you are talking to: {context}."
            "You MUST use this context (like student_id or professor_id) when the user asks a question about 'my' or 'I'."
            "For general questions (like 'search for a course'), you may not need the context."
            "If you need a piece of information you don't have (e.g., a semester_id), you must ask the user for it."
            "If a tool fails, politely inform the user that you couldn't retrieve the information."
        )),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), 
    ])

    
    agent = create_tool_calling_agent(llm, tools, prompt)

   
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print("✅ AI Agent Executor created successfully.")
    return agent_executor