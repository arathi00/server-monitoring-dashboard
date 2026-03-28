from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import psutil
import asyncio
import json
from datetime import datetime

app = FastAPI()

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_system_metrics():
    """Fetch current system metrics using psutil"""
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memory usage
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    memory_used_gb = memory.used / (1024**3)
    memory_total_gb = memory.total / (1024**3)
    
    # Disk usage
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_used_gb = disk.used / (1024**3)
    disk_total_gb = disk.total / (1024**3)
    
    # Running processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu': proc.info['cpu_percent'] or 0,
                'memory': proc.info['memory_percent'] or 0
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage (top 10)
    processes.sort(key=lambda x: x['cpu'], reverse=True)
    
    return {
        'timestamp': datetime.now().isoformat(),
        'cpu': {
            'percent': cpu_percent,
            'cores': psutil.cpu_count()
        },
        'memory': {
            'percent': memory_percent,
            'used_gb': round(memory_used_gb, 2),
            'total_gb': round(memory_total_gb, 2)
        },
        'disk': {
            'percent': disk_percent,
            'used_gb': round(disk_used_gb, 2),
            'total_gb': round(disk_total_gb, 2)
        },
        'processes': processes[:10]  # Top 10 processes
    }

@app.get("/api/metrics")
async def get_metrics():
    """REST endpoint for one-time metrics"""
    return get_system_metrics()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time streaming"""
    await websocket.accept()
    try:
        while True:
            metrics = get_system_metrics()
            await websocket.send_json(metrics)
            await asyncio.sleep(2)  # Update every 2 seconds
    except:
        pass

@app.get("/")
async def root():
    return {"message": "Server Monitoring API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)