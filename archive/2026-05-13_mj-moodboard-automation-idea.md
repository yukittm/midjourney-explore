---
date: 2026-05-13
status: future-automation-option (not implemented)
scope: image generation pipeline menu — one option entry
trigger-condition: when menu-化 phase begins (declared by user)
parent-context:
  - 2026-05-10 Path 2 採用判断 (`.claude/orchestration/2026-05-10_pinterest-midjourney-pipeline-poc.md`)
  - 2026-05-11 Midjourney best practices doc (本フォルダ 6 file)
session: Claude:orchestration
---

> **⚠️ ARCHIVED 2026-06-23 (V7-era).** Moved to `/archive/` — a V7-era moodboard-automation idea
> (carried from marketing-ops), superseded by the current one-pass automation policy in
> `../automation/README.md`. Historical only; NOT the active plan. See `/archive/README.md`.

# Midjourney Moodboard Automation — Future Menu Option

## Why (= user の design intent、2026-05-13 会話)

User は「画像素材生成パイプライン全体」を menu 化する方針。menu の中の **1 option** として、Midjourney moodboard 経由の自動生成 path を確保したい。

実装は現段階では不要、概念として記録。

## Position (パイプライン全体での位置付け)

- 画像素材を作る menu は複数 option が並ぶ想定 (Midjourney / ChatGPT / Krea / Higgsfield / Nano Banana 等、各々強みが違う、`2026-05-11_midjourney-prompt-best-practices/README.md` の「他ツールとの分業」表が menu の素案)
- 本 option = **"Midjourney moodboard automation"** entry
- 他 option との分担: Midjourney は house aesthetic engine、editorial/fashion/surface 系の aesthetic-driven 生成担当

## Abstract steps (actor 非依存)

1. SSE-Lab (`workspace/assets/candidates/`) からテーマ別 reference 画像を pick (manual or theme-filter automation)
2. Browser 経由で Midjourney Web App (`midjourney.com/personalize`) を開く
3. 新規 moodboard 作成、上記 reference を upload
4. snapshot code (英数字、persistent) を取得・記録
5. prompt 設計 (subject + scene のみ、style は moodboard 任せ)
6. `--p <snapshot-code>` 付きで run、4-12 var 取得
7. 出力 download、metadata と共に保存

## Cross-actor requirement (Claude + Codex 双方で実行可能に)

- 運用系の中心は Claude を想定、ただし現時点 (2026-05-13) では **Codex + computer-use** の方が browser 操作の精度・速度が高い (= ツール状況依存)
- ツールアップデートが頻繁なので、その時々で最適な actor を選べる設計が必要
- → menu spec は **abstract step level に保持**、各 actor は自分の tool set (Claude: Playwright MCP / Chrome MCP、Codex: computer-use) に bind して実行

## Implementation 候補 (未確定、選択は menu-化フェーズで)

| Option | 長所 | 短所 |
|---|---|---|
| **Markdown のみ** (1 entry = 1 .md) | 軽量、両 actor が読める、tool 切替容易 | 実行精度は actor の解釈に依存 |
| **Markdown + structured frontmatter** | 必要 tool / permission を明示、規律 up | 軽い overhead |
| **Script-backed** (shell / python wrapper) | 実行 precision 高い | tool 変更に brittle、cross-actor 整合 overhead 大 |
| **Skill / Agent 化** | 再利用性最大、自然な invoke | setup cost 高、actor 差吸収のレイヤー必要 |

→ 直感的に **Markdown + structured frontmatter** が cross-actor + tool flexibility 双方を満たす。実装フェーズで再評価。

## Connected docs

- `2026-05-11_midjourney-prompt-best-practices/README.md` — Midjourney 戦略フレーム
- `2026-05-11_midjourney-prompt-best-practices/03_image-prompts-and-moodboard.md` — moodboard 操作の技術 reference (本 option の bottle-neck step)
- `2026-05-11_midjourney-prompt-best-practices/06_moodboard-semantics-and-starter-recipe.md` — moodboard 仕様 + starter recipe (本 option のデフォルト parameter)
- `2026-05-10_pinterest-midjourney-pipeline-poc.md` — Path 1 不採用 / Path 2 採用判断 (本 option の親系統)

## 実装トリガーまでの保持事項

- 現段階: **記録のみ、実装着手なし**
- トリガー: user が「menu 化フェーズ開始」を宣言した時
- 着手時に再評価するもの:
  - 当時の Claude / Codex / 他 actor の browser 自動化能力 (2026-05-13 時点と差分あり得る)
  - 当時の MJ Web App UI (UI 変更で step 順が変わる可能性)
  - menu 全体構造 (本 option が menu の何番目の entry になるか、ID 付与方針)
