import os
import jinja2
from flask import Flask, request, redirect

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template("input-form.html")
    return template.render()

def length_test(input_string):
    #if len(input_text) < 3 or len(input_text) > 20: "Must be 3-20 characters in length"
    if len(input_string) > 20:
        return False
    elif len(input_string) < 3:
        return False
    else:
        return True

@app.route("/validate-form", methods=["POST"])
def validate_form():
    #initialize jinja template
    template = jinja_env.get_template("input-form.html")

    #validate username
    username = request.form["username"]
    username_error = ""
    if " " in username:
        username_error = "Username must not contain spaces"
        username = ""
    elif not length_test(username):
        username_error = "Username must be 3-20 characters in length"
        username = ""
    
    #validate password_initial
    password_initial = request.form["password_initial"]
    password_initial_error = ""
    if " " in password_initial:
        password_initial_error = "Password must not contain spaces"
        password_initial = ""
    elif not length_test(password_initial):
        password_initial_error = "Password must be 3-20 characters in length"
        password_initial = ""

    #validate password_verify (match)
    password_verify = request.form["password_verify"]
    password_verify_error = ""
    #if password_initial != password_verify: "Passwords do not match"
    if password_initial != password_verify:
        password_verify_error = "Passwords do not match"
        password_verify = ""

    #validate email
    email = request.form["email"]
    email_error = ""
    #if email = False: fine
    #if email = True and ("@" not in email or "." not in email): "Must provide a valid email address"
    if email and (("@" not in email) or ("." not in email)):
        email_error = "Must provide a valid email address"
        email = ""
    
    if not username_error and not password_initial_error and not password_verify_error and not email_error:
        return redirect("/registration-successful")
    else:
        return template.render(
            username=username, 
            username_error=username_error, 
            password_initial=password_initial, 
            password_initial_error=password_initial_error, 
            password_verify=password_verify, 
            password_verify_error=password_verify_error, 
            email=email, 
            email_error=email_error
            )

app.run()