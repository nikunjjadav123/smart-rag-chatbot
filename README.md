# RAG Chatbot – Microservices Architecture

A microservices-based backend system for a **Retrieval-Augmented Generation (RAG) chatbot**, built using **Node.js** and **Python (FastAPI)**.  
Each service is independently developed, deployed, and scaled.

---

## 🧩 Architecture Overview

This project follows a **microservices architecture**, where each service has a single responsibility.

### Services

- **Admin Service (Node.js)**
  - API gateway / admin operations
  - User management, configuration, orchestration
- **RAG Service (Python – FastAPI)**
  - Document ingestion
  - Vector search & retrieval
  - LLM-powered response generation

Services communicate via **HTTP APIs**.

---

## 📁 Project Structure

