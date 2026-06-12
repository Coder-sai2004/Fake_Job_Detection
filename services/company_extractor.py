# services/company_extractor.py

import re


def extract_company_name(job_description):

    patterns = [
        r"Company:\s*(.*)",
        r"Organization:\s*(.*)",
        r"Employer:\s*(.*)"
    ]

    for pattern in patterns:
        match = re.search(pattern, job_description, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None