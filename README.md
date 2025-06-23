# 🧠 AI Assistant for Product Managers

A multi-agent AI system built with Google’s Agent Development Kit and Google Cloud, designed to assist product managers in tracking team progress, scheduling, and coordination. Built for the **Agent Development Kit Hackathon with Google Cloud**, this project demonstrates how autonomous agents can collaborate to streamline complex workflows in modern product teams.

---

## 🚀 Why This Project Matters

Product managers today juggle a complex stack of tools, responsibilities, and expectations — from organizing sprints and meetings to gathering progress updates and analyzing team productivity. This system acts as a collaborative **AI assistant**, orchestrating a network of agents to:

* Analyze team calendars
* Monitor task progress
* Suggest optimal meeting times
* Summarize team updates
* Free up human bandwidth

It reduces the friction of manual coordination, enabling PMs to focus on what really matters: building great products.

---

## 🧩 Features

✅ Natural language chat interface powered by ADK agents <br>
✅ Smart meeting suggestions<br>
✅ Team progress tracking with Firebase<br>
✅ Calendar view for context<br>
✅ Dynamic and interactive UI with React<br>

---

## 🧠 Agent Architecture

The system includes:

* **Orchestrator Agent**: Parses user intent and routes requests to relevant agents
* **Calendar Agent**: Reads/write to team calendars via Firestore
* **Task Agent**: Tracks team progress and status of tasks
* **Team Agent**: Retrieves metadata about team members and their availability
* **Project Agent**: Handles project-wide planning and updates

All agents are developed using Google’s Agent Development Kit and communicate via structured Firestore documents.

---

## 🛠️ Tech Stack

* **Frontend**: React.js + Tailwind CSS + Framer Motion + Nivo
* **Backend**: Python + ADK + Firestore + FastAPI (served via Uvicorn)
* **Database**: Firebase Firestore
* **Deployment**: Render + GitHub + Firebase Hosting

---

## 💻 Local Development Setup

### 1. Backend

#### Step 1: Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

#### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Setup environment variables

Create a `.env` file in the root directory:

```env
GOOGLE_APPLICATION_CREDENTIALS=product-manager-devpost-firebase-adminsdk.json
TYPE=service_account
PROJECT_ID=your-project-id
PRIVATE_KEY_ID=your-private-key-id
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=your-service-account-email@your-project-id.iam.gserviceaccount.com
CLIENT_ID=your-client-id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email
UNIVERSE_DOMAIN=googleapis.com
```

#### Step 4: Run backend

```bash
uvicorn app:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🗃️ Folder Structure

```
├ calendar_agent/
│  ├ agent.py
│  └ firestore_mcp.py
├ task_agent/
│  ├ agent.py
│  └ firestore_mcp.py
├ team_agent/
│  ├ agent.py
│  └ firestore_mcp.py
├ project_agent/
│  ├ agent.py
│  └ firestore_mcp.py
├ orchestrator/
│  └ agent.py
├ shared/
│  ├ firestore.py
│  ├ schema.py
│  └ utils.py
├ testing/
│  ├ fill_calendar_script.py
│  └ write_script_to_firestore.py
├ app.py
├ dev_session.py
├ requirements.txt
├ .env
├ frontend/
   ├ components/
   │  ├ ChatPanel.jsx
   │  ├ Schedule.jsx
   │  ├ TeamProgress.jsx
   └ App.js
```

---

## 🌐 Live Demo & Video

🌍 Hosted Site: [https://product-manager-devpost.web.app](https://product-manager-devpost.web.app) <br>
📺 Demo Video: [Coming Soon](#) <br>
📝 Blog Post: [Coming Soon](#) <br>

---

## 🔗 Links

* 💻 GitHub Repository: [https://github.com/ManojBaasha/gcp-gencal-devpost](https://github.com/ManojBaasha/gcp-gencal-devpost)

---

## 📎 About Me

Hey! I'm **Manoj**, a builder passionate about creating applications that simplify lives. I love developing apps and websites, especially for startups, and I'm always looking to connect and explore new opportunities. Let's talk about code, design, or your next big idea.

* [LinkedIn](https://www.linkedin.com/in/manojelango/)
* [GitHub](https://github.com/ManojBaasha)
* [Portfolio](https://therealmanoj.tech)

---

> This submission was created specifically for the [Agent Development Kit Hackathon with Google Cloud]([https://adk.devpost.com](https://googlecloudmultiagents.devpost.com/)).
