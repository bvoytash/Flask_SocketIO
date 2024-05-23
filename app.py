from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from multiprocessing import Process, Queue
import cv2
import time
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
queue = Queue()  # Create the queue

db_path = os.path.join(os.path.dirname(__file__), 'data.db')


def init_db():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mouse_clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x INTEGER,
                y INTEGER,
                photo_path TEXT
            )
        ''')
        conn.commit()


init_db()


def generate_frames():
    cap = cv2.VideoCapture(0)  # Initialize webcam capture
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if not queue.empty():
            x, y = queue.get()
            print(f"Mouse clicked at ({x}, {y})")
            # Save the captured image (modify the path as needed)
            cv2.imwrite("captured_image.jpg", frame)
            photo_path = save_image(frame)
            save_to_db(x, y, photo_path)
            print("Image captured and saved as 'captured_image.jpg'")
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


# DB DATA
def save_image(frame):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    photo_filename = f"captured_image_{timestamp}.jpg"
    photo_path = os.path.join(os.path.dirname(__file__), 'static', photo_filename)
    cv2.imwrite(photo_path, frame)
    return photo_path


def save_to_db(x, y, photo_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mouse_clicks (x, y, photo_path)
            VALUES (?, ?, ?)
        ''', (x, y, photo_path))
        conn.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('mouse_move')
def handle_mouse_move(data):
    x = data['x']
    y = data['y']
    emit('update_coords', {'x': x, 'y': y})


@socketio.on('mouse_click')
def handle_mouse_click(data):
    x = data['x']
    y = data['y']
    queue.put((x, y))
    emit('response', {'status': 'received'})


if __name__ == "__main__":
    socketio.run(app, debug=True)
