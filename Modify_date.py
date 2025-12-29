"""
File for changing the received date from Bitrix24
"""
import re
from datetime import datetime
from typing import List, Dict, Tuple


def deals_modify(deals: List[Dict]) -> Tuple[List[Tuple], List[int]]:
    """
      Transforms raw deals data from Bitrix24 into structures
    suitable for database insertion.

    :param deals:
    :return:
      tuple:
            - deals_data (list[tuple]): prepared deal records
            - contact_ids (list[int]): list of contact IDs
    """

    deals_data = []
    contact_id = []

    for deal in deals:
        if deal['CONTACT_ID'] is None:
            continue

        # Сreating a list of contact IDs to obtain information
        contact_id.append(int(deal['CONTACT_ID']))
        deals_data.append((
            int(deal['ID']),
            int(deal['CONTACT_ID']) if deal.get('CONTACT_ID') else None,
            deal['SOURCE_ID'],
            # Custom field, employee division
            int(deal['UF_CRM_5F3F5BECDFC07'])if deal.get(
                'UF_CRM_5F3F5BECDFC07'
            ) else None,  # подразделение
            datetime.fromisoformat(deal['DATE_CREATE']).strftime("%Y-%m-%d"),
            int(deal['CREATED_BY_ID']),
            # Custom field where the transaction city is located
            deal['UF_CRM_1760600132'][0] if deal[
                'UF_CRM_1760600132'] else None  # город роз
        ))

    return deals_data, contact_id


def clean_phone(phone: str) -> str | None:
    """
    Normalizes a phone number to the format 7XXXXXXXXXX.
    :param phone:phone (str): raw phone number

    Removes non-digit characters and converts numbers
    starting with 8XXXXXXXXXX to 7XXXXXXXXXX.

    Returns:
        str | None: normalized phone number or None if invalid

    """
    if not phone:
        return None

    # Clearing numbers of +, spaces, and other characters
    digits = re.sub(r'\D', '', phone)

    # Check the number length and replace the 8 with a 7 at
    # the beginning of the number 8xxxxxxxxx -> 7xxxxxxxxxx
    if digits.startswith('8') and len(digits) == 11:
        digits = '7' + digits[1:]

    # Checking the length of the number f at 7xxxxxxxxxxxx
    if digits.startswith('7') and len(digits) == 11:
        return digits

    return None


def modify_date_contact(contacts: List) -> List:
    """
    Changing data received from Bitrix.
    :param
        contacts:
    :return:
        contact_modify : List
    """
    contact_modify = []

    for con in contacts:
        raw_phones = []
        clean_phone_one = None

        # One contact can have multiple numbers
        for phone in con.get('PHONE', []):
            raw = phone.get('VALUE')
            # Skip if there is no contact phone number
            if not raw:
                continue

            raw_phones.append(raw)
            # The first number is retrieved from the
            # string of numbers and is filtered.
            if clean_phone_one is None:
                cleaned = clean_phone(raw)
                # Checking if a valid phone number exists
                if cleaned:
                    clean_phone_one = cleaned
        # Saving clean numbers from Bitrix24 to a string
        phones_row = ','.join(raw_phones)
        if not phones_row:
            continue

        contact_modify.append(
            (
                int(con['ID']),
                phones_row,
                clean_phone_one
            )
        )

    return contact_modify
