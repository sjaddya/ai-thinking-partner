"""Application constants."""

# Supported habit types - strict domain rules
HABIT_TYPES = [
    "boolean",
    "count",
    "duration",
    "time_of_day",
    "scale",
    "signed_scale",
    "note",
    "timer",
]

# Predefined habit categories
HABIT_CATEGORIES = [
    "General",
    "Health",
    "Fitness",
    "Learning",
    "Work",
    "Personal",
    "Social",
    "Finance",
    "Mindfulness",
    "Lifestyle",
]

# Supported habit frequencies
HABIT_FREQUENCIES = [
    "daily",
    "weekly",
    "custom",
]
