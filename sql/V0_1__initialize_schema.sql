CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE city (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    population INTEGER,
    reference_url TEXT,
    country_id INT REFERENCES country(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE museum (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL,
    number_of_visitors INT,
    reference_url TEXT,
    city_id INT REFERENCES city(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE museum_attributes (
    id SERIAL PRIMARY KEY,
    museum_id INT REFERENCES museum(id),
    attribute_key VARCHAR(100) NOT NULL,
    attribute_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(museum_id, attribute_key)
);

CREATE TABLE import_log (
    id SERIAL PRIMARY KEY,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    result JSONB,
    status VARCHAR(20) NOT NULL
);

-- Create indexes for faster lookups
CREATE INDEX idx_museum_attributes_key ON museum_attributes(attribute_key);
CREATE INDEX idx_museum_name ON museum(name);
CREATE INDEX idx_city_name ON city(name);
CREATE INDEX idx_country_name ON country(name);
