from flask import Flask, render_template, request, redirect, url_for
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import os
from dotenv import load_dotenv
from datetime import date, datetime
from pprint import pprint


app = Flask(__name__, template_folder='../templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        load_dotenv()
        uid = os.environ['FT_CLIENT_UID']
        secret = os.environ['FT_CLIENT_SECRET']

        client = BackendApplicationClient(client_id=uid)
        oauth = OAuth2Session(client=client)

        token_url = 'https://api.intra.42.fr/oauth/token'
        token = oauth.fetch_token(token_url=token_url, client_id=uid, client_secret=secret)

        name = request.form['name']
        end_point = f'https://api.intra.42.fr/v2/users/{name}'
        response = oauth.get(end_point)
        if response.status_code != 200:
            return redirect(url_for('index'))
        blackhole_date = datetime.strptime(response.json()['cursus_users'][1]['blackholed_at'].split('T')[0], '%Y-%m-%d').date()
        days_until_blackhole = (blackhole_date - date.today()).days
        return render_template('graph.html', name=name, today=date.today(), days_until_blackhole=days_until_blackhole)

if __name__ == '__main__':
    app.run(debug=True)
