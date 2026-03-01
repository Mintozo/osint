from pathlib import Path
import yaml, json, re

root = Path(".")

(root / "_data").mkdir(exist_ok=True)
(root / "_tools").mkdir(exist_ok=True)
(root / "assets").mkdir(exist_ok=True)
(root / "_layouts").mkdir(exist_ok=True)

# -------------------------
# Create tools.yml if missing
# -------------------------
tools_yml = root / "_data" / "tools.yml"

if not tools_yml.exists():
    tools_yml.write_text("""\
- name: OSINT Framework
  url: https://osintframework.com/
  category: Directory
  tags: [starter, taxonomy]
  pricing: free
  requires_account: false
  data_types: [general]
  notes: "Clickable tree of OSINT resources."
  source: Seed
""", encoding="utf-8")

# -------------------------
# Minimal config
# -------------------------
cfg = root / "_config.yml"
if not cfg.exists():
    cfg.write_text("""\
title: OSINT.Name
description: Marketplace-style OSINT Directory
collections:
  tools:
    output: true
""", encoding="utf-8")

# -------------------------
# Dark Card Layout
# -------------------------
default_layout = root / "_layouts" / "default.html"

default_layout.write_text("""\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ page.title }}</title>
<style>
body {
    background:#0e0e11;
    color:#e6e6e6;
    font-family:Segoe UI, Roboto, sans-serif;
    margin:0;
}
header {
    padding:20px;
    font-size:24px;
    font-weight:600;
    border-bottom:1px solid #222;
}
.container {
    padding:20px;
}
.grid {
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
    gap:20px;
}
.card {
    background:#16161a;
    border:1px solid #26262d;
    border-radius:16px;
    padding:18px;
    transition:0.2s;
}
.card:hover {
    transform:translateY(-4px);
    border-color:#3a3aff;
}
.card h3 {
    margin:0 0 8px 0;
}
.badge {
    display:inline-block;
    padding:4px 10px;
    border-radius:20px;
    font-size:12px;
    margin-right:6px;
}
.free { background:#1f6f3a; }
.paid { background:#7a2d2d; }
.freemium { background:#8a6a1f; }
a { color:#6c8cff; text-decoration:none; }
a:hover { text-decoration:underline; }
</style>
</head>
<body>
<header>OSINT.Name</header>
<div class="container">
{{ content }}
</div>
</body>
</html>
""", encoding="utf-8")

# -------------------------
# Generate pages
# -------------------------
tools = yaml.safe_load(tools_yml.read_text(encoding="utf-8"))

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

search_index = []

for t in tools:
    slug = slugify(t["name"])
    page = root / "_tools" / f"{slug}.md"

    fm = {
        "layout": "default",
        "title": t["name"],
        **t
    }

    content = "---\n"
    content += yaml.safe_dump(fm, sort_keys=False)
    content += "---\n"
    content += f"<div class='card'>"
    content += f"<h3><a href='{t['url']}' target='_blank'>{t['name']}</a></h3>"
    content += f"<p>{t.get('notes','')}</p>"
    content += f"<span class='badge {t['pricing']}'>{t['pricing']}</span>"
    content += "</div>"

    page.write_text(content, encoding="utf-8")

    search_index.append({
        "name": t["name"],
        "category": t["category"],
        "pricing": t["pricing"],
        "notes": t.get("notes", "")
    })

(root / "assets" / "search.json").write_text(
    json.dumps(search_index, indent=2),
    encoding="utf-8"
)

print("Dark marketplace layout generated.")