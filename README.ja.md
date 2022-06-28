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

