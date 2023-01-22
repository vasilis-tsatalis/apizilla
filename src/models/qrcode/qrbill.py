from typing import Optional, List
from pydantic import BaseModel, Field


class Creditorwrk(BaseModel):
    creditor_name: str = Field(...,title='CREDITOR_NAME',description='creditor name')
    creditor_postalcode: str = Field(...,title='CREDITOR_POSTALCODE',description='creditor postal code')
    creditor_city: str = Field(...,title='CREDITOR_CITY',description='creditor city')
    creditor_line1: Optional[str] = Field(title='CREDITOR_LINE1',description='creditor address line 1')
    creditor_line2: Optional[str] = Field(title='CREDITOR_LINE2',description='creditor address line 2')
    creditor_street: Optional[str] = Field(title='CREDITOR_STREET',description='creditor street')
    creditor_housenumber: Optional[str] = Field(title='CREDITOR_HOUSENUMBER',description='creditor house number')
    creditor_country: Optional[str] = Field(title='CREDITOR_COUNTRY',description='creditor country')


class Paymentwrk(BaseModel):
    amount: Optional[str] = Field(...,title='AMOUNT',description='amount of payment')
    currency: Optional[str] = Field(...,title='{CHF,EUR}',description='currency of payment')
    due_date: Optional[str] = Field(...,title='DUE_DATE',description='due date of payment in the form YYYY-MM-DD')


class Debtorwrk(BaseModel):
    debtor_name: Optional[str] = Field(...,title='DEBTOR_NAME',description='debtor name')
    debtor_postalcode: Optional[str] = Field(...,title='DEBTOR_POSTALCODE',description='debtor postal code')
    debtor_city: Optional[str] = Field(...,title='DEBTOR_CITY',description='debtor city')
    debtor_line1: Optional[str] = Field(title='DEBTOR_LINE1',description='debtor address line 1')
    debtor_line2: Optional[str] = Field(title='DEBTOR_LINE2',description='debtor address line 2')
    debtor_street: Optional[str] = Field(title='DEBTOR_STREET',description='debtor street')
    debtor_housenumber: Optional[str] = Field(title='DEBTOR_HOUSENUMBER',description='debtor house number')
    debtor_country: Optional[str] = Field(title='DEBTOR_COUNTRY',description='debtor country')


class QRBillwrk(BaseModel):
    name: Optional[str] = Field(title='OUTPUT',description='output file')
    account: str = Field(...,title='ACCOUNT',description='creditor IBAN account number')
    creditor: Creditorwrk
    payment: Optional[Paymentwrk]
    debtor: Optional[Debtorwrk]
    reference_number: Optional[str] = Field(title='REFERENCE_NUMBER',description='reference number')
    extra_infos: Optional[str] = Field(title='EXTRA_INFOS',description='payment purpose')
    alt_procs: Optional[List[str]] = Field(title='[ALT_PROCS ...]',description='alternative payment parameters (2 lines max)')
    language: Optional[str] = Field(title='{en,de,fr,it}',description='language')
    full_page: Optional[str] = Field(description='Print to full A4 size page')
    no_top_line: Optional[str] = Field(description='Do not print top separation line')
    no_payment_line: Optional[str] = Field(description='Do not print vertical separation line between receipt and payment parts')
    font_factor: Optional[str] = Field(title='FONT_FACTOR',description='Font factor to provide a zoom for all texts on the bill')
