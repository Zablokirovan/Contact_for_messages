import  Bitrix24
import modify_date
from datetime import *
import Base


deals = Bitrix24.get_deals()
modify_deals, contact_id = modify_date.deals_modify(deals)
Base.insert_contact_in_deal(modify_deals)

contact_info = Bitrix24.get_contact_in_deals(contact_id)
modify_contact = modify_date.modify_date_contact(contact_info)
Base.insertc_contact(modify_contact)

department = Bitrix24.department_get()
Base.insert_department(department)