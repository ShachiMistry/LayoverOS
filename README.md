# ✈️ LayoverOS

![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas_Vector_Search-green?style=for-the-badge&logo=mongodb&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Orchestration-orange?style=for-the-badge)
![Fireworks AI](https://img.shields.io/badge/Fireworks_AI-Llama_3.3_70B-purple?style=for-the-badge)

> **"Bringing the Concierge Experience to Every Layover."**

**LayoverOS** is a context-aware AI "Airport Operating System" designed to transform dead layover time into a seamless experience. It replaces static airport maps and confusing kiosks with an intelligent agent that knows where you are, when your flight leaves, and where to find the best coffee near your gate.

---

## 🚀 Executive Summary
Built for the **MongoDB AI Hackathon**, LayoverOS leverages **Atlas Vector Search** for retrieval, **Fireworks AI (Llama 3.3)** for complex reasoning, and **LangGraph** for resilient agent orchestration.

* **Problem:** Travelers are stuck with static maps and generic search engines that don't understand "Gate 54" or "45-minute layover."
* **Solution:** A persistent, state-aware agent that dynamically routes queries between "Amenities" and "Flight Logistics."

---

## 🏗️ System Architecture

### 1. The "Brain" (Backend)
* **Framework:** Python FastAPI + LangGraph.
* **Intelligence:** **Llama 3.3 70B Instruct** (via Fireworks AI) for superior reasoning.
* **Agent Logic (`agent_graph.py`):**
    * **Supervisor Node:** Uses "Adaptive Intent" (Regex + LLM) to route queries.
        * *"I am at SFO"* → **Scout Node** (Vector Search).
        * *"Track UA400"* → **Flight Node** (Real-time Status).
    * **Scout Node:** Uses **Voyage AI** embeddings to query the MongoDB `amenities` collection.
    * **Persistence:** `MongoDBSaver` stores conversation state in Atlas, ensuring users can switch devices without losing context.

### 2. The "Cockpit" (Frontend)
* **Framework:** **Next.js 14** (React).
* **Design:** "Sci-Fi / Dark Mode" aesthetic with Tailwind CSS.
* **Key Components:**
    * `ChatInterface`: Real-time AI chat with auto-scroll and "Quick Action" chips.
    * `TerminalMap`: Interactive SVG map with Framer Motion (Pan/Zoom) showing live user location.
    * `FlightWidget`: Visual flight status ticker.

### 3. Data & AI
* **Database:** MongoDB Atlas.
* **Collections:** `amenities` (160+ real items for SFO/DEN/JFK), `flights` (Mock scenario data).
* **Search:** Atlas Vector Search (Cosine Similarity).

---

## 🎤 Demo Script (Walkthrough)
*Use this script to test the capabilities of LayoverOS.*

### Part 1: The "Hungry Traveler" (Vector Search)
**Action:** Type: *"I am at SFO Terminal 2. I need coffee and a place to charge my phone."*
* **Observation:** The agent identifies your location (SFO T2) and queries the Vector Index.
* **Tech:** It uses Voyage AI embeddings to find spots specifically in Terminal 2 that match "charging" and "coffee" semantically, not just by keyword.

### Part 2: The "Anxious Flyer" (Flight Tracking)
**Action:** Type: *"Check status for flight UA400."*
* **Observation:** The agent switches to the `FlightTracker` node, queries the flights collection, and returns status/gate info.
* **Tech:** LangGraph intelligently switches context from "Search" to "Logistics."

### Part 3: The "Power User" (UI Flex)
**Action:** Click the **Maximize Icon** (Top right of chat).
* **Observation:** The interface expands for complex itinerary planning, demonstrating mobile responsiveness.

---

## ✅ Completed Milestones
* **Phase 1: Core Intelligence:**
    * [x] Agent Routing (Distinguishes "Coffee" vs "Flight").
    * [x] Context Switching (Handles SFO, JFK, DEN).
    * [x] Resilience (Degrades gracefully if AI fails).
    * [x] Persistence (Conversation history saved in MongoDB).
* **Phase 2: UX "Wow" Factors:**
    * [x] Interactive Zoomable Terminal Map.
    * [x] "Concierge Personality" (Llama 3.3).

## 🔮 Future Scope
* **Payments Orchestration:** Integration with Stripe to buy lounge access directly in-chat.
* **Live GPS:** Browser Geolocation API to replace manual location entry.
* **Multi-Modal AI:** GPT-4o Vision to parse boarding pass photos.

---

## 🛠️ Installation

### 1. Clone & Install Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
