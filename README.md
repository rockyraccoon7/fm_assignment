Endpoints
Vendor Endpoints
POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
PUT /api/vendors/{vendor_id}/: Update a vendor's details.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.
Purchase Order Endpoints
POST /api/purchase_orders/: Create a purchase order.
GET /api/purchase_orders/: List all purchase orders with optional filtering by vendor.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
Vendor Performance Endpoint
GET /api/vendors/{vendor_id}/performance: Retrieve performance metrics for a specific vendor.
Running the Test Suite
To run the test suite for this project, follow these steps:

Ensure that you have Python installed on your system.
Clone the project repository from GitHub:
bash
Copy code
git clone <repository_url>
Navigate to the project directory:
bash
Copy code
cd <project_directory>
Install the required dependencies using pip:
Copy code
pip install -r requirements.txt
Run the test suite using the manage.py script:
bash
Copy code
python manage.py test
This command will execute all the tests defined in the tests.py files within the project. You should see the output indicating the success or failure of each test case.
Additional Notes
Ensure that you have set up the database and configured the Django settings appropriately before running the test suite.
Modify the settings.py file if necessary to use the correct database configuration and other settings for your environment.
If any test fails, review the error messages to identify the issues and make necessary corrections to the codebase.


