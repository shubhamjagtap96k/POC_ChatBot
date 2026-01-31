import sqlite3
import os
import random
from faker import Faker

# Setup
fake = Faker()
DB_FILE = "backend/chatbot.db"
DOCS_DIR = "data/docs"

os.makedirs(DOCS_DIR, exist_ok=True)

def get_db_connection():
    return sqlite3.connect(DB_FILE)

def generate_sql_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Generating SQL Data...")

    # 1. Teams (50 teams)
    teams = []
    departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations', 'Legal', 'Product']
    for _ in range(50):
        dept = random.choice(departments)
        name = f"{dept} - {fake.catch_phrase()}"
        desc = fake.bs()
        try:
            cursor.execute("INSERT INTO teams (name, description) VALUES (?, ?)", (name, desc))
            teams.append(cursor.lastrowid)
        except sqlite3.IntegrityError:
            pass # Skip duplicates

    # 2. People (500 people)
    roles = ['Developer', 'Manager', 'Analyst', 'Architect', 'Consultant', 'Intern', 'Director']
    locations = ['India', 'US', 'UK', 'Canada', 'Germany', 'Australia']
    
    # Get existing team IDs
    cursor.execute("SELECT id FROM teams")
    team_ids = [row[0] for row in cursor.fetchall()]
    
    for _ in range(500):
        name = fake.name()
        role = random.choice(roles)
        team_id = random.choice(team_ids)
        email = f"{name.replace(' ', '.').lower()}@company.com"
        location = random.choice(locations)
        cursor.execute("INSERT INTO people (name, role, team_id, email, location) VALUES (?, ?, ?, ?, ?)", 
                       (name, role, team_id, email, location))
        person_id = cursor.lastrowid

        # Assign Skills (Randomly 1-3 skills per person)
        # Assuming skills already exist from seed.sql, let's add more
        skills = ['Java', 'Python', 'React', 'AWS', 'SQL', 'Kubernetes', 'Docker', 'Go', 'Rust', 'Azure', 'C#', 'Angular']
        
        # Ensure skills exist in DB first (simple check)
        for s in skills:
            try:
                cursor.execute("INSERT INTO skills (name) VALUES (?)", (s,))
            except sqlite3.IntegrityError:
                pass
        
        # Get Skill IDs
        cursor.execute("SELECT id, name FROM skills")
        all_skills = cursor.fetchall()
        
        assigned_skills = random.sample(all_skills, k=random.randint(1, 3))
        for s_id, s_name in assigned_skills:
            level = random.choice(['Expert', 'Intermediate', 'Beginner'])
            cursor.execute("INSERT INTO people_skills (person_id, skill_id, proficiency_level) VALUES (?, ?, ?)",
                           (person_id, s_id, level))

    conn.commit()
    conn.close()
    print("SQL Data Generation Complete.")

def generate_docs():
    print("Generating Document Data...")
    
    topics = {
        "VPN_Troubleshooting": "To reset your VPN, go to vpn.company.com. If error 503 occurs, restart the Cisco AnyConnect client. For macOS users, ensure strict enforcement mode is off.",
        "HR_Leave_Policy": "Employees are entitled to 20 days of paid leave per year. Sick leave requires a medical certificate if exceeding 3 days. Carry forward is limited to 10 days.",
        "IT_Security_Guidelines": "Passwords must be 12 characters long. 2FA is mandatory for all internal portals. Phishing attempts should be reported to security@company.com immediately.",
        "Expense_Reimbursement": "Meals are reimbursed up to $30/day. Travel expenses require prior approval from the Project Manager. Submit receipts via the Expensify portal by the 25th of each month.",
        "Onboarding_Guide": "New joiners must complete the 'Day 1' training on the Learning Portal. ID cards can be collected from the Front Desk on Level 2. Laptop setup takes 2-4 hours.",
        "Remote_Work_policy": "Hybrid work is standard: 3 days in office, 2 days remote. Approval needed for full remote work. Core hours are 10 AM to 4 PM local time.",
    }

    # Generate 50 variations of these docs
    for i in range(50):
        topic = random.choice(list(topics.keys()))
        content = topics[topic]
        # Variation
        content += f"\n\nRef Case ID: {fake.uuid4()}\nUpdated by: {fake.name()}\nDate: {fake.date()}"
        
        filename = f"{DOCS_DIR}/{topic}_{i}.md"
        with open(filename, "w") as f:
            f.write(f"# {topic.replace('_', ' ')}\n\n{content}")
            
    print(f"Generated 50 documents in {DOCS_DIR}")

if __name__ == "__main__":
    generate_sql_data()
    generate_docs()
