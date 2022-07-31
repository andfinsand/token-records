from flask_app import application
from flask import render_template, redirect, session, request, flash, url_for
from flask_app.models.user import User
from flask_app.models.nft import Nft
import os
import requests
import json
import decimal

UPLOAD_FOLDER = 'flask_app/static/uploads/'
application.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##################################################### Collection Main Content ##########################################################

@application.route('/collection')
def collection():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }

################# API FLOOR PRICE ###########

    user = User.get_by_id(data)
    nfts = Nft.get_all()
    new_list = []

    for new in nfts:
        if new.status == 0 and new.user_id == data['id']:
            new_list.append(new)
            print(new.collection_name)
    for nft in new_list:
        if nft.metadata_collection_name:

            response = requests.get(f"https://api-mainnet.magiceden.dev/v2/collections/{nft.metadata_collection_name}/stats")
            floor = json.loads(response.content)
            floor_price = floor['floorPrice']
            print(floor_price)

            def move_point(number, shift, base = 10):
                return number * base**shift

            floor_math_decimal = decimal.Decimal(move_point( floor_price , -9))
            nft.floor_price = decimal.Decimal("{:.2f}".format(floor_math_decimal))

    return render_template('/collection/collection.html' , user = user , nfts = new_list )

#################################################### Add new NFT Collection ##########################################################

@application.route('/collection_new')
def add_new_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
    "id":session['user_id']
    }
    return render_template('/collection/collection_new.html' , user = User.get_by_id(data))

####################################################### Process new collection form #################################################

@application.route('/process_new_collection' , methods=['POST'])
def process_new_collection():
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
        image.save(os.path.join(application.config["UPLOAD_FOLDER"], image.filename))

    mint_address = request.form['mint_address']
    if len(mint_address) > 0:

        mint_response = requests.get(f"https://api-mainnet.magiceden.dev/v2/tokens/{mint_address}")
        mint = json.loads(mint_response.content)
        metadata_collection_name = mint['collection']

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

        Nft.create(data)

    elif len(mint_address) <= 0:
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

        Nft.create(data)

    return redirect('/collection')

############################################################ Edit Collection ####################################################

@application.route('/collection/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template('collection/collection_edit.html', edit = Nft.get_by_id(data) , user=User.get_by_id(user_data))

###########################################3########### Process Edit Collection Form ################################################

@application.route('/process_edit_collection', methods=['POST'])
def update():
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
    Nft.update_collection(data)
    return redirect('/collection')

##################################################### Collection VIEW NFT ########################################################

@application.route('/collection_view/<int:id>')
def collection_view(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id ,
    }
    user_data = {
        "id" : session['user_id']
    }

################# API FLOOR PRICE BEGIN###########

    get_nft = Nft.get_mint(data)
    if len(get_nft.metadata_collection_name) > 0:

        response = requests.get(f"https://api-mainnet.magiceden.dev/v2/collections/{get_nft.metadata_collection_name}/stats")
        floor = json.loads(response.content)
        floor_price = floor['floorPrice']
        print(floor_price)

        def move_point(number, shift, base = 10):
            return number * base**shift

        floor_math_decimal = decimal.Decimal(move_point( floor_price , -9))
        floor_math = decimal.Decimal("{:.2f}".format(floor_math_decimal))

        nft = Nft.get_by_id(data)
        image = url_for('static' , filename = 'uploads/' + nft.image_name)

    elif len(get_nft.metadata_collection_name) == 0:

################# API FLOOR PRICE END############

        floor_math = -1
        nft = Nft.get_by_id(data)
        image = url_for('static' , filename = 'uploads/' + nft.image_name)

    return render_template('/collection/collection_view.html' , user = User.get_by_id(user_data) , nft = nft , image = image , floor = floor_math )

########################################################## COLLECTION FROM WATCHLIST ############################################

@application.route('/collection/collection_from_watchlist/<int:id>')
def add_from_watchlist(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template('/collection/collection_from_watchlist.html', nft = Nft.get_by_id(data) , user=User.get_by_id(user_data))

####################################### Process new Collection FROM Watchlist form ################################################

@application.route('/process_from_watchlist' , methods=['POST'])
def process_from_watchlist():
    if 'user_id' not in session:
        return redirect('/logout')

    if request.files:
        image = request.files["image"]
        image.save(os.path.join(application.config["UPLOAD_FOLDER"], image.filename))

    data = {
        "nft_id" : request.form["nft_id"],
        "status" : request.form["status"],
        "collection_name" : request.form['collection_name'],
        "token_number": request.form['token_number'],
        "collection_link_to_exchange": request.form['collection_link_to_exchange'],
        "purchase_price": request.form['purchase_price'],
        "date_of_purchase": request.form['date_of_purchase'],
        "trade_fees": request.form['trade_fees'],
        "has_staking": request.form['has_staking'],
        "notes": request.form['notes'],
        "is_for_sale": request.form['is_for_sale'],
        "sale_price": request.form['sale_price'],
        "link_to_sale": request.form['link_to_sale'],
        "mint_address": request.form['mint_address'],
        "user_id": session["user_id"]
    }
    Nft.update_from_watchlist(data)

    return redirect('/collection')

################################################################ Delete NFT #########################################################

@application.route('/destroy/nft/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Nft.destroy(data)
    return redirect('/collection')

########################################################## Resources ###################################################################
@application.route('/resources')
def resources():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('/resources/resources.html' , user=User.get_by_id(data))

########################################################## SOLANA CHART ###################################################################
@application.route('/solana_chart')
def solana_chart():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('/solana_chart/solana_chart.html' , user=User.get_by_id(data))