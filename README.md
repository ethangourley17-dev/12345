<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1PZeAd8WzVS-Z8mPg-_lf0yf_y2BY6lHi

## Run Locally

### Frontend (React/TypeScript)

**Prerequisites:**  Node.js

1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

### Backend (Streamlit/Python)

**Prerequisites:**  Python 3.12+

1. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py --server.port 8501
   ```

4. Open your browser to `http://localhost:8501`

**Note:** The Streamlit app (`app.py`) is a Roof Damage Classifier that integrates with Google Cloud Vertex AI. You'll need to configure your GCP Project ID in the app's sidebar.
