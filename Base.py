"""
File for loading valid data into tables
"""

import psycopg2
import  os

#Connecting to a PostgreSQL Database
db_client=psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    host= os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

def insert_contact_in_deal(deals: list):
    """
    Function for adding information about transactions and contacts to the database
    """
    with db_client.cursor() as cur:
        cur.executemany("""
            INSERT INTO "MessagingCore".contact_in_deal (
                deal_id,
                contact_id,
                funnel,
                department_id,
                date_create,
                employee_id,
                city_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (deal_id)
            DO UPDATE SET
                contact_id = EXCLUDED.contact_id,
                funnel        = EXCLUDED.funnel,
                department_id = EXCLUDED.department_id,
                date_create   = EXCLUDED.date_create,
                employee_id   = EXCLUDED.employee_id,
                city_id       = EXCLUDED.city_id
        """, deals)

    db_client.commit()


def insertc_contact(contact):
    """
    Function for downloading contact information

    :param contact:
    :return:

    """
    with db_client.cursor() as cur:
        cur.executemany("""
              INSERT INTO "MessagingCore".contact_info (contact_id, phone_raw, phone_num_clear)
    VALUES (%s, %s, %s)
    ON CONFLICT (contact_id, phone_raw)
    DO UPDATE SET
        phone_num_clear = EXCLUDED.phone_num_clear
        """, contact)

    db_client.commit()



def insert_department(department):
    with db_client.cursor() as cur:
        cur.executemany("""
                INSERT INTO "MessagingCore".department_info (id, name)
      VALUES (%s, %s)
      ON CONFLICT (id)
      DO UPDATE SET
          name = EXCLUDED.name
          """, department)

    db_client.commit()
    db_client.close()