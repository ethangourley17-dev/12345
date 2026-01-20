-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    tier VARCHAR(20) NOT NULL,
    price_paid DECIMAL(10, 2) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    stripe_session_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    pdf_url TEXT,
    pdf_storage_path TEXT,
    roof_area_sqft DECIMAL(10, 2),
    roof_area_sqm DECIMAL(10, 2),
    segment_count INT,
    solar_panel_count INT,
    measurements JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- API logs table
CREATE TABLE IF NOT EXISTS api_logs (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    api_provider VARCHAR(50),
    request_data JSONB,
    response_data JSONB,
    cost DECIMAL(10, 4),
    response_time_ms INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_orders_email ON orders(customer_email);
CREATE INDEX idx_orders_created ON orders(created_at DESC);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_reports_order ON reports(order_id);