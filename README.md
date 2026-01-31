# POC Chatbot MVP

An internal chatbot to discover Points of Contact (POC), Team allocations, and Skills within the organization.

## Architecture
- **Backend**: FastAPI (Python)
- **Database**: SQLite (Local file `backend/chatbot.db`)
- **Frontend**: Single HTML file with Vanilla JS
- **NLP**: Mock LLM service (Regex-based for POC, extensible to OpenAI)

## Prerequisites
- Python 3.9+

## Setup & Run

## Setup & Run (Windows Step-by-Step)

1.  **Open PowerShell**
    - Press `Win + X` and select `Terminal` or `PowerShell`.
    - Navigate to the project folder:
      ```powershell
      cd "C:\Users\shubh\POC ChatBot\POC_ChatBot"
      ```

2.  **Install Dependencies**
    ```powershell
    pip install -r requirements.txt
    ```
    *If this fails, try `python -m pip install -r requirements.txt`*

3.  **Initialize Database**
    ```powershell
    python init_db.py
    ```
    *You should see "Database initialized successfully"*

4.  **Start Backend Server**
    ```powershell
    python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8001
    ```
    *Keep this terminal window OPEN. It is the server.*

5.  **Run Frontend**
    - Open a **new** PowerShell window.
    - Navigate to the project folder again:
      ```powershell
      cd "C:\Users\shubh\POC ChatBot\POC_ChatBot"
      ```
    - Start a simple web server:
      ```powershell
      python -m http.server 3000
      ```
    - Open your browser to: [http://localhost:3000/frontend/](http://localhost:3000/frontend/)

## How to Make It Smarter (More Questions)
To handle more complex questions (e.g., "Who handles the iOS app?" which implies "Mobile App"), you need a real LLM like OpenAI GPT-4.
See **[LLM_UPGRADE_GUIDE.md](LLM_UPGRADE_GUIDE.md)** for instructions on how to enable this.

## Example Queries
- "Who owns Mobile App?"
- "Who owns Ledger System?"
- "Who knows Python?"
- "Who is expert in React?"
- "Which team handles Bill Pay?"

## Extending to Real LLM
Uncomment the OpenAI code in `backend/llm_service.py` and provide your API key to replace the regex logic.
