# Pong-Game-with-Pygame

<!-- A simple Pong game with Pygame -->
[Pygame](https://www.pygame.org/news)を利用したシンプルなPongゲーム

<!-- This is a pong game against AI(barely). Main reason I did this game  is to learn the basics of Pygame. -->
AI(ほとんどAIではなない...)と対戦するポンゲームです。
Pygameの基本を学ぶことが、このゲームを作成した主な理由です。

<!-- To play: Pygame installation is required. Than run the main file while it is in the some folder with assets. -->

ゲームをプレイするには、Pygameのインストールが必要です。
assetsのあるフォルダ内で、main.pyを実行します。

## 環境構築

個別に依存パッケージを手動でインストールしても良いですが、`pyproject.toml`も用意しています。

`pyproject.toml`から依存パッケージをインストールできます。
プロジェクトのディレクトリ内で以下を実行してください。

~~~shell
$ poetry install
~~~

ただし、`poetry`が必要になります。
`poetry`のインストール方法については[公式ドキュメント - Installation](https://python-poetry.org/docs/#installation)を参照してください。

## 実行

仮想環境を立ち上げ、その後に`main.py`を実行します。
プロジェクトのディレクトリ内で以下を実行してください。

~~~shell
$ poetry shell
(pong-game-with-pygame-MH9AP2Ay-py3.xx) $ python3 main.py
~~~

## ゲームの操作方法

パドル(ラケット)を上下に操作して、ボールを打ち返すゲームです。

### キー操作

|キー|説明|
|:--:|----|
|`w`| キーを押す(押し続ける)と、パドルは上へ移動 |
|`s`| キーを押す(押し続ける)を、パドルは下へ移動 |

### キーのカスタマイズ

`pyproject.toml`のテーブル`[pong.key]`内に`up`または`down`に`キー定数名`を指定することで、上下操作のキーを変更できます。

利用できる`キー定数名`は `pygame`で使用されている[キー定数](https://www.pygame.org/docs/ref/key.html#key-constants-label)になります。

デフォルトでは、`up`に`K_w`(`w`キー)、`down`に`K_s`(`s`キー)が設定されます。

上下操作を、それぞれ矢印キーのUP,DOWNに設定する場合は、以下のように設定してください。

~~~toml
[pong.key]
up = 'K_UP'
down = 'K_DOWN'
~~~

## 開発者の方へ

### コードフォーマット

ソースをコミットする前に、以下のタスクによりコードをフォーマットしてください。

~~~shell
$ poetry run task format
~~~

### コードチェック

ソースをコミットする前に、`flake8`による、コードをチェックしてください。
なにかエラーが表示される場合は、なるべくエラーを修正してください。

~~~shell
$ poetry run task lint
~~~

また、`vscode`に`flake8`によるコードチェックを有効にする場合は、`Homebrew`などで`flake8`をインストールし、

~~~shell
$ brew install flake8
~~~

`vscode`で以下を設定してください。

~~~json
"python.linting.flake8Enabled": true
"python.linting.flake8Path": "flake8"
"python.linting.flake8Args": [
  "--max-line-length",
  "119",
  "--extend-ignore",
  "E203"
]
~~~
