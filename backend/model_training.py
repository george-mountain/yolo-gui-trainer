import json
from datetime import datetime
import asyncio
import nest_asyncio
import os
from dotenv import find_dotenv, load_dotenv
import torch
from ultralytics import YOLO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from redis.asyncio import Redis
from configs.config import logger

nest_asyncio.apply()

# Load environment variables
load_dotenv(find_dotenv())

r = Redis(host="redis", port=6379, decode_responses=True)


def run_async_task(coro):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(coro)


EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")
FROM_EMAIL = os.getenv("EMAIL_ACCOUNT")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
subject = "Model Training Completed"


class ModelTraining:
    def __init__(self, user_id):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Device: {self.device}")
        logger.info("*" * 50)
        self.start_time = None
        self.end_time = None
        self.user_id = user_id

    def send_email(
        self,
        body,
        from_email=FROM_EMAIL,
        to_emails=RECIPIENT_EMAIL,
        subject=subject,
        api=EMAIL_API_KEY,
    ):
        """Send an email notification when training is complete."""
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_emails
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(from_email, api)
            smtp_server.sendmail(from_email, to_emails, msg.as_string())
            smtp_server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Failed to send email:", e)

    def on_train_start(self, trainer):
        """Callback for training start event."""
        self.start_time = datetime.now()
        print(f"Training started at {self.start_time}")
        print("-" * 50)

    def on_train_epoch_end(self, trainer):
        """Callback for end of each training epoch."""
        curr_epoch = trainer.epoch + 1
        total_epochs = trainer.epochs
        progress = (curr_epoch / total_epochs) * 100
        current_epoch = f"Epoch {curr_epoch}/{total_epochs}"

        print(f"Epoch {curr_epoch}/{total_epochs} completed")
        print("*" * 50)

        run_async_task(
            r.publish(
                f"training_progress_{self.user_id}",
                f"progress:{progress},epoch:{current_epoch}",
            )
        )

    def on_train_end(self, trainer):
        """Callback for training completion."""
        self.end_time = datetime.now()
        time_taken = self.end_time - self.start_time
        trainer_epoch = trainer.epoch
        trainer_metrics = trainer.metrics

        # Format training duration
        hours, remainder = divmod(time_taken.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_taken_str = (
            (f"{int(hours)} hr " if hours > 0 else "")
            + (f"{int(minutes)} mins " if minutes > 0 else "")
            + f"{int(seconds)} secs"
        )

        # Generate email content
        body = f"""
        <html>
            <head>
                <style>
                    table, th, td {{
                        border: 1px solid black;
                        border-collapse: collapse;
                        padding: 5px;
                    }}
                </style>
            </head>
            <body>
                <h1>Training Report</h1>
                <p>Date and Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p>Total Epochs Trained: {trainer_epoch + 1} </p>
                <p>Time Taken to Train Model: {time_taken_str} </p>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                    {''.join([f'<tr><td>{k}</td><td>{v:.2f}</td></tr>' for k, v in trainer_metrics.items()])}
                </table>
            </body>
        </html>
        """
        print("Training completed.")
        print(f"time taken: {time_taken_str}")
        print(f"Total epochs trained: {trainer_epoch + 1}")
        print(f"Metrics: {trainer_metrics}")
        print("*" * 50)
        self.send_email(body)

        # dump using json and publish
        run_async_task(
            r.publish(
                f"training_progress_{self.user_id}",
                json.dumps(
                    {
                        "status": "completed",
                        "time_taken": time_taken_str,
                        "metrics": trainer_metrics,
                    }
                ),
            )
        )

    def train_yolov8_model(self, config_path, num_epochs, training_result_dir):
        """Train the YOLOv8 model using the provided configuration."""
        model = YOLO("yolov8x.pt")

        # Register callbacks
        model.add_callback("on_train_start", self.on_train_start)
        model.add_callback("on_train_epoch_end", self.on_train_epoch_end)
        model.add_callback("on_train_end", self.on_train_end)

        print("Starting training...")

        # Train the model
        model.train(
            data=config_path,
            name="Yolo_Model_Training",
            project=training_result_dir,
            task="detect",
            epochs=num_epochs,
            patience=20,
            batch=16,
            cache=True,
            imgsz=640,
            iou=0.5,
            augment=True,
            degrees=25.0,
            fliplr=0.0,
            lr0=0.0001,
            optimizer="Adam",
            device=self.device,
        )

        print("Training completed.")
