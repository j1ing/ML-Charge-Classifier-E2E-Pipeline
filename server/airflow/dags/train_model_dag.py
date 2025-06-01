from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from training.main import preprocess_and_save, train_and_save

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='invoice_description_model_training',
    default_args=default_args,
    description='Train and save invoice labeler model',
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['training'],
) as dag:

    preprocess_task = PythonOperator(
        task_id='preprocess_and_save',
        python_callable=preprocess_and_save
    )

    train_task = PythonOperator(
        task_id='train_and_save',
        python_callable=train_and_save
    )

    preprocess_task >> train_task  # Dependency: preprocess before train