
from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # Add is_player column to user table
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE "user" ADD COLUMN is_player BOOLEAN DEFAULT FALSE'))
            conn.commit()
        print("Successfully added is_player column to user table!")
    except Exception as e:
        print(f"Error: {e}")
        print("Column might already exist or there's another issue.")
