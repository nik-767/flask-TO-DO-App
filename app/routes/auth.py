from flask import Blueprint , render_template , request , redirect , url_for , flash , session

auth_bp = Blueprint('auth' , __name__ )

USER_CRE = {
    'username' : 'admin',
    'password' : '1234'
}

@auth_bp.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USER_CRE['username'] and password == USER_CRE['password']:
            session['user'] = username
            flash('login successful', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('invalid username or password', 'danger')

    return render_template('login.html')


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # in a real app you'd save these to a database; here we just overwrite the credentials
        USER_CRE['username'] = username
        USER_CRE['password'] = password
        flash('registration successful, please log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('logged out','info')
    return redirect(url_for('auth.login'))
