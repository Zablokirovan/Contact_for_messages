import os
import datetime
import bot_tg

from dotenv import load_dotenv
from fast_bitrix24 import Bitrix

load_dotenv()

# webhook from bitrix
webhook = os.getenv("BITRIX_WEB_HOOK")

# Waits the required amount of time between
# requests to avoid exceeding Bitrix24 limits
b = Bitrix(webhook, respect_velocity_policy=True)

# Date from which to upload
start_date = datetime.date(2025, 5, 20).strftime('%Y-%m-%dT00:00:00')
# Date up to what date to upload
end_date = datetime.date(2025, 5, 30).strftime('%Y-%m-%dT00:00:00')


def get_deals():
    """
    Function for downloading transactions by creation date

    :return: Dict
    """
    try:
        return b.get_all('crm.deal.list', params={'filter': {
            '>=DATE_CREATE': start_date,
            '<=DATE_CREATE': end_date,
            'CATEGORY_ID': 0
        },
            # Select only the fields of interest for unloading
            'select': [
                'ID', 'CONTACT_ID',
                'UF_CRM_5F3F5BECDFC07',
                'DATE_CREATE',
                'CREATED_BY_ID',
                'UF_CRM_1760600132', "SOURCE_ID"
            ]
        })
    except Exception as e:
        bot_tg.telegram_send_messages(f"Error: get_deals \n {e}")


def chunks(lst, size):
    """
        Splitting a large array of IDs
         into chunks to avoid getting caught by the Bitrix24 block
        :param lst:
        :param size: 50
    :return: list
    """
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def get_contact_in_deals(contact_ids, batch_size=50):
    """
    Getting contact information by ID chunks
    :param contact_ids:
    :param batch_size:
    :return: list(dict)
    """
    try:
        result = []
        contact_ids = [int(i) for i in contact_ids]

        for batch in chunks(contact_ids, batch_size):
            res = b.get_all('crm.contact.list', params={
                'filter': {
                    'ID': batch
                },
                'select': [
                    'ID',  'PHONE'
                ]
            })
            result.extend(res)

        return result

    except Exception as e:
        bot_tg.telegram_send_messages(f'Error:  get_contact_in_deals \n {e}')


def department_get():
    """
    function for obtaining departments for subsequent
     communication transaction/city/phone number
    :return: list
    """
    try:
        list_dep = []
        dict_dep_b = b.get_all('department.get')
        for d_value in dict_dep_b:
            list_dep.append((
                d_value['ID'],
                d_value['NAME']
            ))

        return list_dep
    except Exception as e:
        bot_tg.telegram_send_messages(f'Error: department_get \n {e}')
