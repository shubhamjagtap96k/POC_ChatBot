import re

class LLMService:
    def __init__(self):
        # In a real app, you would initialize OpenAI client here
        pass

    def get_intent(self, user_query):
        """
        Mock LLM logic to extract intent and entities from user query.
        Returns a dict: {'intent': str, 'entity': str, 'entity_type': str}
        """
        user_query = user_query.lower()
        
        # 1. Who owns Feature X?
        # Regex: who owns (.*)
        match = re.search(r"who owns (.*)", user_query)
        if match:
            feature_name = match.group(1).strip("? ")
            return {
                "intent": "find_feature_owner",
                "entity": feature_name,
                "entity_type": "feature"
            }

        # 2. Who is expert in Skill Y? / Who knows Skill Y?
        # Regex: who (is expert in|knows) (.*)
        match = re.search(r"who (?:is expert in|knows) (.*)", user_query)
        if match:
            skill_name = match.group(1).strip("? ")
            return {
                "intent": "find_expert",
                "entity": skill_name,
                "entity_type": "skill"
            }
            
        # 3. Which team handles Module Z?
        # Regex: which team handles (.*)
        match = re.search(r"which team (?:handles|owns) (.*)", user_query)
        if match:
            module_name = match.group(1).strip("? ")
            return {
                "intent": "find_team_for_module",
                "entity": module_name,
                "entity_type": "feature" # Treating module same as feature for POC
            }

        return {"intent": "unknown", "entity": None, "entity_type": None}

    # --- REAL LLM IMPLEMENTATION (OpenAI) ---
    # To use this: 
    # 1. pip install openai
    # 2. Uncomment the code below
    # 3. Set your OPENAI_API_KEY environment variable
    
    # def get_intent_openai(self, user_query):
    #     from openai import OpenAI
    #     import json
    #     import os
    #
    #     client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    #
    #     system_prompt = """
    #     You are an intent classifier for a banking POC bot.
    #     Your job is to map natural language questions to structured SQL-like intents.
    #     
    #     Intents:
    #     1. find_feature_owner: User asks who owns/manages a feature, module, or system.
    #     2. find_expert: User asks who knows a skill, language, or technology.
    #     3. find_team_for_module: Similar to feature owner, but specific to "which team".
    #
    #     Output JSON format only:
    #     {
    #         "intent": "intent_name",
    #         "entity": "search_term",
    #         "entity_type": "feature|skill"
    #     }
    #
    #     Examples:
    #     - "Who owns the mobile app?" -> {"intent": "find_feature_owner", "entity": "Mobile App", "entity_type": "feature"}
    #     - "Who knows Python?" -> {"intent": "find_expert", "entity": "Python", "entity_type": "skill"}
    #     - "I need a React expert" -> {"intent": "find_expert", "entity": "React", "entity_type": "skill"}
    #     """
    #
    #     try:
    #         response = client.chat.completions.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "system", "content": system_prompt},
    #                 {"role": "user", "content": user_query}
    #             ],
    #             response_format={ "type": "json_object" }
    #         )
    #         return json.loads(response.choices[0].message.content)
    #     except Exception as e:
    #         print(f"LLM Error: {e}")
    #         return {"intent": "unknown", "entity": None}
