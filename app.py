from flask import Flask, render_template, jsonify, request
import time
import threading

app = Flask(__name__)

# Variáveis globais
time_remaining = 0
timer_running = False
paused_time = 0

def countdown():
    global time_remaining, timer_running
    while timer_running and time_remaining > 0:
        time.sleep(1)
        time_remaining -= 1

@app.route('/')
def index():
    return render_template('index.html', time_remaining=time_remaining)
    
@app.route('/timer')
def timer():
    return render_template('timer.html')  # A nova página do cronômetro

@app.route('/start_timer', methods=['POST'])
def start_timer():
    global time_remaining, timer_running
    time_remaining = int(request.json['time'])
    timer_running = True
    threading.Thread(target=countdown).start()
    return jsonify(success=True)

@app.route('/time_remaining')
def get_time_remaining():
    return jsonify(time_remaining=time_remaining)

@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    global timer_running
    timer_running = False
    return jsonify(success=True)

@app.route('/continue_timer', methods=['POST'])
def continue_timer():
    global timer_running
    timer_running = True
    threading.Thread(target=countdown).start()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='192.168.100.38', port=5000, debug=True)
