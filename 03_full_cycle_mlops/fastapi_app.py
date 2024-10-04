import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
import torch
import numpy as np
import mlflow
from prometheus_client import make_asgi_app, Counter, Histogram, Gauge
import time

# Initialize FastAPI app
app = FastAPI()

# Define Prometheus metrics
REQUEST_COUNT = Counter('model_request_count', 'Total number of requests to the model')
LATENCY = Histogram('model_latency_seconds', 'Time taken to process a request')
PREDICTION_GAUGE = Gauge('model_prediction_value', 'Value of the model prediction')

# Load the model (adjust the path as needed)
mlflow.set_tracking_uri("http://localhost:5000")
model = mlflow.pytorch.load_model("runs:/<run_id>/model")
model.eval()

# Create a Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    REQUEST_COUNT.inc()
    start_time = time.time()

    # Read and preprocess the image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert('L')
    image = image.resize((128, 128))
    image_tensor = torch.from_numpy(np.array(image)).float().unsqueeze(0).unsqueeze(0) / 255.0

    # Make prediction
    with torch.no_grad():
        output = model(image_tensor)

    # Postprocess the output
    output_image = Image.fromarray((output.squeeze().numpy() * 255).astype(np.uint8))
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')

    # Record latency
    latency = time.time() - start_time
    LATENCY.observe(latency)

    # Record prediction value (e.g., mean pixel value of the output)
    pred_value = output.mean().item()
    PREDICTION_GAUGE.set(pred_value)

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)