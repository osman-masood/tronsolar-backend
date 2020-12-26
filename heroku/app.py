# app.py
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logger = logging.getLogger('tcpserver')
logger.setLevel(logging.DEBUG)


# A welcome message to test our server
@app.route('/', methods=['GET', 'POST', 'PUT', 'PATCH'])
def index():
    logger.warning(f"Request args: {request.args.to_dict()}")
    logger.warning(f"Request body: {request.get_data()}")
    return jsonify({"message": "Success"})


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
