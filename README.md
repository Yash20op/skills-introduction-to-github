# Introduction to GitHub

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey Yash20op!

Mona here. I'm done preparing your exercise. Hope you enjoy! 💚

Remember, it's self-paced so feel free to take a break! ☕️

[![](https://img.shields.io/badge/Go%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/Yash20op/skills-introduction-to-github/issues/1)

---

## 📝 Blog Automation Workflow

This repository includes a GitHub Actions workflow that **automatically publishes blog posts to Google Blogger** whenever Markdown files are pushed to the `posts/` directory.

### How It Works

1. Write a blog post as a Markdown file in the `posts/` directory.
2. Add YAML front-matter with a `title` and optional `labels` and `draft` fields (see `posts/_template.md`).
3. Commit and push to the `main` branch.
4. The **Publish Blog Post to Blogger** workflow automatically converts the Markdown to HTML and publishes it via the [Blogger API v3](https://developers.google.com/blogger/docs/3.0/getting_started).

You can also trigger the workflow manually from the **Actions** tab using the `workflow_dispatch` event.

### Setup

1. **Create a Google API OAuth 2.0 credential** with the Blogger API enabled in the [Google Cloud Console](https://console.cloud.google.com/).
2. **Find your Blogger Blog ID** – open your blog in Blogger, and the numeric ID is in the URL.
3. **Add repository secrets** in **Settings → Secrets and variables → Actions**:
   | Secret Name | Description |
   |---|---|
   | `BLOGGER_BLOG_ID` | Your Blogger blog's numeric ID |
   | `BLOGGER_API_KEY` | An OAuth 2.0 access token for the Blogger API |

### Post Format

```markdown
---
title: "My Blog Post Title"
labels:
  - tag1
  - tag2
draft: false
---

Your blog content in **Markdown** goes here.
```

| Front-Matter Field | Required | Description |
|---|---|---|
| `title` | ✅ | The title of the blog post |
| `labels` | ❌ | A list of tags/categories |
| `draft` | ❌ | Set to `true` to create as draft (default: `false`) |

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

