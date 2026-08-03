#!/usr/bin/env python3
"""
凪AI サイト - ブログビルドスクリプト

blog/_source/*.md を読み込み、blog/posts/*.html と blog/index.html を生成します。
トップページ(index.html)の「最新記事」3件(BLOG_LATEST:START〜END間)も同時に更新します。

使い方:
    python scripts/build_blog.py

記事を追加する場合:
    1. blog/_source/ に「YYYY-MM-DD-半角英数のスラッグ.md」という名前でファイルを作成する
    2. ファイル先頭に以下の形式でfrontmatterを書く

       ---
       title: 記事タイトル
       date: 2026-08-15
       tag: タグ名
       excerpt: 一覧に表示される概要文
       ---

       ここから本文（## 見出し2 / ### 見出し3 / - 箇条書き / > 引用 / **強調** に対応）

    3. このスクリプトを実行する
"""
import html as html_lib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "blog" / "_source"
POSTS_DIR = ROOT / "blog" / "posts"
BLOG_INDEX = ROOT / "blog" / "index.html"
SITE_INDEX = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"

BASE_URL = "https://solederlego8-a11y.github.io/nagi-ai-hp/"

STATIC_PAGES = ["", "company.html", "service.html", "case.html", "contact.html"]

NAV_LINKS = [
    ("company.html", "会社概要"),
    ("service.html", "サービス"),
    ("case.html", "導入事例"),
    ("blog/index.html", "ブログ"),
    ("contact.html", "お問い合わせ"),
]


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        raise ValueError("frontmatterが見つかりません（--- で始まり --- で終わる形式にしてください）")
    fm_raw, body = m.group(1), m.group(2)
    meta = {}
    for line in fm_raw.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body.strip()


def inline_md(text):
    text = html_lib.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def markdown_to_html(body):
    html_parts = []
    list_buffer = []
    para_buffer = []

    def flush_para():
        if para_buffer:
            html_parts.append("<p>" + inline_md(" ".join(para_buffer)) + "</p>")
            para_buffer.clear()

    def flush_list():
        if list_buffer:
            items = "".join("<li>" + inline_md(i) + "</li>" for i in list_buffer)
            html_parts.append("<ul>" + items + "</ul>")
            list_buffer.clear()

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            flush_para()
            flush_list()
            continue
        if line.startswith("### "):
            flush_para(); flush_list()
            html_parts.append("<h3>" + inline_md(line[4:]) + "</h3>")
        elif line.startswith("## "):
            flush_para(); flush_list()
            html_parts.append("<h2>" + inline_md(line[3:]) + "</h2>")
        elif line.startswith("> "):
            flush_para(); flush_list()
            html_parts.append("<blockquote>" + inline_md(line[2:]) + "</blockquote>")
        elif line.startswith("- "):
            flush_para()
            list_buffer.append(line[2:])
        else:
            flush_list()
            para_buffer.append(line.strip())

    flush_para()
    flush_list()
    return "\n      ".join(html_parts)


def nav_html(prefix, active_href):
    items = []
    for href, label in NAV_LINKS:
        active = ' class="is-active"' if href == active_href else ""
        items.append(f'<a href="{prefix}{href}"{active}>{label}</a>')
    return "\n      ".join(items)


def page_shell(prefix, title, description, active_href, body_html, canonical_path, extra_head=""):
    canonical_url = BASE_URL + canonical_path
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical_url}">
<link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:locale" content="ja_JP">
<meta property="og:site_name" content="凪AI（NAGI AI Consulting）">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical_url}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
{extra_head}</head>
<body>

<header class="site-header">
  <div class="container">
    <a href="{prefix}index.html" class="brand">
      <span class="brand-mark" aria-hidden="true"></span>
      <span>凪AI<small>NAGI AI CONSULTING</small></span>
    </a>
    <nav class="nav-primary" aria-label="グローバルナビゲーション">
      {nav_html(prefix, active_href)}
    </nav>
    <div class="nav-cta">
      <a href="{prefix}contact.html#form" class="btn btn-ghost btn-sm">資料請求</a>
      <a href="{prefix}contact.html#form" class="btn btn-primary btn-sm">無料相談</a>
    </div>
    <button class="nav-toggle" aria-label="メニューを開く"><span></span></button>
  </div>
