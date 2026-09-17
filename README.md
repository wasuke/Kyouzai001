# 体験授業 コードライブラリ

高校生向け・全6回のコード配布サイトです。授業の回と教材名を選び、コードをコピーして使います。生徒のログインは不要です。

教員の普段の作業は **授業フォルダに教材ファイルを追加してCommitするだけ**。一覧用JSONやHTMLを編集する必要はありません。

## 最初の公開（1回だけ）

1. GitHubで新しいリポジトリを作ります。無料で公開する場合は公開リポジトリを使います。
2. このフォルダの**中身**をリポジトリのルート（最上位）に配置し、`main` ブランチへCommitします。`github-pages-code-library` フォルダで包まないでください。
3. `.github/workflows/pages.yml` がGitHub上に存在することを確認します。隠しフォルダはファイル選択時に漏れる場合があります。漏れた場合は **Add file → Create new file** で `.github/workflows/pages.yml` を作り、同梱ファイルの内容を貼り付けます。
4. **Settings → Pages → Build and deployment → Source** を **GitHub Actions** にします。
5. **Actions → Publish code library → Run workflow** から `main` を選んで実行します。初回Commit時にPages未設定で失敗した場合も、設定後に再実行してください。
6. Actionsが成功したら、Settings → Pagesに表示されるURLを生徒に案内します。通常は `https://アカウント名.github.io/リポジトリ名/` です。

公開用ブランチが `main` 以外なら、`.github/workflows/pages.yml` の `branches: [main]` を変更します。組織の制限でActionsが無効の場合は管理者による有効化が必要です。

公開方式は[GitHub公式の手順](https://docs.github.com/ja/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)に従っています。PythonはGitHub Actions上で公開時の一覧生成にのみ使用します。公開後はHTML/CSS/JavaScriptだけで動き、サーバー・DB・API・外部CDN・アクセストークンは不要です。

## 教材を追加する

例：第3回に「繰り返し練習」を追加する場合

1. GitHubで `codes/03` を開きます。
2. **Add file → Create new file** を選びます。
3. ファイル名を `02_繰り返し練習.py` とし、本文にコードを貼り付けます。
4. **Commit changes** で `main` に保存します。
5. Actionsが成功すると公開ページが更新されます。生徒側でページを再読み込みしてください。

既存ファイルは **Add file → Upload files** でも追加できます。ブランチ保護を設定している場合は、公開用ブランチにマージした時点で反映されます。

| 授業 | 保存場所 |
|---|---|
| 第1回 | `codes/01/` |
| 第2回 | `codes/02/` |
| 第3回 | `codes/03/` |
| 第4回 | `codes/04/` |
| 第5回 | `codes/05/` |
| 第6回 | `codes/06/` |

### ファイル名のルール

- `01_はじめての出力.py` → 表示名は「はじめての出力」。拡張子と先頭の「数字＋アンダースコアまたはハイフン」は省きます。
- `じゃんけん.py` → 「じゃんけん」。連番なしでも使えます。
- ファイル名の数字順で並びます。`01_`、`02_` のように付けると順序を指定できます。教材名には区別できる名前を付けてください。
- 各回のフォルダ**直下**に保存します。サブフォルダは使いません。
- 文字コードは **UTF-8**、1ファイル1MB以下。インデント・改行は保持し、UTF-8 BOMは除去します。
- 対応拡張子：`.py .js .ts .html .css .txt .json .md .csv .java .c .cpp .h .sql .sh .rb .xml .yaml .yml .svg`。
- `.gitkeep` などドットから始まるファイルは無視します。教材がない回は「準備中」と表示します。
- 未対応形式・文字コード不正・サブフォルダは公開処理がエラーになります。Actionsの「Build static website」を確認してください。失敗時は前回成功したサイトが残ります。

### 更新・削除

GitHubで教材ファイルを編集・削除し、Commitすると自動反映されます。一覧ファイルの修正は不要です。Pythonサンプル7件は動作確認用です。実際の授業内容に差し替えてください。第6回のサンプルは `input()` に対応するPython環境で使います。

## 生徒の使い方

1. 配布URLを開きます。
2. 「授業の回」と「コード名」を選びます。
3. 「コードをコピー」を押して、先生が指定したエディタに貼り付けます。

自動コピーはHTTPS環境で利用します。ブラウザの制限などで失敗した場合は「コードを選択して手動コピー」が表示されます。選択後に `Ctrl+C`（Macは `⌘C`）、または選択範囲のメニューでコピーしてください。教材コードをページ内で実行する機能はありません。HTML教材も文字として表示します。

## 手元で確認する

同梱の `_site/index.html` は生成済みの完成ページです。ブラウザで開いて画面を確認できます。直接ファイルを開いた場合、自動コピーが許可されないことがあります。

教材変更後の再生成にはPython 3.9以上が必要です（外部パッケージ不要）。このフォルダで以下を実行します。

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

生成先は `_site/` です。再生成のたびに置き換わるため直接編集しないでください。公開用HTMLは生成後の `_site/index.html` を使います。リポジトリ直下の `index.html` は生成用テンプレートです。生成結果はGit管理不要です。

必要に応じて手元だけの確認用サーバーも使えます。本番でサーバーを運用する必要はありません。

```sh
python3 -m http.server 8000 --directory _site
```

ブラウザで `http://localhost:8000` を開きます。

## 構成

```text
.github/workflows/pages.yml  Commit時に生成・公開
index.html                  画面のテンプレート
assets/style.css            見た目
assets/app.js               選択・表示・コピー
codes/01/ ～ codes/06/       教員が更新する教材
scripts/build.py            一覧・本文を自動収集
tests/test_build.py          生成処理のテスト
_site/                      生成された静的サイト
  index.html
  assets/materials.js       自動生成された教材一覧・全文
  assets/app.js
  assets/style.css
```

教材一覧と全文を1つのJavaScriptにまとめて読み込むため、教材切り替え時の通信はありません。教材は `textContent` でテキストとして表示します。管理画面やGitHubトークンは含めません。独自のアクセス解析や生徒の入力を収集する処理もありません。

全教材は公開ページに含まれるので、授業回の選択は閲覧制限ではありません。未公開の解答や個人情報は置かないでください。授業前に学校の端末・回線で公開URLの閲覧と貼り付けを確認してください。
