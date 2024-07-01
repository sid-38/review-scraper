from flask import Flask, request, render_template, jsonify
import review_scraper

app = Flask(__name__)

# Lazy loads a section of reviews based on the next page token
@app.route('/lazy-reviews', methods=['POST'])
def load_reviews_lazy():
    if request.method == 'POST':
        if 'url' not in request.form:
            return 'Bad request', 400
        if 'next_token' not in request.form:
            next_token = ""
        else:
            next_token = request.form['next_token']
        reviews, new_token = review_scraper.get_reviews_lazy(url=request.form["url"], next_token=next_token)
        return jsonify({'reviews':reviews, 'next_token':new_token})


# A route to render reviews.html, not really important
@app.route('/', methods=['GET', 'POST'])
def reviews_page():
    if request.method == 'POST':
        if 'url' not in request.form:
            return 'Bad request', 400
        next_token= ""
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
    

if __name__ == '__main__':
    app.run()
