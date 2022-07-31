from flask_app.controllers import controller_users
from flask_app.controllers import controller_nfts
from flask_app.controllers import controllers_nfts_watchlist
from flask_app.controllers import controllers_nfts_sold
from flask_app import application

if __name__=='__main__':
    application.run(debug=True)