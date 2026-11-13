# G20YEA Japan Council ウェブサイト（GitHub Pages版）

https://g20yea.jp/ （WordPress）を静的HTMLに変換し、GitHub Pages で公開するためのリポジトリです。

- `docs/` … 公開されるサイト本体（WordPress から取得した静的HTML・画像・CSS・JS）
- `scripts/` … 変換・検査に使ったスクリプト（公開はされません）

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

## 静的化に伴う変更点

- コメント投稿フォーム、RSS フィード、WordPress API へのリンクは削除（静的サイトでは動作しないため）
- 入会申し込みフォームは Google フォームの埋め込みなので、そのまま動作します
- `?ver=...` 付きのファイル名は GitHub Pages で配信できるよう名前を変更しています

## 更新方法

`docs/` 内の HTML を直接編集してコミットすると、自動で反映されます。

## 「最近の活動」ページ（`docs/activities/`）

公式 Instagram（@g20yea_japan_council）の投稿から作成したページです。
写真は `docs/wp-content/uploads/instagram/` に保存しています。投稿を追加するときは
`scripts/build_activities.py` の `EVENTS` に写真ファイル名・日付・文章を追記し、次を実行してください。

```
python3 scripts/build_activities.py docs
```
