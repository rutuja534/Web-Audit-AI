# mission_controller.py

from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from agent_tools import scan_website, KNOWN_TRACKER_DOMAINS
from knowledge_base import direct_lookup
# --- THIS IS THE FIX: We are importing the OSINT agent again ---
from specialist_agents import osint_analyst

llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

class MissionController:

    def run_mission(self, url: str) -> str:
        print(f"--- MISSION CONTROLLER: Mission Start! Target: {url} ---")
        
        intel = scan_website(url)
        if not intel["scripts"] and not intel["cookies"]:
            return "Mission Failed: The Field Agent was unable to gather any intelligence."

        all_found_domains = set(intel["scripts"] + intel["cookies"])
        known_threats = {domain for domain in all_found_domains if any(known in domain for known in KNOWN_TRACKER_DOMAINS)}
        unknown_threats = all_found_domains - known_threats
        
        print(f"--- MISSION CONTROLLER: Identified Known Threats: {known_threats} ---")
        print(f"--- MISSION CONTROLLER: Identified Unknown Threats: {unknown_threats} ---")

        # Use the precise, direct lookup for known threats
        known_threat_report = ""
        if known_threats:
            print("--- MISSION CONTROLLER: Performing direct lookup for known threats... ---")
            contextual_reports = [direct_lookup(tracker) for tracker in known_threats]
            known_threat_report = "\n\n".join(contextual_reports)
        
        # Use the OSINT agent for unknown threats
        unknown_threat_report = ""
        if unknown_threats:
            print("--- MISSION CONTROLLER: Tasking OSINT Analyst with unknown threats... ---")
            threat_to_investigate = list(unknown_threats)[0]
            prompt = f"""
            Investigate the domain: '{threat_to_investigate}'.
            What is its primary purpose? Who is the parent company?
            If it is a subdomain (like 'cdn.' or 'static.'), research the main root domain instead.
            Provide a concise, one-paragraph summary.
            """
            investigation_result = osint_analyst.invoke({"input": prompt})
            unknown_threat_report = investigation_result.get('output', f"No information found for {threat_to_investigate}.")

        print("--- MISSION CONTROLLER: Synthesizing final debrief... ---")
        debrief_prompt_template = """
        You are the Mission Controller for the "Web Audit AI" Privacy Intelligence Unit.
        You have received reports from your specialist agents regarding the target website: {url}.
        Your task is to synthesize these reports into a single, final intelligence debrief for a non-technical user.
        Structure the debrief clearly with sections for "Summary of Findings", "Analysis of Known Trackers", and "Investigation of Unknown Entities".
        Your tone should be professional and informative.
        You MUST base your report ONLY on the context provided by your agents.

        **Analyst's Report on Known Trackers (Context):**
        {known_report}

        **OSINT Analyst's Report on Unknown Entities (Context):**
        {unknown_report}

        ---
        Your Final Intelligence Debrief for {url}:
        """
        debrief_prompt = ChatPromptTemplate.from_template(debrief_prompt_template)
        final_chain = debrief_prompt | llm
        final_debrief = final_chain.invoke({
            "url": url,
            "known_report": known_threat_report or "No known trackers were found in our database.",
            "unknown_report": unknown_threat_report or "No unknown entities were designated for investigation."
        })

        return final_debrief.content