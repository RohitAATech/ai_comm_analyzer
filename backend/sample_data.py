from rag_store import RAGStore
 
# Sample BFSI customer communications — similar to what your CCM platform processes
SAMPLE_CASES = [
    ("case_001", "My credit card was charged twice for the same transaction on 15th January. Amount Rs 4500. Please refund immediately.", {"type": "complaint", "resolved": "true"}),
    ("case_002", "I have not received my account statement for the last 3 months. Please send it to my registered email.", {"type": "query", "resolved": "true"}),
    ("case_003", "Suspicious transaction of Rs 89000 on my account that I did not authorize. This looks like fraud!", {"type": "fraud_alert", "resolved": "true"}),
    ("case_004", "I want to update my mobile number registered with the bank. Current number 9876543210.", {"type": "service_request", "resolved": "true"}),
    ("case_005", "Your app is pathetic. I have complained 5 times and no one responds. I am moving to another bank.", {"type": "escalation", "resolved": "true"}),
    ("case_006", "What is the current interest rate on fixed deposits for senior citizens?", {"type": "query", "resolved": "true"}),
    ("case_007", "My home loan EMI was deducted twice this month. This has happened before also. Very poor service.", {"type": "complaint", "resolved": "true"}),
    ("case_008", "Please block my debit card ending 4521. I lost my wallet.", {"type": "fraud_alert", "resolved": "true"}),
    ("case_009", "I received a call from someone claiming to be from your bank asking for OTP. I think it is phishing.", {"type": "fraud_alert", "resolved": "true"}),
    ("case_010", "Thank you for resolving my complaint so quickly. Very happy with the service.", {"type": "feedback", "resolved": "true"}),
]
 
def seed_database():
    store = RAGStore()
    count = store.collection.count()
    if count > 0:
        print(f"Database already has {count} cases. Skipping seed.")
        return
    print("Seeding ChromaDB with BFSI sample cases...")
    for case_id, text, metadata in SAMPLE_CASES:
        store.add_case(case_id, text, metadata)
    print(f"Seeded {len(SAMPLE_CASES)} cases successfully.")
 
if __name__ == "__main__":
    seed_database()
