
import webbrowser
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
import joblib


model = joblib.load("data/model_train.pkl")


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Timer(
        2,
        lambda: webbrowser.open("http://127.0.0.1:8000/docs")
    ).start()
    yield


app = FastAPI(lifespan=lifespan)


class DiabetesInput(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int


@app.get("/")
def home():
    return {"message": "Diabetes Prediction API Running"}


@app.post("/predict")
def prediction(data: DiabetesInput):

    input_data = [
        data.Pregnancies,
        data.Glucose,
        data.BloodPressure,
        data.SkinThickness,
        data.Insulin,
        data.BMI,
        data.DiabetesPedigreeFunction,
        data.Age
    ]

    final_prediction = model.predict([input_data])

    result = "Diabetes" if final_prediction[0] == 1 else "No Diabetes"

    return {"prediction": result}
