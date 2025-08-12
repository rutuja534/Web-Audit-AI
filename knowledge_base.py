# knowledge_base.py

def load_knowledge_base():
    """Loads the trackers.txt file and splits it into individual entries."""
    with open("knowledge/trackers.txt", "r") as f:
        content = f.read()
    entries = content.strip().split('\n\n')
    return entries

KNOWLEDGE_ENTRIES = load_knowledge_base()

def direct_lookup(tracker_domain: str) -> str:
    """
    Performs a direct string search for a tracker in the knowledge base.
    This version is smarter and handles subdomains.
    """
    print(f"--- KNOWLEDGE BASE: Performing direct lookup for '{tracker_domain}'...")
    
    # --- THIS IS THE FIX ---
    # We find the "core" part of the domain to match against our list.
    # e.g., "ssl.google-analytics.com" becomes "google-analytics.com"
    # We split the domain by dots and take the last two parts.
    parts = tracker_domain.split('.')
    # This handles domains like 'google.com' and 'google.co.uk'
    core_domain = '.'.join(parts[-2:])
    if len(parts) > 2 and parts[-2] in ('co', 'com', 'org', 'net'):
         core_domain = '.'.join(parts[-3:])
    
    # A simple override for our specific case
    if "google-analytics.com" in tracker_domain:
        core_domain = "google-analytics.com"
    # ---------------------

    for entry in KNOWLEDGE_ENTRIES:
        # Now we check if the core domain is in the entry
        if core_domain in entry:
            print(f"--- KNOWLEDGE BASE: Found a match for '{core_domain}'!")
            return entry
            
    print(f"--- KNOWLEDGE BASE: No direct match found for '{core_domain}'.")
    return f"No specific information found for '{tracker_domain}' in the knowledge base."