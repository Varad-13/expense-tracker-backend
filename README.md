# Expense Tracker Backend
## Tech Stack:
- Django
- Postman
- AWS EC2

## Authentication
#### Authentication class: DeviceIDAuthentication
#### Authentication model: Device {deviceID, last_login}
#### Working: 
- Every request must include {DEVICEID} in header
- The authentication class checks for {DEVICEID} in the database
	- If {DEVICEID} is found, we update {last_login} to current timestamp
	- Otherwise create a {DEVICEID, last_login} record in the database
- Authenticated
- For each request, {DEVICEID} is used for identifying and filtering data based on users

## URL Routes
### General Paths:
- /api/auth: Used for testing API authentication and availability
- /api/delete_data: Delete all userdata for a specific user (To be triggered from the backend only)
### Card Paths
- /api/add-card: User for adding cards
- /api/get-cards: Returns all cards for a specific user
- /api/delete-card: Delete a specific card and all its related transactions, limits
- /api/update-limit: Reassign card limits
### Transaction Paths
- /api/add-transaction: Add a transaction (credit/debit)
- /api/get-transactions: Retrieve all transactions for a user
- /api/get-transactions-debit: Retrieve all debit (expense) transactions
- /api/get-transaction-credit: Retrieve all credit (repayment/income) transactions
- api/get-transaction-category: Retrieve transactions by category
- api/get-transaction-card: Retrieve all transactions for a particular card
- api/get-transaction-card-category: Retrieve all transactions for a particular card under a category (Not yet Implemented)
- api/delete-transaction: Delete a particular transaction
- api/delete-all-transaction: Delete all transactions for a user
- api/update-transaction: Edit a transaction
### Limits
- api/get-limit: Returns {card, totall_spent, total_earnt, percent_used, fractional_percent}. Used on dashboard page chart.
- api/get-total-limits: Returns {expense, limit, percent} Used on the analytics below dashboard page chart
- api/get-limit-card: Returns {card, total_spent, total_earnt, percent_used} Not yet implemented on frontend
- api/reset-limit: Reset all limits for a user incase of miscalculations (To be triggered from the backend only)
- api/get-income-expense: Returns total income, savings and expense.
- api/analytics/<str:device_id>: Redirects to an analytics page for the specific device
