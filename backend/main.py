from fastapi import FastAPI

from rl_engine.train import train
from rl_engine.inference import get_best_route

from backend.metrics import route_metrics

app = FastAPI(title="Intelligent Multi-Hop Routing API", version="1.0.0")

@app.get("/")
def home():
    return{
        "message": "Intelligent Multi-Hop Routing API is running. Use the /route endpoints to interact with the model."
    }

@app.get("/route")

def route():

    agent = train()

    best_route = (get_best_route(agent))

    metrics = (route_metrics(best_route))

    return {
        "route":best_route,**metrics
    }