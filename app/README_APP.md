# AIVA App — How to Run

## Setup
```
pip install -r requirements.txt
cp .env.example .env  # then edit .env with your OpenAI API key
streamlit run app.py
```

## Notes
- The app uses environment variables for secrets.
- Outputs are saved to a local `./outputs` folder for easy export.


## Optional: Enable Firebase Cloud Save (Firestore)
1. Create a Firebase project → enable **Firestore** (Native mode).
2. Create a **Service Account** key (JSON) and download it.
3. Set one of the following env vars in `.env` (or shell):
   - `FIREBASE_CREDENTIALS=/absolute/path/to/service_account.json`
   - **OR** `FIREBASE_CREDENTIALS_JSON='{"type":"service_account", ...}'` (inline JSON)
4. Install deps and run again:
```
pip install -r requirements.txt
streamlit run app.py
```
When connected, the sidebar will show **“Firebase connected”** and the **☁️ Save to Cloud** button will write documents to `aiva_prds` collection.


## Export Options
- **Save Markdown**: writes to `./outputs/<name>.md`
- **Export to DOCX**: creates `./outputs/<name>.docx`
- **Send to Notion** (optional):
  - Set `NOTION_API_KEY` in `.env` (from Notion integration settings)
  - (Optional) Set `NOTION_DATABASE_ID` to file pages under a database
  - Click **"Send to Notion"** in the app

## Optional Auth (Firebase, Email/Password)
- Get **Web API Key** from Firebase console → Project Settings → General → Your Apps
- Put in `.env`: `FIREBASE_API_KEY=<web_api_key>`
- Use the **Auth** section in the sidebar to **Sign Up / Sign In**
- (Advanced) Map `idToken` to your Firestore security rules for per-user docs
