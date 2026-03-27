CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_contacts(
    names TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    current_name TEXT;
    current_phone TEXT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        current_name := trim(names[i]);
        current_phone := trim(phones[i]);

        IF current_phone ~ '^[0-9]+$' AND length(current_phone) >= 5 THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = current_name) THEN
                UPDATE phonebook
                SET phone = current_phone
                WHERE first_name = current_name;
            ELSE
                INSERT INTO phonebook(first_name, phone)
                VALUES (current_name, current_phone);
            END IF;
        ELSE
            RAISE NOTICE 'Incorrect data: % - %', current_name, current_phone;
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_proc(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value OR phone = p_value;
END;
$$;