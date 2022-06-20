from flask import Flask, request
from flask_cors import CORS

from server.router import get_orders_of, register_order, update_order_status

app = Flask(__name__)
CORS(app)

# GET
@app.route("/get/orders", methods=["GET"])
def get_orders():
    args = request.args.to_dict()

    user = args["user_address"]

    return {"orders": get_orders_of(user)}


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


@app.route("/delete/order", methods=["DELETE"])
def delete_order():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.json

        print(json)

        id = json["id"]
        all = json["all"]

        update_order_status(id=id, all=all, status="DELETED")

        return {"status": "SUCCESS"}


if __name__ == "__main__":
    app.run(debug=True)
