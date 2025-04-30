import os
import datetime

# Dictionary of inventory controllers (username: password)
controllers = [
    {"username": "admin", "password": "pass"},
    {"username": "one", "password": "pass1"},
    {"username": "two", "password": "pass2"},
    {"username": "three", "password": "pass3"}
]

# PPE items dictionary (item_code: item_name)
PPE_items = {
    "HC": "Head Cover",
    "FS": "Face Shield",
    "MS": "Mask",
    "GL": "Gloves",
    "GW": "Gown",
    "SC": "Shoe Covers"
}

# PPE item codes list (code)
PPE_item_codes = list(PPE_items.keys())

# Initialize inventory
inventory = {
    item_code: {
        "Quantity Available": 0,
        "Supplier Code": None,
        "Latest Date Received (DD/MM/YYYY)": None
    }
    for item_code in PPE_items
}

# Initialize lists for history
distribution_history = []
hospitals = []
hospital_distributions = []
supplier_receptions = []

# Initialize supplier and hospital codes
supplier_codes = ["S1", "S2", "S3"]
hospital_codes = ["H1", "H2", "H3"]

# File path for storing inventory data
file_path = "inventory_data.txt"


def create_hospital_codes_file():
    hospital_file = "hospitals.txt"

    # Check if hospitals.txt already exists
    if os.path.isfile(hospital_file):
        print(f"Hospital codes file '{hospital_file}' already exists.")
        return

    hospital_details = [
        {"code": "H1", "name": "", "location": ""},
        {"code": "H2", "name": "", "location": ""},
        {"code": "H3", "name": "", "location": ""}
    ]

    with open(hospital_file, 'w') as file:
        for hospital in hospital_details:
            hospital['name'] = input(f"Enter name for hospital {hospital['code']}: ")
            hospital['location'] = input(f"Enter location for hospital {hospital['code']}: ")

            file.write(f"{hospital['code']}|{hospital['name']}|{hospital['location']}\n")

    print(f"Hospital codes file '{hospital_file}' created.")


def create_supplier_codes_file():
    supplier_file = "suppliers.txt"

    # Check if suppliers.txt already exists
    if os.path.isfile(supplier_file):
        print(f"Supplier codes file '{supplier_file}' already exists.")
        return

    supplier_details = [
        {"code": "S1", "name": "", "contact_number": ""},
        {"code": "S2", "name": "", "contact_number": ""},
        {"code": "S3", "name": "", "contact_number": ""}
    ]

    with open(supplier_file, 'w') as file:
        for supplier in supplier_details:
            supplier['name'] = input(f"Enter name for supplier {supplier['code']}: ")
            supplier['contact_number'] = input(f"Enter contact number for supplier {supplier['code']}: ")

            file.write(f"{supplier['code']}|{supplier['name']}|{supplier['contact_number']}\n")

    print(f"Supplier codes file '{supplier_file}' created.")


def save_data():
    data_lines = []

    # Save inventory data
    for item_code, details in inventory.items():
        data_lines.append(
            f"{item_code}|{details['Quantity Available']}|{details['Supplier Code']}|{details['Latest Date Received (DD/MM/YYYY)']}")

    # Save distribution history
    data_lines.append("\nDISTRIBUTION_HISTORY")
    for record in distribution_history:
        data_lines.append(f"{record[0]}|{'|'.join(record[1])}")

    # Save hospitals
    data_lines.append("\nHOSPITALS")
    data_lines.extend(hospitals)

    # Save hospital distributions
    data_lines.append("\nHOSPITAL_DISTRIBUTIONS")
    for record in hospital_distributions:
        data_lines.append(f"{record[0]}|{record[1]}|{record[2]}|{record[3]}")

    # Save supplier receptions
    data_lines.append("\nSUPPLIER_RECEPTIONS")
    for record in supplier_receptions:
        data_lines.append(f"{record[0]}|{record[1]}|{record[2]}|{record[3]}")

    # Write all data to file
    with open(file_path, 'w') as file:
        file.write('\n'.join(data_lines))

    print(f"Inventory data has been saved to '{file_path}'.")


