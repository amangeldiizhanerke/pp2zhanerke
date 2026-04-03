from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(30) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created")

def search_by_pattern():
    pattern = input("Enter search pattern: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def upsert_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Insert or update done")

def insert_many_contacts():
    names = input("Enter names separated by comma: ").split(",")
    phones = input("Enter phones separated by comma: ").split(",")

    names = [name.strip() for name in names]
    phones = [phone.strip() for phone in phones]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_many_contacts(%s, %s)", (names, phones))
    conn.commit()
    cur.close()
    conn.close()
    print("Bulk insert finished")

def show_paginated():
    lim = int(input("Enter limit: ").strip())
    offs = int(input("Enter offset: ").strip())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (lim, offs))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_contact():
    value = input("Enter name or phone to delete: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact_proc(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted")

def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def main():
    while True:
        print("\n1. Create table")
        print("2. Search by pattern")
        print("3. Upsert contact")
        print("4. Insert many contacts")
        print("5. Show paginated contacts")
        print("6. Delete contact")
        print("7. Show all contacts")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            search_by_pattern()
        elif choice == "3":
            upsert_contact()
        elif choice == "4":
            insert_many_contacts()
        elif choice == "5":
            show_paginated()
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