# Lead Generation Platform — Backend README

This README is meant to help any team member quickly set up, run, test, and understand the backend of the lead generation platform.

## 1. Project overview

The backend is built to:
- receive incoming WhatsApp messages through a webhook
- parse the user message
- extract lead information such as property type, location, budget, and timeline
- store the lead in the database
- decide what follow-up question to ask next if some details are still missing

At the current stage, the backend mainly focuses on the lead capture and qualification flow.

## 2. Tech stack

- **Python**
- **FastAPI** for the API layer
- **Uvicorn** as the ASGI server
- **SQLAlchemy** for database interaction
- **SQLite** for local database storage
- **Pydantic** for request validation

## 3. Typical backend flow

1. A message is received on the webhook.
2. The backend reads the sender number and message text.
3. The message is parsed.
4. Lead details are extracted from the text.
5. A new lead is created, or an existing lead is updated.
6. The system checks which information is still missing.
7. A next qualification question is generated.

Example:
- User sends: `I want a villa in Dubai Marina around 2M in 2 months`
- Extracted fields may include:
  - Property Type: Villa
  - Location: Dubai Marina
  - Budget: 2M AED
  - Timeline: 2 months

If anything is missing, the backend can ask a targeted follow-up question.

## 4. Suggested project structure

A typical structure we have been using is:

```text
backend/
│
├── main.py
├── routes/
│   └── webhook.py
├── services/
│   ├── whatsapp_service.py
│   ├── lead_service.py
│   └── qualification_service.py
├── models/
│   ├── lead.py
│   └── message.py
└── database/
    └── database.py
```

## 5. Important files and what they do

### `backend/main.py`
Main FastAPI entry point.
Usually imports the router and starts the application.

### `backend/routes/webhook.py`
Contains the webhook endpoints.
This is where incoming requests are received.

### `backend/services/whatsapp_service.py`
Handles parsing of incoming WhatsApp messages.

### `backend/services/lead_service.py`
Creates or updates lead records based on the message content.

### `backend/services/qualification_service.py`
Determines what question should be asked next depending on which lead fields are missing.

### `backend/models/lead.py`
Defines the lead table structure.

### `backend/models/message.py`
Defines message-related storage if message logging is being used.

### `backend/database/database.py`
Creates the SQLAlchemy engine, session, and base.

## 6. How to run the backend

### Step 1: Open the project folder
In PowerShell:

```powershell
cd "E:\Personal Projects\Lead Generator"
```

### Step 2: Activate the virtual environment

```powershell
& "E:/Personal Projects/Lead Generator/venv/Scripts/Activate.ps1"
```

If the environment is already active, you will usually see `(venv)` in the terminal.

### Step 3: Run the FastAPI server

```powershell
python -m uvicorn backend.main:app --reload
```

Alternative command that may also be used:

```powershell
uvicorn backend.main:app --reload
```

## 7. Local server URL

Once the backend starts successfully, it usually runs at:

```text
http://127.0.0.1:8000
```

Swagger docs are available at:

```text
http://127.0.0.1:8000/docs
```

## 8. Current webhook endpoints

### Health / test route

**GET**
```text
/webhook/360dialog
```

Expected response:

```json
{"message": "360dialog webhook GET working"}
```

### Incoming message route

**POST**
```text
/webhook/360dialog
```

Expected request body:

```json
{
  "from": "971501234567",
  "text": "I want a villa in Dubai Marina around 2M in 2 months"
}
```

## 9. Testing the backend

### Option 1: Test using Swagger
Open:

```text
http://127.0.0.1:8000/docs
```

Then test the `POST /webhook/360dialog` endpoint by entering JSON in the request body.

### Option 2: Test using PowerShell

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/webhook/360dialog -Method POST -ContentType application/json -Body '{"from":"971501234567","text":"I want a villa in Dubai Marina around 2M in 2 months"}'
```

Another test example:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/webhook/360dialog -Method POST -ContentType application/json -Body '{"from":"971501234567","text":"In 2 months"}'
```

This is useful for checking whether an existing lead gets updated instead of recreated.

## 10. Database checking commands

To inspect the SQLite database:

```powershell
sqlite3 leads.db
```

Then run:

```sql
SELECT * FROM leads;
```

Example output:

```text
1|971501234567|Villa|Dubai Marina|2M AED|2 months|NEW
```

To exit SQLite:

```sql
.quit
```

## 11. Lead fields currently being extracted

