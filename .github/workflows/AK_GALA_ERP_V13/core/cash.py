from core.database import get_connection


def create_sale(items):
    conn = get_connection()
    cur = conn.cursor()

    total = sum(i["qty"] * i["price"] for i in items)

    # Just a mock insert for the example
    cur.execute("INSERT INTO sales (product_id, quantity, total_sum) VALUES (?, ?, ?)", (0, 1, total))
    sale_id = cur.lastrowid

    cur.execute("INSERT INTO events (event_type, message) VALUES (?, ?)", ("SALE", f"Sale #{sale_id} total: {total}"))

    conn.commit()
    conn.close()
    return sale_id, total