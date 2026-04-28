CREATE OR REPLACE PROCEDURE add_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR,
    p_phone VARCHAR,
    p_phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_contact_id INTEGER;
    new_group_id INTEGER;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO new_group_id
    FROM groups
    WHERE name = p_group_name;

    INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
    VALUES (p_first_name, p_last_name, p_email, p_birthday, new_group_id)
    RETURNING id INTO new_contact_id;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (new_contact_id, p_phone, p_phone_type);
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    found_contact_id INTEGER;
BEGIN
    SELECT id INTO found_contact_id
    FROM contacts
    WHERE first_name = p_contact_name
    LIMIT 1;

    IF found_contact_id IS NOT NULL THEN
        INSERT INTO phones(contact_id, phone, type)
        VALUES (found_contact_id, p_phone, p_type);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_group_id INTEGER;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO new_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = new_group_id
    WHERE first_name = p_contact_name;
END;
$$;


CREATE OR REPLACE PROCEDURE update_contact_phone(
    p_first_name VARCHAR,
    p_new_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE phones
    SET phone = p_new_phone
    WHERE contact_id IN (
        SELECT id FROM contacts WHERE first_name = p_first_name
    );
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact_by_name(
    p_first_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_first_name;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR,
    date_added TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name, c.last_name, c.email, c.birthday, g.name, p.phone, p.type, c.date_added
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR g.name ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR,
    date_added TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name, c.last_name, c.email, c.birthday, g.name, p.phone, p.type, c.date_added
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;