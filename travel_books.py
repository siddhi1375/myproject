import mysql.connector
import random
from faker import Faker

def create_travel_book_simple():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',  # Replace with your MySQL password
            database='my_packing_buddy'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("DROP TABLE IF EXISTS travel_book")

            cursor.execute("""
                CREATE TABLE travel_book (
                    id VARCHAR(10) PRIMARY KEY,
                    destination_id VARCHAR(10),
                    book_title VARCHAR(150),
                    genre VARCHAR(50),
                    FOREIGN KEY (destination_id) REFERENCES destination(destination_id)
                )
            """)

            cursor.execute("SELECT destination_id FROM destination")
            destination_ids = [row[0] for row in cursor.fetchall()]

            fake = Faker()
            genres = ['Travel', 'Adventure', 'History', 'Biography', 'Guide', 'Fiction']

            for i in range(1, 101):
                book_id = f"B{i:03}"
                destination_id = random.choice(destination_ids)
                book_title = fake.sentence(nb_words=4).rstrip('.')
                genre = random.choice(genres)
                cursor.execute("INSERT INTO travel_book (id, destination_id, book_title, genre) VALUES (%s, %s, %s, %s)",
                               (book_id, destination_id, book_title, genre))

            connection.commit()
            print("travel_book table created and 100 random entries inserted.")

    except Exception as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

create_travel_book_simple()
