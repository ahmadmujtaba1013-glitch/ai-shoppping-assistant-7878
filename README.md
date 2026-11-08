# 🛍️ AI E-commerce Shopping & Support Assistant

An AI-powered e-commerce assistant built with **Python, FastAPI, and Groq** that helps customers discover products, explore categories, search catalogs, and get relevant product information through natural language conversations.

Instead of relying on traditional keyword-based search, this project uses LLM-powered tool calling to connect AI responses with application-side business logic and product data.

## 🚀 Features

- **AI-Powered Conversations:** Understands natural-language customer queries.
- **Intelligent Product Search:** Search for products using conversational queries.
- **Category Discovery:** Retrieve available product categories.
- **Category-Based Filtering:** Find products belonging to specific categories.
- **LLM Tool Calling:** Dynamically selects and executes application-defined tools.
- **Multi-Round Tool Execution:** Supports multiple tool-calling rounds to handle more complex requests.
- **FastAPI Backend:** Exposes AI functionality through REST API endpoints.
- **Context-Aware Responses:** Generates responses based on retrieved product information.
- **Token Usage Tracking:** Monitors token consumption during model interactions.

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend API framework |
| Groq API | LLM inference |
| GPT-OSS-20B | Language model |
| Pydantic | Data validation |
| REST API | Application communication |

## ⚙️ Architecture

The application follows a tool-calling workflow:

1. A customer submits a natural-language query.
2. FastAPI receives the request.
3. The query is sent to the Groq-hosted language model.
4. The model determines whether an available tool is needed.
5. The backend executes the requested tool.
6. Tool results are returned to the model.
7. The model generates a final response for the customer.

```text
Customer
   |
   v
FastAPI Backend
   |
   v
Groq LLM (GPT-OSS-20B)
   |
   v
Tool Selection
   |
   +----------------------+
   |          |           |
   v          v           v
Categories  Product     Category
             Search      Filtering
   |          |           |
   +----------+-----------+
              |
              v
       Tool Execution
              |
              v
        Tool Results
              |
              v
        Final AI Response
```

## 📦 Project Structure

```text
AI-Ecommerce-Assistant/
│
├── app/
│   ├── main.py
│   └── ...
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

*The structure may vary depending on the current project implementation.*

## 🔧 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

```bash
cd YOUR_REPOSITORY
```

### 2. Install Dependencies

If using `uv`:

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

### 4. Run the Application

```bash
uv run fastapi dev app/main.py
```

### 5. Explore the API

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 💬 Example Queries

Customers can interact with the assistant using natural language:

- "Show me all available categories."
- "Find me a wireless mouse."
- "What products are available under Accessories?"
- "Search for monitors."
- "What products do you have in stock?"

## 🎯 Project Goals

This project explores how LLMs can be integrated into real-world business applications using backend engineering and tool-calling architectures.

The primary focus is on moving beyond simple AI chatbots toward assistants that can interact with business data and execute application-defined operations.

## 🛠️ Future Improvements

- Integrate PostgreSQL for persistent product data.
- Implement advanced product filtering and comparisons.
- Add conversation history and persistent state.
- Introduce LangChain for structured AI orchestration.
- Implement robust validation, testing, and error handling.
- Explore e-commerce platform integrations such as Shopify.
- Add customer support workflows and order-related tools.

## 👨‍💻 Developer

Built as part of my journey toward **AI Backend Engineering and AI Orchestration**.

Currently exploring the intersection of backend development, LLM integrations, tool calling, and production-oriented AI systems.

---

⭐ If you find this project interesting, consider giving the repository a star!
