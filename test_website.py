from services.website_analyzer import (
    analyze_website
)

url = "https://openai.com"

result = analyze_website(url)

print(result)