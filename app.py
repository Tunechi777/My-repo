from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------
# FOOD DATABASE
# ---------------------------------------------------------

FOODS = [
    {
        "id": 1,
        "name": "Chicken Biryani",
        "category": "Biryani",
        "price": 249,
        "rating": 4.8,
        "time": "30-35 min",
        "emoji": "🍗",
        "description": "Hyderabadi dum biryani with tender chicken"
    },
    {
        "id": 2,
        "name": "Paneer Butter Masala",
        "category": "North Indian",
        "price": 199,
        "rating": 4.7,
        "time": "25-30 min",
        "emoji": "🍛",
        "description": "Creamy tomato gravy with soft paneer"
    },
    {
        "id": 3,
        "name": "Margherita Pizza",
        "category": "Pizza",
        "price": 299,
        "rating": 4.6,
        "time": "20-25 min",
        "emoji": "🍕",
        "description": "Classic pizza with mozzarella and basil"
    },
    {
        "id": 4,
        "name": "Chicken Burger",
        "category": "Burgers",
        "price": 179,
        "rating": 4.5,
        "time": "20-25 min",
        "emoji": "🍔",
        "description": "Crispy chicken burger with fresh vegetables"
    },
    {
        "id": 5,
        "name": "Masala Dosa",
        "category": "South Indian",
        "price": 129,
        "rating": 4.9,
        "time": "15-20 min",
        "emoji": "🥞",
        "description": "Crispy dosa served with chutney and sambar"
    },
    {
        "id": 6,
        "name": "Veg Fried Rice",
        "category": "Chinese",
        "price": 159,
        "rating": 4.4,
        "time": "20-25 min",
        "emoji": "🍚",
        "description": "Wok-tossed rice with fresh vegetables"
    },
    {
        "id": 7,
        "name": "Chicken Noodles",
        "category": "Chinese",
        "price": 189,
        "rating": 4.6,
        "time": "20-25 min",
        "emoji": "🍜",
        "description": "Spicy noodles tossed with chicken"
    },
    {
        "id": 8,
        "name": "Chocolate Brownie",
        "category": "Desserts",
        "price": 99,
        "rating": 4.9,
        "time": "10-15 min",
        "emoji": "🍫",
        "description": "Warm chocolate brownie with rich cocoa"
    }
]


# ---------------------------------------------------------
# FRONTEND
# ---------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------------
# GET ALL FOODS
# ---------------------------------------------------------

@app.route("/api/foods", methods=["GET"])
def get_foods():

    category = request.args.get("category")
    search = request.args.get("search")

    result = FOODS

    if category and category != "All":
        result = [
            food for food in result
            if food["category"] == category
        ]

    if search:
        search = search.lower()

        result = [
            food for food in result
            if search in food["name"].lower()
            or search in food["description"].lower()
        ]

    return jsonify(result)


# ---------------------------------------------------------
# GET SINGLE FOOD
# ---------------------------------------------------------

@app.route("/api/foods/<int:food_id>")
def get_food(food_id):

    food = next(
        (food for food in FOODS if food["id"] == food_id),
        None
    )

    if not food:
        return jsonify({
            "error": "Food not found"
        }), 404

    return jsonify(food)


# ---------------------------------------------------------
# CHECKOUT
# ---------------------------------------------------------

@app.route("/api/order", methods=["POST"])
def create_order():

    data = request.get_json()

    customer = data.get("customer")
    items = data.get("items", [])

    if not customer:
        return jsonify({
            "success": False,
            "message": "Customer information is required"
        }), 400

    if not items:
        return jsonify({
            "success": False,
            "message": "Cart is empty"
        }), 400

    total = 0

    for item in items:

        food = next(
            (food for food in FOODS if food["id"] == item["id"]),
            None
        )

        if food:
            quantity = int(item.get("quantity", 1))
            total += food["price"] * quantity

    return jsonify({
        "success": True,
        "message": "Order placed successfully!",
        "order_id": "FD20260929001",
        "customer": customer,
        "total": total
    })


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
