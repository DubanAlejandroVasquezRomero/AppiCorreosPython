from flask import (
    Blueprint ,
    render_template,
    request,
    flash, 
    redirect,
    url_for,
    current_app
)
import resend
from resend.emails import *
from resend.api_keys import *
import os


from app.db import get_db

bp = Blueprint ('mail', __name__, url_prefix="/")

@bp.route ('/', methods = ['GET'])
def index ():
    db, c = get_db ()

    c.execute("SELECT * FROM email")
    mails = c.fetchall()
    return render_template ('mails/index.html',mails=mails)

@bp.route ('/create',methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        email = request.form.get ('email')
        subject = request.form.get ('subject')
        content = request.form.get ('content')
        errors = []

        if not email:
            errors.append ('Email es Obligatorio')

        if not subject:
            errors.append ('Asunto es Obligatorio')
        
        if not content:
            errors.append ('Contenido es Obligatorio')

        if len (errors) == 0:
            db , c = get_db()
            c.execute("INSERT INTO email (email,subject,content) VALUES (%s,%s,%s)",(email,subject,content))
            db.commit()

            return redirect (url_for('mail.index'))
        else:
            for error in errors:
                flash(error)
    return render_template('mails/create.html')








