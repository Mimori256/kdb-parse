# kdb-parse
kdbのデータをjsonにする。科目番号、科目名、モジュール、時限、教室、備考がパースされる

## フォーマット
**kdb.csv**
```
"科目番号","科目名","授業方法","単位数","標準履修年次","実施学期","曜時限","教室","担当教員","授業概要","備考","科目等履修生申請可否","申請条件","英語(日本語)科目名","科目コード","要件科目名","データ更新日"
```

**kdb.json**
```
{ "科目番号": ["科目名","モジュール","曜時限","教室","備考","単位数"], ・・・}
```

**kdb_twinc.json**

[TwinC](https://mimori256.github.io/twinc/#/)で使われているデータです。モジュールと曜時限は、二重リストで、その対応を表現しています。
```
例: 春A 木3, 春B 木・金3の場合、 module: [[春A], ["春B"]], period: [[木3], [木3, 金3]]
{"科目番号": {"class_id": "科目番号", "name": "科目名", "module": [["モジュール"]], "period": [["曜時限"]], "room":　"教室", "description": "備考"},
```

**kdb_twinc_en.json**

kdb\_twinc.jsonの科目名を英語の科目名に置き換えたものです。

## 備考
教室が不明の場合は、教室名は空白でパースされます。
今年度開講されない科目はパースされません。
レポジトリ内のCSVとJSONは、GitHub Actionsを使って、一週間おきに自動で更新されます。
過去の年度のデータはoldディレクトリに保存されています。

### その他
このコードによるデータを使っているプログラム一覧
* [twinc-core](https://github.com/Mimori256/twinc-core) by Mimori256
* [scs-migration-checker](https://github.com/itsu-dev/scs-migration-checker) by itsu-dev
* [twins2mkdir](https://github.com/yudukikun5120/twins2mkdir) by yudukikun5120
