CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    category_id INT REFERENCES categories(id) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INT CHECK (age > 0 AND age < 150)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(id) NOT NULL,
    product_id INT REFERENCES products(id) NOT NULL,
    user_id INT REFERENCES users(id) NOT NULL,
    quantity INT CHECK (quantity > 0) DEFAULT 1,
    created_at TIMESTAMP NOT NULL
);