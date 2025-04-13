from flask import Flask, render_template, request
import os
import time

app = Flask(__name__)
counter_file =  'counter.txt'
ip_log = {}

def load_count():
	if os.path.exists(counter_file):
		with open(counter_file, 'r') as f:
			return int(f.read())
	return 0

def save_count(count):
	with open(counter_file, 'w') as f:
		f.write(str(count))

visitor_count = load_count()

@app.route('/')
def home():
	global visitor_count
	ip = request.remote_addr
	current_time = time.time()

	if ip not in ip_log or (current_time - ip_log[ip]) > 300:
		visitor_count += 1
		save_count(visitor_count)
		ip_log[ip] = current_time

	return render_template('index.html', count=visitor_count)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
