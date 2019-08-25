from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/app")

@app.route("/")
def home():
    
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.title_scrape()
    mars_info = scrape_mars.paragraph_scrape()
    mars_info = scrape_mars.image_scrape()
    mars_info = scrape_mars.twitter_scrape()
    mars_info = scrape_mars.facts_scrape()
    mars_info = scrape_mars.hems_scrape()
    mars_data.update({}, mars_info, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
