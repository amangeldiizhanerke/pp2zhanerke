import csv
import json
from connect import connect


def print_rows(rows):
    if not rows:
        print("Nothing found.")
        return
    for row in rows:
        print(row)


def add_contact():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group (Family/Work/Friend/Other): ")
    phone = input("Phone number: ")
    phone_type = input("Phone type (home/work/mobile): ")

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL add_contact(%s,%s,%s,%s,%s,%s,%s)",
            (first_name, last_name, email, birthday, group, phone, phone_type)
        )

        conn.commit()
        print("Contact added.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def show_all_contacts():
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, c.birthday,
                   g.name, p.phone, p.type, c.date_added
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id;
        """)

        print_rows(cur.fetchall())

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def search_contact():
    query = input("Search name/email/phone/group: ")

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, c.birthday,
                   g.name, p.phone, p.type, c.date_added
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.first_name ILIKE %s
               OR c.last_name ILIKE %s
               OR c.email ILIKE %s
               OR g.name ILIKE %s
               OR p.phone ILIKE %s
            ORDER BY c.id;
        """, (
            "%" + query + "%",
            "%" + query + "%",
            "%" + query + "%",
            "%" + query + "%",
            "%" + query + "%"
        ))

        print_rows(cur.fetchall())

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def filter_by_group():
    group = input("Group name: ")

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, c.birthday,
                   g.name, p.phone, p.type, c.date_added
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name ILIKE %s
            ORDER BY c.first_name;
        """, ("%" + group + "%",))

        print_rows(cur.fetchall())

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.first_name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.date_added"
    else:
        print("Wrong option.")
        return

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(f"""
            SELECT c.first_name, c.last_name, c.email, c.birthday,
                   g.name, p.phone, p.type, c.date_added
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY {order_by};
        """)

        print_rows(cur.fetchall())

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def paginate_contacts():
    limit = 3
    offset = 0

    while True:
        try:
            conn = connect()
            cur = conn.cursor()

            cur.execute("""
                SELECT c.first_name, c.last_name, c.email, c.birthday,
                       g.name, p.phone, p.type, c.date_added
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                ORDER BY c.id
                LIMIT %s OFFSET %s;
            """, (limit, offset))

            rows = cur.fetchall()

            print("\nPAGE")
            print_rows(rows)

            cur.close()
            conn.close()

        except Exception as error:
            print("Error:", error)
            return

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Wrong command.")


def update_phone():
    first_name = input("First name: ")
    new_phone = input("New phone: ")

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("CALL update_contact_phone(%s,%s)", (first_name, new_phone))

        conn.commit()
        print("Phone updated.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def add_phone():
    first_name = input("Contact first name: ")
    phone = input("New phone: ")
    phone_type = input("Phone type (home/work/mobile): ")

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("CALL add_phone(%s,%s,%s)", (first_name, phone, phone_type))

        conn.commit()
        print("Phone added.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def move_to_group():
    first_name = input("Contact first name: ")
    group = input("New group: ")

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("CALL move_to_group(%s,%s)", (first_name, group))

        conn.commit()
        print("Contact moved.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def delete_contact():
    first_name = input("First name to delete: ")

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("CALL delete_contact_by_name(%s)", (first_name,))

        conn.commit()
        print("Contact deleted.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def import_from_csv():
    try:
        conn = connect()
        cur = conn.cursor()

        with open("contacts.csv", "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cur.execute(
                    "CALL add_contact(%s,%s,%s,%s,%s,%s,%s)",
                    (
                        row["first_name"],
                        row["last_name"],
                        row["email"],
                        row["birthday"],
                        row["group"],
                        row["phone"],
                        row["phone_type"]
                    )
                )

        conn.commit()
        print("CSV imported.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def import_from_json():
    try:
        conn = connect()
        cur = conn.cursor()

        with open("contacts.json", "r") as file:
            data = json.load(file)

        for item in data:
            cur.execute(
                "SELECT id FROM contacts WHERE first_name=%s",
                (item["first_name"],)
            )

            exists = cur.fetchone()

            if exists:
                answer = input(f"{item['first_name']} exists. skip/overwrite: ")

                if answer == "skip":
                    continue
                elif answer == "overwrite":
                    cur.execute("CALL delete_contact_by_name(%s)", (item["first_name"],))

            first_phone = item["phones"][0]

            cur.execute(
                "CALL add_contact(%s,%s,%s,%s,%s,%s,%s)",
                (
                    item["first_name"],
                    item["last_name"],
                    item["email"],
                    item["birthday"],
                    item["group"],
                    first_phone["phone"],
                    first_phone["type"]
                )
            )

            for phone in item["phones"][1:]:
                cur.execute(
                    "CALL add_phone(%s,%s,%s)",
                    (item["first_name"], phone["phone"], phone["type"])
                )

        conn.commit()
        print("JSON imported.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def export_to_json():
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday,
                   g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id;
        """)

        rows = cur.fetchall()
        contacts = {}

        for row in rows:
            contact_id = row[0]

            if contact_id not in contacts:
                contacts[contact_id] = {
                    "first_name": row[1],
                    "last_name": row[2],
                    "email": row[3],
                    "birthday": str(row[4]),
                    "group": row[5],
                    "phones": []
                }

            contacts[contact_id]["phones"].append({
                "phone": row[6],
                "type": row[7]
            })

        with open("exported_contacts.json", "w") as file:
            json.dump(list(contacts.values()), file, indent=4)

        print("Exported to exported_contacts.json")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Add contact")
        print("2. Show all contacts")
        print("3. Search contact")
        print("4. Filter by group")
        print("5. Sort contacts")
        print("6. Paginated view")
        print("7. Update phone")
        print("8. Add phone")
        print("9. Move to group")
        print("10. Delete contact")
        print("11. Import from CSV")
        print("12. Import from JSON")
        print("13. Export to JSON")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_all_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            filter_by_group()
        elif choice == "5":
            sort_contacts()
        elif choice == "6":
            paginate_contacts()
        elif choice == "7":
            update_phone()
        elif choice == "8":
            add_phone()
        elif choice == "9":
            move_to_group()
        elif choice == "10":
            delete_contact()
        elif choice == "11":
            import_from_csv()
        elif choice == "12":
            import_from_json()
        elif choice == "13":
            export_to_json()
        elif choice == "0":
            print("Program finished.")
            break
        else:
            print("Wrong option.")


if __name__ == "__main__":
    menu()