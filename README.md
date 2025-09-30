# RepoStory — Instant GitHub Repo Tour

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![Replit](https://img.shields.io/badge/Replit-Live-7f5af0?logo=replit)](https://replit.com/@YOUR_USERNAME/RepoStory)

---

## 🚀 What is RepoStory?

**RepoStory** instantly converts **any public GitHub repository** into a judge-friendly, runnable tour.  

Paste a repo URL and get:

- Quick **run instructions** for Node, Python, or Docker projects  
- **Architecture diagram** (Mermaid.js) for top-level folders & files  
- One-click **“Open in Replit”** link  
- Downloadable **REPO_TOUR.md** file with step-by-step guide  

This ensures judges (or anyone) can understand and run a repo in **under 60 seconds** — perfect for hackathons.

---

## 🎯 Demo

**Live Demo (Replit):** [Open in Replit](https://replit.com/@YOUR_USERNAME/RepoStory)  

**GIF Preview:**  
![Demo GIF](https://via.placeholder.com/600x300.png?text=Paste+repo+URL+→+Analyze+→+Open+in+Replit)  
*(Replace with your actual 60-second demo GIF showing the workflow)*

---

## 🛠 Tech Stack

- **Backend:** Python + Flask  
- **Frontend:** HTML, CSS, JavaScript + Mermaid.js  
- **API:** GitHub API for fetching repo structure  
- **Deployment:** Replit (or any free hosting service)  
- Optional: OpenAI API for AI-generated file explanations  

---

## ⚡ How to Use

1. Run the app locally or open the live Replit link.  
2. Paste a public GitHub repo URL in the input box.  
3. Click **Analyze** → see instructions, architecture diagram, and “Open in Replit” link.  
4. Download `REPO_TOUR.md` if needed.  

**Local Setup Example:**
```bash
git clone https://github.com/YOUR_USERNAME/RepoStory.git
cd RepoStory
pip install -r requirements.txt
python app.py
