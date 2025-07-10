
from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1pODaqxaibp_WEek6iVBUNbIR3T5uJ9GyiBLAzmS2-nM").sheet1


@app.route('/')
def home():
    return redirect(url_for('apply'))

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        education = request.form['education']
        skills = request.form['skills']
        job = request.form['job']

        row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, age, education, skills, job]
        sheet.append_row(row)
        return redirect('/thankyou')
    return render_template('form.html')

@app.route('/thankyou')
def thankyou():
    return "<h2>Thank you for applying! ✅</h2><p>We have received your submission.</p>"

if __name__ == '__main__':
    app.run(debug=True)
