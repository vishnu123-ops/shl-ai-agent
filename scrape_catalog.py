import json

catalog = [

    {
        "name": "Java 8 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "description": "Assessment for Java programming and object-oriented coding skills.",
        "skills": [
            "java",
            "coding",
            "programming",
            "oop"
        ],
        "test_type": "K"
    },

    {
        "name": "Core Java Entry Level",
        "url": "https://www.shl.com/",
        "description": "Entry-level Java assessment for freshers.",
        "skills": [
            "java",
            "entry",
            "coding"
        ],
        "test_type": "K"
    },

    {
        "name": "Python New",
        "url": "https://www.shl.com/",
        "description": "Assessment for Python programming skills.",
        "skills": [
            "python",
            "coding",
            "automation"
        ],
        "test_type": "K"
    },

    {
        "name": "OPQ32r",
        "url": "https://www.shl.com/",
        "description": "Occupational personality assessment for workplace behavior.",
        "skills": [
            "personality",
            "behavior",
            "communication"
        ],
        "test_type": "P"
    },

    {
        "name": "Agile Software Development",
        "url": "https://www.shl.com/",
        "description": "Assessment for agile software engineering practices.",
        "skills": [
            "agile",
            "software",
            "development"
        ],
        "test_type": "K"
    }
]

with open(
    "data/shl_catalog.json",
    "w"
) as f:

    json.dump(
        catalog,
        f,
        indent=4
    )

print(
    "Catalog saved successfully."
)