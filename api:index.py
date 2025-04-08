from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from recommender import get_recommendations  # adjust this if needed

app = FastAPI()

# Existing POST endpoint
@app.post("/recommend")
async def recommend(data: Request):
    json_data = await data.json()
    query = json_data.get("query")
    recommendations = get_recommendations(query)
    return JSONResponse(content={"input": query, "results": recommendations})


# ✅ New GET endpoint
@app.get("/search")
async def search(query: str = Query(..., description="Search input text")):
    recommendations = get_recommendations(query)
    return JSONResponse(content={"input": query, "results": recommendations})
