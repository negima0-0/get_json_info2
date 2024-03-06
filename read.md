Netmikoを使用して踏み台経由でホストにアクセスする。
またアクセスしたホストには仮でいったんshow configurationを実行する。
アクセスするホストのリストはhosts.csvで提供される。
それぞれの結果はエクセルに追記を行う。
パスワードとユーザ名はconfig.iniから取得する


show hostnameを実行し、対象ホストのホストネームを取得しエクセルに追記できるようにする
# 追記する新しいデータを最終行以降に追加する
max_row = ws.max_row
for i, new_data in enumerate([new_data_list1, new_data_list2, new_data_list3, new_data_list4, new_data_list5], start=1):
    col = ws.cell(row=max_row + 1, column=i)
    for value in new_data:
        col.value = value
        col = ws.cell(row=col.row + 1, column=i)
