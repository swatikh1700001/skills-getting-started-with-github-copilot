"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team soccer training and inter-school matches",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "nina@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games, drills, and seasonal tournaments",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["ryan@mergington.edu", "taylor@mergington.edu"]
    },
    "Art Club": {
        "description": "Exploring drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "liam@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and annual school play productions",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["mia@mergington.edu", "noah@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for competitions",
        "schedule": "Thursdays, 3:30 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["aaron@mergington.edu", "zoe@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking, argumentation, and debate tournaments",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["chloe@mergington.edu", "ben@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    # Validate student is not already signed up and activity is not full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
