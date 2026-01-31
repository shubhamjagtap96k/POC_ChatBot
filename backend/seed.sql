-- Seed Data

-- Teams
INSERT INTO teams (name, description) VALUES 
('Core Banking', 'Handles core transaction ledger and accounts'),
('Mobile App', 'Responsible for iOS and Android retail banking apps'),
('Data Analytics', 'Enterprise data warehousing and reporting'),
('Security Ops', 'Identity management and fraud detection');

-- People
INSERT INTO people (name, role, team_id, email, location) VALUES
('Alice Johnson', 'Tech Lead', 1, 'alice.j@bank.com', 'US'),
('Bob Smith', 'Senior Developer', 2, 'bob.s@bank.com', 'UK'),
('Charlie Dat', 'Data Engineer', 3, 'charlie.d@bank.com', 'India'),
('Diana Sec', 'Security Architect', 4, 'diana.s@bank.com', 'India'),
('Eve Front', 'Frontend Dev', 2, 'eve.f@bank.com', 'US');

-- Skills
INSERT INTO skills (name) VALUES 
('Java'), ('Python'), ('React'), ('AWS'), ('SQL'), ('Kubernetes');

-- Features
INSERT INTO features (name, description, owning_team_id) VALUES
('Ledger System', 'The main book of record for transactions', 1),
('Mobile Login', 'Biometric authentication flow', 2),
('Bill Pay', 'Utility payment module', 2),
('Fraud Alerting', 'Real-time transaction monitoring', 4),
('Regulatory Reporting', 'Daily reports to central bank', 3);

-- People Skills
-- Alice knows Java and AWS
INSERT INTO people_skills (person_id, skill_id, proficiency_level) VALUES 
(1, 1, 'Expert'), (1, 4, 'Intermediate');

-- Bob knows React and Python
INSERT INTO people_skills (person_id, skill_id, proficiency_level) VALUES
(2, 3, 'Expert'), (2, 2, 'Intermediate');

-- Charlie knows SQL and Python
INSERT INTO people_skills (person_id, skill_id, proficiency_level) VALUES
(3, 5, 'Expert'), (3, 2, 'Expert');

-- Diana knows Kubernetes and Security (Not a skill enum, but implied role)
INSERT INTO people_skills (person_id, skill_id, proficiency_level) VALUES
(4, 6, 'Expert');

-- Eve knows React
INSERT INTO people_skills (person_id, skill_id, proficiency_level) VALUES
(5, 3, 'Intermediate');
