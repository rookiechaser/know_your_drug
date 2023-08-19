from flask import Flask, render_template, request
import sqlite3
import csv
import zipfile
import io  # For working with in-memory streams

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword1 = request.form.get('keyword1', '')
        keyword2 = request.form.get('keyword2', '')

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        # Age,Condition,Date,Drug,DrugId,EaseofUse,Effectiveness,Reviews,Satisfaction,Sex,Sides,UsefulCount
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS med_data (
                Age INTEGER,
                Condition TEXT,
                Date TEXT,
                Drug TEXT,
                DrugId INTEGER,
                EaseofUse INTEGER,
                Effectiveness INTEGER,
                Reviews TEXT,
                Satisfaction INTEGER,
                Sex TEXT,
                Sides TEXT,
                UsefulCount INTEGER          
            )
        ''')

        # Extract the CSV file from the ZIP archive
        with zipfile.ZipFile('data.zip') as zip_file:
            csv_filename = 'data.csv'
            with zip_file.open(csv_filename) as csv_file:
                csv_data = csv_file.read().decode('utf-8')

        # Read data from the extracted CSV data and insert into the database
        csv_io = io.StringIO(csv_data)
        csv_reader = csv.reader(csv_io)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            cursor.execute('INSERT INTO med_data (Age,Condition,Date,Drug,DrugId,EaseofUse,Effectiveness,Reviews,Satisfaction,Sex,Sides,UsefulCount) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', row)

        # Commit changes and close the connection
        conn.commit()
        cursor.execute("SELECT * FROM med_data WHERE Drug LIKE ? AND condition LIKE ?", ('%' + keyword1 + '%', '%' + keyword2 + '%'))
        data = cursor.fetchall()
        conn.close()

        return render_template('index.html', data=data)
    
    return render_template('index.html', data=None)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
