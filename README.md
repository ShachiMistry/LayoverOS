## 🚀 Executive Summary
**LayoverOS** is an AI-powered "Airport Operating System" designed to transform valid layover time into a seamless experience. It replaces static airport maps and confusing kiosks with a Context-Aware AI Concierge.

Built for the **MongoDB AI Hackathon**, it leverages **Atlas Vector Search** for retrieval, **Fireworks AI (Llama 3.3)** for complex reasoning, and **LangGraph** for resilient agent orchestration.

**The Problem:** Travelers are stuck with static maps and generic search engines that don't understand "Gate 54" or "45-minute layover."
**The Solution:** A persistent, state-aware agent that dynamically routes queries between "Amenities" and "Flight Logistics."

---

## 🏗️ System Architecture

### 1. The "Brain" (Backend)
* **Framework:** FastAPI + LangGraph.
* **Agent Logic (`agent_graph.py`):**
    * **Supervisor Node:** Uses "Adaptive Intent" to route queries (e.g., "I am at SFO" → Scout Node).
    * **Scout Node:** Uses **Voyage AI** embeddings to search MongoDB `amenities` collection.
    * **Persistence:** `MongoDBSaver` stores conversation state in Atlas, allowing context retention across devices.

### 2. The "Cockpit" (Frontend)
* **Framework:** Next.js 14 (React) with Tailwind CSS.
* **Key Components:**
    * `ChatInterface`: Real-time AI chat with auto-scroll.
    * `TerminalMap`: Interactive SVG map with Pan/Zoom showing live user location.
    * `FlightWidget`: Visual flight status ticker.

### 3. Data & AI Stack
* **Database:** MongoDB Atlas (M0 Sandbox).
* **Vector Search:** Atlas Vector Search (Cosine Similarity).
* **LLM:** Llama 3.3 70B Instruct (via Fireworks AI) for superior reasoning.
* **Embeddings:** Voyage AI.

---

## 🎤 Demo Walkthrough
*Here is how LayoverOS handles real-world traveler scenarios:*

**Scenario A: The "Hungry Traveler" (Vector Search)**
* **User:** "I am at SFO Terminal 2. I need coffee and a place to charge my phone."
* **Agent Action:** Identifies location (SFO T2) and queries the Vector Index using Voyage AI embeddings to find spots that match *both* "charging" and "coffee" semantically.

**Scenario B: The "Anxious Flyer" (Flight Tracking)**
* **User:** "Check status for flight UA400."
* **Agent Action:** Switches context to the `FlightTracker` node, queries the mock `flights` collection in MongoDB, and returns real-time gate/status info.

---

## ✅ Completed Milestones
* **Phase 1: Core Intelligence (DONE):** Successfully implemented agent routing, context switching (SFO/JFK/DEN), and MongoDB state persistence.
* **Phase 2: User Experience (DONE):** Deployed interactive zoomable terminal map and "Concierge Personality" using Llama 3.3.

## 🔮 Future Scope
* **Payments:** Integration with Stripe to buy lounge access directly in-chat.
* **Live GPS:** Browser Geolocation API to replace manual location entry.
* **Multi-Modal AI:** Scanning boarding passes via GPT-4o Vision.
