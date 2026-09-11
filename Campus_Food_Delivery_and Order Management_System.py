import json
import os
# ============================================================
# CAMPUS FOOD DELIVERY AND ORDER MANAGEMENT SYSTEM
# ============================================================

DATA_FILE = "canteen_data.json"


# -------------------- DEFAULT DATA ----------------------------
def initialize_default_data():
    """Create the initial menu, riders and empty order list."""

    return {
        "menu": {
            "Meals": {
                "Rolex Special": 5000,
                "Chicken & Chips": 15000,
                "Beef Pilao": 12000
            },

            "Drinks": {
                "Soda (500ml)": 2500,
                "Bottled Water": 1500,
                "Passion Juice": 3000
            },

            "Snacks": {
                "Samosa": 1000,
                "Chapati": 1000,
                "Mandazi": 500
            }
        },

        # Predefined riders
        "riders": [
            {
                "name": "Rider John",
                "available": True
            },
            {
                "name": "Rider Mark",
                "available": True
            },
            {
                "name": "Rider Alice",
                "available": True
            }
        ],

        # Stores all customer orders
        "orders": []
    }


# -------------------- FILE HANDLING ---------------------------

def load_data():
    """Load saved system data from the JSON file."""

    if not os.path.exists(DATA_FILE):
        return initialize_default_data()

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, IOError):
        print("\nError reading saved data.")
        print("Starting with default system data.\n")
        return initialize_default_data()


def save_data(data):
    """Save system data to the JSON file."""

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except IOError:
        print("\nError: Unable to save data.")


# -------------------- MENU DISPLAY ----------------------------

def display_menu(data):
    """Display all available menu items and their prices."""

    print("\n================ CAMPUS MENU ================")

    for category, items in data["menu"].items():

        print(f"\n--- {category} ---")

        for item, price in items.items():
            print(f"{item:<25} UGX {price:,}")

    print("==============================================")


# ---- FIND MENU ITEM ----

def find_item(data, item_name):
    """Search for an item and return its name and price."""

    for category, items in data["menu"].items():

        for item, price in items.items():

            if item.lower() == item_name.lower():
                return item, price

    return None, None


# ---- RIDER ASSIGNMENT --

def get_available_rider(data):
    """Return the first available rider."""

    for rider in data["riders"]:

        if rider["available"]:
            return rider

    return None


# ---- TAKE CUSTOMER ORDER ----

def take_order(data):
    """Take a new customer order and calculate the total cost."""

    display_menu(data)

    order_items = []

    print("\nEnter food or drink names one at a time.")
    print("Type 'done' when you have finished ordering.")

    while True:

        item_name = input("\nEnter item name: ").strip()

        if item_name.lower() == "done":
            break

        item, price = find_item(data, item_name)

        if item is None:
            print("Item not found. Please select an item from the menu.")
            continue

        # Validate quantity
        while True:

            try:
                quantity = int(
                    input(f"Enter quantity for {item}: ")
                )

                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue

                break

            except ValueError:
                print("Please enter a valid whole number.")

        # Check if the item already exists in the order
        found = False

        for existing_item in order_items:

            if existing_item["name"] == item:

                existing_item["quantity"] += quantity
                existing_item["subtotal"] += price * quantity

                found = True
                break

        # Add a new item to the order
        if not found:

            order_items.append({
                "name": item,
                "price": price,
                "quantity": quantity,
                "subtotal": price * quantity
            })

        print(f"{item} added to order.")

    # Prevent empty orders
    if not order_items:

        print("\nNo items were ordered.")
        return

    # --Calculate subtotal --

    subtotal = sum(
        item["subtotal"] for item in order_items
    )

    print(f"\nOrder subtotal: UGX {subtotal:,}")

    # ---------------- Delivery distance ----------------

    while True:

        try:

            distance = float(
                input("Enter delivery distance in kilometres: ")
            )

            if distance < 0:
                print("Distance cannot be negative.")
                continue

            break

        except ValueError:
            print("Please enter a valid distance.")

    # ---------------- Delivery fee ----------------

    if subtotal >= 30000:

        delivery_fee = 0

    elif distance <= 2:

        delivery_fee = 2000

    elif distance <= 5:

        delivery_fee = 3000

    else:

        delivery_fee = 5000

    total = subtotal + delivery_fee

    # ---------------- Order summary ----------------

    print("\n-------------- ORDER SUMMARY --------------")

    for item in order_items:

        print(
            f"{item['name']} x {item['quantity']} = "
            f"UGX {item['subtotal']:,}"
        )

    print(f"\nSubtotal:       UGX {subtotal:,}")
    print(f"Delivery fee:   UGX {delivery_fee:,}")
    print(f"Total:          UGX {total:,}")

    # ---------------- Assign rider ----------------

    rider = get_available_rider(data)

    if rider is None:

        print("\nNo rider is currently available.")
        print("Order will remain Pending without a rider.")

        assigned_rider = "Not Assigned"

    else:

        rider["available"] = False
        assigned_rider = rider["name"]

        print(f"\nAssigned rider: {assigned_rider}")

    # ---------------- Create order ----------------

    order_id = len(data["orders"]) + 1

    order = {
        "order_id": order_id,
        "items": order_items,
        "distance_km": distance,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "status": "Pending",
        "rider": assigned_rider
    }

    data["orders"].append(order)

    save_data(data)

    print(f"\nOrder #{order_id} successfully recorded.")
    print("Order status: Pending")
    print("--------------------------------------------")


