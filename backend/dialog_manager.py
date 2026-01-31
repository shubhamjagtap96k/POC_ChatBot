from backend.query_engine import QueryEngine
from backend.rag_service import RAGService

# States
STATE_GREETING = "GREETING"
STATE_MENU = "MENU"
STATE_ASK_LOCATION = "ASK_LOCATION"
STATE_ASK_TECHNOLOGY = "ASK_TECHNOLOGY"
STATE_ASK_FEATURE = "ASK_FEATURE"
STATE_ASK_ISSUE = "ASK_ISSUE"
STATE_ASK_DETAILS = "ASK_DETAILS"
STATE_CONFIRM = "CONFIRM"
STATE_SEARCH = "SEARCH"
STATE_ASK_DOCS = "ASK_DOCS"
STATE_END = "END"

class DialogManager:
    def __init__(self):
        self.engine = QueryEngine()
        self.rag = RAGService()

    def handle_turn(self, session, user_input):
        current_state = session.get("state", STATE_GREETING)
        data = session.get("data", {})
        response = ""
        next_state = current_state

        user_input_lower = user_input.lower().strip()

        # --- STATE MACHINE ---

        if current_state == STATE_GREETING:
            val = user_input.lower().strip()
            # If user answers with a selection immediately (ignoring greeting)
            if val and val not in ["hello", "hi", "start", "init"]:
                session["state"] = STATE_MENU
                return self.handle_turn(session, user_input)
            else:
                # Standard Greeting
                response = "Hello 👋 I am your POC Finder Assistant. How may I help you today?"
                next_state = STATE_MENU
                session["state"] = next_state
                return response, next_state

        if current_state == STATE_MENU:
            if user_input: 
                # Check for Option 5 (Docs)
                if "5" in user_input or "doc" in user_input_lower or "knowledge" in user_input_lower or "general" in user_input_lower:
                    response = "What general topic would you like to search the Knowledge Base for? (Example: VPN, HR Policy)"
                    session["category"] = "Docs"
                    next_state = STATE_ASK_DOCS
                
                elif "1" in user_input or "location" in user_input_lower:
                    response = "Which location are you looking for? (Example: India, US, UK)"
                    session["category"] = "Location"
                    next_state = STATE_ASK_LOCATION
                elif "2" in user_input or "tech" in user_input_lower:
                    response = "Which technology or stack do you need a POC for? (Example: Java, React, Python)"
                    session["category"] = "Technology"
                    next_state = STATE_ASK_TECHNOLOGY
                elif "3" in user_input or "feature" in user_input_lower or "app" in user_input_lower:
                    response = "Which feature or application are you working on? (Example: Payments, Mobile App)"
                    session["category"] = "Feature"
                    next_state = STATE_ASK_FEATURE
                elif "4" in user_input or "issue" in user_input_lower or "support" in user_input_lower:
                    response = "Please briefly describe your issue or requirement."
                    session["category"] = "Issue"
                    next_state = STATE_ASK_ISSUE
                else:
                    response = (
                        "Are you looking for a POC based on:\n"
                        "1) Location\n"
                        "2) Technology\n"
                        "3) Feature / Application\n"
                        "4) Issue / Support\n"
                        "5) Knowledge Base / Docs\n"
                        "Please type the number or describe your need."
                    )
            else:
                 response = (
                    "Are you looking for a POC based on:\n"
                    "1) Location\n"
                    "2) Technology\n"
                    "3) Feature / Application\n"
                    "4) Issue / Support\n"
                    "5) Knowledge Base / Docs\n"
                    "Please type the number or describe your need."
                 )

        elif current_state == STATE_ASK_DOCS:
            # Perform RAG Search immediately (No Confirmation needed for simple search)
            results = self.rag.search(user_input)
            response = (
                f"Here is what I found in the Knowledge Base:\n\n"
                f"{results}\n\n"
                f"Would you like to search something else? (Yes/No)"
            )
            next_state = STATE_END

        elif current_state in [STATE_ASK_LOCATION, STATE_ASK_TECHNOLOGY, STATE_ASK_FEATURE, STATE_ASK_ISSUE]:
            # Capture the search term
            data["term"] = user_input
            response = "Can you provide more specific details? (Example: module name, environment, urgency)"
            next_state = STATE_ASK_DETAILS

        elif current_state == STATE_ASK_DETAILS:
            data["details"] = user_input
            
            # Summary
            cat = session.get("category", "Unknown")
            term = data.get("term", "N/A")
            details = data.get("details", "N/A")
            
            response = (
                f"Thank you. I understood that:\n"
                f"- Category: {cat}\n"
                f"- Search: {term}\n"
                f"- Details: {details}\n\n"
                f"Is this correct? (Yes/No)"
            )
            next_state = STATE_CONFIRM

        elif current_state == STATE_CONFIRM:
            if "yes" in user_input_lower or "y" == user_input_lower:
                # Perform Search
                cat = session.get("category")
                term = data.get("term")
                
                search_result = self.engine.search_poc(cat, term)
                
                response = (
                    f"Based on your input, here is the information:\n\n"
                    f"{search_result}\n\n"
                    f"Would you like help with anything else? 😊"
                )
                next_state = STATE_END
            else:
                response = "I didn't fully understand or you said No. Let's start over.\n" + \
                           "Are you looking for a POC based on: 1) Location 2) Tech 3) Feature 4) Issue 5) Docs"
                next_state = STATE_MENU 

        elif current_state == STATE_END:
            if "yes" in user_input_lower:
                response = (
                    "Are you looking for a POC based on:\n"
                    "1) Location\n"
                    "2) Technology\n"
                    "3) Feature / Application\n"
                    "4) Issue / Support\n"
                    "5) Knowledge Base / Docs"
                )
                next_state = STATE_MENU 
                session["data"] = {}
                session.pop("category", None)
            else:
                response = "Goodbye! 👋"
                next_state = STATE_GREETING 

        # Save session state
        session["state"] = next_state
        session["data"] = data
        return response, next_state
