import uuid

def generate_contract(contract_id ,agreement_type, agreement_name, date, party1_name, party1_address, party2_name, party2_address,
                      amount=None, rate=None, duration=None, payment_mode=None, repayment_type=None, penalty=None,
                      days=None, city=None, jurisdiction=None, product_name=None, quantity=None, price_per_unit=None,
                      total_price=None, delivery_days=None, service_name=None, completion_deadline=None, commodity_name=None,
                      amount_sent=None, currency_sent=None, converted_amount=None, currency_received=None, exchange_rate=None,
                      interest_rate=None, late_interest_rate=None, repayment_due_date=None,party1_contact=None,party2_contact=None):
     # Generate a unique contract ID
    document = {
        "contract_id": contract_id,
        "contract_type": agreement_type,
        "contract_title": agreement_name,
        "parties": [
            {"name": party1_name, "role": "Lender" if "LOAN" in agreement_type else "Party A", "contact": party1_address},
            {"name": party2_name, "role": "Borrower" if "LOAN" in agreement_type else "Party B", "contact": party2_address}
        ],
        "jurisdiction": jurisdiction,
        "governing_law": "Indian Contract Act, 1872",
        "validity_period": {"start_date": date, "end_date": repayment_due_date or "N/A"},
        "transaction_details": {},
        "delivery_terms": {},
        "clauses": [],
        "summary": "",
        "tags": []
    }
    
    if agreement_type == "LOAN AGREEMENT" :
        document["transaction_details"] = {
            "amount": f"₹{amount}",
            "currency": "INR",
            "payment_mode": payment_mode,
            "payment_terms": f"Repayment via {repayment_type}",
            "interest_rate": f"{interest_rate if interest_rate else rate}% per annum",
            "due_date": repayment_due_date or "N/A"
        }
        
        document["clauses"].append({
            "clause_id": f"{contract_id}_001",
            "title": "Payment Terms",
            "text": f"The Borrower agrees to repay the Lender ₹{amount} with an interest rate of {rate}% per annum."
        })
        document["tags"] = ["Lending", "Loan Agreement"]

    elif agreement_type == "FRIENDLY LOAN AGREEMENT":
        document["transaction_details"] = {
            "amount": f"₹{amount}",
            "currency": "INR",
            "payment_mode": payment_mode,
            "payment_terms": f"Repayment via {repayment_type}",
            "late_interest_rate": f"{late_interest_rate if late_interest_rate else rate}% per annum",
            "due_date": repayment_due_date or "N/A"
        }
        document["clauses"].append({
            "clause_id": f"{contract_id}_002",
            "title": "Late Interest",
            "text": f"The Borrower agrees to pay an additional {late_interest_rate}% per annum for late repayment."
        })
        document["tags"] = ["Lending", "Loan Agreement"]
    
    elif agreement_type == "SALES AGREEMENT":
        document["transaction_details"] = {
            "product": product_name,
            "quantity": quantity,
            "price_per_unit": f"₹{price_per_unit}",
            "total_price": f"₹{total_price}",
            "payment_mode": payment_mode
        }
        
        document["delivery_terms"] = {
            "mode": "Standard Delivery",
            "conditions": f"Delivery within {delivery_days} days"
        }
        
        document["clauses"].append({
            "clause_id": f"{contract_id}_002",
            "title": "Delivery Terms",
            "text": f"The Seller agrees to deliver the product within {delivery_days} days."
        })
        document["tags"] = ["Sales", "Product Agreement"]
    
    elif agreement_type == "CURRENCY EXCHANGE AGREEMENT":
        document["transaction_details"] = {
            "amount_sent": f"{amount_sent} {currency_sent}",
            "amount_received": f"{converted_amount} {currency_received}",
            "exchange_rate": exchange_rate
        }
        document["tags"] = ["Currency Exchange", "Financial Agreement"]
    
    elif agreement_type == "SERVICE AGREEMENT":
        document["transaction_details"] = {
            "service": service_name,
            "completion_deadline": completion_deadline,
            "payment_mode": payment_mode,
            "amount": f"₹{amount}"
        }
        document["tags"] = ["Service", "Contract"]
    
    elif agreement_type == "BARTER AGREEMENT":
        document["transaction_details"] = {
            "commodity": commodity_name,
            "exchange_terms": f"{party1_name} agrees to exchange {commodity_name} with {party2_name}."
        }
        document["tags"] = ["Barter", "Exchange"]
    
    document["clauses"].append({
        "clause_id": f"{contract_id}_003",
        "title": "Dispute Resolution",
        "text": f"Any dispute shall be resolved through arbitration under the Arbitration and Conciliation Act, 1996, in {city}."
    })
    
    document["summary"] = f"An agreement between {party1_name} and {party2_name} for {agreement_type.lower()}."
    
    return document