# -------------------- UPDATE ORDER STATUS ---------------------

def update_order_status(data):
    """Update an order through its delivery stages."""

    if not data["orders"]:

        print("\nThere are no orders available.")
        return

    print("\n================ ORDERS ================")

    for order in data["orders"]:

        print(
            f"Order #{order['order_id']} | "
            f"Status: {order['status']} | "
            f"Rider: {order['rider']}"
        )

    print("=========================================")

    # Validate order ID
    while True:

        try:

            order_id = int(
                input("Enter order ID to update: ")
            )

            break

        except ValueError:

            print("Please enter a valid order ID.")

    selected_order = None

    for order in data["orders"]:

        if order["order_id"] == order_id:

            selected_order = order
            break

    if selected_order is None:

        print("Order ID not found.")
        return

    current_status = selected_order["status"]

    # Prevent skipping delivery stages
    if current_status == "Pending":

        new_status = "Out for Delivery"

    elif current_status == "Out for Delivery":

        new_status = "Delivered"

    else:

        print("This order has already been delivered.")
        return

    print(f"\nCurrent status: {current_status}")
    print(f"Next status: {new_status}")

    confirmation = input(
        "Confirm status update? (Y/N): "
    ).strip().lower()

    if confirmation == "y":

        selected_order["status"] = new_status

        # Make rider available again after delivery
        if new_status == "Delivered":

            for rider in data["riders"]:

                if rider["name"] == selected_order["rider"]:

                    rider["available"] = True
                    break

        save_data(data)

        print(
            f"Order #{order_id} updated to {new_status}."
        )

    else:

        print("Status update cancelled.")


# -------------------- SALES REPORT ----------------------------

def sales_and_reports(data):
    """Generate sales and order-status reports."""

    orders = data["orders"]

    if not orders:

        print("\nNo orders have been recorded yet.")
        return

    # ---------------- Revenue ----------------

    delivered_revenue = 0

    for order in orders:

        if order["status"] == "Delivered":

            delivered_revenue += order["total"]

    # ---------------- Status counts ----------------

    pending_count = 0
    delivery_count = 0
    delivered_count = 0

    for order in orders:

        if order["status"] == "Pending":

            pending_count += 1

        elif order["status"] == "Out for Delivery":

            delivery_count += 1

        elif order["status"] == "Delivered":

            delivered_count += 1

    # ---------------- Best-selling item ----------------

    item_sales = {}

    for order in orders:

        for item in order["items"]:

            item_name = item["name"]
            quantity = item["quantity"]

            if item_name in item_sales:

                item_sales[item_name] += quantity

            else:

                item_sales[item_name] = quantity

    if item_sales:

        best_selling_item = max(
            item_sales,
            key=item_sales.get
        )

        best_selling_quantity = item_sales[
            best_selling_item
        ]

    else:

        best_selling_item = "None"
        best_selling_quantity = 0

    # ---------------- Display report ----------------

    print("\n============== SALES REPORT ==============")

    print(
        f"Revenue from delivered orders: "
        f"UGX {delivered_revenue:,}"
    )

    print(
        f"Best-selling item: {best_selling_item} "
        f"({best_selling_quantity} sold)"
    )

    print("\nOrder Status:")

    print(f"Pending:            {pending_count}")
    print(f"Out for Delivery:   {delivery_count}")
    print(f"Delivered:          {delivered_count}")

    print("===========================================")


# -------------------- RIDER REPORT ----------------------------

def rider_report(data):
    """Display the current availability of all riders."""

    print("\n============== RIDER STATUS ==============")

    for rider in data["riders"]:

        if rider["available"]:

            status = "Available"

        else:

            status = "Busy"

        print(
            f"{rider['name']:<20} {status}"
        )

    print("===========================================")


# -------------------- MAIN MENU -------------------------------

def main():
    """Run the menu-driven food delivery system."""

    data = load_data()

    while True:

        print("\n")
        print("==============================================")
        print(" CAMPUS FOOD DELIVERY AND ORDER MANAGEMENT")
        print("==============================================")

        print("1. View Menu")
        print("2. Take New Customer Order")
        print("3. Update Order Delivery Status")
        print("4. View Sales and Status Reports")
        print("5. View Rider Status")
        print("6. Exit")

        print("==============================================")

        choice = input(
            "Enter your choice (1-6): "
        ).strip()

        if choice == "1":

            display_menu(data)

        elif choice == "2":

            take_order(data)

        elif choice == "3":

            update_order_status(data)

        elif choice == "4":

            sales_and_reports(data)

        elif choice == "5":

            rider_report(data)

        elif choice == "6":

            print(
                "\nThank you for using the "
                "Campus Food Delivery System."
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select a number from 1 to 6."
            )


# -------------------- PROGRAM START ---------------------------

if __name__ == "__main__":
    main()