# -------------------------------------
# 使い方
#
# 1. Google Cloud Platformでプロジェクト作成
# 2. Google Calender APIを有効化
# 3. サービスアカウント作成
# 4. JSON鍵を作成し、keyフォルダに配置
# 5. 登録先のGoogle Calenderと連携設定する
# 6. シフト表ファイル作成
# 7. このファイルの変数定義を編集
# 8. 下記実行
#    $ python3 ./script.py シフト表ファイル
#
# 例
#
# $ python3 ./script.py shift.txt



import sys
import datetime
import googleapiclient.discovery
import google.auth



# -------------------------------------
# 入力
#

# 参照するシフト表(shift list)
sl      = sys.argv[1]
dict_sl = {}
year    = 0
month   = 0

with open(sl, mode='r') as f:
    lines = f.read().splitlines()

    year, month = map(int, lines.pop(0).split())

    lines.pop(0)

    for i in lines:
        key, value = i.split()
        dict_sl[int(key)] = int(value)
f.close()



# -------------------------------------
# 変数定義
#

# 予定を接続するGoogle Calenderの設定
scopes = ['https://www.googleapis.com/auth/calendar']
calendar_id = 'XXXXXXXX@gmail.com'

# JSON鍵を読み込む
key_dir = 'key/project-id-AAAAAAAAAAAAAAAAAAA-BBBBBBBBBBBB.json'
gapi_creds = google.auth.load_credentials_from_file(key_dir, scopes)[0]

# APIと対話するResourceオブジェクト作成
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)

# シフト番号と内容のマッピング
#   シフト番号: ['タイトル', 開始時, 開始分, 勤務時間]
dict_body = {
    1: ['日勤',  8, 30,  8.5],
    2: ['宿直', 16, 30, 17.0],
    3: ['在宅',  8, 30,  8.5]
}



# -------------------------------------
# 関数定義
#

def insert_gcal(day, shift):

    list  = dict_body[shift]
    title = list[0]
    start = datetime.datetime(year, month, day, list[1], list[2])
    end   = start + datetime.timedelta(hours=list[3])

    body = {
        # 予定のタイトル
        'summary': title,

        # 予定の開始時刻
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'Japan'
        },

        # 予定の終了時刻
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'Japan'
        }
    }

    # APIを通して登録する
    event = service.events().insert(calendarId=calendar_id, body=body).execute()



# -------------------------------------
# 実行
#

def main():

    for k, v in dict_sl.items():
        insert_gcal(k, v)

if __name__ == "__main__":
    main()
