-- schema.sql

-- Create Borrower table
CREATE TABLE borrower (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    credit_score INTEGER NOT NULL,
    annual_income DECIMAL(10, 2) NOT NULL,
    debt_to_income_ratio DECIMAL(5, 2) NOT NULL
);

-- Create LoanApplication table
CREATE TABLE loan_application (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrower_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    term INTEGER NOT NULL,
    purpose TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    disbursed_at TIMESTAMP,
    FOREIGN KEY (borrower_id) REFERENCES borrower (id)
);

-- Create LoanRepayment table
CREATE TABLE loan_repayment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (loan_id) REFERENCES loan_application (id)
);