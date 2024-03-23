# ぬくもりげいすきー新規ユーザー通知

## インフラ
* GCP
  * Cloud Scheduler(毎時起動、Pub/Subのトピック生成)
  * Cloud Pub/Sub
  * Cloud Functions（Pub/Subをトリガーにして起動）

## デプロイ
main.pyの内容をFunctionsのWeb上のエディタに貼り付け、デプロイ
