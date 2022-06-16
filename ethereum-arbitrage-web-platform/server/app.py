from flask import Flask, request
from flask_cors import CORS

from server.router import register_order

app = Flask(__name__)
CORS(app)

# POST
@app.route("/post/order", methods=["POST"])
def post_order():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.json

        register_order(
            json["network"],
            json["user_address"],
            json["token_0_address"],
            json["token_1_address"],
            json["fee"],
        )

        return {"status": "SUCCESS"}


if __name__ == "__main__":
    app.run(debug=True)
