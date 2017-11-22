CREATE TABLE users (
  username TEXT PRIMARY KEY,
  fullname TEXT,
  password TEXT,
  email TEXT,
  can_manage_restaurants boolean
);

CREATE TABLE sessions (
  token text,
  username text REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE restaurants (
  restaurant_id SERIAL PRIMARY KEY,
  name text
);

CREATE TABLE menuitems (
  item_id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
  name TEXT,
  price NUMERIC(7,2)
);

CREATE TABLE grouporders (
  order_id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants(restaurant_id) ON DELETE RESTRICT,
  organizer TEXT REFERENCES users(username) ON DELETE RESTRICT,
  ordertime TIMESTAMP WITH TIME ZONE
);

CREATE TABLE lineitems (
  username TEXT REFERENCES users(username) ON DELETE RESTRICT,
  order_id INT REFERENCES grouporders(order_id) ON DELETE CASCADE,
  item_id INT REFERENCES menuitems(item_id) ON DELETE CASCADE
);