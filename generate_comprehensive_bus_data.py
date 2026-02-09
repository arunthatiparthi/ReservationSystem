import os
import django
from datetime import datetime, date, time, timedelta
import random
import json
import csv
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busreserve.settings')
django.setup()

from reservation.models import Bus

# Clear existing bus data
Bus.objects.all().delete()
print("=" * 80)
print("COMPREHENSIVE INDIA-WIDE BUS RESERVATION DATABASE GENERATOR")
print("=" * 80)

# COMPREHENSIVE INDIAN CITIES DATABASE
CITIES = {
    # Metro Cities
    'Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune',
    
    # North India
    'Noida', 'Gurgaon', 'Faridabad', 'Ghaziabad', 'Greater Noida',
    'Agra', 'Mathura', 'Lucknow', 'Kanpur', 'Varanasi', 'Allahabad', 'Bareilly',
    'Meerut', 'Aligarh', 'Moradabad', 'Saharanpur', 'Gorakhpur',
    
    # Punjab & Haryana
    'Chandigarh', 'Amritsar', 'Ludhiana', 'Jalandhar', 'Patiala', 'Bathinda',
    'Mohali', 'Ambala', 'Karnal', 'Panipat', 'Sonipat', 'Rohtak',
    
    # Rajasthan
    'Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer', 'Bikaner', 'Alwar',
    'Bharatpur', 'Sikar', 'Jaisalmer', 'Mount Abu',
    
    # Himachal & J&K
    'Shimla', 'Manali', 'Dharamshala', 'Kullu', 'Solan', 'Kasauli',
    'Srinagar', 'Jammu', 'Leh', 'Pathankot',
    
    # Uttarakhand
    'Dehradun', 'Haridwar', 'Rishikesh', 'Nainital', 'Mussoorie', 'Roorkee',
    'Haldwani', 'Rudrapur',
    
    # Madhya Pradesh
    'Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain', 'Sagar',
    'Ratlam', 'Satna', 'Dewas', 'Rewa',
    
    # Maharashtra
    'Thane', 'Navi Mumbai', 'Panvel', 'Nashik', 'Nagpur', 'Aurangabad',
    'Solapur', 'Kolhapur', 'Sangli', 'Ahmednagar', 'Latur', 'Jalgaon',
    
    # Gujarat
    'Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar', 'Bhavnagar',
    'Jamnagar', 'Junagadh', 'Anand', 'Navsari', 'Bharuch',
    
    # Goa
    'Goa', 'Panaji', 'Margao', 'Vasco', 'Mapusa', 'Ponda',
    
    # Karnataka
    'Mysore', 'Mangalore', 'Hubli', 'Belgaum', 'Davangere', 'Bellary',
    'Tumkur', 'Shimoga', 'Udupi', 'Hassan', 'Mandya', 'Gulbarga',
    
    # Tamil Nadu
    'Coimbatore', 'Madurai', 'Trichy', 'Salem', 'Tiruppur', 'Erode',
    'Vellore', 'Thanjavur', 'Dindigul', 'Tirunelveli', 'Kanyakumari',
    'Pondicherry', 'Hosur', 'Karur', 'Nagercoil', 'Tuticorin',
    
    # Kerala
    'Kochi', 'Trivandrum', 'Kozhikode', 'Thrissur', 'Kollam', 'Kottayam',
    'Kannur', 'Alappuzha', 'Palakkad', 'Malappuram', 'Munnar', 'Wayanad',
    
    # Andhra Pradesh & Telangana
    'Vijayawada', 'Visakhapatnam', 'Guntur', 'Nellore', 'Warangal',
    'Tirupati', 'Kakinada', 'Rajahmundry', 'Anantapur', 'Kadapa',
    
    # West Bengal
    'Howrah', 'Siliguri', 'Durgapur', 'Asansol', 'Darjeeling', 'Kharagpur',
    
    # Odisha
    'Bhubaneswar', 'Cuttack', 'Puri', 'Rourkela', 'Sambalpur', 'Brahmapur',
    
    # Bihar & Jharkhand
    'Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Ranchi', 'Jamshedpur',
    'Dhanbad', 'Bokaro',
    
    # Northeast
    'Guwahati', 'Shillong', 'Imphal', 'Agartala', 'Aizawl', 'Kohima',
    'Itanagar', 'Gangtok', 'Tezpur', 'Dibrugarh',
    
    # Chhattisgarh
    'Raipur', 'Bilaspur', 'Durg', 'Bhilai', 'Korba', 'Raigarh'
}

