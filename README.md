# RoundSphere Project

A comprehensive water conservation solution using shade balls technology.

## Components

1. Flask API (Backend)
2. Django Frontend
3. PayPal Integration
4. IoT Data Collection
5. Analytics Dashboard

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env`
6. Run migrations:
   - Django: `python manage.py migrate`
   - Flask: `flask db upgrade`
7. Start the servers:
   - Django: `python manage.py runserver`
   - Flask: `python app.py`

## Contributors

- Umair: Flask API Design
- Binjal: Payment System & PayPal Integration
- Saad: Database Architecture
- Jalpa: Frontend Framework
- Hammad: UI/UX Design

## License

MIT License
