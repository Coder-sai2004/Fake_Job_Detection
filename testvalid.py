# test_validator.py

from services.content_validator import validate_content

result = validate_content(
    ":root{ --bg-primary:#0E141B; }"
)

print(result)