</header>

{body_html}

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="{prefix}index.html" class="brand" style="color:#fff;">
          <span class="brand-mark" aria-hidden="true"></span>
          <span>凪AI<small style="color:rgba(217,221,230,0.7)">NAGI AI CONSULTING</small></span>
        </a>
        <p style="font-size:13px;color:rgba(217,221,230,0.75);margin-top:16px;max-width:280px;">
          Claude Codeの法人導入を、研修・伴走コンサルティング・業務エージェント開発から支援します。
        </p>
      </div>
      <div>
        <h4>サービス</h4>
        <ul>
          <li><a href="{prefix}service.html#consulting">導入伴走コンサルティング</a></li>
          <li><a href="{prefix}service.html#training">Claude Code 実務研修</a></li>
          <li><a href="{prefix}service.html#agent">業務エージェント開発</a></li>
          <li><a href="{prefix}service.html#governance">ガバナンス設計</a></li>
        </ul>
      </div>
      <div>
        <h4>会社情報</h4>
        <ul>
          <li><a href="{prefix}company.html">会社概要</a></li>
          <li><a href="{prefix}case.html">導入事例</a></li>
          <li><a href="{prefix}blog/index.html">ブログ</a></li>
          <li><a href="{prefix}contact.html">お問い合わせ</a></li>
        </ul>
      </div>
      <div>
        <h4>お問い合わせ</h4>
        <ul>
          <li><a href="{prefix}contact.html#form">無料相談を予約する</a></li>
          <li><a href="{prefix}contact.html#form">資料請求する</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 NAGI AI Consulting Inc.（架空のサンプル企業）</span>
      <span><a href="#">プライバシーポリシー</a></span>
    </div>
  </div>
</footer>

<script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""


