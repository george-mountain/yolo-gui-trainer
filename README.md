
# **Computer Vision Object Detection Model GUI Trainer**

## **Overview**
This simple project demonstrates how to train and fine-tune a computer vision model using a **GUI-based approach** instead of the command line. The application is built with **FastAPI (backend), ReactJS (frontend), and Redis (real-time progress tracking)**. The primary goal is to educate and provide a simple **user-friendly** way to train object detection models like **YOLOv8**, making it accessible to users with little or no technical knowledge.

With this project, users can:

- Start training with a simple **button click**.
- **Monitor training progress in real-time** via the frontend.

## **Tech Stack**
- **Backend:** FastAPI, Redis, Python, YOLOv8
- **Frontend:** ReactJS, Vite
- **Database:** Redis (for real-time event streaming)
- **Containerization:** Docker

---

## **Project Structure**
```
.
├── backend/
│   ├── main.py               # FastAPI application
│   ├── model_training.py      # Model training logic
│   ├── configs/
│   ├── datasets/              # YOLO dataset folder (train, val, test)
│   ├── data.yml               # Dataset configuration file
│   ├── Dockerfile             # Backend Docker setup
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── src/                   # React source code
│   ├── public/
│   ├── Dockerfile             # Frontend Docker setup
│   └── package.json           # Frontend dependencies
│
├── docker-compose.yml         # Multi-container deployment
└── README.md
```

---

## **Dataset Requirements**
Before running the application, you need a labeled dataset in **YOLO format**.

```
datasets
    ├── train
    │   ├── images
    │   └── labels
    ├── val
    │   ├── images
    │   └── labels
    └── test
        ├── images
        └── labels
```

Additionally, create a **`data.yml`** file inside the `backend/` directory with the following format:

```yaml
train: ./datasets/train/images
val: ./datasets/val/images
test: ./datasets/test/images

nc: 1  # Number of classes in your labelled data
names: ['pothole']  # Replace with your actual class names
```

---

## **Installation & Usage**
### **1. Clone the repository**
```bash
git clone https://github.com/george-mountain/yolo-gui-trainer.git
cd yolo-gui-trainer
```

### **2. Set up environment variables**
Create a **`.env`** file in the root directory and configure necessary variables.

### **3. Start the application using Docker Compose**
```bash
docker-compose up --build
```
This will:
- Start the FastAPI backend (port **8082**). Access API docs via: `http://localhost:8082/docs#/`
- Start the ReactJS frontend (port **3000**). Access GUI via: `http://localhost:3000/`
- Start Redis for real-time progress updates.

---


## **Frontend Features**
- **Start training** with a simple click.
- **Real-time progress updates** from Redis.
- **Interactive UI** to monitor training epochs.

---

## **Enhancements**
Though this is just a simple project for educational purpose in using realtime progress monitoring in object detection model training/fine-tuning, use the knowledge learned in this simple project to extend it to have the following features.
- Support for **multiple object detection models**.
- **User authentication & history tracking**.
- Enhanced **model configuration options** from the GUI.
- Allow users to **upload datasets from the GUI**. Alternatively, you can even allow users to **label their datasets directly from the GUI** and then train their labelled data.

