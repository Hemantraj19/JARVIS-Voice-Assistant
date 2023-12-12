from flask import Flask, render_template
from datetime import datetime
import psutil
import subprocess
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('status_update')
def handle_status_update(data):
    print('Status Update:', data)
    socketio.emit('status_update', data)


if __name__ == '__main__':
    # Start jarvis.py as a subprocess
    jarvis_process = subprocess.Popen(['python', 'jarvis.py'])


@app.route('/')
def index():
    current_date = datetime.now()
    current_day = current_date.strftime('%d')
    current_month = current_date.strftime('%B')
    current_time = current_date.strftime('%H:%M')
    current_day_of_week = current_date.strftime('%A')
    no_of_cores = psutil.cpu_count()
    no_of_processes = len(psutil.pids())
    return render_template('index.html', current_day=current_day, current_month=current_month, 
                           current_time=current_time, current_day_of_week=current_day_of_week,
                           no_of_cores=no_of_cores, no_of_processes=no_of_processes)

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False)

# Wait for the Flask application to start and then run jarvis.py
jarvis_process.wait()

# If the Flask application stops, terminate the jarvis.py subprocess
jarvis_process.terminate()