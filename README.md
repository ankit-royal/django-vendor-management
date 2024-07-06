# Vendor Management System

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone git@github.com:ankit-royal/vendor-management.git
   cd vendor-management
   ```
2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
4. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Run the development server:
    ```bash
    python manage.py runserver
    ```

API Endpoints

- Vendor Endpoints:
    - POST /api/vendors/: Create a new vendor.
    - GET /api/vendors/: List all vendors.
    - GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
    - PUT /api/vendors/{vendor_id}/: Update a vendor's details.
    - DELETE /api/vendors/{vendor_id}/: Delete a vendor.
    - GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.

- Purchase Order Endpoints:
    - POST /api/purchase_orders/: Create a purchase order.
    - GET /api/purchase_orders/: List all purchase orders.
    - GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
    - PUT /api/purchase_orders/{po_id}/: Update a purchase order.
    - DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
    - POST /api/purchase_orders/{po_id}/acknowledge: Acknowledge a purchase order.
