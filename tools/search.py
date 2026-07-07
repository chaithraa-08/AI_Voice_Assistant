from duckduckgo_search import DDGS

def web_search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))

    if not results:
        return "No search results found."

    answer = ""

    for result in results:
        answer += f"{result['title']}\n"
        answer += f"{result['body']}\n\n"

    return answer