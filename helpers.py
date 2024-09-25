import json

from flask import jsonify


def get_available_foods():
    foods = [
        {"item_name": "Burger", "price": 200, "quantity": 5},
        {"item_name": "Pizza", "price": 250, "quantity": 3},
        {"item_name": "Fries", "price": 100, "quantity": 10},
        {"item_name": "Soda", "price": 50, "quantity": 50},
        {"item_name": "Salad", "price": 150, "quantity": 5},
        {"item_name": "Chicken Wings", "price": 180, "quantity": 3},
        {"item_name": "Tacos", "price": 220, "quantity": 2},
        {"item_name": "Sandwich", "price": 120, "quantity": 7},
        {"item_name": "Ice Cream", "price": 80, "quantity": 5},
        {"item_name": "Steak", "price": 300, "quantity": 1},
    ]
    return json.dumps(foods)


def create_order(item_name, quantity):
    foods_json = get_available_foods()
    foods = json.loads(foods_json)

    for food in foods:
        if food["item_name"] == item_name:
            if food["quantity"] >= quantity:
                response = {
                    "message": "Order successful",
                    "item_name": item_name,
                    "requested_quantity": quantity,
                    "available_quantity": food["quantity"],
                    "price_per_unit": food["price"],
                    "total_price": food["price"] * quantity
                }
                return json.dumps(response)
            else:
                response = {
                    "message": "Sorry, not enough quantity available",
                    "item_name": item_name,
                    "requested_quantity": quantity,
                    "available_quantity": food["quantity"]
                }
                return json.dumps(response)

    response = {
        "message": "Sorry, item not available",
        "item_name": item_name,
        "requested_quantity": quantity
    }
    return json.dumps(response)


def update_order(item_name, quantity, order_id=None):
    foods_json = get_available_foods()
    foods = json.loads(foods_json)
    for food in foods:
        if food["item_name"] == item_name:
            food["quantity"] -= quantity
            response = {
                "message": "Order updated successfully",
                "item_name": item_name,
                "requested_quantity": quantity,
                "available_quantity": food["quantity"],
                "price_per_unit": food["price"],
                "total_price": food["price"] * quantity
            }
            return json.dumps(response)

    response = {
        "message": "Sorry, item not available",
        "item_name": item_name,
        "requested_quantity": quantity
    }
    return json.dumps(response)


available_functions = {
    "get_available_foods": get_available_foods,
    "create_order": create_order,
    "update_order": update_order
}


functions = [
    {
        "name": "get_available_foods",
        "description": "Get available foods",
    },
    {
        "name": "create_order",
        "description": "Create order",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {"type": "string", "description": "Item name to order"},
                "quantity": {"type": "number", "description": "Quantity of the item to order"}
            },
            "required": ["item_name", "quantity"]
        }
    },
    {
        "name": "update_order",
        "description": "Update order",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {"type": "string", "description": "Item name to update"},
                "quantity": {"type": "number", "description": "Quantity of the item to update"},
                "order_id": {"type": "string", "description": "Order ID to update"}
            },
            "required": ["item_name", "quantity"]
        }
    }
]
