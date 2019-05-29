import datetime
from app import create_app
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash

print("----")
print("This will drop all existing rows and replace them with test rows.") 
print("----")
print("Are you sure you want to do this? (Y / N)")
answer = input("> ")

if (answer == "Y"):
    print("Started creation process..")
    app = create_app()
    with app.app_context():
            db.drop_all()
            db.create_all()

            for current_id in range(1, 21):
                acc = Account(
                    f"Test-{current_id}", 
                    f"User-{current_id}", 
                    f"testuser{current_id}@gmail.com",
                    f"TestUser{current_id}",
                    generate_password_hash(f"TestUser{current_id}", method='sha256'),
                    "Fake Address at Fake Street",
                    "2020",
                    "0400000000",
                    False,
                    True,
                    datetime.datetime.utcnow()
                )

                print("Created: ", acc)
                db.session.add(acc)

            for current_id in range(1, 21):
                staff = Account(
                    f"StaffTest-{current_id}", 
                    f"User-{current_id}", 
                    f"stafftestuser{current_id}@gmail.com",
                    f"StaffTestUser{current_id}",
                    generate_password_hash(f"StaffTestUser{current_id}", method='sha256'),
                    "Fake Address at Fake Street",
                    "2020",
                    "0400000000",
                    True,
                    True,
                    datetime.datetime.utcnow()
                )

                print("Created: ", staff)
                db.session.add(staff)

            print("20 accounts created")
            print("20 staff created")
            db.session.commit()