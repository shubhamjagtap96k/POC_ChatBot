from backend.query_engine import QueryEngine

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
STATE_END = "END"

class DialogManager:
    def __init__(self):
        self.engine = QueryEngine()

    def handle_turn(self, session, user_input):
        current_state = session.get("state", STATE_GREETING)
        data = session.get("data", {})
        response = ""
        next_state = current_state

        user_input_lower = user_input.lower().strip()

        # --- STATE MACHINE ---

        if current_state == STATE_GREETING:
            # Entry point, user triggers this by connecting or sending anything initially
            response = "Hello 👋 I am your POC Finder Assistant. How may I help you today?"
            next_state = STATE_MENU

        elif current_state == STATE_MENU:
            # We just sent the greeting, now we show options immediately? 
            # Actually, usually the bot sends Greeting AND Menu together or in sequence.
            # But here we are request/response.
            # Let's check if we just moved here.
            
            # If user responds to greeting, we ask the menu question
            response = (
                "Are you looking for a POC based on:\n"
                "1) Location\n"
                "2) Technology\n"
                "3) Feature / Application\n"
                "4) Issue / Support\n"
                "Please type the number or describe your need."
            )
            
            # Logic to parse input if they ALREADY provided it?
            # For simplicity, we assume we just output the menu prompt and wait for next input.
            # But wait, handle_turn expects user_input to Process.
            # If state was GREETING, we ignored input and returned Greeting.
            # But the user sees Greeting, and then types something.
            # So if current is MENU, we process the input.
            
            if user_input: # If this is processing the answer to "How may I help you?"
                # Simple keyword matching or number parsing
                if "1" in user_input or "location" in user_input_lower:
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
                     # Valid menu re-prompt
                     pass 

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
                           "Are you looking for a POC based on: 1) Location 2) Tech 3) Feature 4) Issue"
                next_state = STATE_MENU # Reset to menu parsing
                # Actually if we reset to MENU, we expect next input to be 1/2/3/4. 
                # effectively restarting.

        elif current_state == STATE_END:
            if "yes" in user_input_lower:
                response = (
                    "Are you looking for a POC based on:\n"
                    "1) Location\n"
                    "2) Technology\n"
                    "3) Feature / Application\n"
                    "4) Issue / Support"
                )
                next_state = STATE_MENU # Expect keypress next
                # We need to clear data
                session["data"] = {}
                session.pop("category", None)
            else:
                response = "Goodbye! 👋"
                next_state = STATE_GREETING # Reset for next connect

        # Save session state
        session["state"] = next_state
        session["data"] = data
        return response, next_state
