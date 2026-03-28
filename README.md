# 🖥️ Linux Server Monitoring Dashboard

A real-time server monitoring dashboard built with FastAPI (Python) and React. Displays CPU usage, memory usage, disk usage, and running processes with live updates.

## ✨ Features

- **Real-time Monitoring**: Live updates every 2 seconds via WebSocket
- **CPU Usage**: Real-time percentage with core count
- **Memory Usage**: RAM utilization with used/total GB
- **Disk Usage**: Storage space monitoring
- **Process List**: Top 10 processes by CPU usage
- **Interactive Charts**: Historical trend visualization
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **psutil** - System metrics collection
- **WebSocket** - Real-time communication

### Frontend
- **React 18**
- **Recharts** - Data visualization
- **WebSocket API** - Real-time data streaming

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/server-monitor.git
cd server-monitor