def load_data():
    loaded_data = {
        "inventory": {},
        "distribution_history": [],
        "hospitals": [],
        "hospital_distributions": [],
        "supplier_receptions": []

    }

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            section = None
            for line in lines:
                line = line.strip()
                if line == "DISTRIBUTION_HISTORY":
                    section = "DISTRIBUTION_HISTORY"
                elif line == "HOSPITALS":
                    section = "HOSPITALS"
                elif line == "HOSPITAL_DISTRIBUTIONS":
                    section = "HOSPITAL_DISTRIBUTIONS"
                elif line == "SUPPLIER_RECEPTIONS":
                    section = "SUPPLIER_RECEPTIONS"
                else:
                    if section is None:
                        parts = line.split('|')
                        if len(parts) == 4:
                            item_code, quantity, supplier, date_received = parts
                            loaded_data["inventory"][item_code] = {
                                "Quantity Available": int(quantity),
                                "Supplier Code": supplier if supplier != 'None' else None,
                                "Latest Date Received (DD/MM/YYYY)": date_received if date_received != 'None' else None
                            }
                        else:
                            print(f"Skipping line in inventory section: {line}")
                    elif section == "DISTRIBUTION_HISTORY":
                        parts = line.split('|')
                        if len(parts) > 1:
                            item_code, distributions = parts[0], parts[1:]
                            loaded_data["distribution_history"].append([item_code, distributions])
                        else:
                            print(f"Skipping line in distribution history section: {line}")
                    elif section == "HOSPITALS":
                        loaded_data["hospitals"].append(line)
                    elif section == "HOSPITAL_DISTRIBUTIONS":
                        parts = line.split('|')
                        if len(parts) == 4:
                            item_code, quantity, hospital, date_distributed = parts
                            loaded_data["hospital_distributions"].append([item_code, int(quantity), hospital, date_distributed])
                        else:
                            print(f"Skipping line in hospital distributions section: {line}")
                    elif section == "SUPPLIER_RECEPTIONS":
                        parts = line.split('|')
                        if len(parts) == 4:
                            item_code, quantity, supplier, date_received = parts
                            loaded_data["supplier_receptions"].append([item_code, int(quantity), supplier, date_received])
                        else:
                            print(f"Skipping line in supplier receptions section: {line}")

        print(f"Inventory data has been loaded from '{file_path}'.")
        return loaded_data

    except FileNotFoundError:
        print(f"No existing inventory data found. Starting with empty data.")
        return loaded_data


def login():
    attempts = 1
    logged_in = False
    while attempts <= 3:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        for user in controllers:
            if username == user["username"] and password == user["password"]:
                print(f"{user['username']} has successfully logged in.")
                logged_in = True
                break
        if logged_in:
            options()
            break
        else:
            print("Invalid username or password.")
            attempts += 1
            if attempts > 3:
                print("Access Denied")
            else:
                print("Please try again.\n")


def inventory_reception():
    print("\n")
    for code in PPE_item_codes:
        print(code)
    print("All quantities are recorded in boxes.")
    item_code = input("Enter received item code: ").upper()
    if item_code in PPE_items:
        quantity = int(input("Enter the received quantity: "))
        if quantity <= 0:
            print("\nThat is invalid.")
            retry = input("Would you like to retry (Y/N): ").upper()
            if retry == "Y":
                inventory_reception()
            else:
                options()
        else:
            supplier = inventory[item_code]["Supplier Code"]
            if supplier is None:
                supplier = input("Enter the supplier code: ").upper().strip()
                if supplier not in supplier_codes:
                    print("Invalid supplier code.")
                    retry = input("Would you like to retry (Y/N): ").upper()
                    if retry == "Y":
                        inventory_reception()
                    else:
                        options()
            date_received = datetime.date.today().strftime("%d/%m/%Y")
            inventory[item_code]["Quantity Available"] += quantity
            inventory[item_code]["Supplier Code"] = supplier
            inventory[item_code]["Latest Date Received (DD/MM/YYYY)"] = date_received
            supplier_reception = [item_code, quantity, supplier, date_received]
            supplier_receptions.append(supplier_reception)
            print(f"\n{quantity} {item_code} received from {supplier} on {date_received}")
            print(f"{inventory[item_code]['Quantity Available']} available in inventory.")
            save_data()  # Save updated data to file
            options()
    else:
        print("\nThat is invalid.")
        retry = input("Would you like to retry (Y/N): ").upper()
        if retry == "Y":
            inventory_reception()
        else:
            options()


