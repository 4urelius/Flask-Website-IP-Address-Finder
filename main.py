from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import socket

app = Flask(__name__)
app.secret_key = ''
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)

class ip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(15), nullable=False)

class contact_form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(1000), nullable=False)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        try:
            url = request.form['url']
            if len(url) > 0:
                ip_address = socket.gethostbyname(url)
                data = ip(url=url, ip=ip_address)
                db.session.add(data)
                db.session.commit()
                flash('The IP address of ' + url + ' is ' + ip_address)
                return redirect('/')
            else:
                flash('The URL field was empty.')
                return redirect('/')
        except:
            flash('Invalid URL')
            return redirect('/')
    else:
        ip_addresses = ip.query.order_by(desc(ip.id)).limit(20).all()
        return render_template('index.html', ip_addresses=ip_addresses)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        topic = request.form['topic']
        email = request.form['email']
        message = request.form['message']
        data = contact_form(topic=topic, email=email, message=message)
        try:
            db.session.add(data)
            db.session.commit()
            flash('Contact form submitted.')
            return redirect('/contact')
        except:
            flash('Something went wrong.')
            return redirect('/contact')
    else:
        return render_template('contact.html')

if __name__ == '__main__':
    app.run()
