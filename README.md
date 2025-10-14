# 🎓 EduGraph — Knowledge Graph for Education Analytics

EduGraph is a data integration and visualization project that connects **MongoDB Atlas**, **Neo4j Desktop**, and **Redis (Docker)** using Python.  
It enables building a graph-based model for students, skills, and courses — useful for personalized recommendations and relationship insights.

---

## 🚀 Features

- 🔗 **MongoDB Atlas** for structured student and course data  
- 🧩 **Neo4j Desktop** for graph representation (students → skills → courses)  
- ⚡ **Redis (Docker)** for caching results and quick lookups  
- 🧠 **Streamlit** UI for visualization and interaction  
- 🐍 Built using Python and `pymongo`, `neo4j`, and `redis` libraries  

---

## 🧰 Project Structure

```

edugraph/
├── app/
│   ├── db_config.py          # Connection setup for MongoDB, Neo4j, Redis
│   ├── streamlit.py          # Streamlit dashboard app
│   ├── insert_data.py        # Data insertion script (optional)
│   └── requirements.txt      # Project dependencies
└── README.md

````

---

## ⚙️ Prerequisites

### 1️⃣ Install Required Software

| Tool | Version | Purpose |
|------|----------|----------|
| [Python](https://www.python.org/downloads/) | 3.9+ | Base language |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | latest | For Redis container |
| [Neo4j Desktop](https://neo4j.com/download/) | 5.x | Local graph database |
| [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) | Cloud | NoSQL document store |
| [Streamlit](https://streamlit.io/) | latest | Dashboard UI |

---


## 🧱 Database Setup

### 🟢 1. MongoDB Atlas

1. Log into [MongoDB Atlas](https://cloud.mongodb.com/).
2. Create a cluster → click **Connect → Drivers** → copy connection URI:

   ```
   mongodb+srv://<username>:<password>@cluster0.abcd.mongodb.net/?retryWrites=true&w=majority
   ```
3. Replace your credentials in `db_config.py` inside:

   ```python
   mongo_uri = "mongodb+srv://<username>:<password>@cluster0.abcd.mongodb.net/?retryWrites=true&w=majority"
   mongo_db = mongo_client["edugraph"]
   ```

### 🟣 2. Neo4j Desktop

1. Open **Neo4j Desktop** → create & start a local database.
2. Note down:

   * **Bolt URL**: `bolt://localhost:7687`
   * **Username**: usually `neo4j`
   * **Password**: whatever you set
3. Add in `db_config.py`:

   ```python
   neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test123"))
   ```

### 🔴 3. Redis (Docker)

1. Run Redis in Docker:

   ```bash
   docker run -d --name redis-edugraph -p 6379:6379 redis
   ```
2. Test connection:

   ```bash
   docker exec -it redis-edugraph redis-cli ping
   ```

   Should return `PONG`.

---


## 🖥️ Running the Streamlit App

```bash
streamlit run streamlit.py
```

Then open the local URL displayed in your terminal (usually `http://localhost:8501`).

---
