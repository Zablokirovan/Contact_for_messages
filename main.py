"""
    Main entry point for exporting Bitrix24 deals
        and loading them into PostgreSQL.
"""

import Bitrix24
import Modify_date
import Base
import bot_tg


def main():
    """
        Running a full data dump into PostgreSQL
    """
    # Exporting transactions from Bitrix24
    deals = Bitrix24.get_deals()

    # Editing received data
    modify_deals, contact_id = Modify_date.deals_modify(deals)

    # Loading the received data into the PostgreSQL database
    Base.insert_contact_in_deal(modify_deals)

    # Getting contact information from Bitrix24 using ID_CONTACT
    contact_info = Bitrix24.get_contact_in_deals(contact_id)

    # Changing received contact data
    modify_contact = Modify_date.modify_date_contact(contact_info)

    # Loading contact data in contact locations
    Base.insertc_contact(modify_contact)

    # Downloading information about all departments from Bitrix24
    department = Bitrix24.department_get()

    # Loading department data into a PostgreSQL database
    Base.insert_department(department)

    # Send successful messages
    bot_tg.telegram_send_messages(
        "The upload of contacts and deals was completed successfully."
    )


if __name__ == "__main__":
    main()
