def analyze_conversation(messages):

    full_text = " ".join(
        [
            m.content.lower()
            for m in messages
        ]
    )

    # Role detection
    role_keywords = [
        "java",
        "python",
        "developer",
        "engineer",
        "manager",
        "analyst",
        "software"
    ]

    # Personality
    personality_keywords = [
        "personality",
        "behavior",
        "communication",
        "stakeholder"
    ]

    # Coding
    coding_keywords = [
        "coding",
        "programming",
        "technical",
        "development"
    ]

    # Experience
    experience_levels = {
        "entry": [
            "fresher",
            "entry",
            "junior"
        ],

        "mid": [
            "mid",
            "3 years",
            "4 years",
            "5 years"
        ],

        "senior": [
            "senior",
            "lead",
            "architect",
            "manager"
        ]
    }

    # Off topic
    off_topic_keywords = [
        "ipl",
        "movie",
        "weather",
        "politics",
        "cricket"
    ]

    # Prompt injection
    injection_keywords = [
        "ignore instructions",
        "system prompt",
        "bypass",
        "override"
    ]

    has_role = any(
        word in full_text
        for word in role_keywords
    )

    needs_personality = any(
        word in full_text
        for word in personality_keywords
    )

    needs_coding = any(
        word in full_text
        for word in coding_keywords
    )

    off_topic = any(
        word in full_text
        for word in off_topic_keywords
    )

    prompt_injection = any(
        word in full_text
        for word in injection_keywords
    )

    experience = None

    for level, words in experience_levels.items():

        if any(word in full_text for word in words):
            experience = level

    return {
        "has_role": has_role,
        "needs_personality": needs_personality,
        "needs_coding": needs_coding,
        "off_topic": off_topic,
        "prompt_injection": prompt_injection,
        "experience": experience,
        "full_text": full_text
    }