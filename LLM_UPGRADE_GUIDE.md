# Upgrade to Real LLM (OpenAI)

To make the chatbot "smarter" and capable of understanding diverse phrasing (e.g., "Who can help me with React?" vs "React experts"), you should switch from the Regex Mock to a real LLM.

## Why?
- **Regex**: Matches exact patterns (`who owns X`). Fails on `Does anyone own X?`.
- **LLM**: Understands intent (`find_owner`) regardless of phrasing. extracts entities (`X`) even with typose.

## Steps to Upgrade

1.  **Get an OpenAI API Key**
    - Sign up at [platform.openai.com](https://platform.openai.com).
    - Create a new API Key.

2.  **Install OpenAI Library**
    ```powershell
    pip install openai
    ```

3.  **Update `backend/llm_service.py`**
    - I have already added the code for `get_intent_openai` in the file, but it is commented out.
    - **Uncomment** the `get_intent_openai` method.
    - **Modify** `backend/main.py` to call `llm.get_intent_openai(request.question)` instead of `llm.get_intent(request.question)`.

4.  **Set Environment Variable**
    - In PowerShell, before running the server:
      ```powershell
      $env:OPENAI_API_KEY = "sk-YOUR-ACTUAL-KEY-HERE"
      ```

## Making it EVEN MORE Efficient (RAG)
For a production system with thousands of documents, you wouldn't just query SQL. You would use **RAG (Retrieval Augmented Generation)**.
1.  **Vector Database**: Store documentation chunks in a vector DB (like ChromaDB or Pinecone).
2.  **Embeddings**: Convert user query to numbers.
3.  **Search**: Find relevant docs.
4.  **Answer**: Feed docs to LLM to generate a natural language answer.

For this MVP, the **Intent -> SQL** approach is the most efficient and accurate for structured organization data.
