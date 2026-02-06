def calculate_score(answers):
    """
    Calculates the eligibility score (0-100) for each country based on user answers.
    
    Targets:
    - NL: Netherlands
    - FI: Finland
    - DK: Denmark
    - UAE: United Arab Emirates
    - CA: Canada
    
    Expected 'answers' dictionary keys (from Deep Dive):
    - d_1_age, d_1_edu, d_1_eng
    - d_2_cash, d_2_nw
    - d_3_team, d_3_idea
    - d_4_rejection, d_4_active
    """
    
    # Initialize scores
    scores = {
        "NL": 50, # Netherlands starts neutral
        "FI": 50,
        "DK": 50,
        "UAE": 50,
        "CA": 50
    }

    # Helper to safe get answer
    def get_ans(key):
        return answers.get(key, "")

    # --- 1. PROFILE (Age, Edu, English) ---
    # Age
    age = get_ans("d_1_age")
    if age == "low": # 18-35 (Ideal for most)
        scores["CA"] += 10
        scores["NL"] += 5
    elif age == "high": # 51+ (Harder for points-based)
        scores["CA"] -= 10
    
    # Edu
    edu = get_ans("d_1_edu")
    if edu == "high":
        scores["NL"] += 10
        scores["DK"] += 5
    elif edu == "low":
        scores["DK"] -= 10 # Denmark likes highly skilled

    # English
    eng = get_ans("d_1_eng")
    if eng == "low":
        # Almost all require English
        for country in scores:
            scores[country] -= 20
    
    # --- 2. TREASURE (Cash, Net Worth) ---
    cash = get_ans("d_2_cash")
    nw = get_ans("d_2_nw")

    # UAE & Canada love money
    if cash == "high": # > $50k
        scores["UAE"] += 20
        scores["CA"] += 10
        scores["NL"] += 10 # Good runway
    elif cash == "low": # < $20k
        scores["UAE"] -= 30
        scores["CA"] -= 20
        scores["NL"] -= 10
    
    if nw == "high": # > $300k
        scores["CA"] += 20 # Critical for Canada Angels
        scores["UAE"] += 10
    
    # --- 3. STRATEGY (Team, Idea) ---
    team = get_ans("d_3_team")
    idea = get_ans("d_3_idea")

    # Finland Constraint: TEAM IS MANDATORY
    if team == "solo":
        scores["FI"] = 0
        scores["DK"] -= 10 # Denmark prefers teams
    elif team == "team":
        scores["FI"] += 30 # Huge boost for Finland
        scores["DK"] += 10
    
    # Idea Type
    if idea == "tech":
        scores["DK"] += 20 # Denmark loves tech/innovative
        scores["FI"] += 10
        scores["NL"] += 10
    elif idea == "service": # Consulting/Agency
        scores["DK"] = 0 # Denmark usually rejects traditional
        scores["FI"] -= 20
        scores["NL"] -= 10 # Netherlands prefers innovative
        scores["UAE"] += 10 # UAE is okay with services
    
    # --- 4. FINAL BOSS (History, Active) ---
    rejection = get_ans("d_4_rejection")
    if rejection == "yes":
        # Rejections are bad news generally
        for country in scores:
            scores[country] -= 20
    
    active = get_ans("d_4_active")
    if active == "active":
        scores["NL"] += 20 # Netherlands likes traction
        scores["UK"] = 0 # (Not in target list but good to know)
        scores["UAE"] += 10

    # --- FINAL CLAMP & FORMATTING ---
    for country in scores:
        if scores[country] > 100: scores[country] = 100
        if scores[country] < 0: scores[country] = 0

    return scores

def format_results(scores):
    """
    Returns a markdown string for the results.
    """
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    text = "🎯 **Assessment Results:**\n\n"
    for country, score in sorted_scores:
        bar = "🟩" * (score // 10) + "⬜️" * ((100 - score) // 10)
        text += f"**{country}:** {score}/100\n{bar}\n\n"
    
    text += "ℹ️ *NL=Netherlands, FI=Finland, DK=Denmark, UAE=Dubai, CA=Canada*\n"
    return text
