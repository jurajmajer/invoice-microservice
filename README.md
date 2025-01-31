# Invoice Microservice
[![Build Docker Image](https://github.com/jurajmajer/invoice-microservice/actions/workflows/build-docker-image.yml/badge.svg)](https://github.com/jurajmajer/invoice-microservice/actions/workflows/build-docker-image.yml)
![pylint Score](https://mperlet.github.io/pybadge/badges/9.74.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/jurajmajer/invoice-microservice/blob/main/LICENSE)

## Installation on Kubernetes
1. Create database on your DB server. We use MySQL.
```sql
CREATE DATABASE IF NOT EXISTS `invoice-microservice` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'invoice-microservice'@'%' IDENTIFIED BY '<insert_password_here>';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, LOCK TABLES ON `invoice-microservice`.* TO 'invoice-microservice'@'%';
```
2. Create schema in the database using Alembic migration.
3. Review deployment scripts for Kubernetes in folder `infra/k8s`. At minimum you have to modify `1-init.yaml` and set secret values (replace `<define-this>` with actual value).
4. Apply kubernetes scripts:
```
kubectl apply -f infra/k8s/1-init.yaml
kubectl apply -f infra/k8s/2-define-storage.yaml
kubectl apply -f infra/k8s/3-deployment.yaml
```
5. Save your invoice templates to TEMPLATE_ROOT. See details about TEMPLATE_ROOT structure below.

### Environment variables which need to be set in runtime
* `TEMPLATE_ROOT` - folder where all templates are stored. No default value, must be set.
* `OUTPUT_FOLDER` - folder where created invoices will be saved. No default value, must be set.
* `DEFAULT_LANG` - default language. If template for requested language is not found, default language will be used if set. No default value, optional parameter.
* `DB_URI` - Database connection string. No default value, must be set. E.g.: mysql://invoice-microservice:<password>@<db-server>/invoice-microservice

### TEMPLATE_ROOT structure
invoice-microservice assumes following structure of TEMPLATE_ROOT folder:

```
TEMPLATE_ROOT
│
└───en
│   │
│   └───<templateId1>
│   │      html.jinja2
│   │      params.json
│   │  
│   └───<templateId2>
|          html.jinja2
|          params.json
│
└───de
│   │
│   └───<templateId1>
│   │      html.jinja2
│   │  
│   └───<templateId2>
|          html.jinja2
```
Under TEMPLATE_ROOT there is a set of folders named by languages (`en`, `de` etc.). In every language folder there are folders named by template IDs. In every template ID folder there must be one file for html invoice template named exactly `html.jinja2` and one optional file containing template params named exactly `params.json`.

## Usage
Other pods should use OpenAPI interface of invoice-microservice to use it. OpenAPI interface does not require any authentication. It is assumed invoice-microservice is accessible only within the cluster. Swagger documentation is available after installation under [http://\<invoice-microservice\>/docs](http://invoice-microservice/docs). Alternatively, you can check out the swagger UI [here](https://jurajmajer.github.io/invoice-microservice/openapi/).


## Contribution / Development
### Generate requirements.txt (Powershell)
Navigate in Powershell to the root folder of project, e.g. `C:\projects\invoice-microservice` and execute:
```Powershell
.\script\create-pip-requirements.ps1
```

### Generate and apply Alembic migration (Powershell)
Navigate in Powershell to `db` folder of project, e.g. `C:\projects\invoice-microservice\app\db` and execute:
```Powershell
$env:PYTHONPATH = 'C:/projects/invoice-microservice/'
$env:DB_URI = 'mysql://invoice-microservice:<password>@localhost/invoice-microservice'
alembic revision --autogenerate -m "<custom message>"
alembic upgrade head
```
