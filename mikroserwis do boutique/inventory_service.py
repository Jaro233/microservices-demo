from flask import Flask, jsonify, request
import sys

app = Flask(__name__)

# Sample inventory state (normally this should be in a database)
inventory = {
    "OLJCESPC7Z": 10,
    "66VCHSJNUP": 15,
    "1YMWWN1N4O": 5,
    "LS4PSXUNUM": 20,
    "L9ECAV7KIM": 0,  # Product unavailable
    "2ZYFJ3GM2N": 30,
    "0PUK6V6EV0": 2,
    "9SIQT8TOJO": 10,
    "6E92ZMYYFZ": 0,
}

@app.route('/inventory/<product_id>', methods=['GET'])
def get_inventory(product_id):
    quantity = inventory.get(product_id, 0)
    response = {
        "productId": product_id,
        "inStock": quantity > 0,
        "quantity": quantity
    }
    return jsonify(response)


@app.route('/inventory/update/<product_id>', methods=['POST'])
def update_inventory(product_id):
  # Assuming you pass the change in quantity as a JSON payload
  data = request.get_json()
  change = -data['change']
  if product_id in inventory:
    inventory[product_id] = max(0, inventory[product_id] + change)  # Prevent negative inventory
    return jsonify({product_id: inventory[product_id]}), 200
  else:
    return jsonify({"error": "Product not found"}), 404


@app.route('/inventory/set/<product_id>', methods=['POST'])
def set_inventory(product_id):
    # Directly set the inventory for a product
    quantity = request.json.get('quantity', 0)
    inventory[product_id] = max(quantity, 0)  # Prevent negative inventory
    return jsonify({product_id: inventory[product_id]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
