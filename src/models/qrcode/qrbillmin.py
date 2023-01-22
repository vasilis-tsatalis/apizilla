from typing import Optional, List
from pydantic import BaseModel, Field

class Creditor(BaseModel):
    creditor_name: str = Field(...,title='CREDITOR_NAME',description='creditor name')
    creditor_postalcode: str = Field(...,title='CREDITOR_POSTALCODE',description='creditor postal code')
    creditor_city: str = Field(...,title='CREDITOR_CITY',description='creditor city')
    creditor_street: Optional[str] = Field(title='CREDITOR_STREET',description='creditor street')
    creditor_housenumber: Optional[str] = Field(title='CREDITOR_HOUSENUMBER',description='creditor house number')
    creditor_country: Optional[str] = Field(title='CREDITOR_COUNTRY',description='creditor country')

class Debtor(BaseModel):
    debtor_name: Optional[str] = Field(...,title='DEBTOR_NAME',description='debtor name')
    debtor_postalcode: Optional[str] = Field(...,title='DEBTOR_POSTALCODE',description='debtor postal code')
    debtor_city: Optional[str] = Field(...,title='DEBTOR_CITY',description='debtor city')
    debtor_street: Optional[str] = Field(title='DEBTOR_STREET',description='debtor street')
    debtor_housenumber: Optional[str] = Field(title='DEBTOR_HOUSENUMBER',description='debtor house number')
    debtor_country: Optional[str] = Field(title='DEBTOR_COUNTRY',description='debtor country')

class QRBillmin(BaseModel):
    name: Optional[str] = Field(title='OUTPUT',description='output file')
    account: str = Field(...,title='ACCOUNT',description='creditor IBAN account number')
    amount: Optional[str] = Field(...,title='AMOUNT',description='amount of payment')
    currency: Optional[str] = Field(...,title='{CHF,EUR}',description='currency of payment')
    due_date: Optional[str] = Field(...,title='DUE_DATE',description='due date of payment in the form YYYY-MM-DD')
    reference_number: Optional[str] = Field(title='REFERENCE_NUMBER',description='reference number')
    language: Optional[str] = Field(title='{en,de,fr,it}',description='language')
    creditor: Optional[Creditor]
    debtor: Optional[Debtor]
