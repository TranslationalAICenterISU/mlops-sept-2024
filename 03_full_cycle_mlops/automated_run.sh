#!/bin/bash

# MLOps Demo Orchestration Script

# Exit on error
set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get the host's IP address
get_ip_address() {
    ip_address=$(hostname -I | awk '{print $1}')
    if [ -z "$ip_address" ]; then
        ip_address=$(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' | head -n 1)
    fi
    if [ -z "$ip_address" ]; then
        ip_address="127.0.0.1"
        echo "Warning: Could not determine IP address. Using localhost (127.0.0.1)."
    fi
    echo "$ip_address"
}

# Function to stop a process
stop_process() {
    local process_name=$1
    local pid=$(pgrep -f "$process_name")
    if [ ! -z "$pid" ]; then
        echo "Stopping existing $process_name process..."
        kill $pid
        sleep 2
    fi
}

# Get the IP address
HOST_IP=$(get_ip_address)

# Stop existing processes
stop_process "mlflow server"
stop_process "prometheus"
stop_process "grafana-server"
stop_process "streamlit run"
stop_process "uvicorn fastapi_app:app"

# Clean up any leftover MLflow run ID file
rm -f mlflow_run_id.txt



for cmd in docker python3 pip streamlit mlflow uvicorn ./prometheus-2.40.0.linux-amd64/prometheus grafana-server; do
    if ! command_exists $cmd; then
        echo "Error: $cmd is not installed."
        case $cmd in
            ./prometheus-2.40.0.linux-amd64/prometheus)
                echo "To install Prometheus, visit: https://prometheus.io/docs/prometheus/latest/installation/"
                ;;
            grafana-server)
                echo "To install Grafana, visit: https://grafana.com/docs/grafana/latest/installation/"
                ;;
            docker)
                echo "To install Docker, visit: https://docs.docker.com/get-docker/"
                ;;
            *)
                echo "Please install it and try again."
                ;;
        esac
        exit 1
    fi
done

# Setup Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv mlops_demo_env
source mlops_demo_env/bin/activate

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt

# For PyTorch with CUDA support (uncomment if needed)
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Setup Weights & Biases
echo "Please enter your Weights & Biases API key:"
read -s WANDB_API_KEY
export WANDB_API_KEY

# Start MLflow tracking server
echo "Starting MLflow tracking server..."
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlflow-artifacts --host 0.0.0.0 --port 5000 &
MLFLOW_PID=$!

# Start Prometheus
echo "Starting Prometheus..."
prometheus --config.file=prometheus.yml &
PROMETHEUS_PID=$!

# Start Grafana
echo "Starting Grafana..."
grafana-server --config=/etc/grafana/grafana.ini --homepath /usr/share/grafana &
GRAFANA_PID=$!

# Wait for services to start
sleep 10

# Start Streamlit app for data upload
echo "Starting Streamlit app for data upload..."
streamlit run streamlit_app.py &
STREAMLIT_PID=$!

# Print URLs for accessing services
echo "Access the following URLs in your browser:"
echo "Streamlit: http://${HOST_IP}:8501"
echo "MLflow UI: http://${HOST_IP}:5000"
echo "Grafana: http://${HOST_IP}:3000"
echo "Prometheus: http://${HOST_IP}:9090"

# Wait for user to upload data
read -p "Press enter after uploading the house images zip file..."

# Process images
echo "Processing images..."
python process_images.py

# Train model
echo "Training model..."
python train_model.py

# Check if the run ID file was created
if [ ! -f "mlflow_run_id.txt" ]; then
    echo "Error: MLflow run ID file not found. Training may have failed."
    exit 1
fi

# Deploy model with FastAPI
echo "Deploying model with FastAPI..."
uvicorn fastapi_app:app --host "${HOST_IP}" --port 8000 &
FASTAPI_PID=$!

# Wait for FastAPI to start
sleep 5

# Send test prediction
echo "Sending test prediction..."
curl -X POST -F "file=@sample_house.jpg" http://${HOST_IP}:8000/predict/ --output prediction_output.png

echo "Prediction saved as prediction_output.png"

# Keep the script running
echo "Demo is now running. Press Ctrl+C to stop all services and exit."
wait

# Cleanup function
cleanup() {
    echo "Stopping all services..."
    kill $MLFLOW_PID $PROMETHEUS_PID $GRAFANA_PID $STREAMLIT_PID $FASTAPI_PID 2>/dev/null
    echo "Demo stopped."
}

# Set up trap to call cleanup function on script exit
trap cleanup EXIT