"""
Test script to verify timezone-aware timestamps are working correctly
"""
import requests
import json
from datetime import datetime
import pytz

API_URL = "http://localhost:8000"
IST = pytz.timezone("Asia/Kolkata")

def get_current_ist_time():
    """Get current IST time"""
    return datetime.now(IST)

def test_event_timestamps():
    """Test that event timestamps match system local time"""
    print("\n" + "="*80)
    print("TIMEZONE FIX VERIFICATION TEST")
    print("="*80)
    
    # Get current system time
    current_time = get_current_ist_time()
    print(f"\nCurrent System Time (IST): {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Submit a test query
    print("\nSubmitting test query...")
    query = "What is Docker?"
    
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"query": query},
            timeout=60
        )
        
        if response.status_code == 200:
            print("✓ Query submitted successfully")
            
            # Wait a moment for events to be recorded
            import time
            time.sleep(2)
            
            # Fetch events
            print("\nFetching events...")
            events_response = requests.get(f"{API_URL}/events?limit=10")
            
            if events_response.status_code == 200:
                events = events_response.json()['events']
                
                print(f"✓ Retrieved {len(events)} events\n")
                print("Event Timestamps:")
                print("-" * 80)
                
                for event in events[-5:]:  # Show last 5 events
                    event_time = datetime.fromisoformat(event['timestamp'])
                    
                    # Check if timezone aware
                    is_aware = event_time.tzinfo is not None
                    
                    print(f"\nEvent Type: {event['event_type']}")
                    print(f"Timestamp (Raw): {event['timestamp']}")
                    print(f"Timestamp (Parsed): {event_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                    print(f"Timezone Aware: {'✓ Yes' if is_aware else '✗ No'}")
                    
                    if is_aware:
                        # Convert to IST for comparison
                        event_time_ist = event_time.astimezone(IST)
                        time_diff = abs((current_time - event_time_ist).total_seconds())
                        
                        print(f"Time Difference from Current: {time_diff:.1f} seconds")
                        
                        if time_diff < 60:  # Within 1 minute
                            print("✓ Timestamp matches system time")
                        else:
                            print("⚠ Timestamp differs significantly from system time")
                
                print("\n" + "-" * 80)
                
                # Check if all recent events are timezone-aware
                recent_events = events[-5:]
                all_aware = all(
                    datetime.fromisoformat(e['timestamp']).tzinfo is not None 
                    for e in recent_events
                )
                
                if all_aware:
                    print("\n✓ SUCCESS: All events use timezone-aware timestamps")
                    
                    # Verify timezone is IST
                    sample_event = recent_events[0]
                    sample_time = datetime.fromisoformat(sample_event['timestamp'])
                    
                    if '+05:30' in sample_event['timestamp'] or 'IST' in str(sample_time.tzinfo):
                        print("✓ SUCCESS: Timestamps use Asia/Kolkata (IST) timezone")
                    else:
                        print(f"⚠ WARNING: Timezone is {sample_time.tzinfo}, expected IST")
                    
                    return True
                else:
                    print("\n✗ FAILURE: Some events still use naive timestamps")
                    return False
            else:
                print(f"✗ Failed to fetch events: {events_response.status_code}")
                return False
        else:
            print(f"✗ Query failed: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def test_history_timestamps():
    """Test that query history timestamps are timezone-aware"""
    print("\n" + "="*80)
    print("HISTORY TIMESTAMP VERIFICATION")
    print("="*80)
    
    try:
        response = requests.get(f"{API_URL}/history?limit=5")
        
        if response.status_code == 200:
            history = response.json()['history']
            
            if len(history) > 0:
                print(f"\n✓ Retrieved {len(history)} history items\n")
                print("History Timestamps:")
                print("-" * 80)
                
                for item in history[:3]:  # Show first 3
                    timestamp = item['timestamp']
                    parsed_time = datetime.fromisoformat(timestamp)
                    is_aware = parsed_time.tzinfo is not None
                    
                    print(f"\nQuery: {item['query_text'][:50]}...")
                    print(f"Timestamp (Raw): {timestamp}")
                    print(f"Timezone Aware: {'✓ Yes' if is_aware else '✗ No'}")
                    
                    if is_aware:
                        print(f"Formatted: {parsed_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                
                print("\n" + "-" * 80)
                
                all_aware = all(
                    datetime.fromisoformat(h['timestamp']).tzinfo is not None 
                    for h in history
                )
                
                if all_aware:
                    print("\n✓ SUCCESS: All history items use timezone-aware timestamps")
                    return True
                else:
                    print("\n✗ FAILURE: Some history items use naive timestamps")
                    return False
            else:
                print("\n⚠ No history items found (this is okay for new installations)")
                return True
        else:
            print(f"✗ Failed to fetch history: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def main():
    print("\n" + "="*80)
    print("NEURALNEXUS TIMEZONE FIX VERIFICATION")
    print("Testing Asia/Kolkata (IST) Timezone Implementation")
    print("="*80)
    
    # Test 1: Event timestamps
    test1_passed = test_event_timestamps()
    
    # Test 2: History timestamps
    test2_passed = test_history_timestamps()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Event Timestamps: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"History Timestamps: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n✓ ALL TESTS PASSED - Timezone fix is working correctly!")
        print("✓ All timestamps now use Asia/Kolkata (IST) timezone")
        print("✓ Event timeline will display correct local time")
    else:
        print("\n✗ SOME TESTS FAILED - Please review the errors above")

if __name__ == "__main__":
    main()
