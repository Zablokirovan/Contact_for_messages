import re

from datetime import datetime


def deals_modify(deals):
    deals_data =[]
    contact_id = []
    for deal in deals:
        if deal['CONTACT_ID'] is None:
            continue
        contact_id.append(int(deal['CONTACT_ID']))
        deals_data.append((
            int(deal['ID']),
            int(deal['CONTACT_ID']) if deal.get('CONTACT_ID') else None,
            deal['SOURCE_ID'],
            int(deal['UF_CRM_5F3F5BECDFC07'])if deal.get('UF_CRM_5F3F5BECDFC07') else None,  # подразделение
            datetime.fromisoformat(deal['DATE_CREATE']).strftime("%Y-%m-%d"),
            int(deal['CREATED_BY_ID']),
            deal['UF_CRM_1760600132'][0] if deal['UF_CRM_1760600132'] else None  #город роз
        ))
    return deals_data, contact_id

def clean_phone(phone: str) -> str | None:
    if not phone:
        return None

    digits = re.sub(r'\D', '', phone)

    if digits.startswith('8') and len(digits) == 11:
        digits = '7' + digits[1:]

    if digits.startswith('7') and len(digits) == 11:
        return digits

    return None

def modify_date_contact(contacts):
    contact_modify = []

    for con in contacts:
        raw_phones = []
        clean_phone_one = None

        for phone in con.get('PHONE', []):
            raw = phone.get('VALUE')
            if not raw:
                continue

            raw_phones.append(raw)

            if clean_phone_one is None:
                cleaned = clean_phone(raw)
                if cleaned:
                    clean_phone_one = cleaned

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