# BUS OPERATORS - Mix of Government and Private
OPERATORS = {
    'Government': [
        'KSRTC', 'TNSTC', 'SETC', 'APSRTC', 'MSRTC', 'RSRTC', 'GSRTC',
        'UPSRTC', 'HRTC', 'Kerala RTC', 'DTC', 'Goa RTC', 'OSRTC'
    ],
    'Private': [
        'RedBus Express', 'VRL Travels', 'SRS Travels', 'Orange Travels',
        'Parveen Travels', 'Kallada Travels', 'KPN Travels', 'Neeta Travels',
        'IntrCity SmartBus', 'Jabbar Travels', 'Paulo Travels', 'Shrinath Travels',
        'Raj Travels', 'National Travels', 'Green Line Travels', 'Konduskar Travels',
        'SR Travels', 'Greenline Travels', 'Sharma Travels', 'Mahasagar Travels'
    ]
}

# BUS TYPES WITH PRICING MULTIPLIERS
BUS_TYPES = [
    {'name': 'AC Sleeper', 'capacity': 35, 'price_mult': 1.8, 'rating_boost': 0.3},
    {'name': 'Non-AC Sleeper', 'capacity': 40, 'price_mult': 1.3, 'rating_boost': 0.1},
    {'name': 'AC Semi-Sleeper', 'capacity': 40, 'price_mult': 1.5, 'rating_boost': 0.2},
    {'name': 'Volvo AC', 'capacity': 40, 'price_mult': 2.0, 'rating_boost': 0.4},
    {'name': 'Multi-Axle Volvo', 'capacity': 43, 'price_mult': 2.2, 'rating_boost': 0.5},
    {'name': 'AC Seater', 'capacity': 45, 'price_mult': 1.4, 'rating_boost': 0.2},
    {'name': 'Non-AC Seater', 'capacity': 50, 'price_mult': 1.0, 'rating_boost': 0.0},
    {'name': 'Electric Bus', 'capacity': 40, 'price_mult': 1.6, 'rating_boost': 0.3},
]

