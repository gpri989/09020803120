import requests
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

def get_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get("numbers", [])
    except requests.Timeout:
        pass
    except requests.RequestException:
        pass
    return []

@app.route('/numbers', methods=['GET'])
def get_merged_numbers():
    urls = request.args.getlist('url')
    numbers = []
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        results = executor.map(get_numbers, urls)
        for result in results:
            numbers.extend(result)
    numbers = list(set(numbers))
    numbers.sort()
    return jsonify({"numbers": numbers})

if __name__ == '__main__':
    app.run(port=8008)