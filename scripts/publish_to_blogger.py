"""Publish a Markdown blog post to Google Blogger via the Blogger API v3.

Usage:
    python scripts/publish_to_blogger.py posts/my-post.md

Required environment variables:
    BLOGGER_BLOG_ID  – The numeric ID of the target Blogger blog.
    BLOGGER_API_KEY  – A Google API key with the Blogger API enabled,
                       or an OAuth 2.0 access token.

The Markdown file must contain YAML front-matter with at least a ``title``
field.  Optional front-matter fields:
    labels   – A list of tags/categories for the post.
    draft    – If ``true`` the post is created as a draft (default: false).
"""

import json
import os
import sys

import frontmatter
import markdown
import requests


def load_post(filepath: str) -> dict:
    """Read a Markdown file and return structured post data."""
    post = frontmatter.load(filepath)

    title = post.get("title")
    if not title:
        raise ValueError(f"Post file '{filepath}' is missing a 'title' in front-matter.")

    html_content = markdown.markdown(post.content, extensions=["extra", "codehilite"])

    return {
        "title": title,
        "labels": post.get("labels", []),
        "is_draft": post.get("draft", False),
        "html": html_content,
    }


def publish(post_data: dict, blog_id: str, api_key: str) -> dict:
    """Publish a post to Blogger and return the API response."""
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "kind": "blogger#post",
        "title": post_data["title"],
        "content": post_data["html"],
    }

    if post_data["labels"]:
        body["labels"] = post_data["labels"]

    params = {}
    if post_data["is_draft"]:
        params["isDraft"] = "true"

    response = requests.post(url, headers=headers, json=body, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python publish_to_blogger.py <path-to-post.md>")
        sys.exit(1)

    filepath = sys.argv[1]

    blog_id = os.environ.get("BLOGGER_BLOG_ID")
    api_key = os.environ.get("BLOGGER_API_KEY")

    if not blog_id:
        print("Error: BLOGGER_BLOG_ID environment variable is not set.")
        sys.exit(1)
    if not api_key:
        print("Error: BLOGGER_API_KEY environment variable is not set.")
        sys.exit(1)

    post_data = load_post(filepath)

    print(f"{'Title':<7}: {post_data['title']}")
    print(f"{'Labels':<7}: {', '.join(post_data['labels']) if post_data['labels'] else '(none)'}")
    print(f"{'Draft':<7}: {post_data['is_draft']}")

    result = publish(post_data, blog_id, api_key)

    print(f"Published! Post URL: {result.get('url', '(not available)')}")
    print(f"Post ID: {result.get('id', '(not available)')}")


if __name__ == "__main__":
    main()
