# Car Rental Project

Django backend project for managing a car rental company.

## Part 1 – Car management
- Car registration
- Brand-based minimum daily rate
- Automatic daily rate calculation
- Automatic insurance calculation (5% of daily rate, minimum 50)
- Field validations using custom validators
- Business rules using clean() and save()
- Django Admin integration

## Part 2 – Rental management (Admin)
- Rental creation and finalization flow
- Business rules using clean(), save() and domain methods
- Admin actions to finalize rentals
- Rental history and filters

## Part 3 – REST API (Django REST Framework)

### Car API
- Full CRUD implementation
- Pagination
- Search by brand and model
- Ordering support
- Permission control (read-only for unauthenticated users)
- Clean separation between serializer, view, and domain logic

### Rental API
- Full CRUD implementation
- Automatic user association (request.user)
- Isolation by authenticated user
- Business rule: prevent renting an already rented car
- Rental finalization via API
- Prevent editing finalized rentals
- Filter by active/inactive rentals
- Search and ordering support
- Nested car representation in rental responses
- Hide internal user field from API responses

### Automated Tests
- Prevent duplicate rental of the same car
- Prevent editing finalized rentals
- Validate rental finalization logic
- Ensure business rules integrity

## Technologies
- Python
- Django
- Django Admin
- Django REST Framework (DRF)
- Django Filters
- MySQL
- Automated testing (Django TestCase + DRF APIClient)

## Next steps – Frontend (React)

- Create React project structure
- Implement authentication flow
- Consume Car API endpoints
- Consume Rental API endpoints
- Implement rental creation and finalization UI
- Add filtering and search on frontend
- Global state management using Context API
- Connect frontend to deployed backend
