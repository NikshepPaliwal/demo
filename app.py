from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "abc"

# Initialize the database and create the students table if it doesn't exist
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  email TEXT NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
init_db()
# Route to display the home page with student data
@app.route('/')
def hello():
    return render_template('index.html', stdData= [[1, "Rahul", "rahul@gmail.com"],
                                                   [2, "Raj", "raj@gmail.com"],
                                                   [3, "Ravi", "ravi@gmail.com"]])
    
# Route to display the registration form
@app.route('/registerbtn')
def registerbtn():
    return render_template('registration.html')

# Registration functionality
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        
        userName  = request.form['username']
        email = request.form['email']
        password = request.form['password']

        c.execute("INSERT INTO students (username, email, password) VALUES (?, ?, ?)", 
                  (userName, email, password))
        conn.commit()
        conn.close()

        return "Registration successful!"
    
    return redirect(url_for('registerbtn'))

# Displaying students data
@app.route('/students')
def students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    stdData = c.fetchall()
    conn.close()
    return render_template('index.html', students=stdData)



# Login functionality

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Username or Password"

    return render_template('loginPage.html')

# Dashboard route

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    return redirect(url_for('login'))




@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()  
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        c.execute("UPDATE students SET username=?, email=?, password=? WHERE id=?", 
                  (username, email, password, id))
        conn.commit()
        conn.close()
        return redirect(url_for('students'))
    

    c.execute("SELECT * FROM students WHERE id=?", (id,))
    student = c.fetchone()
    conn.close()    
    return render_template('edit.html', student=student)


@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('students'))

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3000)
