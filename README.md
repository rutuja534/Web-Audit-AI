# 🛡️ Web Audit AI: A Multi-Agent System for Privacy Intelligence

Project Web Audit AI is a sophisticated, multi-agent AI system designed to autonomously perform deep privacy audits on live websites. This system mimics a human intelligence task force, dispatching specialized agents to analyze technical trackers, third-party cookies, and investigate unknown domains to generate a holistic, easy-to-understand risk assessment.


## Target Audience & Use Cases

This project is a proof-of-concept for an advanced analysis tool helpful for several key audiences:

*   **Privacy-Conscious Consumers:** Empowers non-technical users to get a clear, understandable summary of how a website is tracking them, moving beyond simple lists to actionable insights.
*   **Journalists & Researchers:** Provides a powerful tool for investigating the data-sharing ecosystems of websites, uncovering hidden third-party relationships for data privacy stories.
*   **Corporate Compliance & Legal Teams:** Offers a starting point for automated audits, helping to verify if a company's marketing and analytics trackers align with its public privacy policy.
*   **Web Developers:** Allows developers to quickly audit their own sites or third-party dependencies to ensure no unexpected or malicious trackers have been introduced.

## Beyond a Simple Scanner: Key Differentiators

While many browser extensions can block trackers, this project demonstrates a far more advanced set of AI engineering capabilities. Existing tools are data presenters; this system is a **knowledge synthesis and judgment engine.**

| Capability | Standard Tracker Blockers | Web Audit AI |
| :--- | :--- | :--- |
| **Handling New Threats** | **Reactive:** Blind to new trackers until a human manually updates their static blocklist. | **Proactive & Dynamic:** The **OSINT Analyst** autonomously investigates unknown domains using live web searches, assessing new threats in real-time. |
| **Output Quality** | **Data Listing:** Shows a list of blocked domains (e.g., `krxd.net`). The user must do their own research. | **Insight Generation:** Explains *what* `krxd.net` is (a Salesforce DMP), its purpose, and integrates this into a synthesized, human-readable report. |
| **Core Task** | **Filtering:** Follows a simple, rules-based algorithm to block items on a list. | **Reasoning & Judgment:** Mimics a human research workflow by delegating tasks, analyzing disparate data sources, and forming a final, expert-level conclusion. |
| **Technical Challenge**| Overcoming basic ad-tech. | **Overcoming Adversarial Environments:** Uses Selenium to defeat advanced, enterprise-grade bot-detection systems on major websites. |

## 🚀 Key Features

This project is built on a swarm of collaborating, specialized agents:

*   **Mission Controller:** The central "brain" that receives a target URL and manages the entire audit workflow, delegating tasks and synthesizing the final report.
*   **Field Agent (Selenium-Powered):** The "scout" that navigates live websites, executing JavaScript and overcoming advanced bot-detection systems to reliably gather raw intelligence.
*   **The Analyst (Knowledge-Powered):** The "expert" that uses a direct-lookup mechanism on a custom knowledge base to precisely identify known advertising and analytics trackers.
*   **OSINT Analyst (Agentic Web Search):** The "investigator" that autonomously researches *unknown* domains using the Tavily web search API to assess new threats.

## 🛠️ Tech Stack

| Category | Technology / Library |
| :--- | :--- |
| **Core Language** | Python |
| **AI Framework** | LangChain |
| **Large Language Model** | Groq API (Llama 3) |
| **Web Automation** | Selenium, WebDriver-Manager |
| **HTML Parsing** | BeautifulSoup |
| **Knowledge Base** | Custom Direct-Lookup Engine |
| **Web UI** | Streamlit |

## How to Run This Project Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Your-Repo-Name.git
    cd Your-Repo-Name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API keys:** Create a `.env` file in the root directory and add your keys:
    ```
    GROQ_API_KEY="your_groq_key_here"
    TAVILY_API_KEY="your_tavily_key_here"
    ```

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
