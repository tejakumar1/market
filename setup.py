from app import db, app  # Replace `your_app_file` with your main script name

with app.app_context():
    db.create_all()
    print("Database tables created!")