def inventory_distribution():
    print("\n")
    for code in PPE_item_codes:
        print(code)
    print("All quantities are recorded in boxes.")
    item_code = input("Enter distributed item code: ").upper()
    if item_code in PPE_items:
        quantity = int(input("Enter the quantity to be distributed: "))
        if quantity <= 0:
            print("\nInvalid quantity.")
            retry = input("Would you like to retry (Y/N): ").upper()
            if retry == "Y":
                inventory_distribution()
            else:
                options()
        elif quantity > inventory[item_code]["Quantity Available"]:
            print("\nInsufficient stock in inventory.")
            print("Available stock: " + str(inventory[item_code]["Quantity Available"]))
            retry = input("Would you like to retry (Y/N): ").upper()
            if retry == "Y":
                inventory_distribution()
            else:
                options()
        else:
            inventory[item_code]["Quantity Available"] -= quantity
            date_distributed = datetime.date.today().strftime("%d/%m/%Y")
            hospital = input("Enter the hospital code to be distributed to: ").upper().strip()
            if hospital not in hospital_codes:
                print("Invalid hospital code.")
                retry = input("Would you like to retry (Y/N): ").upper()
                if retry == "Y":
                    inventory_distribution()
                else:
                    options()
            if hospital not in hospitals:
                hospitals.append(hospital)
            distribution = [item_code, [(str(quantity) + " distributed to " + hospital + ", " + date_distributed)]]
            distribution_history.append(distribution)
            hospital_distribution = [item_code, quantity, hospital, date_distributed]
            hospital_distributions.append(hospital_distribution)
            print(f"\n{quantity} {item_code} distributed to {hospital} on {date_distributed}")
            print(f"{inventory[item_code]['Quantity Available']} remaining in inventory.")
            save_data()  # Save updated data to file
            options()
    else:
        print("\nThat is an invalid code.")
        retry = input("Would you like to retry (Y/N): ").upper()
        if retry == "Y":
            inventory_distribution()
        else:
            options()


def view_distribution():
    print("\n")
    if not distribution_history:
        print("No distribution history available.")
    else:
        for code in PPE_item_codes:
            print(code)
        print("If no distributions appear, there is no distribution history found.")
        item_code = input("Enter item code to view distributions: ").upper()
        if item_code in PPE_item_codes:
            print("")
            total_dist = 0
            for distribution in distribution_history:
                if item_code == distribution[0]:
                    quantity = int(distribution[1][0].split()[0])
                    total_dist += quantity
                    print(f"{distribution[0]}: {distribution[1]}")
            print(f"Total distributed: {total_dist}")
        else:
            print("\nThat is invalid.")
            retry = input("Would you like to retry (Y/N): ").upper()
            if retry == "Y":
                view_distribution()
            else:
                options()
    options()


def inventory_tracking():
    print("\n")

    def quantity(x):
        return x[1]

    tracking = ["View Quantity (ASC) - 1", "View Quantity (DESC) - 2", "View Low Stock Quantity (<25) - 3"]
    for option in tracking:
        print(option)
    choice = int(input("Enter the number of the option you would like to select (1/2/3): "))
    print("If nothing appears, no item in inventory matches the conditions.")
    print("")
    tracking_quantity = []
    for item_code in inventory:
        tracking_quantity.append([item_code, inventory[item_code]["Quantity Available"]])
    print("(key: Item Code, Quantity)")
    if choice == 1:
        tracking_quantity.sort(key=quantity)
        for item in tracking_quantity:
            print(item)
    elif choice == 2:
        tracking_quantity.sort(reverse=True, key=quantity)
        for item in tracking_quantity:
            print(item)
    elif choice == 3:
        for item in tracking_quantity:
            if item[1] < 25:
                print(item)
        return
    else:
        print("\nThat is invalid.")
        retry = input("Would you like to retry (Y/N): ").upper()
        if retry == "Y":
            inventory_tracking()
        else:
            options()
        return
    options()


