from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app) 

# MongoDB Connection
MONGO_URI = "mongodb+srv://shebinkallankunnan_db_user:B4lYE1tisJoDvgew@poovil.idg80rk.mongodb.net/?appName=poovil"

try:
    client = MongoClient(MONGO_URI)
    db = client['bakery_db'] 
    products_collection = db['products']
    orders_collection = db['orders']
    print("MongoDB Connected Successfully! 🎉")
except Exception as e:
    print("Database Connection Failed:", e)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Backend is Running!"})

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = []
        for doc in products_collection.find():
            doc['_id'] = str(doc['_id'])
            products.append(doc)
        return jsonify(products)
    except Exception as e:
        print("Error fetching products:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/add-product', methods=['POST'])
def add_product():
    data = request.json
    new_product = {
        "name": data.get("name"),
        "price": data.get("price"),
        "category": data.get("category"),
        "image_url": data.get("image_url"),
        "available": True
    }
    result = products_collection.insert_one(new_product)
    return jsonify({"message": "Product added!", "id": str(result.inserted_id)}), 201

@app.route('/api/place-order', methods=['POST'])
def place_order():
    data = request.json
    new_order = {
        "customer_name": data.get("customer_name"),
        "phone": data.get("phone"),
        "address": data.get("address"),
        "items": data.get("items"),
        "total_amount": data.get("total_amount"),
        "status": "Pending"
    }
    result = orders_collection.insert_one(new_order)
    return jsonify({"message": "Order placed successfully!", "order_id": str(result.inserted_id)}), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        orders = []
        for doc in orders_collection.find().sort('_id', -1):
            doc['_id'] = str(doc['_id'])
            orders.append(doc)
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    # use_reloader=False is added to prevent Windows errors
     app.run(host="0.0.0.0", port=5000)
