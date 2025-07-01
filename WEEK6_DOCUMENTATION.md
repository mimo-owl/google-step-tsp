## STEP Week6 Documentation
### Author: Mimo Shirasaka

## Challenge
巡回セールスマン問題を解く。
ランダムとgreedy 探索により経路を求めるプログラムはベースラインとして提供されている。
総合経路長を求めるプログラムは `output_vefifier.py`
ベースラインよりも良いスコアを出せるアルゴリズムを実装して、output_i.csv (i = 0 ~ 6)を書き換え、`output_verifier.py`を実行してスコアを確認しよう。
先週より高いスコアを目指す。

## 私のプログラムの実行結果（as of 2025.6.25）
他の人と組み合わせた実行結果（2opt の後に ILS）：
ILS finished. Final Best Distance: 20947.12

オリジナルの工夫の実行結果：

Challenge 5
output          :   24123.07
sample/random   :  347392.97
sample/greedy   :   25331.84
sample/sa       :   21119.55


## 実装の説明
実装は、`solver_area2opt.py`に行いました。
内容:

エリアを４分割
エリアごとに、greedy + 2opt で経路最適化
全ての順列パターンを試す（4! = 24通り）し、最短経路になる順序で４エリアを連結

という方法をとってみました。


実行方法：
```bash
python solver_area2opt.py input_0.csv
```

結果は、`output_0.csv` に保存されます。


## 結果の考察



