import csv  # Import CSV module to save and read order history

# Global dictionary to store user orders
myOrder = {}

# Menu Items categorized into dictionaries
appetizers_menu = {
    "Aloo Tikki": 16.00,
    "Chotte Samosa's": 16.00,
    "Chatpata Gobi": 16.00,
    "Aloo Papdi Chaat": 16.00,
    "Palak Chaat": 18.00
}

entrees_menu = {
    "Butter Chicken": 22.00,
    "Paneer Tikka Masala": 20.00,
    "Goat Curry": 25.00,
    "Fish Tandoori": 24.00,
    "Dal Makhani": 18.00
}

desserts_menu = {
    "Gulab Jamun": 8.00,
    "Rasmalai": 10.00,
    "Kheer": 7.00,
    "Jalebi": 9.00,
    "Kulfi": 12.00
}

beverages_menu = {
    "Mango Lassi": 6.00,
    "Masala Chai": 4.00,
    "Sweet Lassi": 6.00,
    "Cold Coffee": 8.00,
    "Soft Drink": 3.00
}

# Function to display restaurant details
def restaurant_info():
    print("\nRestaurant: Samudhra")
    print("Location: 3391 State Route 27 Franklin Park, NJ 08823")
    print("Website: www.Samudhra.com")

# Function to display a menu and take orders from the user
def order_items(menu, category):
    print(f"\n{category} Menu:")
    for item, price in menu.items():
        print(f"{item}: ${price:.2f}")

    while True:
        choice = input(f"\nWould you like to order something from {category}? (yes/no): ").lower()
        if choice != "yes":
            break  # Exit ordering loop if the user doesn't want to order
        
        item_name = input("Enter the item name: ").title()
        if item_name not in menu:
            print("Invalid item. Please select from the menu.")
            continue  # Ask for item name again if input is invalid
        
        quantity = int(input("Enter quantity: "))

        # Update order dictionary, adding quantity if item already exists
        if item_name in myOrder:
            myOrder[item_name]["quantity"] += quantity
        else:
            myOrder[item_name] = {"price": menu[item_name], "quantity": quantity}

# Function to modify or delete an item from the order
def modify_order():
    if not myOrder:
        print("\nYour order is empty!")  # No modifications can be made if no items exist
        return

    print("\nYour Current Order:")
    for item, details in myOrder.items():
        print(f"{item}: {details['quantity']} x ${details['price']:.2f}")

    item_name = input("\nEnter item to modify (or 'exit' to cancel): ").title()
    if item_name == "Exit":
        return

    if item_name not in myOrder:
        print("Item not found in order.")  # Input validation for incorrect item name
        return

    action = input("Would you like to 'delete' or 'update quantity'?: ").lower()
    if action == "delete":
        del myOrder[item_name]  # Remove item from order
    elif action == "update quantity":
        new_quantity = int(input("Enter new quantity: "))
        if new_quantity == 0:
            del myOrder[item_name]  # Remove item if quantity is set to 0
        else:
            myOrder[item_name]["quantity"] = new_quantity  # Update quantity
    else:
        print("Invalid action.")

# Function to finalize and place an order
def place_order():
    if not myOrder:
        print("\nYour order is empty!")  # Ensure user has selected items before checkout
        return

    print("\nYour Final Order:")
    subtotal = 0
    for item, details in myOrder.items():
        item_total = details["quantity"] * details["price"]
        subtotal += item_total
        print(f"{item}: {details['quantity']} x ${details['price']:.2f} = ${item_total:.2f}")

    # Apply Discounts
    coupon = input("\nDo you have a coupon? (yes/no): ").lower()
    discount = 0
    if coupon == "yes":
        coupon_type = input("Is it a percentage or a fixed amount? (percent/fixed): ").lower()
        if coupon_type == "percent":
            discount = subtotal * (float(input("Enter discount percentage: ")) / 100)
        elif coupon_type == "fixed":
            discount = float(input("Enter discount amount: "))

    subtotal -= discount  # Apply discount to subtotal

    # Apply Tip (User chooses tip percentage)
    tip_percentage = float(input("Would you like to tip 15%, 18%, or 20%?: "))
    tip_amount = (tip_percentage / 100) * subtotal
    subtotal += tip_amount  # Add tip to total cost

    # Apply Tax (Fixed tax rate of 6.625%)
    tax = subtotal * 0.06625
    subtotal += tax

    # Delivery Charge (Adds $5 for delivery)
    delivery = input("Would you like pickup or delivery? (pickup/delivery): ").lower()
    if delivery == "delivery":
        subtotal += 5

    print(f"\nTotal Price (after discounts, tip, and tax): ${subtotal:.2f}")

    # Save order details to CSV file
    save_order()

# Function to save the order details to a CSV file
def save_order():
    with open("order_history.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        for item, details in myOrder.items():
            writer.writerow([item, details["quantity"], details["price"]])  # Save each order item
    print("\nOrder has been saved successfully!")

# Function to view previous orders from the CSV file
def view_order():
    try:
        with open("order_history.csv", mode="r") as file:
            reader = csv.reader(file)
            print("\nPast Orders:")
            for row in reader:
                print(f"{row[0]} - {row[1]} x ${row[2]}")  # Display order history
    except FileNotFoundError:
        print("\nNo past orders found.")  # Handle case where order file doesn't exist

# Main function to display the menu and handle user input
def main():
    while True:
        print("\nWelcome to the Restaurant Ordering System!")
        print("1. Restaurant Information")
        print("2. Order Appetizers")
        print("3. Order Entrees")
        print("4. Order Desserts")
        print("5. Order Beverages")
        print("6. Modify Order")
        print("7. Place Order")
        print("8. View Past Orders")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        # Menu selection based on user input
        if choice == "1":
            restaurant_info()
        elif choice == "2":
            order_items(appetizers_menu, "Appetizers")
        elif choice == "3":
            order_items(entrees_menu, "Entrees")
        elif choice == "4":
            order_items(desserts_menu, "Desserts")
        elif choice == "5":
            order_items(beverages_menu, "Beverages")
        elif choice == "6":
            modify_order()
        elif choice == "7":
            place_order()
        elif choice == "8":
            view_order()
        elif choice == "9":
            print("Exiting... Thank you!")
            break  # Exit the loop and end program
        else:
            print("Invalid choice. Please select a valid option.")  # Handle invalid input

# Run the program when executed
if __name__ == "__main__":
    main()
