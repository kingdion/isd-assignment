import datetime
import random
from app import create_app
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
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

            # Test Users
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
                db.session.commit()

                for log in range(1, 21):
                    randomDate = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 9))
                    randomLogoutTime = randomDate + datetime.timedelta(minutes=10)
                    loginLog = UserAccessLog(acc.id, randomDate, "Login")
                    logoutLog = UserAccessLog(acc.id, randomLogoutTime, "Logout")
                    db.session.add(loginLog)
                    db.session.add(logoutLog)


            # Test Staff
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
                db.session.commit()

                for log in range(1, 21):
                    randomDate = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 9))
                    randomLogoutTime = randomDate + datetime.timedelta(minutes=10)
                    loginLog = UserAccessLog(acc.id, randomDate, "Login")
                    logoutLog = UserAccessLog(acc.id, randomLogoutTime, "Logout")
                    db.session.add(loginLog)
                    db.session.add(logoutLog)


            print("20 accounts created")
            print("20 staff created")

            maturity_ratings = [
                MaturityRating("G"),
                MaturityRating("PG"),
                MaturityRating("M"),
                MaturityRating("MA"),
                MaturityRating("R")
            ]

            genres = [
                Genre("Fantasy"),
                Genre("Comedy"),
                Genre("Horror"),
                Genre("Romance"),
                Genre("Thriller"),
                Genre("Anime"),
                Genre("Family"),
                Genre("Classic"),
                Genre("Drama"),
            ]

            print(f"{len(maturity_ratings)} genres created")
            print(f"{len(genres)} maturity ratings created")

            for rating in maturity_ratings:
                db.session.add(rating)

            for genre in genres:
                db.session.add(genre)

            db.session.commit()

            for movie_id in range(1, 50):
                randomDate = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 9)) - datetime.timedelta(days=random.randint(1, 9)*365)
                movie = Movie(
                    f"Movie {movie_id}",
                    randomDate,
                    "static/images/thumbnails/sharknado.png",
                    random.randint(1,59),
                    random.choice(maturity_ratings).id
                )

                movie.release_year = randomDate.year

                movie.genres.append(genres[0])

            db.session.commit()

            accounts = db.session.query(Account).all()
            for order_id in range(1, 100):
                order = Orders(
                    random.choice(accounts).id,  # random account id
                    "tracking status whatever this is",
                    uuid.uuid4()
                )
                print(f"Created order {order}")
                db.session.add(order)

            db.session.commit()

            orders = db.session.query(Orders).all()

            for i, order in enumerate(orders):
                random_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 9)) - datetime.timedelta(days=random.randint(1, 9)*365)
                shipment_details = ShipmentDetails(
                    date=random_date,
                    shipment_method=random.choice(("Standard", "Express")),
                    address=f"Random address {i}",
                    order_id=order.id
                )
                print(f"Created shipment details {shipment_details}")
                db.session.add(shipment_details)

            db.session.commit()
