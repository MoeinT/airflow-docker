CREATE TABLE IF NOT EXISTS allusers (
    firstname TEXT not NULL,
    lastname TEXT not NULL,
    country TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    registrationdate TIMESTAMPTZ NOT NULL);