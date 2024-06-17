# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, render_template, jsonify
import review_scraper

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

@app.route('/lazy-reviews', methods=['POST'])
def load_reviews_lazy():
    if request.method == 'POST':
        if 'url' not in request.form:
            return 'Bad request', 400
        if 'next_token' not in request.form:
            next_token = ""
        else:
            next_token = request.form['next_token']
        reviews, new_token = review_scraper.get_reviews_sub(request.form["url"], next_token)
        print("Token: ", new_token)
        return jsonify({'reviews':reviews, 'next_token':new_token})


@app.route('/', methods=['GET', 'POST'])
def load_reviews():
    if request.method == 'POST':
        if 'url' not in request.form:
            return 'Bad request', 400
        if 'next_token' not in request.form:
            next_token = ""
        else:
            next_token = request.form['next_token']
        # reviews, next_token = review_scraper.get_reviews_sub(request.form["url"], next_token)
        # return(render_template("reviews.html", url=request.form["url"], reviews=reviews, next_token=next_token))
        return(render_template("reviews.html", url=request.form["url"], next_token=next_token))
        
    if request.method == "GET":
        return '''
        <!doctype html>
        <title>Get Reviews</title>
        <h1>Get Reviews</h1>
        <form method=post>
          <input type=text name=url>
          <input type=submit value=Submit>
        </form>
        '''
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
