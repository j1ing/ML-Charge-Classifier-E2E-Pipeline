from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI()

MODEL_PATH = "airflow/trained_weights/best_model.joblib"
VECTORIZER_PATH = "airflow/trained_weights/best_vectorizer.joblib"

class ChargeCategoryRequest(BaseModel):
  description: str

class ChargeCategoryResponse(BaseModel):
  label: str

def predict(user_input, vectorizer, model):
  user_input_vec = vectorizer.transform([user_input])
  return model.predict(user_input_vec)

@app.post("/ChargeCategory", response_model=ChargeCategoryResponse)
async def chargeCategory(request: ChargeCategoryRequest):
  try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)     
    prediction = predict(request.description, vectorizer, model)
    return ChargeCategoryResponse(label=prediction[0])
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Charge classification service error: {e}")
  

@app.get("/health")
def health_check():
    return {"status": "ok"}
