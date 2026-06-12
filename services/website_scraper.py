import requests
from bs4 import BeautifulSoup


def extract_website_content(url):
    """
    Extract title, headings and paragraph text
    from a website homepage.
    """

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = ""

        if soup.title:
            title = soup.title.get_text(strip=True)

        content_parts = []

        # Headings
        for heading in soup.find_all(
            ["h1", "h2", "h3"]
        ):
            text = heading.get_text(
                separator=" ",
                strip=True
            )

            if text:
                content_parts.append(text)

        # Paragraphs
        for paragraph in soup.find_all("p"):
            text = paragraph.get_text(
                separator=" ",
                strip=True
            )

            if text:
                content_parts.append(text)

        content = "\n".join(content_parts)

        # Prevent huge prompts
        content = content[:5000]

        return {
            "status": "success",
            "title": title,
            "content": content
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }