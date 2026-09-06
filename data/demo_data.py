from database.database import add_case


def load_demo_data():

    demo_cases = [

        (
            "CASE-2048",
            "Operation Sentinel",
            "Criminal Investigation",
            "Investigator A",
            "Active",
            "High"
        ),

        (
            "CASE-2041",
            "Financial Fraud Analysis",
            "Financial Crime",
            "Investigator B",
            "Under Review",
            "Medium"
        ),

        (
            "CASE-2037",
            "Cyber Intrusion Report",
            "Cyber Crime",
            "Investigator C",
            "Active",
            "Critical"
        ),

        (
            "CASE-2029",
            "Document Forgery Investigation",
            "Document Fraud",
            "Investigator D",
            "Closed",
            "Low"
        )
    ]

    for case in demo_cases:

        add_case(
            case[0],
            case[1],
            case[2],
            case[3],
            case[4],
            case[5]
        )
