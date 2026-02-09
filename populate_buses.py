import os
import django
from datetime import datetime, date, time, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busreserve.settings')
django.setup()

from reservation.models import Bus

# Clear existing bus data
Bus.objects.all().delete()
print("Cleared existing bus data")

# Comprehensive list of Indian cities covering all states
cities = {
    # North India
    'Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Ghaziabad',
    # Uttar Pradesh
    'Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Meerut', 'Allahabad', 'Bareilly', 'Aligarh', 'Moradabad', 'Mathura',
    # Punjab & Haryana
    'Chandigarh', 'Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda', 'Mohali', 'Ambala', 'Karnal', 'Panipat',
    # Rajasthan
    'Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer', 'Bikaner', 'Alwar', 'Bharatpur', 'Sikar', 'Jaisalmer',
    # Himachal Pradesh & J&K
    'Shimla', 'Manali', 'Dharamshala', 'Kullu', 'Solan', 'Srinagar', 'Jammu', 'Leh',
    # Uttarakhand
    'Dehradun', 'Haridwar', 'Rishikesh', 'Nainital', 'Mussoorie', 'Roorkee',
    # Madhya Pradesh
    'Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain', 'Sagar', 'Ratlam', 'Satna',
    # Maharashtra
    'Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Solapur', 'Thane', 'Navi Mumbai', 'Kolhapur', 'Sangli',
    # Gujarat
    'Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar', 'Bhavnagar', 'Jamnagar', 'Junagadh', 'Anand',
    # Goa
    'Goa', 'Panaji', 'Margao', 'Vasco',
    # South India - Karnataka
    'Bangalore', 'Mysore', 'Mangalore', 'Hubli', 'Belgaum', 'Davangere', 'Bellary', 'Tumkur', 'Shimoga',
    # Tamil Nadu
    'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tiruppur', 'Erode', 'Vellore', 'Thanjavur', 'Kanyakumari',
    # Kerala
    'Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur', 'Kollam', 'Kottayam', 'Kannur', 'Alappuzha', 'Palakkad',
    # Andhra Pradesh & Telangana
    'Hyderabad', 'Vijayawada', 'Visakhapatnam', 'Guntur', 'Nellore', 'Warangal', 'Tirupati', 'Kakinada', 'Rajahmundry',
    # East India - West Bengal
    'Kolkata', 'Howrah', 'Siliguri', 'Durgapur', 'Asansol', 'Darjeeling', 'Kharagpur',
    # Odisha
    'Bhubaneswar', 'Cuttack', 'Puri', 'Rourkela', 'Sambalpur', 'Brahmapur',
    # Bihar & Jharkhand
    'Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Ranchi', 'Jamshedpur', 'Dhanbad', 'Bokaro',
    # Northeast India
    'Guwahati', 'Shillong', 'Imphal', 'Agartala', 'Aizawl', 'Kohima', 'Itanagar', 'Gangtok',
    # Chhattisgarh
    'Raipur', 'Bilaspur', 'Durg', 'Bhilai', 'Korba'
}

