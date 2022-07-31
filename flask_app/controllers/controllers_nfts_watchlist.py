from flask_app import app
from flask import render_template, redirect, session, request, flash, url_for
from flask_app.models.user import User
from flask_app.models.nft import Nft
import os

UPLOAD_FOLDER = 'flask_app/static/uploads/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

####################################################### Main Content #############################################

@app.route('/watchlist')
def watchlist():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    nfts = Nft.get_all()

    return render_template('/watchlist/watchlist.html' , user = user , nfts = nfts)

###################################################### Add New Watchlist #############################################

@app.route('/watchlist_new')
def add_new_watchlist():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
    "id":session['user_id']
    }
    return render_template('/watchlist/watchlist_new.html' , user = User.get_by_id(data))

############################################# Process New Watchlist Form #############################################

@app.route('/process_new_watchlist' , methods=['POST'])
def process_new_watchlist():
    if 'user_id' not in session:
        return redirect('/logout')
    if request.files:
        image = request.files["image"]
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))

    data = {
        "image_name" : image.filename,
        "status" : request.form["status"],
        "collection_name" : request.form['collection_name'],
        "token_number": request.form['token_number'],
        "collection_link_to_exchange": request.form['collection_link_to_exchange'],
        "trade_fees": request.form['trade_fees'],
        "bid_price": request.form['bid_price'],
        "has_staking": request.form['has_staking'],
        "notes": request.form['notes'],
        "sale_price": request.form['sale_price'],
        "link_to_sale": request.form['link_to_sale'],
        "mint_address": request.form['mint_address'],
        "user_id": session["user_id"]
    }
    # return redirect(f'/main/{id}')
    Nft.create_watchlist(data)

    return redirect('/watchlist')

############################################# Edit Watchlist #############################################

@app.route('/watchlist/edit/<int:id>')
def edit_watchlist(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template('watchlist/watchlist_edit.html', edit = Nft.get_by_id(data) , user=User.get_by_id(user_data))

############################################# Process Edit Watchlist Form #############################################

@app.route('/process_edit_watchlist', methods=['POST'])
def update_watchlist():
    if 'user_id' not in session:
        return redirect('/logout')

    if request.files:
        image = request.files["image"]
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))

    data = {
        "nft_id" : request.form["nft_id"],
        "status" : request.form["status"],
        "collection_name" : request.form['collection_name'],
        "token_number": request.form['token_number'],
        "collection_link_to_exchange": request.form['collection_link_to_exchange'],
        "trade_fees": request.form['trade_fees'],
        "bid_price": request.form['bid_price'],
        "has_staking": request.form['has_staking'],
        "notes": request.form['notes'],
        "sale_price": request.form['sale_price'],
        "link_to_sale": request.form['link_to_sale'],
        "user_id": session["user_id"]
    }
    Nft.update_watchlist(data)
    return redirect('/watchlist')

############################################# Watchlist View #############################################

@app.route('/watchlist_view/<int:id>')
def watchlist_view(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id ,
    }
    user_data = {
        "id" : session['user_id']
    }

    nft = Nft.get_by_id(data)
    image = url_for('static' , filename = 'uploads/' + nft.image_name)

    return render_template('/watchlist/watchlist_view.html' , user = User.get_by_id(user_data) , nft = nft , image = image)

################################################ Delete NFT ################################################

@app.route('/destroy_watchlist/nft/<int:id>')
def destroy_watchlist(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Nft.destroy(data)
    return redirect('/watchlist')