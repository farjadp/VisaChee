class BotText:
    WELCOME = (
        "👋 Welcome to the **VisaChee Immigration Assessment Bot**! 🌍\n\n"
        "Let's figure out where you belong. Choose your path:\n\n"
        "⚡️ *Path A: Quick Scan* - Fast, fun, binary choices. (Tinder style)\n"
        "🎮 *Path B: Deep Dive* - Detailed assessment with RPG levels."
    )
    
    CHOOSE_PATH_BUTTONS = {
        "A": "⚡️ Quick Scan",
        "B": "🎮 Deep Dive"
    }

    # --- Path A: Quick Scan ---
    QUICK_QUESTIONS = [
        {
            "id": "q1",
            "text": "💰 **War Chest Check:** Do you have more than $20k USD available for this move?",
            "options": [("Yes", "yes"), ("No", "no")]
        },
        {
            "id": "q2",
            "text": "🚀 **Team Status:** Are you a solo founder or do you have a co-founder?",
            "options": [("Solo", "solo"), ("Team (2+)", "team")]
        },
        {
            "id": "q3",
            "text": "💡 **Idea Type:** Is your business idea highly innovative/tech or more traditional (agency/service)?",
            "options": [("Innovative/Tech", "innovative"), ("Traditional/Service", "traditional")]
        },
        {
            "id": "q4",
            "text": "🎓 **Experience:** Do you have significant management experience or high net worth (> $300k)?",
            "options": [("Yes", "yes"), ("No", "no")]
        },
        {
            "id": "q5",
            "text": "🦄 **Ambition:** You want to scale globally (VC money) or build a lifestyle business?",
            "options": [("Global/VC Scale", "scale"), ("Lifestyle", "lifestyle")]
        }
    ]

    QUICK_RESULT_MATCH = "✅ **It looks like a MATCH!**\nBased on your quick answers, you have potential for our target countries."
    QUICK_RESULT_NO_MATCH = "❌ **Result:**\nIdeally, you need a stronger profile for our primary targets. However, let's talk!"

    # --- Path B: Deep Dive (Levels) ---
    LEVELS = {
        "1": {
            "name": "Level 1: Profile 👤",
            "questions": [
                {
                    "id": "d_1_age",
                    "text": "🎂 **Age:** How young are you at heart (and on paper)?",
                    "options": [("18-35", "low"), ("36-50", "mid"), ("51+", "high")]
                },
                {
                    "id": "d_1_edu",
                    "text": "🎓 **Education:** What's your highest degree?",
                    "options": [("Bachelor's or higher", "high"), ("Below Bachelor's", "low")]
                },
                {
                    "id": "d_1_eng",
                    "text": "🗣️ **English Skills:** Can you pitch to an investor in English?",
                    "options": [("Fluent", "high"), ("Basic", "low")]
                }
            ]
        },
        "2": {
            "name": "Level 2: The Treasure 💎",
            "questions": [
                {
                    "id": "d_2_cash",
                    "text": "💰 **Liquid Cash:** How much capital can you deploy immediately?",
                    "options": [("< $20k", "low"), ("$20k - $50k", "mid"), ("> $50k", "high")]
                },
                {
                    "id": "d_2_nw",
                    "text": "🏦 **Net Worth:** Total assets (Property + Cash + Shares)?",
                    "options": [("< $300k", "low"), ("> $300k", "high")]
                }
            ]
        },
        "3": {
            "name": "Level 3: The Strategy 🗺️",
            "questions": [
                {
                    "id": "d_3_team",
                    "text": "👥 **The Team:** Who is coming with you?",
                    "options": [("Just me (Solo)", "solo"), ("Existing Team", "team")]
                },
                {
                    "id": "d_3_idea",
                    "text": "💡 **The Concept:** Which describes your business best?",
                    "options": [("Software/AI/Tech", "tech"), ("Consulting/Agency", "service"), ("Physical Goods", "goods")]
                }
            ]
        },
        "4": {
            "name": "Level 4: Final Boss 👹",
            "questions": [
                {
                    "id": "d_4_rejection",
                    "text": "🚫 **History:** Have you ever been rejected for a visa in EU/US/CA?",
                    "options": [("Yes", "yes"), ("No", "no")]
                },
                {
                    "id": "d_4_active",
                    "text": "🏢 **Operations:** Is the business already active and making money?",
                    "options": [("Yes", "active"), ("No, Idea Stage", "idea")]
                }
            ]
        }
    }

    CONTACT_ADMIN = "📞 Contact Admin"
    RESTART = "🔄 Restart"
