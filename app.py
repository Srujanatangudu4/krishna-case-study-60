from flask import Flask, render_template, request
import requests, random
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fact', methods=['POST'])
def fact():
    date = request.form.get('date')

    try:
        if date:
            _, month, day = date.split('-')
        else:
            now = datetime.now()
            month, day = now.month, now.day

        url = f"https://history.muffinlabs.com/date/{month}/{day}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        events = data['data']['Events']
        random_event = random.choice(events)
        year = random_event['year']
        text = random_event['text']

        date_display = f"{day}-{month}" if date else "Today"
        return render_template('result.html', year=year, text=text, date=date_display)

    except Exception:
        return render_template(
            'result.html',
            year="N/A",
            text="Could not fetch historical facts. Please try again later.",
            date="Error"
        )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)

