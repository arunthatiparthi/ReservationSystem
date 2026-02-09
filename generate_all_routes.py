import os
import django
from datetime import datetime, date, time, timedelta
import random
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busreserve.settings')
django.setup()

from reservation.models import Bus

print("=" * 100)
print("🔄 GENERATING ALL POSSIBLE CITY COMBINATIONS (BIDIRECTIONAL)")
print("=" * 100)

# Clear existing data
Bus.objects.all().delete()
print("\n✓ Cleared existing bus data")

# MAJOR CITIES - Top 50 most searched
MAJOR_CITIES = [
    # Metro Cities
    'Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad',
    
    # Tier-1 Cities
    'Vijayawada', 'Visakhapatnam', 'Surat', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 
    'Indore', 'Bhopal', 'Coimbatore', 'Kochi', 'Trivandrum', 'Madurai', 'Nashik',
    
    # Popular Destinations
    'Goa', 'Mysore', 'Mangalore', 'Trichy', 'Salem', 'Tirupati', 'Guntur', 'Nellore',
    'Rajahmundry', 'Kakinada', 'Chandigarh', 'Amritsar', 'Ludhiana', 'Shimla', 'Manali',
    'Haridwar', 'Rishikesh', 'Agra', 'Varanasi', 'Patna', 'Ranchi', 'Bhubaneswar',
    'Guwahati', 'Udaipur', 'Jodhpur', 'Aurangabad', 'Solapur', 'Hubli', 'Belgaum'
]

# BUS TYPES
BUS_TYPES = [
    {'name': 'AC Sleeper', 'capacity': 35, 'price_mult': 1.8},
    {'name': 'Non-AC Sleeper', 'capacity': 40, 'price_mult': 1.2},
    {'name': 'Volvo AC', 'capacity': 40, 'price_mult': 2.2},
    {'name': 'AC Seater', 'capacity': 45, 'price_mult': 1.4},
    {'name': 'Non-AC Seater', 'capacity': 50, 'price_mult': 1.0},
]

# OPERATORS
OPERATORS = [
    'KSRTC', 'TNSTC', 'SETC', 'APSRTC', 'TSRTC', 'MSRTC', 'RSRTC', 'GSRTC',
    'RedBus Express', 'VRL Travels', 'SRS Travels', 'Orange Travels', 
    'Kallada Travels', 'KPN Travels', 'IntrCity SmartBus', 'National Travels'
]

# TIME SLOTS - Multiple departures per day
TIME_SLOTS = [
    time(5, 0), time(6, 0), time(7, 0), time(8, 0), time(9, 0), time(10, 0),
    time(11, 0), time(12, 0), time(14, 0), time(16, 0), time(18, 0), time(19, 0),
    time(20, 0), time(21, 0), time(22, 0), time(23, 0)
]

def calculate_price(source, dest, bus_type):
    """Calculate realistic price"""
    # Base prices for major routes
    base_prices = {
        ('Vijayawada', 'Chennai'): 800,
        ('Chennai', 'Vijayawada'): 800,
        ('Vijayawada', 'Delhi'): 1800,
        ('Delhi', 'Vijayawada'): 1800,
        ('Delhi', 'Chennai'): 2000,
        ('Chennai', 'Delhi'): 2000,
        ('Vijayawada', 'Hyderabad'): 500,
        ('Hyderabad', 'Vijayawada'): 500,
        ('Vijayawada', 'Bangalore'): 900,
        ('Bangalore', 'Vijayawada'): 900,
    }
    
    # Get base price or estimate
    base = base_prices.get((source, dest), 600)
    price = base * bus_type['price_mult']
    
    # Round to nearest 50
    return round(price / 50) * 50

