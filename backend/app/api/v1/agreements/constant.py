DB_QUERIES = {
    "create_contract": """
    INSERT INTO contracts (contract_id, contract_data, contract_status, transaction_id, contract_title, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)

    """,
    "get_user_by_user_id": """
    SELECT * FROM users WHERE user_id = %s
    """,
    "get_user_by_email": """
    SELECT * FROM users WHERE email = %s
    """
}
