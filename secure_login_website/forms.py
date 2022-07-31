''' This python file creates two classes. The first class creates a flask form
for a log in page and initializes an email address and a password field. The
second class creates a flask form for a registration form and initializes
first name, last name, email address, user pass, and user pass confirmation
fields. They both include submit fields as well.'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Length, Email, EqualTo,
                                ValidationError)
import re


def validate_pw(form, field):
    ''' This method validates that a password as at least 12 characters, a
    capital letter, a lower case letter, and a special character'''
    try:
        # Read in the user data file
        with open("CommonPassword.txt", "r") as file:
            # Format data into a 2d list
            lines = [line.replace('\n', '') for line in file]

        # If any off the unsecure words are in the user entry
        if any(substring in field.data.lower() for substring in lines):
            # Display error message
            raise ValidationError("Password contains an unsecure word. Please choose a \
            different password.")
        # If the password is not in the correct format
        if not re.match(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-_]).{12,}$",
                str(field.data)):
            # Display an error message
            raise ValidationError('Password Invalid. Must be least 12 \
            characters in length, and include at least 1 uppercase character, \
            1 lowercase character, 1 number and 1 special character.')

    # If the list does not exist, display error message
    except FileNotFoundError:
        raise ValidationError('Error saving info. Please contact customer service at \
        customerservice@admin.com')


class LoginForm(FlaskForm):

    # Create a string field for the user to enter their email address.
    # Must be in email format, else display error message
    email_address = StringField('Email Address',
                                validators=[DataRequired(),
                                            Email(message='Enter a \
                                            Valid Email')])
    # Create a string field for the user to enter their password.
    # Must be at least 12 characters long.
    user_pass = PasswordField('Password', validators=[DataRequired(),
                                                      Length(min=12,
                                                             message='Enter a Valid\
                                           Password. Must be least 12 \
                                           characters in length, and include \
                                           at least 1 uppercase character, 1 \
                                           lowercase character, 1 number and 1\
                                            special character.')])

    # Create a submit button to submit field
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):

    # Create a string field for the user to enter their first name.
    # Must be between 1 and 20 characters.
    first_name = StringField('First Name',
                             validators=[DataRequired(),
                                         Length(min=1, max=20,
                                                message='Enter a Valid First \
                                                Name')])

    # Create a string field for the user to enter their last name.
    # Must be between 1 and 20 characters.
    last_name = StringField('Last Name',
                            validators=[DataRequired(),
                                        Length(min=1, max=20,
                                               message='Enter a Valid Last \
                                               Name')])

    # Create a string field for the user to enter their email address.
    # Must be in email format.
    email_address = StringField('Email Address',
                                validators=[DataRequired(),
                                            Email(message='Enter a Valid Email\
                                            ')])

    # Create a string field for the user to enter their password.
    # Must be at least 12 characters long.
    user_pass = PasswordField('Password',
                              validators=[DataRequired(),
                                          Length(min=12), validate_pw])

    # Create a string field for the user to re-enter their password.
    # Must match the previously entered password.
    confirm_user_pass = PasswordField('Confirm Password',
                                      validators=[DataRequired(),
                                                  EqualTo('user_pass',
                                                          message='Passwords \
                                                          Must Match')])

    # Create a submit button to submit field
    submit = SubmitField('Register')


class UpdatePassword(FlaskForm):

        # Create a string field for the user to enter their current password.
    # Must be at least 12 characters long.
    current_pass = PasswordField('Current Password',
                                 validators=[DataRequired(),
                                             Length(min=12)])

    # Create a string field for the user to enter their new password.
    # Must be at least 12 characters long.
    new_pass = PasswordField('New Password',
                             validators=[DataRequired(),
                                         Length(min=12), validate_pw])

    # Create a string field for the user to re-enter their password.
    # Must match the previously entered password.
    confirm_user_pass = PasswordField('Confirm Password',
                                      validators=[DataRequired(),
                                                  EqualTo('new_pass',
                                                          message='Passwords \
                                                          Must Match')])

    # Create a submit button to submit field
    submit = SubmitField('Register')
