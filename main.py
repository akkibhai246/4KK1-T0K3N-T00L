from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>4KK1-T0K3N-T00L</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h2>4KK1-T0K3N-T00L</h2>
    <form method="post" action="/get-token">
        <textarea name="cookie" rows="4" cols="60" placeholder="COOKIE PASTE INPUT" required></textarea><br><br>
        <button type="submit">GET TOKEN</button>
    </form>

    {% if token %}
    <h3>Access Token:</h3>
    <textarea rows="2" cols="60" readonly>{{ token }}</textarea>
    {% endif %}

    <hr style="margin: 40px 0;">

    <form method="post" action="/check-token">
        <textarea name="token" rows="2" cols="60" placeholder="TOKEN PASTE HERE INPUT" required></textarea><br><br>
        <button type="submit">CHECK TOKEN</button>
    </form>

    {% if result %}
    <h3>Token Status:</h3>
    <p>{{ result }}</p>
    {% endif %}

    <p style="margin-top: 60px;">@ DEVELOPED BY AKKI</p>
</body>
</html>
'''

def get_token_from_cookie(cookie):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Cookie': cookie
        }
        response = requests.get('https://business.facebook.com/business_locations', headers=headers)
        token = re.search(r'EAAG\w+', response.text)
        return token.group(0) if token else None
    except:
        return None

def check_token_validity(token):
    url = f'https://graph.facebook.com/me?fields=id,name&access_token={token}'
    response = requests.get(url).json()
    if 'id' in response:
        return f"VALID - Name: {response['name']}, ID: {response['id']}"
    elif 'error' in response:
        return "INVALID TOKEN"
    return "UNKNOWN ERROR"

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get-token', methods=['POST'])
def get_token():
    cookie = request.form['cookie']
    token = get_token_from_cookie(cookie)
    return render_template_string(HTML_TEMPLATE, token=token)

@app.route('/check-token', methods=['POST'])
def check_token():
    token = request.form['token']
    result = check_token_validity(token)
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    