
-- COMPREHENSIVE BUS RESERVATION DATABASE SCHEMA

CREATE TABLE IF NOT EXISTS operators (
    operator_id INT PRIMARY KEY AUTO_INCREMENT,
    operator_name VARCHAR(100) NOT NULL,
    operator_type ENUM('Government', 'Private') NOT NULL,
    rating DECIMAL(2,1),
    total_buses INT DEFAULT 0,
    contact_number VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bus_types (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    has_ac BOOLEAN DEFAULT TRUE,
    is_sleeper BOOLEAN DEFAULT FALSE,
    price_multiplier DECIMAL(3,2) DEFAULT 1.0,
    amenities JSON
);

CREATE TABLE IF NOT EXISTS routes (
    route_id INT PRIMARY KEY AUTO_INCREMENT,
    source_city VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    distance_km INT,
    estimated_duration_hours DECIMAL(4,2),
    base_price DECIMAL(8,2),
    is_popular BOOLEAN DEFAULT FALSE,
    is_highway_route BOOLEAN DEFAULT TRUE,
    INDEX idx_cities (source_city, destination_city)
);

CREATE TABLE IF NOT EXISTS buses (
    bus_id INT PRIMARY KEY AUTO_INCREMENT,
    bus_number VARCHAR(50) UNIQUE NOT NULL,
    operator_id INT,
    bus_type_id INT,
    route_id INT,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME,
    journey_date DATE NOT NULL,
    ticket_price DECIMAL(8,2) NOT NULL,
    rating DECIMAL(2,1),
    is_night_service BOOLEAN DEFAULT FALSE,
    is_weekend_service BOOLEAN DEFAULT FALSE,
    has_live_tracking BOOLEAN DEFAULT FALSE,
    cancellation_allowed BOOLEAN DEFAULT TRUE,
    status ENUM('Active', 'Cancelled', 'Delayed', 'Completed') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (operator_id) REFERENCES operators(operator_id),
    FOREIGN KEY (bus_type_id) REFERENCES bus_types(type_id),
    FOREIGN KEY (route_id) REFERENCES routes(route_id),
    INDEX idx_journey (journey_date, departure_time),
    INDEX idx_route_date (route_id, journey_date),
    INDEX idx_price (ticket_price),
    INDEX idx_seats (available_seats)
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    bus_id INT NOT NULL,
    user_id INT NOT NULL,
    passenger_name VARCHAR(100),
    passenger_age INT,
    passenger_gender ENUM('M', 'F', 'Other'),
    seat_numbers VARCHAR(200),
    number_of_seats INT NOT NULL,
    total_amount DECIMAL(8,2) NOT NULL,
    booking_status ENUM('Confirmed', 'Cancelled', 'Pending') DEFAULT 'Pending',
    payment_status ENUM('Paid', 'Pending', 'Refunded') DEFAULT 'Pending',
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id),
    INDEX idx_user (user_id),
    INDEX idx_status (booking_status)
);

CREATE TABLE IF NOT EXISTS pricing_rules (
    rule_id INT PRIMARY KEY AUTO_INCREMENT,
    route_id INT,
    day_of_week ENUM('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'),
    time_slot ENUM('Morning','Afternoon','Evening','Night'),
    surge_multiplier DECIMAL(3,2) DEFAULT 1.0,
    is_festival_season BOOLEAN DEFAULT FALSE,
    effective_from DATE,
    effective_to DATE,
    FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

-- INDEXES FOR SEARCH OPTIMIZATION
CREATE INDEX idx_search_routes ON buses(route_id, journey_date, available_seats);
CREATE INDEX idx_price_range ON buses(ticket_price, rating);
CREATE INDEX idx_bus_type_search ON buses(bus_type_id, journey_date);

-- SAMPLE QUERIES

-- Search buses by route and date
-- SELECT * FROM buses WHERE route_id = ? AND journey_date = ? AND available_seats > 0 ORDER BY departure_time;

-- Filter by price range
-- SELECT * FROM buses WHERE ticket_price BETWEEN ? AND ? AND journey_date = ?;

-- Top rated buses
-- SELECT * FROM buses WHERE rating >= 4.0 ORDER BY rating DESC, ticket_price ASC;

-- Night services
-- SELECT * FROM buses WHERE is_night_service = TRUE AND journey_date = ?;

-- Popular routes
-- SELECT source_city, destination_city, COUNT(*) as trip_count FROM routes r JOIN buses b ON r.route_id = b.route_id GROUP BY r.route_id ORDER BY trip_count DESC LIMIT 10;
