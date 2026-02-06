from questions import BotText

def calculate_score(answers):
    """
    Analyzes user profile and returns the specific archetype message + scores.
    """
    
    # Extract Answers
    field = answers.get("q_field", "")
    stage = answers.get("q_stage", "")
    team = answers.get("q_team", "")
    cash = answers.get("q_cash", "")
    lang = answers.get("q_eng", "")
    
    messages = []
    
    # --- منطق تشخیص تیپ شخصیتی (Archetype Logic) ---

    # --- منطق تشخیص تیپ شخصیتی (Archetype Logic) ---

    # 1. تیپ "سرمایه گذار / PNP" (> 70k USD)
    if cash == "high": # > 70k
        main_message = BotText.RESULT_INVESTOR
        scores = {"CA": 95, "UAE": 85, "DK": 40, "FI": 10}
        
    # 2. تیپ "نخبگان آمریکا" (50k-100k + Fluent + Tech/Science)
    elif cash == "high_mid" and lang == "fluent" and field == "tech":
        main_message = BotText.RESULT_USA_ELITE
        scores = {"US": 98, "CA": 80, "NL": 70, "DK": 70}

    # 3. تیپ "اسکاندیناوی / اروپا" (20k - 50k)
    elif cash == "mid":
        # Good budget for Finland/Denmark startup visas
        main_message = BotText.RESULT_SOLO_FIGHTER
        scores = {"FI": 90, "DK": 90, "NL": 80, "CA": 30}

    # 4. تیپ "بودجه کم" (< 20k)
    elif cash == "low":
        main_message = BotText.RESULT_NOT_READY
        scores = {"UAE": 40, "UK": 30, "FI": 10, "CA": 0}

    # 5. حالت پیشفرض (Default)
    else:
        main_message = (
            "🔍 **نتیجه تحلیل:**\n"
            "شرایطت بینابینه. با این بودجه و شرایط، باید دقیق‌تر بررسی بشه.\n"
            "پیشنهاد میکنم تحلیل دقیق (۲۰ سوالی) رو انجام بدی."
        )
        scores = {"NL": 50, "FI": 50, "DK": 50}

    return scores, [main_message]

def format_results(scores, messages):
    """
    Returns a markdown string for the results.
    """
    # Simply return the main archetype message, followed by scores if needed, 
    # but the prompt emphasis is on the "Message" more than scores now.
    
    text = messages[0] + "\n\n"
    
    # Add small score summary at bottom
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    text += "📊 **امتیازهای تخمینی:**\n"
    for country, score in sorted_scores:
        if score > 0:
            text += f"{country}: {score}% | "
            
    return text
