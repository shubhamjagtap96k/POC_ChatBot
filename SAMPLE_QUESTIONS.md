# Sample Questions to Try

Now that your chatbot is loaded with **Massive Data** and **Knowledge Base** capabilities, here are some questions you can try.

## 1. Finding People (Structured SQL Data)
*Select options 1, 2, or 3 from the main menu.*

### By Location (Option 1)
- **Input**: `India`
- **Input**: `US`
- **Input**: `UK`
- **Input**: `Germany`

### By Technology / Skill (Option 2)
- **Input**: `Java`
- **Input**: `Python`
- **Input**: `React`
- **Input**: `Kubernetes`
- **Input**: `AWS`
- **Input**: `Docker`

### By Feature / App (Option 3)
- **Input**: `Payments`
- **Input**: `Mobile`
- **Input**: `Data Analytics`

## 2. General Knowledge (RAG / Docs)
*Select Option 5 from the main menu.*
*(Requires `chromadb` to be installed manually)*

- **Topic**: `VPN`
    - "How do I fix VPN error 503?"
    - "What is the VPN troubleshooting guide?"
- **Topic**: `HR Policy`
    - "What is the leave policy?"
    - "How many sick days do I get?"
- **Topic**: `Remote Work`
    - "Can I work from home?"
    - "What are the core hours?"
- **Topic**: `Expenses`
    - "What is the meal reimbursement limit?"
    - "How do I submit expenses?"
- **Topic**: `Onboarding`
    - "Where do I collect my ID card?"
    - "How long does laptop setup take?"

## 3. How to Test the Flow
1.  Say **"Hello"** (or just load the page).
2.  Type **"5"** (for Knowledge Base).
3.  Type **"How do I reset my VPN?"**.
4.  See the answer extracted from the `VPN_Troubleshooting_x.md` file!
