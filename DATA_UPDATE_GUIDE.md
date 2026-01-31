# How to Update Chatbot Data

You have two types of data in this system. Here is how to update each.

## 1. "General Knowledge" (RAG / Documents)
*Used for questions like "How do I fix VPN?", "HR Policy", etc.*

1.  **Navigate to**: `POC_ChatBot/data/docs/`
2.  **Delete** all the dummy files (e.g., `VPN_Troubleshooting_x.md`).
3.  **Add your own files**:
    - Create new `.md` text files.
    - Paste your content (Policies, Guides, FAQs).
    - *Example*: `HR_Policy.md`
4.  **Restart the Server** (or run the `generate_data.py` script if you modified it).
    - The server automatically ingests these files on startup if using `rag_service.py`.

## 2. "People & Teams" (Structured Database)
*Used for questions like "Who owns X?", "Where is Y location?"*

### Option A: Clean Slate (Manual Entry)
1.  Open `backend/seed.sql`.
2.  **Delete** the sample `INSERT` statements.
3.  **Add your real data**:
    ```sql
    INSERT INTO teams (name, description) VALUES ('My Real Team', 'Description');
    INSERT INTO people (name, role, team_id, location) VALUES ('John Real', 'Dev', 1, 'US');
    ```
4.  **Run Initialization**:
    ```powershell
    python init_db.py
    ```
    *(Warning: This wipes the existing database and re-creates it from `seed.sql`)*

### Option B: Bulk Import (Script)
If you have a lot of data (e.g., in Excel/CSV), modify the generator script.

1.  Open `generate_data.py`.
2.  Look at the `generate_sql_data()` function.
3.  Modify the lists `roles`, `locations`, etc., or write code to read from your CSV.
    ```python
    # Example modification
    employees = [
        ("Real Name 1", "Dev", "India"),
        ("Real Name 2", "Manager", "US")
    ]
    # Loop through `employees` and insert into DB
    ```
4.  Run the script:
    ```powershell
    python generate_data.py
    ```
