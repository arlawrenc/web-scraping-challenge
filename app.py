from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
from scrape_mars import scrape 

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'

mongo = PyMongo(app)


@app.route('/')
def index(): 

    mars_data = mongo.db.mars.find_one()
    return render_template('index.html', data=mars_data)


@app.route('/scrape')
def scrape_mars(): 

    data = scrape()
    mongo.db.mars.update({}, data, upsert=True)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

