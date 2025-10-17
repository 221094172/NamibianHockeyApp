
from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # Add user_id column to player table
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE "player" ADD COLUMN user_id INTEGER REFERENCES "user"(id)'))
            conn.commit()
        print("Successfully added user_id column to player table!")
    except Exception as e:
        print(f"Error: {e}")
        print("Column might already exist or there's another issue.")
