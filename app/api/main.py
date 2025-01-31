import logging
import os

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED
import yaml

from app.api.controller import controller
from app.api.controller.schemas import CreateInvoiceBody, CreateInvoiceResponse

app = FastAPI(
    title='Invoice Microservice API',
    description='Invoice Microservice API',
    version='0.0.1',
    servers=[
        {'url': 'http://localhost:8000', 'description': 'Development server'},
    ],
)

# Configure logging
LOG_CONFIG_FILE = 'app/log_conf.yaml'
if os.path.isfile(LOG_CONFIG_FILE):
    with open(LOG_CONFIG_FILE, 'rt', encoding='utf-8') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.info('Starting API...')


@app.post('/createInvoice',
          status_code=HTTP_201_CREATED,
          responses={'201': {'description': 'Invoice Created'},
                     '500': {'description': 'Internal server error'}},
          tags=['Invoice'])
def create_invoice(
        body: CreateInvoiceBody,
        db: Session = Depends(controller.get_db),
) -> CreateInvoiceResponse:
    return controller.create_invoice(body.template_id, body.template_params, body.lang, db)
