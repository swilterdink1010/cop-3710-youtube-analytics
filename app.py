import oracledb
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")
LIB_DIR = os.getenv("LIB_DIR")

oracledb.init_oracle_client(LIB_DIR)

def connect_db():
    try:
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASS,
            dsn=DB_DSN
        )
        print("Connected to Oracle Database")
        return connection
    except Exception as e:
        print("Error connecting to database:", e)
        return None

def filter_by_date(conn):
    start_date = input("Enter start date (MM/DD/YYYY): ")
    end_date = input("Enter end date (MM/DD/YYYY): ")

    cursor = conn.cursor()
    query = """
            SELECT vid_id, vid_title, vid_upload_date, vid_views
            FROM video
            WHERE TRUNC(vid_upload_date) BETWEEN TO_DATE(:1, 'MM/DD/YYYY')
                                            AND TO_DATE(:2, 'MM/DD/YYYY')
            ORDER BY vid_upload_date
        """
    cursor.execute(query, (start_date, end_date))

    print("\nVideos in Date Range:")
    for row in cursor:
        vid_id, title, upload_date, views = row
        print(f"{vid_id} | {title} | {upload_date.strftime('%m/%d/%Y')} | {views} views")


def filter_by_category(conn):
    category = input("Enter category name: ")

    cursor = conn.cursor()
    query = """
        SELECT v.vid_id, v.vid_title, c.category_name
        FROM video v
        JOIN video_category vc ON v.vid_id = vc.vid_id
        JOIN category c ON vc.category_id = c.category_id
        WHERE c.category_name = :1
    """
    cursor.execute(query, (category,))

    print("\nVideos in Category:")
    for row in cursor:
        vid_id, title, category = row
        print(f"{vid_id} | {title} | {category}")


def filter_by_channel(conn):
    channel = input("Enter channel name: ")

    cursor = conn.cursor()
    query = """
        SELECT v.vid_id, v.vid_title, ch.channel_name, v.vid_views
        FROM video v
        JOIN channel ch ON v.channel_id = ch.channel_id
        WHERE ch.channel_name = :1
    """
    cursor.execute(query, (channel,))

    print("\nVideos by Channel:")
    for row in cursor:
        vid_id, title, channel_name, views = row
        print(f"{vid_id} | {title} | {channel_name} | {views} views")


def filter_by_views(conn):
    min_views = input("Enter minimum views: ")

    cursor = conn.cursor()
    query = """
        SELECT DISTINCT vid_id, vid_title, vid_views
        FROM video
        WHERE vid_views >= :1
        ORDER BY vid_views DESC
    """
    cursor.execute(query, (min_views,))

    print("\nVideos with Minimum Views:")
    for row in cursor:
        vid_id, title, views = row
        print(f"{vid_id} | {title} | {views} views")


def categories_by_avg_views(conn):
    cursor = conn.cursor()
    query = """
        SELECT c.category_name, cp.performance_avg_views
        FROM category c
        JOIN category_performance cp 
        ON c.category_id = cp.category_id
        ORDER BY cp.performance_avg_views DESC
    """
    cursor.execute(query)

    print("\nCategories Ranked by Average Views:")
    for row in cursor:
        category, avg_views = row
        print(f"{category} | {avg_views} views")


def menu():
    print("\n--- Video Database Menu ---")
    print("1. Filter videos by upload date")
    print("2. Filter videos by category")
    print("3. Filter videos by channel")
    print("4. Filter videos by views")
    print("5. View categories by average views")
    print("6. Exit")


def main():
    conn = connect_db()
    if not conn:
        return

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            filter_by_date(conn)
        elif choice == "2":
            filter_by_category(conn)
        elif choice == "3":
            filter_by_channel(conn)
        elif choice == "4":
            filter_by_views(conn)
        elif choice == "5":
            categories_by_avg_views(conn)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

    conn.close()


if __name__ == "__main__":
    main()