from flask_app import app
from flask import render_template, redirect, session, request, flash, url_for
from flask_app.models.user import User
from flask_app.models.nft import Nft
import os
import requests
import json
import decimal

UPLOAD_FOLDER = 'flask_app/static/uploads/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##################################################### Collection Main Content ##########################################################

@app.route('/collection')
def collection():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }

    ############### API TEST FLOOR PRICE BEGIN###########

    # url = "https://api-mainnet.magiceden.dev/v2/collections/akari/stats"

    # payload={}
    # headers = {}

    # response = requests.request("GET", url, headers=headers, data=payload)
    # floor = json.loads(response.content)
    # floor_price = floor['floorPrice']
    # print(response.text)
    # def move_point(number, shift, base = 10):
    #     return number * base**shift

    # new = move_point( floor_price , -9)

############### API TEST FLOOR PRICE END 1 ###########

################# API TEST FLOOR PRICE BEGIN 2 ###########

    user = User.get_by_id(data)
    nfts = Nft.get_all()
    with_mint = []
    no_mint = []
    new_list = []

    for new in nfts:
        if new.status == 0:
            new_list.append(new)

    for nft in new_list:
        if nft.mint_address:

            mint_response = requests.get(f"https://api-mainnet.magiceden.dev/v2/tokens/{nft.mint_address}")
            mint = json.loads(mint_response.content)
            collection_name = mint['collection']
            print(collection_name)


            response = requests.get(f"https://api-mainnet.magiceden.dev/v2/collections/{collection_name}/stats")
            floor = json.loads(response.content)
            floor_price = floor['floorPrice']
            print(floor_price)

            # nft.floor_price = str(floor_price).strip("0") + "0"

            #function inside loop is not good practice
            def move_point(number, shift, base = 10):
                return number * base**shift

            floor_math_decimal = decimal.Decimal(move_point( floor_price , -9))
            nft.floor_price = decimal.Decimal("{:.2f}".format(floor_math_decimal))

    return render_template('/collection/collection.html' , user = user , nfts = new_list )

#################################################### Add new NFT Collection ########################################################

@app.route('/collection_new')
def add_new_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
    "id":session['user_id']
    }
    return render_template('/collection/collection_new.html' , user = User.get_by_id(data))

####################################################### Process new collection form #################################################

@app.route('/process_new_collection' , methods=['POST'])
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
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))
        print(image.filename + '*****************************************************************')

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
        "user_id": session["user_id"]
    }
    # return redirect(f'/main/{id}')
    Nft.create(data)

    return redirect('/collection')

############################################################ Edit Collection ####################################################

@app.route('/collection/edit/<int:id>')
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

@app.route('/process_edit_collection', methods=['POST'])
def update():
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
        "is_for_sale": request.form['is_for_sale'],
        "sale_price": request.form['sale_price'],
        "link_to_sale": request.form['link_to_sale'],
        "user_id": session["user_id"]
    }
    Nft.update_collection(data)
    return redirect('/collection')

##################################################### Collection VIEW NFT ########################################################

@app.route('/collection_view/<int:id>')
def collection_view(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id ,
    }
    user_data = {
        "id" : session['user_id']
    }

################# API TEST FLOOR PRICE BEGIN###########


    mint_address_db = Nft.get_mint(data)
    if len(mint_address_db.mint_address) > 0:

        payload={}
        headers = {}

        mint_address_url = "https://api-mainnet.magiceden.dev/v2/tokens/{}".format(mint_address_db.mint_address)

        mint_response = requests.request("GET", mint_address_url, headers=headers, data=payload)
        mint = json.loads(mint_response.content)
        collection_name = mint['collection']

        collection_url = "https://api-mainnet.magiceden.dev/v2/collections/{}/stats".format(collection_name)

        response = requests.request("GET", collection_url, headers=headers, data=payload)
        floor = json.loads(response.content)
        floor_price = floor['floorPrice']
        def move_point(number, shift, base = 10):
            return number * base**shift

        floor_math_decimal = decimal.Decimal(move_point( floor_price , -9))
        floor_math = decimal.Decimal("{:.2f}".format(floor_math_decimal))

        nft = Nft.get_by_id(data)
        image = url_for('static' , filename = 'uploads/' + nft.image_name)

    elif len(mint_address_db.mint_address) == 0:

################# API TEST FLOOR PRICE END###########
        floor_math = -1
        nft = Nft.get_by_id(data)
        image = url_for('static' , filename = 'uploads/' + nft.image_name)

    return render_template('/collection/collection_view.html' , user = User.get_by_id(user_data) , nft = nft , image = image , floor = floor_math )

########################################################## COLLECTION FROM WATCHLIST ############################################

@app.route('/collection/collection_from_watchlist/<int:id>')
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

@app.route('/process_from_watchlist' , methods=['POST'])
def process_from_watchlist():
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
        "trade_fees": request.form['trade_fees'],
        "has_staking": request.form['has_staking'],
        "notes": request.form['notes'],
        "is_for_sale": request.form['is_for_sale'],
        "sale_price": request.form['sale_price'],
        "link_to_sale": request.form['link_to_sale'],
        "mint_address": request.form['mint_address'],
        "user_id": session["user_id"]
    }
    # return redirect(f'/main/{id}')
    Nft.update_from_watchlist(data)

    return redirect('/collection')

################################################################ Delete NFT #########################################################

@app.route('/destroy/nft/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Nft.destroy(data)
    return redirect('/collection')

########################################################## Resources ###################################################################
@app.route('/resources')
def resources():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    # nfts = nft.get_all()
    return render_template('/resources/resources.html' , user=User.get_by_id(data))

########################################################## SOLANA CHART ###################################################################
@app.route('/solana_chart')
def solana_chart():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    # nfts = nft.get_all()
    return render_template('/solana_chart/solana_chart.html' , user=User.get_by_id(data))






##################### THIS IS FOR VIEW PAGE BEFORE THE TWO API INTEGRATIONS ############################################
# Will have to delete 'mint_address' from DB and remove from controller, model and html.

##################################################### Collection VIEW NFT ########################################################

# @app.route('/collection_view/<int:id>')
# def collection_view(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id" : id ,
#     }
#     user_data = {
#         "id" : session['user_id']
#     }

# ################# API TEST FLOOR PRICE BEGIN###########

#     url = "https://api-mainnet.magiceden.dev/v2/collections/akari/stats"

#     payload={}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)
#     floor = json.loads(response.content)
#     floor_price = floor['floorPrice']
#     print(response.text)
#     def move_point(number, shift, base = 10):
#         return number * base**shift

#     floor_math = decimal.Decimal(move_point( floor_price , -9))

#     # floor_display = move_point( floor_price , -9)

# ################# API TEST FLOOR PRICE END###########

#     nft = Nft.get_by_id(data)
#     image = url_for('static' , filename = 'uploads/' + nft.image_name)

#     return render_template('/collection/collection_view.html' , user = User.get_by_id(user_data) , nft = nft , image = image , floor = floor_math )