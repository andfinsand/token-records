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

######################################################## Main Content ##############################################################

@app.route('/sold')
def sold():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    nfts = Nft.get_all()


    return render_template('/sold/sold.html' , user = user , nfts = nfts)

###################################################### Add New Sold #############################################

@app.route('/sold_new')
def add_new_sold():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
    "id":session['user_id']
    }
    return render_template('/sold/sold_new.html' , user = User.get_by_id(data))

############################################# Process New Sold Form #############################################

@app.route('/process_new_sold' , methods=['POST'])
def process_new_sold():
    if 'user_id' not in session:
        return redirect('/logout')
        # return render_template("collection/collection.html", uploaded_image=image.filename)

    # Display image without DB*****************************

    # if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect('/collection_new')
    # file = request.files['file']
    # if file.filename == '':
    #     flash('No image selected for uploading')
    #     return redirect('/collection_new')
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     return render_template('/collection/collection.html' , filename = filename)
    # else:
    #     flash('Allowed image types are - png, jpg, jpeg, gif')
    #     return redirect('/collection_new')
        #*************************************************
    # if not Nft.validate_title(request.form):
    #     return redirect ('/new_collection')
    if request.files:
        image = request.files["image"]
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))


    metadata_collection_name = ""
    data = {
        "image_name" : image.filename,
        "status" : request.form["status"],
        "collection_name" : request.form['collection_name'],
        "token_number": request.form['token_number'],
        "collection_link_to_exchange": request.form['collection_link_to_exchange'],
        "purchase_price": request.form['purchase_price'],
        "date_of_purchase": request.form['date_of_purchase'],
        "date_of_sale": request.form['date_of_sale'],
        "trade_fees": request.form['trade_fees'],
        "has_staking": request.form['has_staking'],
        "notes": request.form['notes'],
        "is_for_sale": request.form['is_for_sale'],
        "sale_price": request.form['sale_price'],
        "link_to_sale": request.form['link_to_sale'],
        "mint_address": request.form['mint_address'],
        "metadata_collection_name": metadata_collection_name,
        "user_id": session["user_id"]
    }
    # return redirect(f'/main/{id}')
    Nft.create(data)

    return redirect('/sold')

############################################################ Edit Sold ####################################################

@app.route('/sold/edit/<int:id>')
def edit_sold(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template('sold/sold_edit.html', edit = Nft.get_by_id(data) , user=User.get_by_id(user_data))

###########################################3########### Process Edit Sold Form ################################################

@app.route('/process_edit_sold', methods=['POST'])
def update_sold():
    if 'user_id' not in session:
        return redirect('/logout')

    # if not Nft.validate_title(request.form):
    #     page = request.form['id']
    #     return redirect (f'/main/edit/{page}')

    if request.files:
        image = request.files["image"]
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))

    data = {
        "nft_id" : request.form["nft_id"],
        "status" : request.form["status"],
        "collection_name" : request.form['collection_name'],
        "token_number": request.form['token_number'],
        "collection_link_to_exchange": request.form['collection_link_to_exchange'],
        "purchase_price": request.form['purchase_price'],
        "date_of_purchase": request.form['date_of_purchase'],
        "date_of_sale": request.form['date_of_sale'],
        "trade_fees": request.form['trade_fees'],
        "has_staking": request.form['has_staking'],
        "notes": request.form['notes'],
        "sale_price": request.form['sale_price'],
        "link_to_sale": request.form['link_to_sale'],
        "user_id": session["user_id"]
    }
    Nft.update_sold(data)
    return redirect('/sold')

##################################################### Sold View ####################################################

@app.route('/sold_view/<int:id>')
def sold_view(id):
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

    return render_template('/sold/sold_view.html' , user = User.get_by_id(user_data) , nft = nft , image = image)

############################################ Add new NFT Sold FROM COLLECTION #####################################

@app.route('/sold/sold_from_collection/<int:id>')
def add_from_collection(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template('/sold/sold_from_collection.html', nft = Nft.get_by_id(data) , user=User.get_by_id(user_data))

############################################## Process new sold FROM COLLECTION form ##########################################

@app.route('/process_from_collection' , methods=['POST'])
def process_from_collection():
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
        "purchase_price": request.form['purchase_price'],
        "date_of_purchase": request.form['date_of_purchase'],
        "date_of_sale": request.form['date_of_sale'],
        "trade_fees": request.form['trade_fees'],
        "has_staking": request.form['has_staking'],
        "notes": request.form['notes'],
        "is_for_sale": request.form['is_for_sale'],
        "sale_price": request.form['sale_price'],
        "link_to_sale": request.form['link_to_sale'],
        "user_id": session["user_id"]
    }
    Nft.update(data)

    return redirect('/sold')

########################################################### Delete NFT ##########################################################

@app.route('/destroy_sold/nft/<int:id>')
def destroy_sold(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Nft.destroy(data)
    return redirect('/sold')