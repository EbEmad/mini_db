import pickle
from fastapi import FastAPI
import uvicorn
from typing import Dict,Any
from pydantic import BaseModel, Field
from typing import Literal,Annotated
# request
class Customer(BaseModel):
    gender: Literal["male", "female"]
    seniorcitizen: Annotated[int, Field(ge=0,le=1)]
    partner: Literal["yes", "no"]
    dependents: Literal["yes", "no"]
    phoneservice: Literal["yes", "no"]
    multiplelines: Literal["no", "yes", "no_phone_service"]
    internetservice: Literal["dsl", "fiber_optic", "no"]
    onlinesecurity: Literal["yes", "no", "no_internet_service"]
    onlinebackup: Literal["yes", "no", "no_internet_service"]
    deviceprotection: Literal["yes", "no", "no_internet_service"]
    techsupport: Literal["yes", "no", "no_internet_service"]
    streamingtv: Literal["yes", "no", "no_internet_service"]
    streamingmovies: Literal["yes", "no", "no_internet_service"]
    contract: Literal["month-to-month", "one_year", "two_year"]
    paperlessbilling: Literal["yes", "no"]
    paymentmethod: Literal[
        "electronic_check",
        "mailed_check",
        "bank_transfer_(automatic)",
        "credit_card_(automatic)"
    ]

    # Numerical with constraints from dataset stats
    tenure: Annotated[int, Field(ge=0)]
    monthlycharges: Annotated[float, Field(ge=0)]
    totalcharges: Annotated[float, Field(ge=0)]


# response
class PredictResponse(BaseModel):
    churn_probability: float
    churn: bool



app=FastAPI(title='churn-prediction')

with open('model.bin','rb') as f_in:
    pipeline=pickle.load(f_in)

def predict_single(customer):
    result=pipeline.predict_proba(customer)[0,1]
    return float(result)
@app.post("/predict")
def predict(customer:Customer)->PredictResponse:
    prob=predict_single(customer.dict())
    return PredictResponse (
        churn_probability=prob,
        churn=bool(prob>=0.5)
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)