def reports():
    print("\n")
    report_types = ["Suppliers - S", "Hospitals (Distributions) - H", "Monthly Transactions - M"]
    for report in report_types:
        print(report)
    choice = input("Select report type (S/H/M): ").upper()
    if choice == "S":
        suppliers = set()
        for item_code in inventory:
            if inventory[item_code]["Supplier Code"]:
                suppliers.add(inventory[item_code]["Supplier Code"])
        print("")
        for supplier in suppliers:
            print(supplier)
        option = input("Select a supplier: ").upper()
        if option not in suppliers:
            print("That is invalid.")
            reports()
        else:
            supplied = [item_code for item_code in inventory if inventory[item_code]["Supplier Code"] == option]
            print(f"\n{option} supplies: {supplied}")
        options()

    elif choice == "H":
        if not hospitals:
            print("No distribution report available.")
            options()
        else:
            print("")
            for hospital in hospitals:
                print(hospital)
            choice = input("Select a hospital: ").upper()
            if choice not in hospitals:
                print("That is invalid.")
                reports()
            else:
                distributed = [[dist[0], dist[1]] for dist in hospital_distributions if dist[2] == choice]
                print("")
                for item_code in inventory:
                    print(item_code)
                option = input("Enter item code: ").upper()
                if option not in PPE_item_codes:
                    print("That is invalid.")
                    reports()
                else:
                    total = sum([dist[1] for dist in distributed if dist[0] == option])
                    print(f"Total received: {total}")
                user_cont = input("Would you like to continue (Y/N): ").upper()
                if user_cont == "Y":
                    reports()
                else:
                    options()

    elif choice == "M":
        cont = True
        while cont:
            print("")
            month = input("Enter month and year (MM/YYYY): ")
            current_year = datetime.date.today().strftime("%Y")
            if len(month) != 7 or month[2] != "/" or not month[:2].isdigit() or not month[3:].isdigit() or int(
                    month[:2]) > 12 or int(month[3:]) > int(current_year):
                print("That is invalid. Please input the month and year according to the given format.")
                reports()
            else:
                print("\nReceptions (R)\nDistributions (D)")
                print("If nothing appears, there is no history found for the given month.")
                option = input("Enter choice (R/D): ").upper()
                print("")
                if option == "R":
                    print("(key: Item Code, Quantity, Supplier, Date Received)")
                    for supplier_reception in supplier_receptions:
                        if supplier_reception[3][3:] == month:
                            print(supplier_reception)
                    user_cont = input("Would you like to continue (Y/N): ").upper()
                    if user_cont == "Y":
                        continue
                    else:
                        cont = False
                elif option == "D":
                    if not hospital_distributions:
                        print("No distribution history available.")
                    else:
                        print("(key: Item Code, Quantity, Hospital, Date Distributed)")
                        for hospital_distribution in hospital_distributions:
                            if hospital_distribution[3][3:] == month:
                                print(hospital_distribution)
                        user_cont = input("Would you like to continue (Y/N): ").upper()
                        if user_cont == "Y":
                            continue
                        else:
                            cont = False
                else:
                    print("That is invalid.")
                    user_cont = input("Would you like to continue (Y/N): ").upper()
                    if user_cont == "Y":
                        reports()
                    else:
                        options()
        options()


def view_data():
    print("\n")
    for item_code, details in inventory.items():
        print(f"{PPE_items[item_code]} ({item_code}): {details['Quantity Available']} boxes available.")
        print(f"  Supplier Code: {details['Supplier Code']}")
        print(f"  Latest Date Received: {details['Latest Date Received (DD/MM/YYYY)']}\n")
    input("Press Enter to return to the main menu.")


def options():
    running = True
    while running:
        print("\nOptions:")
        print("V. Inventory Viewing (V)")
        print("R. Inventory Reception (R)")
        print("D. Inventory Distribution (D)")
        print("T. Inventory Tracking (T)")
        print("S. Distribution Searching (S)")
        print("P. View Reports (P)")
        print("E. Exit (E)")

        user_option = input("Enter your choice (V/R/D/T/S/P/E): ").upper()

        if user_option == "V":
            view_data()
        elif user_option == "R":
            inventory_reception()
        elif user_option == "D":
            inventory_distribution()
        elif user_option == "T":
            inventory_tracking()
        elif user_option == "S":
            view_distribution()
        elif user_option == "P":
            reports()
        elif user_option == "E":
            exit_program()
        else:
            print("That is invalid.")


def exit_program():
    print("\nYou have been logged out.")
    save_data()
    exit()


# Load existing data
loaded_data = load_data()
if loaded_data:
    inventory.update(loaded_data.get("inventory", {}))
    distribution_history = loaded_data.get("distribution_history", distribution_history)
    hospitals = loaded_data.get("hospitals", hospitals)
    hospital_distributions = loaded_data.get("hospital_distributions", hospital_distributions)
    supplier_receptions = loaded_data.get("supplier_receptions", supplier_receptions)

# Save data to ensure the file is created
save_data()

# Create hospital and supplier codes files if not exist
create_hospital_codes_file()
create_supplier_codes_file()

# Start login process
login()
