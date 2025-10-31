import os, json, requests

NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")

NOTION_VERSION = "2022-06-28"
API_BASE = "https://api.notion.com/v1"

def _headers():
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

def send_markdown_as_page(title: str, markdown: str):
    """
    Creates a page in a database (if NOTION_DATABASE_ID provided) or as a child of workspace.
    Uses paragraph blocks per line for simplicity.
    """
    if not NOTION_API_KEY:
        return False, "Missing NOTION_API_KEY"
    # Build blocks: each non-empty line -> paragraph block
    blocks = []
    for ln in markdown.splitlines():
        if not ln.strip():
            blocks.append({"object": "block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":""}}]}})
        else:
            blocks.append({
                "object":"block",
                "type":"paragraph",
                "paragraph":{"rich_text":[{"type":"text","text":{"content": ln[:1950]}}]}
            })

    payload = None
    if NOTION_DATABASE_ID:
        payload = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Name": {"title": [{"type": "text", "text": {"content": title[:200]}}]}
            },
            "children": blocks[:95]  # Notion limit guard
        }
        url = f"{API_BASE}/pages"
    else:
        # Create a page in the workspace (requires a parent page if available; fallback simple create may fail)
        payload = {
            "parent": {"type":"workspace","workspace": True},
            "properties": {"title": {"title": [{"type":"text","text":{"content": title[:200]}}]}},
            "children": blocks[:95]
        }
        url = f"{API_BASE}/pages"

    resp = requests.post(url, headers=_headers(), data=json.dumps(payload))
    if resp.status_code in (200, 201):
        data = resp.json()
        return True, data.get("id", "Created")
    else:
        try:
            return False, f"Notion error {resp.status_code}: {resp.json()}"
        except Exception:
            return False, f"Notion error {resp.status_code}: {resp.text}"
