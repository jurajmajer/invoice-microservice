import os
from datetime import datetime

from sqlalchemy.orm import Session

from app.api.controller.schemas import CreateInvoiceResponse
from app.bl.renderer.html_renderer import render_html
from app.bl.renderer.pdf_renderer import render_pdf
from app.db.database import SessionLocal
from app.db.models import InvoiceSequence


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_invoice(template_id: str, template_params: object, lang: str, db: Session) -> CreateInvoiceResponse:
    today = datetime.today()
    invoice_prefix = 'Z' + str(today.year)
    invoice_number = get_invoice_number(invoice_prefix, db)
    template_params = add_template_parms(template_params, invoice_number, today, lang)
    html_filename = render_html(template_id, template_params, lang, invoice_number)
    pdf_output_filename = get_pdf_output_filename(invoice_number + '.pdf', today)
    render_pdf(html_filename, pdf_output_filename)
    ret_val = CreateInvoiceResponse()
    ret_val.invoice_file_name = pdf_output_filename
    return ret_val


def get_invoice_number(invoice_prefix, db):
    try:
        db_row = db.query(InvoiceSequence).filter(InvoiceSequence.invoice_prefix == invoice_prefix).\
            with_for_update().first()
        if db_row is None:
            db_row = InvoiceSequence()
            db_row.invoice_prefix = invoice_prefix
            db_row.last_sequence_number = 1
            db.add(db_row)
        else:
            db_row.last_sequence_number = db_row.last_sequence_number + 1
        last_sequence_number = db_row.last_sequence_number
        db.commit()
    except Exception as exc:
        db.rollback()
        raise

    if last_sequence_number is None:
        raise Exception('last_sequence_number is None, cannot generate invoice number')
    return invoice_prefix + str(last_sequence_number).zfill(5)


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