def load_posts():
    posts = []
    for md_file in sorted(SOURCE_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        required = ["title", "date", "tag", "excerpt"]
        missing = [k for k in required if k not in meta]
        if missing:
            print(f"[警告] {md_file.name}: frontmatterに {missing} がありません。スキップします。")
            continue
        posts.append({
            "slug": md_file.stem,
            "title": meta["title"],
            "date": meta["date"],
            "tag": meta["tag"],
            "excerpt": meta["excerpt"],
            "content_html": markdown_to_html(body),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def post_card_html(post, link_prefix, indent="      "):
    date_disp = post["date"].replace("-", ".")
    return (
        f'{indent}<div class="post-card">\n'
        f'{indent}  <div class="post-meta"><span>{date_disp}</span><span class="tag">{html_lib.escape(post["tag"])}</span></div>\n'
        f'{indent}  <h3>{html_lib.escape(post["title"])}</h3>\n'
        f'{indent}  <p>{html_lib.escape(post["excerpt"])}</p>\n'
        f'{indent}  <a href="{link_prefix}{post["slug"]}.html" class="card-link">記事を読む →</a>\n'
        f'{indent}</div>'
    )


def build_post_pages(posts):
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    for post in posts:
        date_disp = post["date"].replace("-", ".")
        body_html = f"""<div class="post-hero">
  <div class="container">
    <div class="post-meta"><span>{date_disp}</span><span class="tag">{html_lib.escape(post["tag"])}</span></div>
    <h1>{html_lib.escape(post["title"])}</h1>
  </div>
</div>
<section>
  <div class="container">
    <div class="post-body">
      {post["content_html"]}
      <p style="margin-top:48px;"><a href="../index.html" class="btn btn-ghost">← ブログ一覧に戻る</a></p>
    </div>
  </div>
</section>"""
        ld_data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post["title"],
            "datePublished": post["date"],
            "description": post["excerpt"],
            "author": {"@type": "Organization", "name": "凪AI（NAGI AI Consulting）"},
            "publisher": {"@type": "Organization", "name": "凪AI（NAGI AI Consulting）"},
        }
        json_ld = (
            '<script type="application/ld+json">\n'
            + json.dumps(ld_data, ensure_ascii=False, indent=2).replace("</", "<\\/")
            + "\n</script>\n"
        )
        page = page_shell(
            prefix="../../",
            title=f'{post["title"]}｜凪AI ブログ',
            description=post["excerpt"],
            active_href="blog/index.html",
            body_html=body_html,
            canonical_path=f'blog/posts/{post["slug"]}.html',
            extra_head=json_ld,
        )
        out_path = POSTS_DIR / f'{post["slug"]}.html'
        out_path.write_text(page, encoding="utf-8")
        print(f"生成: {out_path.relative_to(ROOT)}")


def build_blog_index(posts):
    cards = "\n".join(post_card_html(p, link_prefix="posts/") for p in posts)
    body_html = f"""<div class="page-header">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">TOP</a> ／ ブログ</div>
    <span class="eyebrow">BLOG</span>
    <h1>ブログ</h1>
    <p>Claude Codeの法人導入・業務自動化に関する実践ノウハウを継続的にお届けします。</p>
  </div>
</div>
<section>
  <div class="container">
    <div class="blog-grid">
{cards}
    </div>
  </div>
</section>"""
    page = page_shell(
        prefix="../",
        title="ブログ｜凪AI - NAGI AI Consulting",
        description="Claude Codeの法人導入・業務自動化に関する実践ノウハウをお届けするブログです。",
        active_href="blog/index.html",
        body_html=body_html,
        canonical_path="blog/index.html",
    )
    BLOG_INDEX.write_text(page, encoding="utf-8")
    print(f"生成: {BLOG_INDEX.relative_to(ROOT)}")


def update_homepage_latest(posts, count=3):
    latest = posts[:count]
    cards = "\n".join(post_card_html(p, link_prefix="blog/posts/") for p in latest)
    replacement = "\n" + cards + "\n      "
    site_html = SITE_INDEX.read_text(encoding="utf-8")
    new_html, n = re.subn(
        r"(<!-- BLOG_LATEST:START.*?-->)(.*?)(<!-- BLOG_LATEST:END -->)",
        lambda m: m.group(1) + replacement + m.group(3),
        site_html,
        flags=re.S,
    )
    if n == 0:
        print("[警告] index.html内に BLOG_LATEST:START/END マーカーが見つかりませんでした。トップページの最新記事は更新されていません。")
        return
    SITE_INDEX.write_text(new_html, encoding="utf-8")
    print("更新: index.html（最新記事3件）")


def build_sitemap(posts):
    urls = [BASE_URL + p for p in STATIC_PAGES]
    urls.append(BASE_URL + "blog/index.html")
    urls.extend(BASE_URL + f'blog/posts/{p["slug"]}.html' for p in posts)
    lastmod = {p["slug"]: p["date"] for p in posts}
    today = max([p["date"] for p in posts], default="")

    entries = []
    for url in urls:
        if "blog/posts/" in url:
            slug = url.rsplit("/", 1)[-1].removesuffix(".html")
            lm = lastmod.get(slug, today)
        else:
            lm = today
        entries.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lm}</lastmod>\n  </url>")

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    SITEMAP.write_text(xml, encoding="utf-8")
    print(f"生成: {SITEMAP.relative_to(ROOT)}")


def main():
    posts = load_posts()
    if not posts:
        print("記事が見つかりませんでした。blog/_source/ にMarkdownファイルを追加してください。")
        return
    build_post_pages(posts)
    build_blog_index(posts)
    update_homepage_latest(posts)
    build_sitemap(posts)
    print(f"\n完了: {len(posts)}件の記事を反映しました。")


if __name__ == "__main__":
    main()
