"""
Test script to verify the response pipeline is working correctly
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_simple_query():
    """Test simple informational query"""
    print("\n" + "="*80)
    print("TEST 1: Simple Informational Query")
    print("="*80)
    
    query = "Explain Kubernetes architecture in 5 bullet points"
    print(f"Query: {query}\n")
    
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"query": query},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Agent: {result.get('agent')}")
            print(f"✓ Planning Used: {result.get('planning_used')}")
            print(f"✓ Has Response Field: {'response' in result}")
            
            if 'response' in result and result['response']:
                print(f"✓ Response Length: {len(result['response'])} characters")
                print(f"✓ Response Word Count: {len(result['response'].split())} words")
                print(f"\n--- RESPONSE ---")
                print(result['response'])
                print("--- END RESPONSE ---\n")
                return True
            else:
                print("✗ ERROR: No response field or empty response!")
                print(f"Full result: {json.dumps(result, indent=2)}")
                return False
        else:
            print(f"✗ ERROR: Status {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def test_complex_query():
    """Test complex query that triggers planner"""
    print("\n" + "="*80)
    print("TEST 2: Complex Query with Multi-Agent Planning")
    print("="*80)
    
    query = "Design a comprehensive strategy to build a scalable microservices architecture for an e-commerce platform"
    print(f"Query: {query}\n")
    
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"query": query},
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Agent: {result.get('agent')}")
            print(f"✓ Planning Used: {result.get('planning_used')}")
            print(f"✓ Has Response Field: {'response' in result}")
            print(f"✓ Has Results Field: {'results' in result}")
            
            if result.get('results'):
                print(f"✓ Number of Tasks: {len(result['results'])}")
            
            if 'response' in result and result['response']:
                print(f"✓ Synthesized Response Length: {len(result['response'])} characters")
                print(f"✓ Synthesized Response Word Count: {len(result['response'].split())} words")
                print(f"\n--- SYNTHESIZED RESPONSE ---")
                print(result['response'])
                print("--- END SYNTHESIZED RESPONSE ---\n")
                return True
            else:
                print("✗ ERROR: No response field or empty response!")
                print(f"Full result keys: {result.keys()}")
                return False
        else:
            print(f"✗ ERROR: Status {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def check_events():
    """Check if refinement events are being published"""
    print("\n" + "="*80)
    print("TEST 3: Event Timeline Verification")
    print("="*80)
    
    try:
        response = requests.get(f"{API_URL}/events?limit=30")
        if response.status_code == 200:
            events = response.json()['events']
            
            event_types = [e['event_type'] for e in events]
            
            print(f"✓ Total Events: {len(events)}")
            print(f"\nEvent Types Found:")
            for event_type in set(event_types):
                count = event_types.count(event_type)
                print(f"  - {event_type}: {count}")
            
            # Check for refinement events
            refinement_events = [
                'AGENT_DRAFT_GENERATED',
                'CRITIC_VALIDATION',
                'FORMATTER_ENFORCED_LIMITS',
                'RESPONSE_SYNTHESIZED'
            ]
            
            print(f"\nRefinement Pipeline Events:")
            for event_type in refinement_events:
                if event_type in event_types:
                    print(f"  ✓ {event_type}")
                else:
                    print(f"  ✗ {event_type} (not found)")
            
            return True
        else:
            print(f"✗ ERROR: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def main():
    print("\n" + "="*80)
    print("NEURALNEXUS RESPONSE PIPELINE TEST")
    print("="*80)
    
    # Test 1: Simple query
    test1_passed = test_simple_query()
    
    # Test 2: Complex query
    test2_passed = test_complex_query()
    
    # Test 3: Events
    test3_passed = check_events()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Simple Query Test: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"Complex Query Test: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    print(f"Event Timeline Test: {'✓ PASSED' if test3_passed else '✗ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n✓ ALL TESTS PASSED - Response pipeline is working correctly!")
    else:
        print("\n✗ SOME TESTS FAILED - Please review the errors above")

if __name__ == "__main__":
    main()
