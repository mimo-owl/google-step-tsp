## STEP Week5 Documentation
### Author: Mimo Shirasaka

## Challenge
巡回セールスマン問題を解く。
ランダムとgreedy 探索により経路を求めるプログラムはベースラインとして提供されている。
総合経路長を求めるプログラムは `output_vefifier.py`
ベースラインよりも良いスコアを出せるアルゴリズムを実装して、output_i.csv (i = 0 ~ 6)を書き換え、`output_verifier.py`を実行してスコアを確認しよう。

## 私のプログラムの実行結果（as of 2025.6.25）
注: output というところが、私の実装による出力結果を計算したものです。

Challenge 1
output          :    3832.29
sample/random   :    6101.57
sample/greedy   :    3832.29
sample/sa       :    3778.72

Challenge 2
output          :    4994.89
sample/random   :   13479.25
sample/greedy   :    5449.44
sample/sa       :    4494.42

Challenge 3
output          :    8970.05
sample/random   :   47521.08
sample/greedy   :   10519.16
sample/sa       :    8150.91

Challenge 4
output          :   11559.68
sample/random   :   92719.14
sample/greedy   :   12684.06
sample/sa       :   10675.29

Challenge 5
output          :   21363.79
sample/random   :  347392.97
sample/greedy   :   25331.84
sample/sa       :   21119.55


## 実装の説明
実装は、`solver_2opt.py`に行いました。
内容は、まず、greedy探索して経路を求めます。
その結果を用い、そのうちの2ノード（city）を選び、その間の経路を反転させます。
反転させた結果、総合経路が反転前と比べて短くなれば反転させた経路を採用。長くなってしまったら元のままで、また別の２ノードを選んで検討する。
という処理を繰り返します。

これを書いている時点では、`input_6.csv` の実行が終わっていませんが、1~5 の計算結果から、random や greedy の時よりも、output の経路長がより短くなっていることがわかり、より良い経路が求められていることが確認できます。

実行方法：
```bash
python solver_2opt.py input_0.csv
```

結果は、`output_0.csv` に保存されます。

