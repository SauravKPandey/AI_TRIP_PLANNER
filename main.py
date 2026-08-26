from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os


app = FastAPI()

class QueryRequest(BaseModel):
    query:str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Travel Planner Backend is running!"}

@app.post("/query")
async def query_travel_request(query: QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider= "gemini")
        print("GraphBuilder completed")
        react_app = graph()
        print("Graph invoked")
        png_graph= react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        print(f"Graph saved as png at: {os.getcwd()}")
        messages = {"messages": [query.query]} 
        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content #last AI response
        else:
            final_output = str(output)

        return {"answer": final_output}
        
    except Exception as  e:
        return JSONResponse(status_code = 500, content= {"error": str(e)})
