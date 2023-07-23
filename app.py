from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def is_scrapable(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return True, soup.title.string.strip()
        else:
            return False, f"Failed to fetch URL. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Error: {e}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    if request.method == 'POST':
        data = request.get_json()
        website_url = data['url']
        result, message = is_scrapable(website_url)
        return jsonify({'result': result, 'message': message})

if __name__ == '__main__':
    app.run(debug=True)
