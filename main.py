from flask import Flask, jsonify, request

customers = [
             {
              "email": "jan.novak@example.cz",
              "username": "johny",
              "name": "Jan Novak",
              "newsletter_status": True,
              "trips": [
                            {
                             "destination": "Oslo, Norway",
                             "price": 150.00
                            },
                            {
                             "destination": "Bangkok, Thailand",
                             "price": 965.00
                            }
                          ]
             },
             {
              "email": "ivan.opletal@example.com",
              "username": "ivan123",
              "name": "Ivan Opletal",
              "newsletter_status": False,
              "trips": []
             }
        ]

app = Flask(__name__)


@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers), 200


@app.route('/customers/<string:username>', methods=['GET'])
def get_customer(username):
    for customer in customers:
        if customer["username"] == username:
            return jsonify(customer["username"]), 200
    return {"message": f"There is no user with username: {username}"}, 404


@app.route('/customer', methods=['POST'])
def create_customer():
    request_data = request.get_json()
    new_customer = {
        "email": request_data['email'],
        "username": request_data['username'],
        "name": request_data['name'],
        "newsletter_status": request_data['newsletter_status'],
        "trips": []
    }
    for customer in customers:
        if customer['username'] == new_customer['username']:
            return jsonify({'error': 'username already exist'}), 409

    customers.append(new_customer)
    return jsonify(new_customer), 201


@app.route('/customer/<string:username>', methods= ['PUT'])
def update_customer(username):
    request_data = request.get_json()
    updated_customer = {
        "email": request_data['email'],
        "username": request_data['username'],
        "name": request_data['name'],
        "newsletter_status": request_data['newsletter_status'],
        "trips": []
    }
    for customer in customers:
        if username == customer['username']:
            customer.update(updated_customer)
            return jsonify(updated_customer), 200

    new_customer = {
        "email": request_data['email'],
        "username": username,
        "name": request_data['name'],
        "newsletter_status": request_data['newsletter_status'],
        "trips": []
    }
    customers.append(new_customer)
    return jsonify(new_customer), 201

@app.route('/customer/<string:username>', methods=['DELETE'])
def delete_customer(username):
    for customer in customers:
        if customer["username"] == username:
            customers.remove(customer)
            return jsonify({f'message': f'customer {username} was successfully removed'})
    return jsonify({"message": "Username not found"}), 404

@app.route('/customer/<string:username>/trips', methods=['GET'])
def show_trips(username):
    for customer in customers:
        if customer["username"] == username:
            return jsonify({"trips": customer["trips"]})
        return jsonify({"message": "Username not found"}), 404


@app.route('/customer/<string:username>/trips', methods=['POST'])
def add_trips(username):

    for customer in customers:
        request_data = request.get_json()
        new_trip = {
            "destination": request_data['destination'],
            "price": request_data['price']
        }
        if customer["username"] == username:
            customer["trips"].append(new_trip)
            return new_trip, 201
    return jsonify({"message": "Username not found"}), 404


if __name__=='__main__':
    app.run(port=3333, debug=True)