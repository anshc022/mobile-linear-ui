CREATE TABLE IF NOT EXISTS client_requests (
    id SERIAL PRIMARY KEY,
    content TEXT,
    media_urls TEXT[],
    category VARCHAR(50),
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verify table existence by selecting from information_schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name = 'client_requests';

-- Verify columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'client_requests';
