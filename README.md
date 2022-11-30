# insert_gcal
GoogleCalendarAPIで予定を登録



# 1. ライブラリ導入
まずはAPI操作に必要なライブラリを導入します。

```sh
$ pip3 install google-api-python-client google-auth
```



# 2. 事前準備

以下のディレクトリ構成を想定します。

```
insert_gcal
├── key
│   └── project-id-AAAAAAAAAAAAAAAAAAA-BBBBBBBBBBBB.json <- 自身で配置
├── script.py
└── shift.txt <- 適宜作成
```

ソースを準備します。

```sh
git clone https://github.com/otiba30/insert_gcal.git
cd insert_gcal
```



## 2.1. Google Cloud Platform(以下GCP)でAPIの準備

### 2.1.1 GCPプロジェクトを作成
- [GCP公式](https://console.cloud.google.com)

### 2.1.2 Google Calender APIを有効化

1. 左上のナビゲーションメニュー -> "APIとサービス" -> "ライブラリ"
2. 中央の "APIとサービスを検索" と記載された検索窓から "Google Calendar API" と検索し、"有効化"

### 2.1.3 サービスアカウントを作成

1. 左上のナビゲーションメニュー -> "IAMと管理" -> "サービスアカウント"
2. 上の "+ サービスアカウントを作成" -> サービスアカウント名だけ入力(他は不要) -> "完了"

### 2.1.4 サービスアカウントの鍵を作成・配置

1. 左の "サービスアカウント" -> 先程作成したサービスアカウントをクリック -> 上の "キー"
2. "鍵を追加" -> "新しい鍵を作成" -> キーのタイプJSON で "作成"
3. 保存された秘密鍵を keyフォルダに配置する

### 2.1.5 鍵の名前や登録先のGoogleカレンダーアカウントの入力(script.py)

```python script.py
# 予定を接続するGoogle Calenderの設定
scopes = ['https://www.googleapis.com/auth/calendar']
calendar_id = 'XXXXXXXX@gmail.com' <- ここを修正

# JSON鍵を読み込む
key_dir = 'key/project-id-AAAAAAAAAAAAAAAAAAA-BBBBBBBBBBBB.json' <- ここを修正
gapi_creds = google.auth.load_credentials_from_file(key_dir, scopes)[0]
```



## 2.2 登録先のGoogle Calenderと連携設定する
1. Googleカレンダーを開く
2. 左のマイカレンダーの中の登録先となるスケジュールのオーバーフローメニュー -> "設定と共有"
3. GCPの画面左の "サービスアカウント" -> 作成したサービスアカウントをクリック -> メールを確認
4. "特定のユーザーとの共有" -> "+ ユーザーを追加"
5. 先程確認したメールアドレスを入力し 権限を"変更および共有の管理権限" にして送信



## 2.3. シフト表の入力(shift.txt)
2022年12月のシフト表で、2日が日勤で出社、3日が宿直で出社、8日が日勤で在宅の場合は下記のように記述します。

``` shift.txt
2022 12

2 1
3 2
8 3
```



## 2.4. 予定のタイトルや勤務時間の入力(script.py)
シフトのタイトルや勤務時間の編集をします。</br>
日勤が8:30-17:00(8.5時間)、夜勤が16:30-33:30(17時間)の場合は下記のように記述します。

```python script.py
dict_body = {
    1: ['日勤',  8, 30,  8.5],
    2: ['宿直', 16, 30, 17.0],
    3: ['在宅',  8, 30,  8.5]
}
```



# 3. 実行
実行するとGoogleカレンダーに予定が登録されます。

```sh
$ python3 script.py shift.txt
```
