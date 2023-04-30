CREATE TABLE IF NOT EXISTS vendors(
    vendor_id VARCHAR(11) NOT NULL,
    vendor_name VARCHAR(50) NOT NULL,
    PRIMARY KEY(vendor_id)
);

CREATE TABLE IF NOT EXISTS clients(
    client_id VARCHAR(11) NOT NULL,
    client_name VARCHAR(50) NOT NULL,
    PRIMARY KEY(client_id)
);

INSERT INTO clients VALUES
("20222222223", "Anonymous Client");

CREATE TABLE IF NOT EXISTS general_journal(
    operation_date VARCHAR(10) NOT NULL,
    account VARCHAR(60) NOT NULL,
    debits INT(11) DEFAULT 0,
    credits INT(11) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS buys_bills_invoices_docs(
    user_type_input VARCHAR(3) NOT NULL,
    doc_letter VARCHAR(1) NOT NULL,
    document_POS INT(5) NOT NULL,
    document_numb INT(8) NOT NULL,
    doc_date VARCHAR(10) NOT NULL,
    vendor_id VARCHAR(11) NOT NULL,
    vendor_name VARCHAR(50) NOT NULL,
    afip_doc_type VARCHAR(3) NOT NULL,
    vat_base_10.5 INT(40),
    vat_base_21 INT(40),
    vat_base_27 INT(40),
    vat_10.5 INT(40),
    vat_21 INT(40),
    vat_27 INT(40),
    vat_withholdings INT(40),
    gross_income_withholdings INT(40),
    other_withholdings INT(40),
    other_amounts_not_vat_Base INT(40),
    total_invoice_ticket_amount INT(40),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS sales_bills_invoices_docs(
    user_type_input VARCHAR(3) NOT NULL,
    doc_letter VARCHAR(1) NOT NULL,
    document_POS INT(5) NOT NULL,
    document_numb INT(8) NOT NULL,
    doc_date VARCHAR(10) NOT NULL,
    client_id VARCHAR(11) NOT NULL,
    client_name VARCHAR(50) NOT NULL,
    afip_type_of_doc VARCHAR(3) NOT NULL,
    vat_base INT(40),
    vat INT(40),
    vat_withholdings INT(40),
    gross_income_withholdings INT(40),
    other_withholdings INT(40),
    other_amounts_not_vat_Base INT(40),
    total_invoice_ticket_amount INT(40),
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);