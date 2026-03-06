# AI Investment Intelligence Dashboard

This project is a **data pipeline and analytics dashboard** that analyzes AI-related news to identify which AI topics are receiving the most attention. The system processes news data, calculates topic popularity, and visualizes the results through an interactive dashboard.

The dashboard helps quickly understand **which AI domains are trending or gaining hype in the news ecosystem.**

---

# Project Workflow

The system works in three main steps:

## 1. Data Storage

News data is stored in a **SQLite database**. Each record represents a news article with fields such as:

- Title  
- Description  
- Content  
- Source  
- Publication date  
- URL  

---

## 2. Topic Grouping

Each article is assigned to a **topic cluster** based on its content.  
These clusters group similar news articles together.

Examples of topic labels:

- **topic0**
- **topic1**
- **topic2**
- **topic3**

These topic labels are **automatically generated identifiers** representing groups of related AI news articles.

Example interpretation:

| Topic Label | Possible Meaning |
|--------------|------------------|
| topic0 | AI startups and funding news |
| topic1 | AI tools and technology releases |
| topic2 | AI regulations or policy discussions |
| topic3 | AI research and breakthroughs |

The exact meaning depends on the articles grouped within that cluster.

---

## 3. Hype Score Calculation

The system calculates a **hype score** for each topic using:

```
hype_score = articles_in_topic / total_articles
```

This score represents the **share of news coverage each topic receives**.

- Higher hype score → more media attention  
- Lower hype score → less news coverage  

---

# Dashboard

The dashboard is built using **FastAPI, Plotly, and Jinja Templates**.

It displays a **bar chart of AI topic hype scores**, showing:

- **X-axis:** Topic cluster (topic0, topic1, etc.)
- **Y-axis:** Hype score

This visualization allows users to quickly identify:

- Which AI topics dominate news coverage
- Which topics are emerging trends
- Relative popularity of different AI themes

---

# Dashboard Features

- Interactive chart
- Lightweight FastAPI backend
- Automatically updates when database changes
- Public deployment using Render

---

# Live Dashboard

https://ai-investment-intelligence-1.onrender.com/

---

# Tech Stack

- Python
- FastAPI
- Pandas
- Plotly
- SQLite
- Jinja2
- Render (Deployment)

---

# Note

Topic labels such as **topic0, topic1, topic2** are automatically generated clusters.  
They represent groups of similar AI news articles rather than predefined categories.
