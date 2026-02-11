# Python Invoice PDF Generator

Generate professional, branded PDF invoices directly from Python using ReportLab.

This project is a **production-style example** of how to create invoices automatically for:

* SaaS platforms
* subscription billing
* marketplaces
* freelancers
* internal business tools

![invoice preview](docs/preview 1.jpg)
![invoice preview](docs/preview 2.jpg)

## Why this exists

Generating invoices sounds easy… until you actually need it in production.

Typical problems:

* HTML to PDF tools break layouts
* Stripe invoices are not customizable enough
* Word templates don't scale
* libraries have poor documentation

This repository shows a clean, maintainable way to generate invoices **directly in Python code**, with full layout control and zero external dependencies.


## Quick Start

```bash
git clone https://github.com/hasff/python-invoice-pdf-generator.git
cd python-invoice-pdf-generator
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python generate_invoice.py
```

The script will create:

```
output/invoice_sample.pdf
```

## Need custom PDF generation?

I help companies automate document generation:

* invoices
* certificates
* reports
* labels
* batch exports
* integration with APIs and databases

Typical use cases:

* SaaS billing systems
* automated emailing
* ERP integrations
* internal dashboards

📩 Contact: hugoferro@gmail.com
<!-- 🌐 Portfolio: https://hasff.github.io/site/ -->
