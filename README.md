# Stellarculator

## 概要
2bit全加減算機をラズベリーパイに接続して、それを用いて計算させることができます。

現在は2つの数の足し算・引き算・掛け算に対応しています。割り算その他演算や、3つ以上の数の計算は現在開発中です。

## 使い方
### 環境
開発は以下の環境を用いて行いました。
- Python 3.10

- Raspberry Pi 3B

また、以下のモジュールを必要とします。
- gpiozeroモジュール

- timeモジュール

### 使用方法
#### 1.接続
以下の「2bit加算器とピンとの接続」セクションにて説明している通りに2bit加減算機を接続してください。

#### 2.実行
Pythonとモジュールを用意したら、[main.py](https://github.com/starkoka/Stellarculator/blob/main/main.py)を実行してください。

#### 3.クロック設定
1回の計算にかかる時間を設定できます。速ければ速いほど、計算終了までにかかる時間は早くなりますが、その分エラーの発生率が上がって結果がずれる可能性が出てきます。標準では0.05を使用しています。1を指定したい場合は1.0と入力してください。

#### 4.各種モード
クロックの設定が終わると、モードを選択できます。以下の2つのモードのほかに、クロックを設定しなおすこともできます。 

##### 演算モード

演算ができます。2つの数の足し算・引き算・掛け算に対応しています。掛け算の記号は「*」を使用してください。

##### 確認モード
この加減算機が実行できるすべての入出力をテストしてくれます。線の左側が内蔵加算器の結果、右側が外付け加算器の結果です。

![](https://user-images.githubusercontent.com/103174676/219950730-a6ba76b1-7e1e-4899-bba0-2d31d63b94f0.png)
### 2bit加算器とピンとの接続
Sへの入力が0なら足し算、1なら引き算になり、AB ± CD = XYZと出力する5入力3出力の2bit全加減算機を使用します。なお、これらのピンはmain.pyを編集することで変更も可能です。詳細はこのリポジトリのWikiを確認してください。

ABCDSに関しては、以下のピンとGNDを繋ぐそれぞれの回路に電気が流れればON、流れなければOFFと全加算器に入力できるような回路を作ってください。

また、XYZは以下のピンとGNDを繋ぐ回路に1ならば電流が流れ、0なら電流が流れないよう制御するような回路を作ってください。


| 記号  | GPIOポート | ピン番号 |
|-----|---------|------| 
| A   | 15      | 10   | 
| B   | 7       | 26   | 
| C   | 20      | 38   | 
| D   | 21      | 40   | 
| X   | 26      | 37   | 
| Y   | 22      | 15   | 
| Z   | 5       | 29   | 
| S   | 4       | 7    | 

以下は僕と[Kouro](https://github.com/Kou-Ro)が作成した回路の写真と回路図になります。詳細についてはこのリポジトリのwikiに記載してあります。
![回路図](https://user-images.githubusercontent.com/103174676/219946610-940df084-ac2e-4b30-b841-0aa902131f44.png)
![回路の写真](https://user-images.githubusercontent.com/103174676/219946811-b3b054f9-046c-408a-85c6-f7d648984a45.jpg)