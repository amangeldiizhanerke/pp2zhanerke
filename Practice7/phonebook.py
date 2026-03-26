import csv  # module to work with CSV files (read/write tabular data)
from connect import get_connection  # function to connect to PostgreSQL database

def create_table():
    conn = get_connection()  # open connection to DB
    cur = conn.cursor()  # create cursor to execute SQL commands
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,  # auto-increment ID
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(30) NOT NULL UNIQUE  # UNIQUE prevents duplicate numbers
        )
    """)
    conn.commit()  # save changes
    cur.close()
    conn.close()
    print("Table created")

def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    # open CSV file and read it as dictionary (column_name -> value)
    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # insert each row into database
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                    (row["first_name"], row["phone"])
                )
                conn.commit()
            except:
                conn.rollback()  # undo if error (e.g. duplicate phone)

    cur.close()
    conn.close()
    print("Data inserted from CSV")

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact added")

def update_contact():
    old_name = input("Enter the name to update: ")
    new_name = input("Enter new name: ")
    new_phone = input("Enter new phone: ")

    conn = get_connection()
    cur = conn.cursor()
    # update existing contact
    cur.execute(
        "UPDATE phonebook SET first_name = %s, phone = %s WHERE first_name = %s",
        (new_name, new_phone, old_name)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated")

def query_contacts():
    print("1. Search by name")
    print("2. Search by phone prefix")
    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "2":
        prefix = input("Enter prefix: ")
        # LIKE used to search by beginning of phone number
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + "%",))
    else:
        print("Invalid choice")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()  # get all results
    for row in rows:
        print(row)

    cur.close()
    conn.close()

def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")
    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("Invalid choice")
        cur.close()
        conn.close()
        return

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted")

def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")  # sort by ID
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def main():
    while True:
        # simple CLI menu
        print("\n1. Create table")
        print("2. Insert from CSV")
        print("3. Insert from console")
        print("4. Update contact")
        print("5. Query contacts")
        print("6. Delete contact")
        print("7. Show all contacts")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            show_all_contacts()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()