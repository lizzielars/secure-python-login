''' This program creates a website that displays a 3 day workout week. Each day
has a separate page with the necessary exercises and links to videos showing
proper technique. The website also includes log in and registration pages. If
the user does not log in or register, they will not be able to access the rest
of the website.'''

__author__ = "Elizabeth Larson"


from datetime import datetime
from flask import (Flask, render_template, flash, redirect, url_for, request,
                   session)
from passlib.hash import sha256_crypt
from week_8_website.forms import RegisterForm, LoginForm, UpdatePassword


app = Flask(__name__)


# Set secret key to protect against modifying cookies, crosssite requests,
# forgary attacks, etc.
app.config['SECRET_KEY'] = 'e87369226e0f1fe37a009a94e41f7f76'

# Initializes workout information
workouts = [
    {
        'workout': 'Chest, Triceps, & Shoulders',
        'equipment': 'Dumbells & Bench',
        'time': '30 Minutes'
    },
    {
        'workout': 'Legs',
        'equipment': 'Barbell & Dumbbells',
        'time': '60 Minutes'
    },
    {
        'workout': 'Back & Biceps',
        'equipment': 'Pullup Bar & Dumbbells',
        'time': '45 Minutes'}
]

# Gets the current day and time
current_date_time = datetime.now()
displayed_date_time = current_date_time.strftime("%m/%d/%Y, %H:%M")


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    ''' This method renders a template for the login page of the website. It
    reads in the html for the log in page.'''
    # Initializes log in form
    form = LoginForm()
    if request.method == "POST":
        # If form validated
        if form.validate_on_submit():
            # If the username and password match
            if verify_login(form.email_address.data, form.user_pass.data):
                session['email'] = form.email_address.data
                # Print confirmation and redirect to home page
                flash('Logged In')
                return redirect(url_for('home'))
            # Else print error
            flash('Invalid Username/Password. Please Try Again')
        append_login_attempt()

    return render_template('login.html', title='3 Day Workout Plan', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    ''' This method renders a template for the login page of the website. It
    reads in the html for the log in page.'''
    form = RegisterForm()
    if request.method == "POST":
        if verify_user(form.email_address.data):
            flash('User Name Already Taken. Please Enter a Different Email.')
            return redirect(url_for('register'))
        if form.validate_on_submit():
            session['email'] = form.email_address.data
            append_new_user(form.first_name.data, form.last_name.data,
                            form.email_address.data, form.user_pass.data)
            flash(f'Account Created for {form.first_name.data} \
            {form.last_name.data}')
            return redirect(url_for('home'))
    return render_template('register.html', title='3 Day Workout Plan',
                           form=form)


@app.route("/updatepass", methods=['GET', 'POST'])
def updatepass():
    ''' This method renders a template for the password reset page of the
    website. It reads in the html for the updatepass page.'''

    if not session.get('email'):
        flash('Please log in to access the Home Page')
        return redirect(url_for('login'))

    form = UpdatePassword()

    if request.method == "POST":
        if form.validate_on_submit():
            if verify_login(session['email'], form.current_pass.data):
                set_new_pass(form.new_pass.data)
                del session['email']
                flash('Password Updated.')
                return redirect(url_for('login'))
            flash('Current password incorrect. Please re-enter.')
            return redirect(url_for('updatepass'))

    return render_template('updatepass.html', title='3 Day Workout Plan',
                           form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    ''' This method clears the session and logs the user out. It then redirects
    the user to the log in page.'''

    # If the session does not have a user name assigned, user was never logged
    # in.
    if not session.get('email'):
        flash('You were not logged in')
        return redirect(url_for('login'))
    # Else delete session and redirect to log in page
    del session['email']
    flash('You are successfully logged out!')
    return redirect(url_for('login'))


@app.route("/home")
def home():
    ''' This method renders a template for the home page of the website. It
    reads in the html for the home page, the workouts to be displayed, the
    title,  and the current date and time. '''

    # If user not logged in, redirect to log in page and display an error
    # message
    if not session.get('email'):
        flash('Please log in to access the Home Page')
        return redirect(url_for('login'))

    # Otherwise, render home page
    return render_template('home.html', workouts=workouts, title="Home",
                           datetime=displayed_date_time)


@app.route("/day1")
def day1():
    ''' This method renders a template for the day 1 page of the website. It
    reads in the html for the day 1 page, the workout information for day 1,
    the title, and the current date and time. '''

    # If user not logged in, redirect to log in page and display an error
    # message
    if not session.get('email'):
        flash('Please log in to access the Day 1 Workout Page')
        return redirect(url_for('login'))

    # Otherwise, render day1 page
    return render_template('day1.html', workout=workouts[0], title='Day 1',
                           datetime=displayed_date_time)


@app.route("/day2")
def day2():
    ''' This method renders a template for the day 2 page of the website. It
    reads in the html for the day 2 page, the workout information for day 2,
    the title, and the current date and time. '''

    # If user not logged in, redirect to log in page and display an error
    # message
    if not session.get('email'):
        flash('Please log in to access the Day 2 Workout Page')
        return redirect(url_for('login'))

    # Otherwise, render day2 page
    return render_template('day2.html', workout=workouts[1], title='Day 2',
                           datetime=displayed_date_time)


@app.route("/day3")
def day3():
    ''' This method renders a template for the day 3 page of the website. It
    reads in the html for the day 3 page, the workout information for day 3,
    the title, and the current date and time. '''

    # If user not logged in, redirect to log in page and display an error
    # message
    if not session.get('email'):
        flash('Please log in to access the Day 3 Workout Page')
        return redirect(url_for('login'))
    # Otherwise, render day3 page
    return render_template('day3.html', workout=workouts[2], title='Day 3',
                           datetime=displayed_date_time)


def verify_login(entered_username, entered_pass):
    ''' This method verifies that the log in information is in the user date
    file'''

    # Creates a 2d list of the txt file contents
    stored_info = read_in_file()

    # For each row in the list
    for item, row in enumerate(stored_info):
        # For each column in the list
        for column in enumerate(row):
            # If the entered username is in the column
            if entered_username in column:
                # Check if the user entered pass matches the stored one
                return bool(sha256_crypt.verify(entered_pass,
                                                stored_info[item][4]))

    return False


def verify_user(entered_username):
    ''' This method verifies is a username has already been entered'''

    # Creates a 2d list of the txt file contents
    stored_info = read_in_file()

    # If the user entered email address is in the list, return True
    if any(entered_username in row for row in stored_info):
        return True
    # Else return false
    return False


def append_new_user(new_first, new_last, new_email, new_user_pass):
    ''' This method adds new user information to csv'''

    # Create a list of the user entered registration information
    row = [str(calc_new_user_id()), new_first, new_last, new_email,
           sha256_crypt.hash(new_user_pass)]

    # Append the list to the end of the user data file
    with open('user_info.txt', 'a') as users:
        users.write("\n" + "\t".join(row))


def read_in_file():
    ''' This function reads in the user file and returns a list of the
    information.'''
    try:
        # Read in the user data file
        with open("user_info.txt", "r") as file:
            # Format data into a 2d list
            lines = [line.replace('\n', '').split("\t") for line in file]

    # If the list does not exist, display error message
    except FileNotFoundError:
        flash('Error saving info. Please contact customer service at \
        customerservice@admin.com')

    # Return list
    return lines


def calc_new_user_id():
    ''' This method determines what a new user's id will be'''

    # Creates a 2d list of the txt file contents
    stored_info = read_in_file()
    # Returns the number of rows that are in the file
    return len(stored_info)


def get_user_id(entered_username):
    ''' This method gets the user id based on the user's input username.'''
    stored_info = read_in_file()

    for item, row in enumerate(stored_info):
        for column in enumerate(row):
            if entered_username in column:
                return stored_info[item][0]
            # Else return false
            return False


def set_new_pass(new_pass):
    ''' This method sets the current user's password to the new password they
    entered.'''

    # Read in the user data file
    stored_info = read_in_file()

    user_id = get_user_id(session['email']) - 1

    stored_info[user_id][4] = sha256_crypt.hash(new_pass)

    # Write the list to the user data file
    with open('user_info.txt', 'w') as users:
        for row in stored_info:
            users.write('\t'.join([str(item) for item in row]) + '\n')


def append_login_attempt():
    ''' This method logs failed log in attempts and stores them in a file.'''

    date_time = datetime.now()
    formatted_date = date_time.strftime("%m/%d/%Y")
    formatted_time = date_time.strftime("%H:%M")
    # Create a list of the user entered registration information
    row = [formatted_date, formatted_time, request.remote_addr]

    # Append the list to the end of the user data file
    with open('failed_logins.txt', 'a') as users:
        users.write("\n" + "\t".join(row))
