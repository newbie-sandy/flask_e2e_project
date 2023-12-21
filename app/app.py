from flask import Flask, redirect, url_for, render_template, session
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '7f1b2002b88b850f561cdd76578e8ccc'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://shangdancloud504:Yd9903155@hostname:35.203.121.71/final-e2e'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='421997200535-miej8ggm817jl999jan1p5k3n1sts97t.apps.googleusercontent.com',  # Replace with your Google OAuth client ID
    consumer_secret='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',  # Replace with your Google OAuth client secret
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    return 'Welcome to Water Tracker!'

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return 'Logged out'

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    return f'Logged in as: {user_info.data["email"]}'

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)

class WaterEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount_consumed = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<WaterEntry {self.date} - {self.amount_consumed} liters>'

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
