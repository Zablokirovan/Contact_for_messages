import os
import datetime
from dotenv import load_dotenv


from fast_bitrix24 import Bitrix

load_dotenv()

#webhook from bitrix
webhook = os.getenv("BITRIX_WEB_HOOK")
b = Bitrix(webhook, respect_velocity_policy=True)


start_date = datetime.date(2025,5, 20).strftime('%Y-%m-%dT00:00:00')
end_date = datetime.date(2025, 5, 30).strftime('%Y-%m-%dT00:00:00')

def get_deals():
    return  b.get_all('crm.deal.list', params= {
        'filter':{
            '>=DATE_CREATE':start_date,
            '<=DATE_CREATE': end_date,
            'CATEGORY_ID': 0
        },
        'select':[
            'ID', 'CONTACT_ID', 'UF_CRM_5F3F5BECDFC07', 'DATE_CREATE', 'CREATED_BY_ID', 'UF_CRM_1760600132',"SOURCE_ID"
        ]
    })

def chunks(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def get_contact_in_deals(contact_ids, batch_size=50):
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



def department_get():
    list_dep = []
    dict_dep_b =  b.get_all('department.get')

    for d_value in dict_dep_b:
        list_dep.append((
            d_value['ID'],
            d_value['NAME']
        ))

    return list_dep

