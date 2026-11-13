# G20YEA Japan Council ウェブサイト（GitHub Pages版）

https://g20yea.jp/ を GitHub Pages で公開するためのリポジトリです（旧WordPressサイトから移行）。


## 公開手順

1. GitHub のリポジトリ画面 → **Settings → Pages**
2. **Source** を「Deploy from a branch」、Branch を `main`（またはこのブランチ）、フォルダを **`/docs`** にして Save
3. 数分後に `https://wordplugin.github.io/g20yea-japan/` で表示を確認

## 独自ドメイン g20yea.jp を移す場合

1. Settings → Pages → **Custom domain** に `g20yea.jp` を入力して Save（`docs/CNAME` が自動で作られます）
2. ドメインのDNS設定を変更
   - `g20yea.jp`（apex）: A レコード `185.199.108.153` / `185.199.109.153` / `185.199.110.153` / `185.199.111.153`
     （IPv6 も使う場合は AAAA `2606:50c0:8000::153` / `8001::153` / `8002::153` / `8003::153`）
   - `www.g20yea.jp`: CNAME `wordplugin.github.io`
3. DNS 反映後、Pages 設定で **Enforce HTTPS** をオンにする

※ `ask@g20yea.jp` などのメール（MX レコード）は変更しないでください。

## サイトの構成

- `docs/` … 公開されるサイト本体（HTMLは自動生成。直接編集しないでください）
  - `docs/assets/css/site.css` … デザイン（色・文字・レイアウト）
  - `docs/assets/js/site.js` … メニュー開閉・スクロール演出・数字のカウントアップ
  - `docs/wp-content/uploads/` … 画像（旧WordPressから引き継いだ写真とInstagramの写真）
- `scripts/site/build.py` … 全ページを生成するスクリプト
- `scripts/site/members.json` … メンバー・スタッフ・メンバー紹介ページの内容
- `scripts/site/activities.py` … 「最近の活動」ページの内容
- `scripts/check.js` … リンク切れチェック（Playwright）

## 更新方法

1. 内容を変える
   - メンバー・スタッフ：`scripts/site/members.json` を編集（写真は `docs/wp-content/uploads/` に置いてパスを書く）
   - 最近の活動：`scripts/site/activities.py` の `EVENTS` に追記（写真は `docs/wp-content/uploads/instagram/<投稿ID>.jpg`）
   - トップページなどの文章：`scripts/site/build.py` を編集
2. ページを生成する

```
python3 scripts/site/build.py docs
```

3. 生成された `docs/` をコミットして push すると、GitHub Pages に反映されます。

## 旧WordPressからの変更点

- デザインを一新（WordPressテーマ Lightning は使っていません）。URLは旧サイトと同じです
- コメント欄、RSSフィード、WordPress API は廃止
- 入会申し込みフォームは Google フォームの埋め込みなので、そのまま動作します
- 「組織」「G20YEA Summit 2025」ページは旧サイトでも本文が空だったため「準備中」と表示しています
