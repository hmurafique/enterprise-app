from celery import Celery
import time

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672//')

@app.task
def process_order(order_id):
    time.sleep(3)
    return f"Order {order_id} processed"