# Comprehensive routes covering all of India (source, destination, base_price)
all_india_routes = [
    # North India Routes
    ('Delhi', 'Agra', 550), ('Delhi', 'Jaipur', 750), ('Delhi', 'Chandigarh', 600),
    ('Delhi', 'Shimla', 900), ('Delhi', 'Manali', 1400), ('Delhi', 'Lucknow', 800),
    ('Delhi', 'Dehradun', 700), ('Delhi', 'Haridwar', 650), ('Delhi', 'Amritsar', 950),
    ('Delhi', 'Mathura', 400), ('Delhi', 'Gurgaon', 150), ('Delhi', 'Noida', 100),
    ('Agra', 'Jaipur', 600), ('Agra', 'Mathura', 150), ('Agra', 'Lucknow', 650),
    ('Jaipur', 'Jodhpur', 500), ('Jaipur', 'Udaipur', 550), ('Jaipur', 'Ajmer', 300),
    ('Jaipur', 'Bikaner', 600), ('Jaipur', 'Alwar', 350), ('Jaipur', 'Kota', 450),
    ('Chandigarh', 'Shimla', 400), ('Chandigarh', 'Manali', 700), ('Chandigarh', 'Amritsar', 500),
    ('Chandigarh', 'Ludhiana', 300), ('Chandigarh', 'Dehradun', 550),
    ('Lucknow', 'Kanpur', 200), ('Lucknow', 'Varanasi', 600), ('Lucknow', 'Allahabad', 450),
    ('Lucknow', 'Bareilly', 450), ('Lucknow', 'Agra', 650),
    
    # Maharashtra Routes
    ('Mumbai', 'Pune', 450), ('Mumbai', 'Nashik', 350), ('Mumbai', 'Goa', 1200),
    ('Mumbai', 'Aurangabad', 750), ('Mumbai', 'Nagpur', 1300), ('Mumbai', 'Kolhapur', 850),
    ('Mumbai', 'Ahmedabad', 900), ('Mumbai', 'Surat', 650), ('Mumbai', 'Thane', 100),
    ('Pune', 'Mumbai', 450), ('Pune', 'Nashik', 300), ('Pune', 'Goa', 900),
    ('Pune', 'Aurangabad', 550), ('Pune', 'Kolhapur', 600), ('Pune', 'Nagpur', 1000),
    ('Nagpur', 'Pune', 1000), ('Nagpur', 'Hyderabad', 950), ('Nagpur', 'Indore', 600),
    ('Nashik', 'Mumbai', 350), ('Nashik', 'Pune', 300), ('Nashik', 'Aurangabad', 400),
    
    # Gujarat Routes
    ('Ahmedabad', 'Surat', 350), ('Ahmedabad', 'Vadodara', 250), ('Ahmedabad', 'Rajkot', 400),
    ('Ahmedabad', 'Gandhinagar', 100), ('Ahmedabad', 'Mumbai', 900), ('Ahmedabad', 'Udaipur', 550),
    ('Surat', 'Mumbai', 500), ('Surat', 'Vadodara', 300), ('Surat', 'Ahmedabad', 350),
    ('Rajkot', 'Ahmedabad', 400), ('Rajkot', 'Jamnagar', 200), ('Rajkot', 'Bhavnagar', 250),
    
    # South India - Karnataka Routes
    ('Bangalore', 'Mysore', 400), ('Bangalore', 'Chennai', 950), ('Bangalore', 'Coimbatore', 850),
    ('Bangalore', 'Mangalore', 800), ('Bangalore', 'Hubli', 900), ('Bangalore', 'Goa', 1100),
    ('Bangalore', 'Hyderabad', 1000), ('Bangalore', 'Ooty', 750), ('Bangalore', 'Kochi', 1200),
    ('Mysore', 'Bangalore', 400), ('Mysore', 'Ooty', 450), ('Mysore', 'Coimbatore', 550),
    ('Mangalore', 'Bangalore', 800), ('Mangalore', 'Goa', 650), ('Mangalore', 'Kochi', 750),
    
    # Tamil Nadu Routes
    ('Chennai', 'Bangalore', 950), ('Chennai', 'Coimbatore', 850), ('Chennai', 'Madurai', 700),
    ('Chennai', 'Tiruchirappalli', 600), ('Chennai', 'Pondicherry', 350), ('Chennai', 'Salem', 650),
    ('Chennai', 'Vellore', 300), ('Chennai', 'Tirupati', 350), ('Chennai', 'Kanyakumari', 1100),
    ('Coimbatore', 'Chennai', 850), ('Coimbatore', 'Bangalore', 850), ('Coimbatore', 'Ooty', 250),
    ('Coimbatore', 'Madurai', 400), ('Coimbatore', 'Kochi', 350), ('Coimbatore', 'Salem', 300),
    ('Madurai', 'Chennai', 700), ('Madurai', 'Coimbatore', 400), ('Madurai', 'Kanyakumari', 450),
    
    # Kerala Routes
    ('Kochi', 'Thiruvananthapuram', 450), ('Kochi', 'Kozhikode', 350), ('Kochi', 'Bangalore', 1200),
    ('Kochi', 'Coimbatore', 350), ('Kochi', 'Thrissur', 200), ('Kochi', 'Kollam', 300),
    ('Thiruvananthapuram', 'Kochi', 450), ('Thiruvananthapuram', 'Kanyakumari', 250),
    ('Kozhikode', 'Kochi', 350), ('Kozhikode', 'Bangalore', 950), ('Kozhikode', 'Mangalore', 400),
    
    # Andhra Pradesh & Telangana Routes
    ('Hyderabad', 'Vijayawada', 500), ('Hyderabad', 'Visakhapatnam', 850), ('Hyderabad', 'Bangalore', 1000),
    ('Hyderabad', 'Chennai', 1100), ('Hyderabad', 'Tirupati', 700), ('Hyderabad', 'Guntur', 550),
    ('Hyderabad', 'Warangal', 350), ('Hyderabad', 'Nagpur', 950),
    ('Vijayawada', 'Hyderabad', 500), ('Vijayawada', 'Chennai', 750), ('Vijayawada', 'Visakhapatnam', 600),
    ('Visakhapatnam', 'Hyderabad', 850), ('Visakhapatnam', 'Vijayawada', 600),
    
    # East India Routes
    ('Kolkata', 'Siliguri', 900), ('Kolkata', 'Darjeeling', 1000), ('Kolkata', 'Patna', 650),
    ('Kolkata', 'Bhubaneswar', 850), ('Kolkata', 'Guwahati', 1600), ('Kolkata', 'Ranchi', 700),
    ('Kolkata', 'Puri', 900), ('Kolkata', 'Durgapur', 350),
    ('Patna', 'Kolkata', 650), ('Patna', 'Varanasi', 450), ('Patna', 'Ranchi', 500),
    ('Bhubaneswar', 'Kolkata', 850), ('Bhubaneswar', 'Puri', 150), ('Bhubaneswar', 'Visakhapatnam', 600),
    ('Ranchi', 'Kolkata', 700), ('Ranchi', 'Patna', 500), ('Ranchi', 'Jamshedpur', 300),
    
    # Northeast Routes
    ('Guwahati', 'Kolkata', 1600), ('Guwahati', 'Shillong', 250), ('Guwahati', 'Siliguri', 700),
    ('Guwahati', 'Imphal', 850), ('Guwahati', 'Agartala', 900),
    
    # Central India Routes
    ('Bhopal', 'Indore', 300), ('Bhopal', 'Jabalpur', 550), ('Bhopal', 'Gwalior', 600),
    ('Bhopal', 'Ujujain', 350), ('Bhopal', 'Nagpur', 700),
    ('Indore', 'Bhopal', 300), ('Indore', 'Ujujain', 150), ('Indore', 'Ahmedabad', 550),
    ('Indore', 'Mumbai', 950), ('Indore', 'Nagpur', 600),
    ('Raipur', 'Nagpur', 550), ('Raipur', 'Bhopal', 650), ('Raipur', 'Bilaspur', 250),
]

