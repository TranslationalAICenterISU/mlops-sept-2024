from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import docker

default_args = {
        'owner' : 'airflow',
        'start_date': datetime(2024, 9, 13),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),                            
        }

dag = DAG(
        'streamlit_labelstudio_pipeline',
        default_args=default_args,
        description='Streamlit and Label Studio MLOps Pipeline',
        schedule_interval=timedelta(minutes=2),
        )

def launch_streamlit():
    client = docker.from_env()
    container = client.containers.run(
            'streamlit-app:latest',
            detach=True,
            ports={'8501/tcp': 8501},
            volumes={'/home/exouser/data': {'bind': '/app/output', 'mode': 'rw'}}
            )
    return container.id

def launch_label_studio():
    client = docker.from_env()
    container = client.containers.run(
            'heartexlabs/label-studio:latest',
            detach=True,
            ports={'8080/tcp': 8080},
            volumes={'/home/exouser/data': {'bind': '/label-studio/data', 'mode': 'rw'}}
            )
    return container.id

launch_streamlit_task = PythonOperator(
        task_id='launch_streamlit',
        python_callable=launch_streamlit,
        dag=dag,
        )
               
launch_label_studio_task = PythonOperator(
        task_id='launch_label_studio',
        python_callable=launch_label_studio,
        dag=dag,
        )

launch_streamlit_task >> launch_label_studio_task
