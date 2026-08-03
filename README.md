# 凪AI（NAGI AI Consulting）コーポレートサイト

Claude Code法人導入支援サービスのコーポレートサイトです。
**架空のサンプル企業「凪AI」** として、デジライズ社（https://claudecode.digirise.ai/）とは無関係の
独自ブランド・独自コピー・独自数値で新規に作成しています（社名・実績・代表者名等は一切流用していません）。

**公開URL**: https://solederlego8-a11y.github.io/nagi-ai-hp/
**リポジトリ**: https://github.com/solederlego8-a11y/nagi-ai-hp

## ページ構成

```
nagi_ai_hp/
├── index.html            トップページ
├── company.html          会社概要
├── service.html          サービス詳細（6メニュー）
├── case.html             導入事例一覧
├── contact.html          お問い合わせ・資料請求フォーム
├── contact-thanks.html   送信完了ページ（検索エンジンには非表示）
├── robots.txt            クローラー向け設定
├── sitemap.xml           サイトマップ（自動生成、直接編集しない）
├── blog/
│   ├── index.html         ブログ一覧（自動生成）
│   ├── posts/              記事詳細（自動生成、直接編集しないでください）
│   ├── _source/             記事の原稿（Markdown、自動生成用）
│   └── _template.html       手動で記事を追加する場合のコピー元テンプレート
├── assets/
│   ├── css/style.css      共通デザイン
│   ├── js/main.js         ナビ開閉・FAQアコーディオン
│   └── img/favicon.svg
├── scripts/
│   └── build_blog.py      ブログ生成スクリプト（Markdown→HTML、sitemap更新）
└── README.md
```

## ブログ記事の追加方法（2通り）

### 方法A：Markdown＋自動生成（複数記事をまとめて管理したい場合におすすめ）

1. `blog/_source/` に `YYYY-MM-DD-スラッグ.md` という名前でファイルを作成する
2. ファイル先頭に以下の形式でfrontmatterを書く

   ```
   ---
   title: 記事タイトル
   date: 2026-08-15
   tag: タグ名
   excerpt: 一覧に表示される概要文
   ---

   本文（## 見出し2 / ### 見出し3 / - 箇条書き / > 引用 / **強調** に対応）
   ```

3. 以下を実行する

   ```bash
   python scripts/build_blog.py
   ```

   `blog/posts/*.html`・`blog/index.html`・トップページの「最新記事」3件・`sitemap.xml` がすべて自動更新されます。

### 方法B：HTMLを直接手編集（Pythonを使わず、1本だけサクッと足したい場合）

1. `blog/_template.html` を `blog/posts/YYYY-MM-DD-スラッグ.html` という名前でコピーする
2. コピーしたファイルを開き、`[ ]` で囲まれた部分（タイトル・日付・タグ・概要・本文）をすべて書き換える
3. `blog/index.html` を開き、既存の `<div class="post-card">...</div>` を1つコピーして、新しい記事の情報に書き換えて貼り付ける
4. （任意）目立たせたい場合は `index.html` の `<!-- BLOG_LATEST:START -->` 〜 `<!-- BLOG_LATEST:END -->` の間にも同様のカードを追加する

**注意**：方法Aで生成した記事を方法Bで手編集した場合、次に `build_blog.py` を実行すると `blog/posts/` と `blog/index.html`、トップページの最新記事欄が**自動生成物で上書き**されます。手編集した記事は `blog/_source/` に対応するMarkdownを作らないか、以後スクリプトを実行しない運用にしてください。

## 確認方法（ローカルプレビュー）

このサイトはビルド不要の静的HTMLです。フォルダごとブラウザで開くか、簡易サーバーで確認できます。

```bash
cd nagi_ai_hp
python -m http.server 8000
# → http://localhost:8000/index.html
```

## 公開・更新の反映方法（GitHub Pages）

GitHub Pagesは `main` ブランチの内容をそのまま配信します。変更を公開に反映するには、変更後に以下を実行してpushしてください。

```bash
git add -A
git commit -m "update: 内容更新"
git push
```

push後、数十秒〜数分でhttps://solederlego8-a11y.github.io/nagi-ai-hp/ に反映されます。

## 公開前に必ず編集してほしい箇所（プレースホルダー）

`company.html` 内に実在情報が未入力のプレースホルダーがあります。検索して埋めてください。

- 【要編集：正式法人名】
- 【要編集：設立年月】
- 【要編集：代表者名】
- 【要編集：本社所在地】
- 【要編集：電話番号】／【要編集：メールアドレス】

また、トップページ・事例ページの実績数値（120社+、87%など）はサンプル値です。実際の実績に差し替えてください。

## お問い合わせフォームについて

`contact.html` のフォームは [FormSubmit](https://formsubmit.co/) 経由で **naoren.38@gmail.com 宛に実際にメール送信されます**（サーバー不要・無料）。

- 項目：社名／ご担当者／メールアドレス／問い合わせ内容（以上必須）、電話番号／住所（任意）
- 送信後は `contact-thanks.html` にリダイレクトされます
- **初回のみ**：フォームが最初に送信された際、FormSubmitからnaoren.38@gmail.com宛に確認メールが届きます。メール内の「Activate」リンクをクリックするまで、それ以降の送信内容が転送されません。公開後、必ず一度テスト送信して確認・有効化してください
- スパム対策として簡易的なハニーポット欄（`_honey`）を仕込んでいます

## SEO対応状況

- 全ページに `<title>` / `meta description` / `canonical` / OGP・Twitter Card を設定
- トップページに Organization の構造化データ（JSON-LD）、各ブログ記事に BlogPosting の構造化データを設定
- `robots.txt` と `sitemap.xml` を設置（`sitemap.xml` は `build_blog.py` 実行のたびに自動更新）
- 公開後、[Google Search Console](https://search.google.com/search-console) にサイトを登録し、`sitemap.xml` を送信するとインデックスが早まります（このスクリプトからは実行できないため、ご自身でご登録ください）

## デザインコンセプト

- ブランドカラー：深藍（`--color-navy`）× 凪いだ海の緑青（`--color-teal`）× 夜明けの陽（`--color-amber`）
- ポジショニング：インフルエンサー個人の発信力ではなく「エンジニア出身チームによる、現場に定着する堅実な導入支援」
