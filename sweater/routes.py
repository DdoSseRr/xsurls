from flask import render_template, redirect, url_for, request, flash
import requests

from PIL import Image
from sweater import app, db,QRcode
from sweater.models import Database
from sweater.randomizer import random_after_slash








@app.route('/get/<short_link>',methods=['GET'])
def redirecting(short_link):
    full_link = Database.query.filter_by(src_link=f'{short_link}').first()
    long_link = full_link.dest_link
    print(long_link)
    if long_link is not None:
        if long_link.startswith('http://') or long_link.startswith('https://'):
            return redirect(long_link, 301)

        elif long_link.startswith('www.'):
            return redirect(f'http://{long_link}',301)

    else:
        flash('SHORT LINK NOT EXIST')




@app.route('/',methods=['POST','GET'])
@app.route('/main',methods=['POST','GET'])
def index():

    return render_template('index.html')




@app.route('/url-shortener',methods=['POST','GET'])
def url_shortener():
    if request.method == 'POST':

        url = request.form.get('user_link')
        short_link = random_after_slash()

        userdata = Database(dest_link=url,src_link=short_link)
        db.session.add(userdata)
        db.session.commit()
        return render_template('get_xsurl_qr.html', short_link=short_link)

    return render_template('form.html')





@app.errorhandler(404)
def errror_hendler(e):

    return redirect('/main')



