# 🧠Overview
This project demonstrates a complete ML workflow that includes data processing, model training, and deployment using modern tools:

- Machine Learning: Training a charge description classification model.

- Airflow: Orchestrating the workflow with DAGs, scheduling, and automation.

- Docker: Containerizing server and client for reproducibility and easy deployment.

The core goal is to showcase a maintainable and extensible end-to-end ML system, designed to bridge development and production workflows.

⚠️ The sample freight invoice dataset is synthetically generated (via ChatGPT) and not representative of real-world data. For production-grade performance, replace with actual charge description data.

🧪 This example model classifies into four categories: Freight, Fuel, Accessorial, and Duty and Tax.

🔐 Note: Any keys included are invalid and for illustrative purposes only.

# 🚀Features
📊 Airflow DAG for training orchestration

⚡ FastAPI server to serve real-time predictions

📦 Client container to send classification requests

🔁 Docker Compose for orchestration of multi-container setup

🧩 Modular design for scalability and future extension

# 📦Project Structure
<pre><code>
ml-charge-classifier-e2e-pipeline/
│
├── server/                  # FastAPI server, Airflow DAGs, and Dockerfile
│   ├── server.py            # Entry point for FastAPI app
│   ├── airflow/             # Airflow DAGs, logs, and trained model
│   │   ├── dags/            # DAG files
│   │   └── trained_weights/ # Trained model and vectorizer files
│   └── Dockerfile           # Dockerfile for server container
│
├── client/                  # Client code and Dockerfile
│   └── Dockerfile           # Dockerfile for client container
│
├── docker-compose.yml       # Docker Compose for orchestration
├── requirements.txt         # Python dependencies for server
├── README.md                # Project documentation
└── .gitignore
</code></pre>

# ⚙️Getting Started
## ✅Prerequisites
- Docker Desktop installed and running (https://www.docker.com/products/docker-desktop)
- Docker Compose (comes with Docker Desktop)
- (Optional) Docker Extension for VSCode

## 🛠️Setup and Run
1. Clone and configure environment

Create a .env file in the root directory with the following content:

<pre><code>
API_CHARGE_CLASSIFICATION = "http://server:8000/ChargeCategory"
</code></pre>

2. Run Airflow to train the model

- Navigate to Airflow directory
<pre><code>
cd server/airflow
</code></pre>

- Initialize Airflow containers:
<pre><code>
docker compose up airflow-init
</code></pre>
Wait until: airflow-init-1 exited with code 0

- Start Airflow Docker container
<pre><code>
docker-compose up -d
</code></pre>

3. Trigger training DAG
Via Web UI:

- Access: https://localhost:8080
- Login: airflow/ airflow
- Locate invoice_description_model_training DAG
- Click the ▶️ (trigger) button

Via CLI:

- Trigger DAG:
<pre><code>
docker exec -it airflow-airflow-scheduler-1 airflow dags trigger invoice_description_model_training 
</code></pre>
- Check DAG run status:
<pre><code>
docker exec -it airflow-airflow-scheduler-1 airflow dags list-runs invoice_description_model_training 
</code></pre>

4. Shut down Airflow once training completes
<pre><code>
docker compose down -v
</code></pre>

5. Start client and server containers by cd back to root directory of the repo

6. Clean up logs (PowerShell)
<pre><code>
Remove-Item -Path .\server\airflow\logs\* -Recurse -Force
</code></pre>

7. Start server container
<pre><code>
docker compose up -d server
</code></pre>

8. Start client container
<pre><code>
docker compose run --rm client
</code></pre>

9. To shut everything down
<pre><code>
docker compose down --rmi all
</code></pre>


# 📝Notes
- The model files (best_model.joblib and best_vectorizer.joblib) are saved inside the Airflow container’s trained_weights folder.

- The DAG passes intermediate training data (e.g., X_train, y_test) by writing them to disk to avoid XCom limitation (default: limit 25 KB per XCom value).

- The server loads the trained model dynamically on each request.

- Modify DAGs in the airflow/dags/ folder to customize training workflow.

- Environment variables are handled via .env file inside client folder.

