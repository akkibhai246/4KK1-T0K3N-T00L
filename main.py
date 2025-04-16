from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>4KK1-T0K3N-T00L</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f8f9fa; }
        .container { max-width: 600px; margin-top: 40px; }
        .footer { text-align: center; margin-top: 40px; font-weight: bold; }
    </style>
</head>
<body>
<div class="container">
    <h2 class="text-center mb-4">4KK1-T0K3N-T00L</h2>

    <form method="POST">
        <div class="mb-3">
            <label class="form-label">COOKIE PASTE INPUT</label>
            <textarea class="form-control" name="cookie" rows="2" placeholder="Paste your Facebook cookie here..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary w-100 mb-3">GET TOKEN</button>
    </form>

    {% if token_output %}
    <div class="mb-3">
        <label class="form-label">TOKEN COPY OUTPUT</label>
        <div class="input-group">
            <input type="text" class="form-control" id="tokenField" value="{{ token_output }}" readonly>
            <button class="btn btn-outline-secondary" onclick="copyToken()">Copy</button>
        </div>
    </div>
    {% endif %}

    <form method="POST">
        <div class="mb-3">
            <label class="form-label">TOKEN PASTE HERE INPUT</label>
            <input class="form-control" name="token_to_check" placeholder="Paste token to check validity">
        </div>
        <button type="submit" class="btn btn-success w-100 mb-3">CHECK TOKEN</button>
    </form>

    {% if result %}
    <div class="alert {{ 'alert-success' if result.valid else 'alert-danger' }}">
        {% if result.valid %}
            VALID TOKEN<br>
            Name: <strong>{{ result.name }}</strong><br>
            ID: <strong>{{ result.id }}</strong>
        {% else %}
            INVALID TOKEN
        {% endif %}
    </div>
    {% endif %}

    <div class="footer">@ DEVELOPED BY AKKI</div>
</div>

<script>
    function copyToken() {
        const copyText = document.getElementById("tokenField");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
        alert("Token copied!");
    }
</script>
</body>
</html>
'''

def parse_cookie(cookie_str):
    cookie_dict = dict(item.strip().split('=', 1) for item in cookie_str.split(';') if '=' in item)
    return cookie_dict.get('c_user'), cookie_dict.get('xs')

def get_token(cookie_str):
    c_user, xs = parse_cookie(cookie_str)
    if not c_user or not xs:
        return None

    session = requests.Session()
    session.cookies.update({'c_user': c_user, 'xs': xs})
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = session.get("https://business.facebook.com/business_locations", headers=headers)
    match = re.search(r"EAAG\w+", res.text)
    return match.group(0) if match else None

def check_token(token):
    url = f"https://graph.facebook.com/me?access_token={token}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return {"valid": True, "name": data.get("name"), "id": data.get("id")}
    else:
        return {"valid": False}

@app.route('/', methods=['GET', 'POST'])
def index():
    token_output = ""
    token_check_result = None

    if request.method == 'POST':
        if 'cookie' in request.form and request.form['cookie']:
            cookie = request.form['cookie']
            token_output = get_token(cookie) or "Token Not Found"
        elif 'token_to_check' in request.form and request.form['token_to_check']:
            token_to_check = request.form['token_to_check']
            token_check_result = check_token(token_to_check)

    return render_template_string(HTML_TEMPLATE, token_output=token_output, result=token_check_result)

if __name__ == '__main__':
    app.run(debug=False
    )