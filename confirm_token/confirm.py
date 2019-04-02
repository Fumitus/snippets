from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
admin_email = app.config['MAIL_USERNAME']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

    email = request.form['email']
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm new user', sender='admin_email', recipients=['abaikstys@gmail.com'])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = 'A person with e-mail {} is trying to create account in FamilyBlog.' \
               ' Link to confirm this user is {}'.format(email, link)
    mail.send(msg)

    return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=300)
    except SignatureExpired:
        return '<h2>Your token is expired!</h2>'
    except BadTimeSignature:
        return '<h2>Bad token!</h2>'
    return '<h2>Token works!</h2>'


if __name__ == '__main__':
    app.run(debug=True, host='192.0.0.1', port=5000)