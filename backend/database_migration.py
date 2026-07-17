import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def main():
    load_dotenv(dotenv_path="backend/.env")
    db_url = os.getenv("db_url")
    if not db_url:
        print("Error: db_url not found in backend/.env")
        sys.exit(1)

    print(f"Connecting to database: {db_url}")
    engine = create_engine(db_url)
    
    with engine.begin() as conn:
        # 1. Modify users role column to include 'admin'
        print("Modifying users.role enum...")
        conn.execute(text("ALTER TABLE users MODIFY COLUMN role ENUM('patient', 'doctor', 'admin') NOT NULL;"))
        print("Successfully updated users.role enum.")

        # 2. Add allergies to patient table if it doesn't exist
        print("Checking if allergies column exists in patient...")
        result = conn.execute(text("SHOW COLUMNS FROM patient LIKE 'allergies';")).fetchone()
        if not result:
            print("Adding allergies column to patient table...")
            conn.execute(text("ALTER TABLE patient ADD COLUMN allergies VARCHAR(255) NULL;"))
            print("Successfully added allergies column.")
        else:
            print("allergies column already exists.")

        # 3. Create default admin user if not exists
        print("Checking for default admin user...")
        admin_email = "admin@hospital.com"
        admin_user = conn.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": admin_email}
        ).fetchone()

        if not admin_user:
            print("Creating default admin user...")
            hashed_pw = hash_password("admin123")
            conn.execute(
                text("INSERT INTO users (email, hashed_password, role, is_active, created_at) VALUES (:email, :pw, 'admin', 1, NOW())"),
                {"email": admin_email, "pw": hashed_pw}
            )
            print("Successfully created default admin user (email: admin@hospital.com, password: admin123).")
        else:
            print("Default admin user already exists.")

if __name__ == "__main__":
    main()
