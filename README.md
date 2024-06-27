# Loan Provisioning System

This is a Django-based Loan Provisioning System that allows users to apply for loans, approve/reject loan applications, disburse loans, and record repayments.

## Features

- Loan application creation
- Loan application approval/rejection
- Loan disbursement
- Loan repayment recording
- Validation and error handling

## Requirements

- Python 3.8+
- Django 4.2+
- Django Rest Framework 3.12+

## Setup Instructions

### 1. Clone the Repository

- git clone https://github.com/AAteddy/Kifiya-LPS.git
- cd loan-provisioning-system

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

- python -m venv venv
- source venv/bin/activate # On Windows: venv\Scripts\activate

### 3. Install Dependencies

Install the required Python packages using pip:

- pip install -r requirements.txt

### 4. Configure the Database

By default, the project is configured to use SQLite. If you want to use a different database (like PostgreSQL), update the DATABASES setting in loan_system/settings.py.

### 5. Apply Migrations

Run the following command to apply database migrations:

- python manage.py migrate

### 6. Run the Development Server

Start the Django development server:

- python manage.py runserver
  The application will be accessible at http://127.0.0.1:8000/.

### 7. Access the Admin Interface

Log in to the admin interface to manage users and loan applications:

- http://127.0.0.1:8000/admin/

- http://127.0.0.1:8000/loans/

## Running Tests

To run the test suite, use the following command:

- python manage.py test

This will run all the unit tests and provide a summary of the results.

## API Endpoints

Here are some of the key API endpoints:

- Create Loan Application: POST /api/loanapplications/
- Retrieve Loan Application: GET /api/loanapplications/{id}/
- Approve Loan Application: PUT /api/loanapplications/{id}/approve/
- Reject Loan Application: PUT /api/loanapplications/{id}/reject/
- Disburse Loan Application: POST /api/loanapplications/{id}/disburse/
- Record Repayment: POST /api/loanapplications/{id}/repay/

## Project Structure

loan-provisioning-system/
│
├── loan_system/ # Main Django project folder
│ ├── settings.py # Project settings
│ ├── urls.py # URL configurations
│ └── ...
│
├── loans/ # App for managing loans
│ ├── models.py # Data models
│ ├── views.py # API views
│ ├── serializers.py # Serializers for API
│ ├── urls.py # App-specific URL configurations
│ ├── business_logic.py # Business logic for loan processing
│ ├── test_views.py # Unit tests for views
│ └── ...
│
├── requirements.txt # Project dependencies
└── README.md # Project README

## Contributing

Contributions are welcome! Please create a pull request with a description of your changes.

## License

## Contact

For questions or support, please contact [tedsaasfaha@gmail.com].
