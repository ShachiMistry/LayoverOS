# LayoverOS ✈️

A "Smart Agent" for airports that works offline and connects to real-time data.

## 1. Setup (First Time Only)
### Backend
1.  Install Python 3.11+.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Important:** Create a `.env` file in this folder with your keys:
    ```env
    MONGO_URI="your_mongodb_connection_string"
    VOYAGE_API_KEY="your_voyage_ai_key"
    FIREWORKS_API_KEY="your_fireworks_key"
    ```

### Frontend
1.  Navigate to the frontend folder:
    ```bash
    cd frontend
    ```
2.  Install packages:
    ```bash
    npm install
    ```

## 2. Running the App
You need **two** terminal windows.

**Terminal 1 (Backend):**
```bash
python3 api.py
```
*Wait until you see "Uvicorn running on http://0.0.0.0:8000"*

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
*Wait until you see "Ready in ... ms"*

## 3. Usage
Open your browser to: [http://localhost:3000](http://localhost:3000)

*   **Plan a Trip:** "Plan a flight from SFO to JFK"
*   **Find Amenities:** "Where is the nearest coffee?" (Works without flight info!)
