import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from core.agent_factory import create_agent_executor 


try:
    agent_executor = create_agent_executor()
    print("✅ AI Agent Executor created successfully and is ready.")
except Exception as e:
    print(f"❌ CRITICAL ERROR: Failed to create AI Agent Executor. {e}")
    agent_executor = None


app = FastAPI(
    title="Campus Copilot AI Agent",
    description="The AI brain service that connects to the Node.js backend.",
)


class Query(BaseModel):
    query: str
    user_identity: dict 

@app.post("/ask")
async def ask_agent(query: Query):
    """
    This is the main endpoint for the AI agent.
    It receives a query and user identity, invokes the agent,
    and returns the final answer.
    """
    if not agent_executor:
        return {"response": "Sorry, the AI Agent is not initialized. Please check the server logs."}

    print(f"AI Agent received question: '{query.query}' for user: {query.user_identity.get('userId')}")
    
    user_context = f"Role: {query.user_identity.get('role')}"
    if query.user_identity.get('role') == 'Student':
        user_context += f", student_id: {query.user_identity.get('studentId')}"
        user_context += f", entry_date: {query.user_identity.get('entryDate')}"
    elif query.user_identity.get('role') == 'Professor':
        user_context += f", professor_id: {query.user_identity.get('professorId')}"

    try:
    
        response = agent_executor.invoke({
            "input": query.query,
            "context": user_context
        })

       
        return {"response": response['output']}
    
    except Exception as e:
        print(f"❌ Error during agent invocation: {e}")
        return {"response": "Sorry, I encountered an error while processing your request."}

@app.get("/")
def read_root():
    return {"message": "Campus Copilot AI Agent is running."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

