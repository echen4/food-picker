#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sys
import scrape
import random
import os

app = Flask(__name__)
app.debug=True
app.secret_key = 'S3CR3T'


# initial page
@app.route('/', methods=['POST', 'GET'])
def main_page():
    if request.method == "GET" or request.method == "POST":
        return render_template('index.html', title="Food Picker")
        # return redirect(url_for('findMovie', search=searchInput))
        

# pick location + add cuisine choices        
@app.route('/pickLocation', methods=['POST', 'GET'])
def pickLocation():
    if request.method == "GET":
        return render_template('location.html', title="Food Picker")
    else:
        print(request.form)
        return render_template('location.html', title="Food Picker")
        # location = request.form['location']
        # cuisine = request.form['cuisine']
        

# show restaurant result        
@app.route('/result', methods=['POST', 'GET'])
def chooseRestaurant():
    if request.method == "GET":
        return render_template('location.html', title="Food Picker")
    else:
        # obtain form inputs
        foodList = request.form.getlist("cuisine")
        foodList = [x for x in foodList if len(x.strip()) > 0]
        loc = request.form["location"]
        
        food = random.choice(foodList) # choose random cuisine
        
        success, result = scrape.searchCuisine(food, loc)
        
        if success: # if successfully accessed yelp
            if len(result["area"]) > 0:
                loc = result["area"]
            return render_template('result.html', location=loc, cuisine=food, 
                                    restaurant=result["name"], phone=result["phone"],
                                    address=result["address"], url=result["url"])
        else: # if unable to get results
            flash(result)
            return redirect(url_for("main_page"))
        

'''
Script to launch app in debug mode
'''
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