# HIGH DEMAND ROUTES (Major corridors)
POPULAR_ROUTES = [
    # North Corridor
    ('Delhi', 'Chandigarh', 600, 5), ('Delhi', 'Jaipur', 750, 5.5),
    ('Delhi', 'Agra', 550, 4), ('Delhi', 'Lucknow', 800, 8),
    ('Delhi', 'Shimla', 900, 8), ('Delhi', 'Manali', 1400, 13),
    ('Delhi', 'Haridwar', 650, 5.5), ('Delhi', 'Dehradun', 700, 6),
    
    # Mumbai Corridor
    ('Mumbai', 'Pune', 450, 3.5), ('Mumbai', 'Nashik', 350, 4),
    ('Mumbai', 'Goa', 1200, 12), ('Mumbai', 'Ahmedabad', 900, 9),
    ('Mumbai', 'Surat', 650, 6), ('Mumbai', 'Indore', 1100, 13),
    ('Mumbai', 'Aurangabad', 750, 8),
    
    # South Corridor - Bangalore Hub
    ('Bangalore', 'Chennai', 950, 7), ('Bangalore', 'Hyderabad', 1000, 8),
    ('Bangalore', 'Mysore', 400, 3), ('Bangalore', 'Coimbatore', 850, 7),
    ('Bangalore', 'Kochi', 1200, 11), ('Bangalore', 'Goa', 1100, 12),
    ('Bangalore', 'Mangalore', 800, 8), ('Bangalore', 'Pondicherry', 750, 6),
    
    # Chennai Hub
    ('Chennai', 'Coimbatore', 850, 7.5), ('Chennai', 'Madurai', 700, 8),
    ('Chennai', 'Trichy', 600, 6), ('Chennai', 'Salem', 650, 6),
    ('Chennai', 'Pondicherry', 350, 3), ('Chennai', 'Bangalore', 950, 7),
    ('Chennai', 'Tirupati', 350, 3.5), ('Chennai', 'Vellore', 300, 3),
    
    # Kerala Corridor
    ('Kochi', 'Trivandrum', 450, 5), ('Kochi', 'Kozhikode', 350, 4),
    ('Kochi', 'Bangalore', 1200, 11), ('Kochi', 'Coimbatore', 350, 4),
    ('Trivandrum', 'Kanyakumari', 250, 2.5), ('Kozhikode', 'Bangalore', 950, 9),
    
    # East Corridor
    ('Kolkata', 'Siliguri', 900, 10), ('Kolkata', 'Patna', 650, 8),
    ('Kolkata', 'Bhubaneswar', 850, 8), ('Kolkata', 'Ranchi', 700, 8),
    
    # Gujarat Circuit
    ('Ahmedabad', 'Surat', 350, 3.5), ('Ahmedabad', 'Vadodara', 250, 2),
    ('Ahmedabad', 'Rajkot', 400, 4), ('Surat', 'Mumbai', 500, 5),
    
    # Inter-State Premium
    ('Hyderabad', 'Vijayawada', 500, 5), ('Hyderabad', 'Visakhapatnam', 850, 10),
    ('Pune', 'Goa', 900, 10), ('Jaipur', 'Udaipur', 550, 6),
]

# TIME SLOTS - Multiple departures throughout the day
TIME_SLOTS = [
    time(4, 0), time(4, 30), time(5, 0), time(5, 30), time(6, 0), time(6, 30),
    time(7, 0), time(7, 30), time(8, 0), time(8, 30), time(9, 0), time(9, 30),
    time(10, 0), time(10, 30), time(11, 0), time(11, 30), time(12, 0), time(13, 0),
    time(14, 0), time(15, 0), time(16, 0), time(17, 0), time(18, 0), time(19, 0),
    time(20, 0), time(20, 30), time(21, 0), time(21, 30), time(22, 0), time(22, 30),
    time(23, 0), time(23, 30)
]

def calculate_arrival_time(departure_time, duration_hours):
    """Calculate arrival time based on departure and duration"""
    departure_dt = datetime.combine(date.today(), departure_time)
    arrival_dt = departure_dt + timedelta(hours=duration_hours)
    return arrival_dt.time()

def get_dynamic_price(base_price, bus_type, is_night, is_weekend, days_ahead):
    """Calculate dynamic pricing"""
    price = base_price * bus_type['price_mult']
    
    # Night service premium
    if is_night:
        price *= 1.15
    
    # Weekend surge
    if is_weekend:
        price *= 1.25
    
    # Early booking discount / last minute surge
    if days_ahead > 15:
        price *= 0.9  # Early bird discount
    elif days_ahead < 3:
        price *= 1.3  # Last minute surge
    
    return round(price, 2)

