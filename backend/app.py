import os 
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from ai_assistant import get_budget_advice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

transactions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    transactions.append(data)
    socketio.emit('new_transaction', data, broadcast=True)
    return jsonify({"status": "success"})

@app.route('/advice')
def advice():
    income = sum(float(t['amount']) for t in transactions if t['type'] == 'income')
    expenses = sum(float(t['amount']) for t in transactions if t['type'] == 'expense')
    return jsonify({"advice": get_budget_advice(income, expenses)})

if __name__ == '__main__':
  socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))