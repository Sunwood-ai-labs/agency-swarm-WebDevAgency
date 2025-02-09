<div align="center">

![Image](https://github.com/user-attachments/assets/237c4efa-3b16-4c82-9167-bde3a5996cf4)

# agency-swarm-WebDevAgency

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-API-darkgreen.svg)](https://docs.github.com/en/rest)
[![agency-swarm](https://img.shields.io/badge/agency--swarm-Framework-orange.svg)](https://github.com/agency-swarm)

</div>

## 🌟 概要

agency-swarmフレームワークを使用したWeb開発エージェンシーのAIエージェントシステムです。プロジェクトマネージャー、フロントエンド開発者、バックエンド開発者、UIデザイナーの4つのエージェントが協力してWebサイト開発プロジェクトを遂行します。

## 🤖 エージェント構成

- **🎯 プロジェクトマネージャー**: クライアントとの連絡、プロジェクト進行管理を担当
- **💻 フロントエンド開発者**: ユーザーインターフェースの実装を担当
- **🔧 バックエンド開発者**: サーバーサイド機能の実装を担当
- **🎨 UIデザイナー**: デザインの作成、プロトタイピングを担当

## 🛠️ 技術スタック

### フレームワーク
- agency-swarm: AIエージェントフレームワーク
- GitHub API: コードバージョン管理、チーム連携

### 開発言語
- Python: エージェントシステムの実装
- 各種Web開発言語: プロジェクトに応じて使用

## 📚 機能一覧

- GitHub APIを活用したコード管理
  - リポジトリ管理
  - プルリクエスト管理
  - ブランチ管理
  - 進捗トラッキング
  - デザインファイル管理

## 🚀 使用方法

1. 環境変数の設定
```bash
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
```

2. エージェントの起動
```python
python agency.py
```

## 📋 プロジェクト構造

各エージェントは以下のような構成になっています：

- 📁 instructions.md: エージェントの役割と指示
- 📁 tools/: GitHub API操作用ツール
- 📁 files/: 作業用ファイル
- 📁 schemas/: データスキーマ

## 🔒 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