def generate_all_routes():
    """Generate buses for ALL possible city pairs in BOTH directions"""
    
    all_buses = []
    bus_counter = 20000
    
    # Date range - Feb and March 2026
    start_date = date.today()
    total_days = 59  # Feb + March
    
    # Generate ALL possible combinations (A->B and B->A)
    city_pairs = []
    for i, city1 in enumerate(MAJOR_CITIES):
        for city2 in MAJOR_CITIES[i+1:]:
            # Add both directions
            city_pairs.append((city1, city2))
            city_pairs.append((city2, city1))
    
    print(f"\n📊 Generating routes:")
    print(f"   Cities: {len(MAJOR_CITIES)}")
    print(f"   Route combinations: {len(city_pairs)}")
    print(f"   Days: {total_days}")
    print(f"   Time slots: {len(TIME_SLOTS)}")
    
    # Generate for each day
    for day_offset in range(total_days):
        current_date = start_date + timedelta(days=day_offset)
        
        # For each city pair
        for source, dest in city_pairs:
            # Skip same city
            if source == dest:
                continue
            
            # Generate 3-6 buses per route per day
            num_buses = random.randint(3, 6)
            selected_times = random.sample(TIME_SLOTS, min(num_buses, len(TIME_SLOTS)))
            
            for dept_time in selected_times:
                bus_type = random.choice(BUS_TYPES)
                operator = random.choice(OPERATORS)
                
                bus_counter += 1
                capacity = bus_type['capacity']
                seats_available = random.randint(10, capacity)
                price = calculate_price(source, dest, bus_type)
                
                all_buses.append({
                    'bus_name': f"{bus_type['name'][:3].upper()}-{bus_counter}",
                    'capacity': capacity,
                    'source': source,
                    'dest': dest,
                    'rem': seats_available,
                    'price': Decimal(str(price)),
                    'date': current_date,
                    'time': dept_time
                })
        
        # Progress update
        if (day_offset + 1) % 10 == 0:
            print(f"   ✓ Day {day_offset + 1}/{total_days} - {len(all_buses)} buses generated")
    
    print(f"\n✅ Total buses generated: {len(all_buses):,}")
    return all_buses

def save_to_database(buses):
    """Save all buses to database using bulk create"""
    print("\n💾 Saving to database (using bulk insert)...")
    
    batch_size = 1000
    total_created = 0
    
    for i in range(0, len(buses), batch_size):
        batch = buses[i:i + batch_size]
        try:
            # Convert to Bus model objects
            bus_objects = [Bus(**bus_data) for bus_data in batch]
            # Bulk create
            Bus.objects.bulk_create(bus_objects, ignore_conflicts=True)
            total_created += len(batch)
            
            if total_created % 10000 == 0:
                print(f"   ✓ {total_created:,} buses saved...")
        except Exception as e:
            # If bulk fails, try individual inserts
            for bus_data in batch:
                try:
                    Bus.objects.create(**bus_data)
                    total_created += 1
                except:
                    pass
    
    print(f"✅ {total_created:,} buses saved successfully")
    return total_created

def verify_routes():
    """Verify key routes exist"""
    print("\n🔍 Verifying key routes...")
    
    test_routes = [
        ('Vijayawada', 'Chennai'),
        ('Chennai', 'Vijayawada'),
        ('Vijayawada', 'Delhi'),
        ('Delhi', 'Vijayawada'),
        ('Delhi', 'Chennai'),
        ('Chennai', 'Delhi'),
        ('Vijayawada', 'Hyderabad'),
        ('Hyderabad', 'Vijayawada'),
        ('Vijayawada', 'Bangalore'),
        ('Bangalore', 'Vijayawada'),
    ]
    
    for source, dest in test_routes:
        count = Bus.objects.filter(source=source, dest=dest).count()
        print(f"   {source} → {dest}: {count} buses")
    
    print("\n✓ Verification complete")

# MAIN EXECUTION
if __name__ == '__main__':
    print("\n🚀 Starting comprehensive route generation...\n")
    
    # Generate all routes
    buses = generate_all_routes()
    
    # Save to database
    saved = save_to_database(buses)
    
    # Verify
    verify_routes()
    
    # Summary
    print("\n" + "=" * 100)
    print("✅ COMPLETE - ALL ROUTES GENERATED")
    print("=" * 100)
    print(f"\n📈 STATISTICS:")
    print(f"   Total Buses: {saved:,}")
    print(f"   Cities Covered: {len(MAJOR_CITIES)}")
    print(f"   Unique Routes: {Bus.objects.values('source', 'dest').distinct().count()}")
    print(f"   Date Range: {Bus.objects.earliest('date').date} to {Bus.objects.latest('date').date}")
    print(f"\n🎯 Now you can search:")
    print(f"   ✓ Vijayawada → Chennai")
    print(f"   ✓ Chennai → Vijayawada")
    print(f"   ✓ Vijayawada → Delhi")
    print(f"   ✓ Delhi → Chennai")
    print(f"   ✓ And ALL other combinations!")
    print("\n" + "=" * 100)
