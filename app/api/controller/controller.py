import json
import os
from datetime import datetime

from app.api.controller.schemas import CreateInvoiceResponse
from app.bl.renderer.html_renderer import render_html
from app.bl.renderer.pdf_renderer import render_pdf


def create_invoice(template_id: str, template_params: object, lang: str) -> CreateInvoiceResponse:
    invoice_number = get_invoice_number()
    today = datetime.today()
    template_params = add_template_parms(template_params, invoice_number, today, lang)
    html_filename = render_html(template_id, template_params, lang, invoice_number)
    pdf_output_filename = get_pdf_output_filename(invoice_number + '.pdf', today)
    render_pdf(html_filename, pdf_output_filename)
    ret_val = CreateInvoiceResponse()
    ret_val.invoice_file_name = pdf_output_filename
    return ret_val


def get_invoice_number():
    return 'Z202500001'


def add_template_parms(template_params, invoice_number, today, lang):
    template_params['invoice']['number'] = invoice_number
    template_params['invoice']['dateOfCreation'] = format_current_date(today)
    template_params['invoice']['dateOfDelivery'] = format_current_date(today)
    template_params['invoice']['dueDate'] = format_current_date(today)
    template_params['invoice']['formOfPayment'] = get_form_of_payment(lang)
    return template_params


def format_current_date(today):
    return today.strftime('%d. %b %Y')


def get_form_of_payment(lang):
    if lang == 'sk':
        return 'Platobná brána'
    elif lang == 'cs':
        return 'Platební brána'
    elif lang == 'pl':
        return 'Bramka płatności'
    elif lang == 'de':
        return 'Zahlungsgateway'
    return 'Payment gateway'


def get_pdf_output_filename(output_filename, today):
    return os.path.join(str(today.year), output_filename)
