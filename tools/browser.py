import webbrowser


WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chat.openai.com"
}


def browser_execute(action, parameters):

    action = action.lower()

    try:

        if action == "open":

            website = parameters.get("website", "").lower()

            if website in WEBSITES:
                webbrowser.open(WEBSITES[website])
                return f"Opened {website}."

            # If a full URL is provided
            url = parameters.get("url")
            if url:
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
                webbrowser.open(url)
                return f"Opened {url}"

            # Automatically construct URL
            if website:
                url = f"https://www.{website}.com"
                webbrowser.open(url)
                return f"Opened {website}."

            return "Website not specified."

        elif action == "search":

            query = parameters.get("query")

            if not query:
                return "Search query missing."

            webbrowser.open(
                f"https://www.google.com/search?q={query}"
            )

            return f"Searching Google for '{query}'."

        else:
            return "Unsupported browser action."

    except Exception as e:
        return str(e)