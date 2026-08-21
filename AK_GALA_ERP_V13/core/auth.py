from core.database import get_connection

def login(username, password):
        if not username.strip():
            return "PLEASE enter your username"

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        if user is None:
            cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'admin')", (username, password))
            conn.commit()

            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cur.fetchone()
            print(f"✨TAZE ULANYJY GOŞULDY {username}")
        else:
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
            user = cur.fetchone()
        conn.close()
        return user