import psycopg2
from config import DB_CONFIG


def connect():
#connect db
    return psycopg2.connect(**DB_CONFIG)


def get_or_create_player(username):
#get or create player
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    row = cur.fetchone()

    if row:
        player_id = row[0]
    else:
        cur.execute(
            "INSERT INTO players(username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return player_id


def save_game(username, score, level):
#save game
    player_id = get_or_create_player(username)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO game_sessions(player_id, score, level_reached) VALUES (%s,%s,%s)",
        (player_id, score, level)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_personal_best(username):
#get best score
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(score)
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        WHERE p.username=%s
    """, (username,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result if result else 0


def get_leaderboard():
#top 10
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        ORDER BY gs.score DESC
        LIMIT 10
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows