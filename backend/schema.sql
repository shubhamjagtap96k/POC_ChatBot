-- Database Schema

-- Teams within the organization
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- People/Employees
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT,
    team_id INTEGER,
    email TEXT,
    location TEXT, -- 'India', 'US', 'UK'
    FOREIGN KEY(team_id) REFERENCES teams(id)
);

-- Skills that people can have
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Features/Modules of the application
CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    owning_team_id INTEGER,
    FOREIGN KEY(owning_team_id) REFERENCES teams(id)
);

-- Mapping people to skills (Many-to-Many)
CREATE TABLE IF NOT EXISTS people_skills (
    person_id INTEGER,
    skill_id INTEGER,
    proficiency_level TEXT, -- e.g., 'Expert', 'Intermediate'
    PRIMARY KEY (person_id, skill_id),
    FOREIGN KEY(person_id) REFERENCES people(id),
    FOREIGN KEY(skill_id) REFERENCES skills(id)
);
