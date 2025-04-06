from fastapi import FastAPI, Query, Body
from pydantic import BaseModel
import pandas as pd
from recommender import AssessmentRecommender
import uvicorn
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="API for recommending SHL assessments based on job descriptions or queries",
    version="1.0.0",
)

# Initialize the recommender
recommender = AssessmentRecommender()


class QueryModel(BaseModel):
    text: str
    max_recommendations: Optional[int] = 10


class Assessment(BaseModel):
    name: str
    url: str
    remote_testing: str
    adaptive_support: str
    duration: str
    test_type: str


class RecommendationResponse(BaseModel):
    recommendations: List[Assessment]
    query_analysis: dict


@app.get("/")
async def root():
    return {
        "message": "Welcome to the SHL Assessment Recommendation API. Use /recommend endpoint to get recommendations."}


@app.get("/recommend")
async def recommend_get(
        query: str = Query(..., description="Natural language query or job description"),
        max_recommendations: int = Query(10, description="Maximum number of recommendations to return")
):
    """
    Get assessment recommendations based on a query string
    """
    recommendations = recommender.recommend(query, max_recommendations)

    # Extract analysis information
    analysis = {
        "duration_limit": recommender._extract_duration_limit(query),
        "skills": recommender._extract_skills(query),
        "test_types": recommender._extract_test_types(query)
    }

    # Convert DataFrame to list of dicts
    recommendations_list = recommendations.to_dict(orient="records")

    return {
        "recommendations": recommendations_list,
        "query_analysis": analysis
    }


@app.post("/recommend")
async def recommend_post(query_model: QueryModel):
    """
    Get assessment recommendations based on request body containing query text
    """
    recommendations = recommender.recommend(
        query_model.text,
        query_model.max_recommendations
    )

    # Extract analysis information
    analysis = {
        "duration_limit": recommender._extract_duration_limit(query_model.text),
        "skills": recommender._extract_skills(query_model.text),
        "test_types": recommender._extract_test_types(query_model.text)
    }

    # Convert DataFrame to list of dicts
    recommendations_list = recommendations.to_dict(orient="records")

    return {
        "recommendations": recommendations_list,
        "query_analysis": analysis
    }


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)