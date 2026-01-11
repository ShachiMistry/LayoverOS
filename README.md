<div align="center">
  <br />
    <a href="https://youtu.be/example" target="_blank">
      <img src="https://img.shields.io/badge/Watch_Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch Demo">
    </a>
  <br />
  <br />

  <h1 align="center">LayoverOS</h1>
  <p align="center">
    <strong>The First Context-Aware Operating System for Modern Travel</strong>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/MongoDB-Atlas_Vector_Search-green?style=flat-square&logo=mongodb" />
    <img src="https://img.shields.io/badge/AI-LangGraph_Agents-blue?style=flat-square&logo=python" />
    <img src="https://img.shields.io/badge/LLM-Llama_3_70B-purple?style=flat-square&logo=meta" />
    <img src="https://img.shields.io/badge/Frontend-Next.js_14-black?style=flat-square&logo=next.js" />
  </p>
</div>

---

## 🛑 The Problem: Airports are "Dead Zones"

We spend **4.5 billion hours** annually waiting in airports. 
Currently, the experience is fragmented:
1.  **Static Maps:** Blueprints that don't know who you are or what you like.
2.  **Disconnected Data:** Flight apps tracking planes, Yelp tracking food, but nothing connecting the two.
3.  **Cognitive Load:** Trying to find a quiet spot with an outlet and good coffee in a new terminal is a research project.

Airports shouldn't be valid "waiting rooms." They should be **responsive environments**.

---

## ⚡️ The Solution: LayoverOS

**LayoverOS** is not a chatbot. It is an **Agentic Coordinator** that sits between the traveler and the airport's infrastructure.

It transforms a static location ("I am at SFO") into a dynamic set of actionable opportunities.
*   *"I have 2 hours"* → Agent finds a lounge.
*   *"My flight is delayed"* → Agent suggests a sleeping pod near the new gate.
*   *"I'm hungry"* → Agent filters for open restaurants in *your* terminal, using Vector Search to match your preferences (e.g., "healthy," "fast").

### Key Differentiator: "Context-Aware Action"
Most AI bots answer questions. LayoverOS **takes action**.
Through our **Supervisor Node architecture**, the system detects intent not just to *chat*, but to *transact*.
*   **Example:** A user asking "Can I buy a pass?" triggers the **Bursar Node**, which bypasses the LLM's text output and directly commands the Frontend to render a secure **Payment Modal**. This bridge between *Natural Language Intent* and *React Component Rendering* is the core innovation.

---

## 🏗 Technical Deep Dive

We built a sophisticated **multi-agent system** orchestrated by **LangChain/LangGraph**, using **MongoDB Atlas** as the central nervous system.

### 1. The "Hippocampus": MongoDB Atlas (Vector + Memory)
We utilize MongoDB beyond simple storage. It acts as the shared memory for our agent fleet.

*   **Vector Search (Semantic Retrieval):** 
    *   **Data:** We ingested 160+ real amenity data points from SFO, JFK, and DEN.
    *   **Embeddings:** Used **Voyage AI (`voyage-3-large`)** to generate high-fidelity 1024-dimensional vectors.
    *   **Index:** Configured an Atlas Vector Search index using `cosine` similarity with accurate **Metadata Filtering**.
    *   **Why MongoDB?** Unlike Pinecone, we needed to store the *metadata* (Opening Hours, Terminal ID) right next to the *vectors*. This allowed us to perform **Hybrid Search**—finding "Coffee" (Vector) that is also "Open Now" (Boolean Filter) in a single query.

*   **Graph Checkpointing (Long-Term Memory):** 
    *   Using `MongoDBSaver` with LangGraph, we persist the `AgentState` frame-by-frame.
    *   **Impact:** This enables true **Offline Resilience**. A user can lose cell service in an elevator, reload the page 5 minutes later, and the Agent acts as if no time passed, remembering the exact context.

### 2. The "Cortex": LangGraph & Agent Swarm
We moved beyond simple "prompt engineering" to **Flow Engineering**. The `agent_graph.py` defines a state machine with strict typing:

```python
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    user_location: str   # e.g., "Terminal 2"
    airport_code: str    # e.g., "SFO", "JFK", "DEN"
    flight_number: str   # e.g., "UA400" (Persisted)
    next_step: str
```

*   **🤖 Supervisor Node:** The dispatcher. It uses regex pattern matching (`[A-Z]{2}\d{3}`) and keyword density analysis to route traffic. IF it detects a User changing airports ("I just landed at JFK"), it updates the global `airport_code` state instantly.
*   **🔍 Scout Node:** The researcher. Steps:
    1.  **Concierge Check:** If the query is vague ("I'm hungry"), IT STOPS. It asks clarifying questions ("Which terminal?") to save compute.
    2.  **Vector Lookup:** Queries MongoDB.
    3.  **Synthesis:** Uses Llama 3 to turn raw JSON results into a friendly recommendation.
*   **✈️ Flight Node:** Tracks real-time status. It has "Sticky Memory"—once you mention `UA400`, it remembers it for the rest of the session until you clear it.

### 3. The "Face": Generative UI (Next.js 14)
*   **Aesthetics:** "Glassmorphism" Design System using Tailwind CSS and Framer Motion.
*   **Interactive Blueprint:** Built a custom Scalable Vector Graphic (SVG) map engine. It is not an image; it is a DOM structure. This allows us to programmatically highlight "Gate F12" or "Starbucks" on the map in response to AI events.
*   **Hybrid Rendering:** The chat is **fully streaming**, but critical actions (Payments, Maps) are rendered as **Client Components** triggered by specific tokens (`[PAYMENT_REQUIRED]`) hidden in the AI's response stream.

---

## 🛠 Challenges & Engineering Solutions

### 1. The "Hallucination" Problem
**Challenge:** LLMs love to invent gates that don't exist.
**Solution:** We implemented **Strict RAG (Retrieval Augmented Generation)**. The Scout Node is *forbidden* from answering from its training data. It can ONLY synthesize answers from the `found_items` list returned by MongoDB. If MongoDB returns empty, the Agent says "I don't know," rather than lying.

### 2. The "412 Precondition" Incident
**Challenge:** During stress testing, our primary model (Llama 3.3 70B) began rejecting requests due to provider overload (`412 Precondition Failed`).
**Solution:** We built a **Self-Healing Fallback Mechanism**:
*   The system wraps every LLM call in a `try/catch` block.
*   If the LLM fails (Network/Auth/RateLimit), the system **bypasses the brain** and returns the raw structured data from MongoDB directly to the user.
*   *Result:* The user *always* gets their answer (e.g., list of coffee shops), even if the "personality" of the bot is temporarily offline.

---

## 🚀 How to Run

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   MongoDB Atlas Cluster (M0 or higher)

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file with:
# MONGO_URI=...
# FIREWORKS_API_KEY=...
# VOYAGE_API_KEY=...

python3 api.py
# Server runs on http://localhost:8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Dashboard available at http://localhost:3000
```

---

<div align="center">
  <p>Built with ❤️ for the MongoDB AI Hackathon</p>
</div>
