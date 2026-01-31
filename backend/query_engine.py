from backend.database import execute_query

class QueryEngine:
    def run_query(self, intent_data):
        intent = intent_data.get("intent")
        entity = intent_data.get("entity")

        if intent == "find_feature_owner" or intent == "find_team_for_module":
            # Find feature by name (case-insensitive search)
            sql = """
                SELECT f.name as feature, t.name as team, t.description as team_desc, p.name as team_lead, p.email
                FROM features f
                JOIN teams t ON f.owning_team_id = t.id
                LEFT JOIN people p ON p.team_id = t.id AND p.role LIKE '%Lead%'
                WHERE f.name LIKE ?
            """
            results = execute_query(sql, (f"%{entity}%",))
            if not results:
                return f"I couldn't find a feature named '{entity}'. Parsing is basic in POC mode."
            
            # Format answer
            r = results[0]
            return f"Feature **{r['feature']}** is owned by Team **{r['team']}** ({r['team_desc']}).\nYou should contact **{r['team_lead']}** ({r['email']})."

        elif intent == "find_expert":
            # Find experts in a skill
            sql = """
                SELECT p.name, p.email, ps.proficiency_level, t.name as team
                FROM people p
                JOIN people_skills ps ON p.id = ps.person_id
                JOIN skills s ON ps.skill_id = s.id
                JOIN teams t ON p.team_id = t.id
                WHERE s.name LIKE ?
                ORDER BY ps.proficiency_level DESC
            """
            results = execute_query(sql, (f"%{entity}%",))
            if not results:
                return f"No experts found for skill '{entity}'."

            answer = f"Here are the experts for **{entity}**:\n"
            for r in results:
                answer += f"- **{r['name']}** ({r['proficiency_level']}) from {r['team']} - {r['email']}\n"
            return answer

        else:
            return "I'm not sure how to answer that yet. Try asking 'Who owns Feature X' or 'Who knows Skill Y'."

    def search_poc(self, category, term):
        """
        Structured search based on category and term.
        category: 'Location', 'Technology', 'Feature', 'Issue'
        term: User's input (e.g., 'India', 'React', 'Payments')
        """
        category = category.lower()
        term = f"%{term}%"

        if category == 'location':
            # Find people in a specific location
            sql = """
                SELECT p.name, p.role, p.email, p.location, t.name as team
                FROM people p
                JOIN teams t ON p.team_id = t.id
                WHERE p.location LIKE ?
            """
            results = execute_query(sql, (term,))
            if not results:
                return f"No POCs found in location matching '{term.strip('%')}'. Try 'US', 'UK', or 'India'."
            
            answer = f"Found the following POCs in **{term.strip('%')}**:\n"
            for r in results:
                answer += f"- **{r['name']}** ({r['role']}) - {r['team']} ({r['email']})\n"
            return answer

        elif category == 'technology':
            # Reuse logic for finding experts
            sql = """
                SELECT p.name, p.email, ps.proficiency_level, t.name as team
                FROM people p
                JOIN people_skills ps ON p.id = ps.person_id
                JOIN skills s ON ps.skill_id = s.id
                JOIN teams t ON p.team_id = t.id
                WHERE s.name LIKE ?
                ORDER BY ps.proficiency_level DESC
            """
            results = execute_query(sql, (term,))
            if not results:
                return f"No experts found for technology '{term.strip('%')}'."

            answer = f"Here are the experts for **{term.strip('%')}**:\n"
            for r in results:
                answer += f"- **{r['name']}** ({r['proficiency_level']}) from {r['team']} - {r['email']}\n"
            return answer

        elif category == 'feature' or category == 'issue':
            # Search features (Issue is treated as searching for a feature relevant to the issue)
            sql = """
                SELECT f.name as feature, f.description, t.name as team, p.name as team_lead, p.email
                FROM features f
                JOIN teams t ON f.owning_team_id = t.id
                LEFT JOIN people p ON p.team_id = t.id AND p.role LIKE '%Lead%'
                WHERE f.name LIKE ? OR f.description LIKE ?
            """
            results = execute_query(sql, (term, term))
            if not results:
                return f"No feature or team found matching '{term.strip('%')}'."
            
            r = results[0]
            return f"For **{r['feature']}** ({r['description']}):\nOwner: Team **{r['team']}**\nPOC: **{r['team_lead']}** ({r['email']})"

        return "Invalid category."
