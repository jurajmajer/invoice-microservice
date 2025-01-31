from fastapi import FastAPI

from app.api.controller import controller
from app.api.controller.schemas import CreateInvoiceBody, CreateInvoiceResponse
from starlette.status import HTTP_201_CREATED

app = FastAPI(
    title='Invoice Microservice API',
    description='Invoice Microservice API',
    version='0.0.1',
    servers=[
        {'url': 'http://localhost:8000', 'description': 'Development server'},
    ],
)


@app.post('/createInvoice',
          status_code=HTTP_201_CREATED,
          responses={'201': {'description': 'Invoice Created'},
                     '500': {'description': 'Internal server error'}},
          tags=['Invoice'])
def create_invoice(
        body: CreateInvoiceBody,
) -> CreateInvoiceResponse:
    return controller.create_invoice(body.template_id, body.template_params, body.lang)