# Bus types and their characteristics
bus_types = [
    {'prefix': 'Express', 'capacity': 40, 'price_multiplier': 1.0},
    {'prefix': 'Volvo', 'capacity': 50, 'price_multiplier': 1.4},
    {'prefix': 'Sleeper', 'capacity': 35, 'price_multiplier': 1.3},
    {'prefix': 'Deluxe', 'capacity': 45, 'price_multiplier': 1.2},
    {'prefix': 'AC', 'capacity': 38, 'price_multiplier': 1.25},
    {'prefix': 'Super', 'capacity': 42, 'price_multiplier': 1.15},
    {'prefix': 'Luxury', 'capacity': 32, 'price_multiplier': 1.5},
    {'prefix': 'Semi-Sleeper', 'capacity': 40, 'price_multiplier': 1.1},
]

# Time slots throughout the day
time_slots = [
    time(5, 0), time(6, 0), time(6, 30), time(7, 0), time(7, 30),
    time(8, 0), time(8, 30), time(9, 0), time(9, 30), time(10, 0),
    time(10, 30), time(11, 0), time(11, 30), time(12, 0), time(13, 0),
    time(14, 0), time(15, 0), time(16, 0), time(17, 0), time(18, 0),
    time(19, 0), time(19, 30), time(20, 0), time(20, 30), time(21, 0),
    time(22, 0), time(23, 0), time(23, 30)
]

buses_data = []
bus_number = 100

buses_data = []
bus_number = 100

# Calculate dates for February and March 2026
start_date = date.today()  # February 2, 2026
feb_days_remaining = 28 - start_date.day  # Days left in February
march_days = 31  # All of March

total_days = feb_days_remaining + march_days + 1  # Include today

print(f"Generating bus data for {total_days} days (Feb {start_date.day} - March 31, 2026)")

# Generate buses for all routes across February and March
for day_offset in range(total_days):
    current_date = start_date + timedelta(days=day_offset)
    
    # For each route, add multiple buses throughout the day
    for route in all_india_routes:
        source, dest, base_price = route
        
        # Add 2-4 buses per day for each route
        num_buses_per_route = random.randint(2, 4)
        selected_times = random.sample(time_slots, min(num_buses_per_route, len(time_slots)))
        
        for departure_time in selected_times:
            # Pick a random bus type
            bus_type = random.choice(bus_types)
            
            bus_number += 1
            bus_name = f"{bus_type['prefix']}-{bus_number}"
            capacity = bus_type['capacity']
            price = round(base_price * bus_type['price_multiplier'], 2)
            
            buses_data.append({
                'bus_name': bus_name,
                'capacity': capacity,
                'source': source,
                'dest': dest,
                'price': price,
                'date': current_date,
                'time': departure_time
            })

print(f"Generated {len(buses_data)} bus records")
print(f"Routes covered: {len(all_india_routes)}")
print(f"Average buses per route per day: {len(buses_data) / (len(all_india_routes) * total_days):.1f}")

# Create bus objects
created_count = 0
failed_count = 0

for bus_data in buses_data:
    try:
        bus = Bus.objects.create(**bus_data)
        created_count += 1
        
        # Show progress every 500 buses
        if created_count % 500 == 0:
            print(f"✓ Progress: {created_count} buses created...")
    except Exception as e:
        failed_count += 1
        if failed_count <= 5:  # Show first 5 errors only
            print(f"✗ Error: {bus_data['bus_name']} - {e}")

# Show sample of created buses
print(f"\n📊 Sample of created buses:")
sample_buses = Bus.objects.all()[:10]
for bus in sample_buses:
    print(f"  {bus.bus_name}: {bus.source} → {bus.dest} on {bus.date} at {bus.time} (₹{bus.price})")

print(f"\n✅ Successfully created {created_count} bus records!")
if failed_count > 0:
    print(f"⚠️  Failed to create {failed_count} records")
print(f"📈 Total buses in database: {Bus.objects.count()}")
print(f"📅 Date range: {Bus.objects.earliest('date').date} to {Bus.objects.latest('date').date}")
print(f"🚌 Total routes covered: {Bus.objects.values('source', 'dest').distinct().count()}")