def generate_bus_data():
    """Generate comprehensive bus database"""
    
    all_buses = []
    bus_counter = 1000
    
    # Calculate date range - Feb and March 2026
    start_date = date.today()
    feb_remaining = 28 - start_date.day + 1
    total_days = feb_remaining + 31  # Feb remaining + March
    
    print(f"\n📅 Generating data for {total_days} days (Feb {start_date.day} - March 31)")
    print(f"🚌 Processing {len(POPULAR_ROUTES)} major routes")
    print(f"🏢 Operators: {len(OPERATORS['Government']) + len(OPERATORS['Private'])}")
    
    # Generate buses for all popular routes
    for day_offset in range(total_days):
        current_date = start_date + timedelta(days=day_offset)
        is_weekend = current_date.weekday() >= 5  # Saturday = 5, Sunday = 6
        days_ahead = day_offset
        
        for source, dest, base_price, duration in POPULAR_ROUTES:
            # Generate 4-8 buses per route per day
            num_buses = random.randint(6, 10) if is_weekend else random.randint(4, 7)
            
            selected_times = random.sample(TIME_SLOTS, min(num_buses, len(TIME_SLOTS)))
            
            for dept_time in selected_times:
                bus_type = random.choice(BUS_TYPES)
                is_night = dept_time.hour >= 20 or dept_time.hour <= 5
                
                # Select operator
                operator_category = random.choice(['Government', 'Private'])
                operator = random.choice(OPERATORS[operator_category])
                
                bus_counter += 1
                bus_name = f"{bus_type['name'][:3].upper()}-{bus_counter}"
                
                # Dynamic pricing
                price = get_dynamic_price(base_price, bus_type, is_night, is_weekend, days_ahead)
                
                # Calculate arrival
                arrival_time = calculate_arrival_time(dept_time, duration)
                
                # Rating (govt buses slightly lower)
                base_rating = 3.5 if operator_category == 'Government' else 3.8
                rating = round(base_rating + bus_type['rating_boost'] + random.uniform(0, 0.4), 1)
                rating = min(rating, 4.9)  # Cap at 4.9
                
                # Seats available
                total_capacity = bus_type['capacity']
                seats_booked = random.randint(0, total_capacity) if days_ahead < 7 else random.randint(0, int(total_capacity * 0.3))
                seats_available = total_capacity - seats_booked
                
                bus_data = {
                    'bus_id': bus_counter,
                    'bus_name': bus_name,
                    'source': source,
                    'dest': dest,
                    'operator': operator,
                    'bus_type': bus_type['name'],
                    'capacity': total_capacity,
                    'seats_available': seats_available,
                    'departure_time': dept_time,
                    'arrival_time': arrival_time,
                    'duration_hours': duration,
                    'price': price,
                    'date': current_date,
                    'rating': rating,
                    'is_night_service': is_night,
                    'is_weekend': is_weekend,
                    'is_popular_route': True,
                    'cancellation_allowed': random.choice([True, True, True, False]),
                    'live_tracking': operator_category == 'Private' and random.random() > 0.3,
                }
                
                all_buses.append(bus_data)
    
    print(f"\n✅ Generated {len(all_buses)} bus records")
    return all_buses

def save_to_django_db(buses_data):
    """Save to Django database"""
    print("\n💾 Saving to Django database...")
    created_count = 0
    
    for bus_data in buses_data:
        try:
            Bus.objects.create(
                bus_name=bus_data['bus_name'],
                capacity=bus_data['capacity'],
                source=bus_data['source'],
                dest=bus_data['dest'],
                rem=bus_data['seats_available'],
                price=Decimal(str(bus_data['price'])),
                date=bus_data['date'],
                time=bus_data['departure_time']
            )
            created_count += 1
            
            if created_count % 1000 == 0:
                print(f"  ✓ {created_count} buses saved...")
        except Exception as e:
            if created_count < 5:
                print(f"  ✗ Error: {e}")
    
    print(f"✅ {created_count} buses saved to database")
    return created_count

def export_to_json(buses_data, filename='bus_data.json'):
    """Export to JSON"""
    print(f"\n📄 Exporting to JSON: {filename}")
    
    # Convert datetime objects to strings
    json_data = []
    for bus in buses_data:
        bus_copy = bus.copy()
        bus_copy['date'] = str(bus['date'])
        bus_copy['departure_time'] = str(bus['departure_time'])
        bus_copy['arrival_time'] = str(bus['arrival_time'])
        json_data.append(bus_copy)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON exported: {len(json_data)} records")

