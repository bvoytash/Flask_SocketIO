# Flask_SocketIO
Flask App which visualize the current reading of serial data from the movement of the mouse and when the left mouse’s button is pressed take a picture of a connected webcam

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Setup Instructions

1. **Clone the repository:**

    ```
    git clone git@github.com:bvoytash/Flask_SocketIO.git
    cd Flask_SocketIO
    ```

2. **Create and activate a virtual environment:**

    ```
    sudo apt install python3-venv
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```
    python app.py
    ```

    The database will be created automatically if it does not already exist.

## Usage

Once the application is running, you can access it in your web browser at `http://127.0.0.1:5000/`. The app should be functional and the real-time features powered by 
Socket.IO will be active.
