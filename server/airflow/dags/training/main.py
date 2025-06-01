from training.preprocessing import preprocess_dataset
from training.model import train_model
from training.evaluation import evaluate
import os
import numpy as np
import joblib

DATASET_FILEPATH = '/opt/airflow/dags/training/dataset/invoice_autolabeler_1000.csv'
X = 'invoice_line'
Y = 'category'
TARGET_F1 = 0.95
PATIENCE_COUNTER = 3
TRAINED_DIR = "/opt/airflow/trained_weights"
os.makedirs(TRAINED_DIR, exist_ok=True)

def preprocess_and_save():
  X_train_vec, y_train, X_test_vec, y_test, vectorizer = preprocess_dataset.process_data(DATASET_FILEPATH, X, Y)
  joblib.dump(X_train_vec, f"{TRAINED_DIR}/X_train_vec.joblib")
  joblib.dump(y_train, f"{TRAINED_DIR}/y_train.joblib")
  joblib.dump(X_test_vec, f"{TRAINED_DIR}/X_test_vec.joblib")
  joblib.dump(y_test, f"{TRAINED_DIR}/y_test.joblib")
  joblib.dump(vectorizer, f"{TRAINED_DIR}/best_vectorizer.joblib")

def train_and_save():
  X_train_vec = joblib.load(f"{TRAINED_DIR}/X_train_vec.joblib")
  y_train=joblib.load(f"{TRAINED_DIR}/y_train.joblib")
  X_test_vec=joblib.load(f"{TRAINED_DIR}/X_test_vec.joblib")
  y_test=joblib.load(f"{TRAINED_DIR}/y_test.joblib")

  best_model = None
  best_score = -np.inf
  best_iter = None
  patience_count = 0
  for iter_count in [100, 300, 500, 700, 900, 1100]:
    print(f"\nTraining with max_iter={iter_count}...")
    model = train_model.train(X_train_vec, y_train, iter_count)
    y_pred = model.predict(X_test_vec)
    report = evaluate.report(y_test, y_pred)
    f1_macro = report['macro avg']['f1-score']
    print(f"F1-macro: {f1_macro:.4f}")

    # Track the best
    if f1_macro > best_score:
      best_score = f1_macro
      best_model = model 
      best_iter = iter_count
      patience_count = 0 # reset
    else:
      patience_count += 1
    
    if f1_macro >= TARGET_F1:
      print(f"Target F1 reached: {f1_macro:.4f} at iter={iter_count}")
      break

    if patience_count >= PATIENCE_COUNTER:
      print(f"No improvement in {PATIENCE_COUNTER} steps. Early stopping at iter={iter_count}.")
      break
  
  print(f"\nBest model at iter={best_iter} with F1-macro={best_score:.4f}")
  # Save the best model and vectorizer to disk
  joblib.dump(best_model, f"{TRAINED_DIR}/best_model.joblib")

