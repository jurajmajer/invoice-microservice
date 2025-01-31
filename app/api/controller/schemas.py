from pydantic import BaseModel, Field


class CreateInvoiceBody(BaseModel):
    template_id: str = Field(None, alias='templateId')
    template_params: object | None = Field(None, alias='templateParams')
    lang: str | None = 'en'


class CreateInvoiceResponse(BaseModel):
    invoice_file_name: str = Field(None, alias='invoiceFileName')