def export_to_csv(buses_data, filename='bus_data.csv'):
    """Export to CSV"""
    print(f"\n📊 Exporting to CSV: {filename}")
    
    if not buses_data:
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = buses_data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(buses_data)
    
    print(f"✅ CSV exported: {len(buses_data)} records")

def generate_sql_schema(filename='bus_schema.sql'):
    """Generate SQL schema"""
    print(f"\n🗃️  Generating SQL schema: {filename}")
    
    sql_schema = """
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
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sql_schema)
    
    print(f"✅ SQL schema generated")

def generate_analytics_report(buses_data):
    """Generate analytics report"""
    print("\n" + "="*80)
    print("📈 DATABASE ANALYTICS REPORT")
    print("="*80)
    
    total_buses = len(buses_data)
    total_routes = len(set((b['source'], b['dest']) for b in buses_data))
    operators = set(b['operator'] for b in buses_data)
    bus_types = set(b['bus_type'] for b in buses_data)
    
    avg_price = sum(b['price'] for b in buses_data) / total_buses
    max_price = max(b['price'] for b in buses_data)
    min_price = min(b['price'] for b in buses_data)
    
    avg_rating = sum(b['rating'] for b in buses_data) / total_buses
    
    night_services = sum(1 for b in buses_data if b['is_night_service'])
    weekend_services = sum(1 for b in buses_data if b['is_weekend'])
    
    print(f"\n🚌 Total Buses: {total_buses:,}")
    print(f"🛣️  Total Routes: {total_routes}")
    print(f"🏢 Total Operators: {len(operators)}")
    print(f"🚍 Bus Types: {len(bus_types)}")
    
    print(f"\n💰 PRICING ANALYTICS:")
    print(f"   Average Price: ₹{avg_price:.2f}")
    print(f"   Max Price: ₹{max_price:.2f}")
    print(f"   Min Price: ₹{min_price:.2f}")
    
    print(f"\n⭐ RATING ANALYTICS:")
    print(f"   Average Rating: {avg_rating:.2f}/5.0")
    
    print(f"\n🌙 SERVICE DISTRIBUTION:")
    print(f"   Night Services: {night_services:,} ({night_services/total_buses*100:.1f}%)")
    print(f"   Weekend Services: {weekend_services:,} ({weekend_services/total_buses*100:.1f}%)")
    
    # Top 10 routes by frequency
    route_freq = {}
    for b in buses_data:
        route = f"{b['source']} → {b['dest']}"
        route_freq[route] = route_freq.get(route, 0) + 1
    
    print(f"\n🔥 TOP 10 ROUTES BY FREQUENCY:")
    for i, (route, count) in enumerate(sorted(route_freq.items(), key=lambda x: x[1], reverse=True)[:10], 1):
        print(f"   {i}. {route}: {count} buses")
    
    print("\n" + "="*80)

# MAIN EXECUTION
if __name__ == '__main__':
    print("\n🚀 Starting comprehensive bus data generation...")
    
    # Generate data
    buses_data = generate_bus_data()
    
    # Save to Django DB
    saved_count = save_to_django_db(buses_data)
    
    # Export to multiple formats
    export_to_json(buses_data)
    export_to_csv(buses_data)
    generate_sql_schema()
    
    # Generate analytics
    generate_analytics_report(buses_data)
    
    print("\n" + "="*80)
    print("✅ DATA GENERATION COMPLETE!")
    print("="*80)
    print("\nGenerated Files:")
    print("  📄 bus_data.json - Complete JSON export")
    print("  📊 bus_data.csv - CSV for Excel/imports")
    print("  🗃️  bus_schema.sql - SQL table schemas")
    print(f"\n💾 Database: {saved_count:,} buses saved")
    print("\n🎯 Ready for production use!")
    print("="*80)
