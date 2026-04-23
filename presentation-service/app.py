from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

WORKFLOW_URL = os.getenv('WORKFLOW_URL', 'http://workflow-service:5001')

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Campus Buzz - Submit Event</title>
    <style>
        body { font-family: Arial; margin: 50px; }
        input, textarea { display: block; margin: 10px 0; padding: 8px; width: 300px; }
        button { padding: 10px 20px; background: blue; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Submit Campus Event</h1>
    <form id="eventForm">
        Title: <input type="text" name="title"><br>
        Description (min 40 chars): <textarea name="description" rows="3"></textarea><br>
        Location: <input type="text" name="location"><br>
        Date (YYYY-MM-DD): <input type="text" name="date"><br>
        Organizer: <input type="text" name="organizer"><br>
        <button type="submit">Submit</button>
    </form>
    <div id="result"></div>

    <script>
        document.getElementById('eventForm').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            const response = await fetch('/api/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await response.json();
            
            if (result.id) {
                document.getElementById('result').innerHTML = `Submitted! ID: ${result.id}<br><a href="/result/${result.id}">View Result</a>`;
            }
        };
    </script>
</body>
</html>
'''

HTML_RESULT = '''
<!DOCTYPE html>
<html>
<head>
    <title>Event Result</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body { font-family: Arial; margin: 50px; }
        .approved { color: green; }
        .needs_revision { color: orange; }
        .incomplete { color: red; }
    </style>
</head>
<body>
    <h1>Event Processing Result</h1>
    <p><strong>Status:</strong> <span class="{{ status_class }}">{{ status }}</span></p>
    <p><strong>Category:</strong> {{ category }}</p>
    <p><strong>Priority:</strong> {{ priority }}</p>
    <p><strong>Note:</strong> {{ note }}</p>
    <a href="/">Submit Another</a>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/result/<record_id>')
def result_page(record_id):
    try:
        resp = requests.get(f'{WORKFLOW_URL}/result/{record_id}')
        if resp.status_code == 200:
            data = resp.json()
            status = data.get('status', 'UNKNOWN')
            status_class = status.lower().replace('_', '')
            return render_template_string(HTML_RESULT,
                                        status=status,
                                        status_class=status_class,
                                        category=data.get('category', 'N/A'),
                                        priority=data.get('priority', 'N/A'),
                                        note=data.get('note', 'Processing...'))
    except:
        pass
    
    return render_template_string(HTML_RESULT,
                                status='PENDING',
                                status_class='pending',
                                category='N/A',
                                priority='N/A',
                                note='Your event is being processed...')

@app.route('/api/submit', methods=['POST'])
def submit_api():
    resp = requests.post(f'{WORKFLOW_URL}/submit', json=request.json)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)