At this stage, the backend is mainly extracting:
- **phone number**
- **property type**
- **location**
- **budget**
- **timeline**
- **status**

Typical model fields include:
- `id`
- `phone_number`
- `property_type`
- `location`
- `budget`
- `timeline`
- `status`

## 12. Current qualification logic

The qualification flow checks which lead detail is still missing and asks the next relevant question.

Typical priority order used:
1. budget
2. location
3. property type
4. timeline

Example:
- If a user only says: `I want something in 2 months`
- The backend may still need:
  - property type
  - location
  - budget

So the next question should target one of the missing fields.

## 13. Common test scenarios

### Scenario 1: Full lead provided in one message
Message:

```text
I want a villa in Dubai Marina around 2M in 2 months
```

Expected result:
- property type extracted
- location extracted
- budget extracted
- timeline extracted
- lead stored or updated successfully

### Scenario 2: Partial lead information
Message:

```text
I want a villa in Dubai Marina around 2M
```

Expected result:
- timeline remains missing
- backend asks: when are you planning to buy the property?

### Scenario 3: Existing lead updated later
First message:

```text
I want a villa in Dubai Marina around 2M
```

Second message:

```text
In 2 months
```

Expected result:
- same lead record updated
- timeline field filled in later

## 14. Common problems and fixes

### Problem 1: `Attribute "app" not found in module "main"`
Possible reason:
- wrong file path or wrong module path while running Uvicorn

Fix:
- make sure you run from the project root
- use:

```powershell
python -m uvicorn backend.main:app --reload
```

### Problem 2: Import errors
Possible reason:
- wrong folder structure
- missing `__init__.py` if needed
- running command from the wrong directory

Fix:
- make sure the backend folder structure is correct
- make sure imports match the structure exactly

### Problem 3: SQLite database not updating
Possible reason:
- wrong database path
- session not committing
- wrong model import

Fix:
- confirm `leads.db` exists in the project root
- confirm session commit is being called
- inspect records manually with SQLite

### Problem 4: Request body not accepted in Swagger
Possible reason:
- incorrect JSON format
- wrong field names

Correct request format:

```json
{
  "from": "971501234567",
  "text": "I want a villa in Dubai Marina around 2M"
}
```

## 15. Example of the webhook payload model

A version of the payload model used in the route may look like this:

```python
class WebhookPayload(BaseModel):
    from_: str = Field(..., alias="from")
    text: str

    class Config:
        populate_by_name = True
```

This is important because `from` is a reserved keyword in Python, so `from_` is used internally while still accepting `from` in the JSON.

## 16. Recommended daily workflow

1. Activate the virtual environment.
2. Run the backend server.
3. Open Swagger docs.
4. Send test webhook requests.
5. Check terminal logs.
6. Verify lead records in SQLite.
7. Fix extraction or qualification logic if needed.

## 17. Useful terminal commands summary

### Activate venv

```powershell
& "E:/Personal Projects/Lead Generator/venv/Scripts/Activate.ps1"
```

### Run backend

```powershell
python -m uvicorn backend.main:app --reload
```

### Open SQLite

```powershell
sqlite3 leads.db
```

### Check leads table

```sql
SELECT * FROM leads;
```

### Sample API test

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/webhook/360dialog -Method POST -ContentType application/json -Body '{"from":"971501234567","text":"I want a villa in Dubai Marina around 2M in 2 months"}'
```

## 18. What is currently complete

- basic FastAPI backend setup
- webhook route creation
- request body validation using Pydantic
- message parsing flow
- lead extraction logic for core fields
- lead creation / update flow
- SQLite integration
- qualification question logic
- terminal and Swagger-based testing

## 19. Possible next steps

Depending on the project plan, future work may include:
- better NLP-based extraction
- message history tracking
- improved lead scoring
- dashboard integration
- frontend connection
- CRM integration
- deployment to a cloud environment
- authentication and role-based access
- logging and monitoring improvements

## 20. Notes for handover

If someone new is continuing this backend, they should first:
- confirm the environment is activating correctly
- confirm the server runs without import errors
- confirm `/docs` is accessible
- test the webhook with sample messages
- verify that records appear correctly in `leads.db`

Once this works, they can safely continue with feature development.

---

## Quick Start

```powershell
cd "E:\Personal Projects\Lead Generator"
& "E:/Personal Projects/Lead Generator/venv/Scripts/Activate.ps1"
python -m uvicorn backend.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```
