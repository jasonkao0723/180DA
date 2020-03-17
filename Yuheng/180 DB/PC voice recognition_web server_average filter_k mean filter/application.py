
# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event

__author__ = ''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def randomNumberGenerator():

    while True:
        val = input("Enter voice signal:")
        if val == "0":
            v_signal = "START"
        if val == "1":
            v_signal = "FIRE"
        if val == "2":
            v_signal = "EXPLODE"
        if val == "3":
            v_signal = "ARMOR"
        if val == "4":
            v_signal = "ANTIBIOTIC"
        if val == "5":
            v_signal = "SURRENDER"
        socketio.emit('newnumber', {'number': v_signal}, namespace='/test')
        socketio.sleep(0.01)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
