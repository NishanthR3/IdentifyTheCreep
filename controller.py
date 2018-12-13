from flask import Flask, render_template, request, abort
from flask import redirect, url_for, request, session
from ML_obj import ML_obj
from werkzeug.utils import secure_filename
import model
import submission_history
import os

# Global variables and utility function
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'ogg', 'm4a'])
UPLOAD_FOLDER = './uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


clt = ML_obj()

# Create the application and set it up
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'

# Homepage


@app.route('/', methods=['GET', 'POST'])
def homepage():
    # Regular requests
    if request.method == 'GET':
        return render_template("index.html")
    # Sign up form submissions
    if request.method == 'POST':
        try:
            # Check if user already exists or not
            if model.register(request):
                # return render_template("dashboard.html", name=request.form["username"])
                return render_template("index.html", success=True)
            else:
                return render_template("index.html", failed=True)
        except:
            return render_template("index.html", error=True)

#Sign in page


@app.route('/sign_in')
def sign_in():
    return render_template("sign_in.html")

# User's Dashboard
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    # Authenticate the user
    if request.method == 'GET':
        try:
            if session['username']:
                return render_template("dashboard.html", name=session["username"])
            else:
                abort(401)
        except:
            abort(401)
    else:
        if model.authenticate(request):
            return render_template("dashboard.html", name=session["username"])
        else:
            return render_template("sign_in.html", failed=True)

# File submission page


@app.route('/input')
def input():
    try:
        if session['username']:
            return render_template("input.html")
        else:
            abort(401)
    except:
        abort(401)

# Result output page


@app.route('/output', methods=['GET','POST'])
def output():
    if request.method == 'GET':
        abort(400)
    elif request.method == 'POST':
        # Check that two files have been uploaded
        if 'file1' not in request.files or 'file2' not in request.files:
            print('No file part')
            return redirect(request.url)
        file1 = request.files['file1']
        file2 = request.files['file2']
        if file1.filename == '' or file2.filename == '':
            print('No selected file')
            return redirect(request.url)
        # Make sure they are allowed: audio files
        if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
            # Store the files temporarily and securely
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            # Get the percentage match and then remove the files
            perc = clt.get_percentage(filename1, filename2)
            submission_history.add_submission(
                session['username'], perc, filename1, filename2)
            os.system("rm " + UPLOAD_FOLDER + '/' + filename1)
            os.system("rm " + UPLOAD_FOLDER + '/' + filename2)
            return render_template("output.html", percentage=perc, file1=filename1, file2=filename2)

# Past submission page


@app.route('/showall')
def showall():
    try:
        rows = submission_history.get_user_submissions(session['username'])
        return render_template('showall.html', rows=rows)
    except:
        abort(401)

# logout page


@app.route('/logout')
def logout():
    if 'username' in session:
        name = session.pop('username')
        return render_template('logout.html', msg="you are logged out")
    return render_template('logout.html', msg="you are already logged out")


if __name__ == '__main__':
    model.create()
    submission_history.create()
    app.debug = True
    app.run()
