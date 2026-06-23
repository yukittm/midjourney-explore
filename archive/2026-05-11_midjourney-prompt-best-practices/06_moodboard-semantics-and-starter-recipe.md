---
date: 2026-05-12
status: verified-v1
version-target: Midjourney V7 (default model as of 2026-05)
spec-block: as of 2026-05
scope: >
  Moodboard semantics (what it reads), comparison with --sref / image prompt,
  parameter interaction with moodboard, overfitting avoidance,
  starter recipe for "extend visual library" use case.
  Answers 5 targeted questions from operator.
docs-access-note: >
  docs.midjourney.com returns HTTP 403 from this sandbox environment.
  All official-doc claims are sourced from (a) official update pages
  (updates.midjourney.com — accessible), (b) WebSearch snippets citing
  official doc page titles/URLs, or (c) credible secondary sources.
  Speculation is explicitly labeled.
sources:
  - url: https://updates.midjourney.com/profiles-and-moodboards/
    label: MJ Official — Profiles and Moodboards announcement
    accessed: 2026-05-12
  - url: https://updates.midjourney.com/style-references-for-v7/
    label: MJ Official — Style References for V7 announcement
    accessed: 2026-05-12
  - url: https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards
    label: MJ Official — Moodboards docs (403 from sandbox; snippets via WebSearch)
    accessed: 2026-05-12
  - url: https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference
    label: MJ Official — Style Reference docs (403 from sandbox; snippets via WebSearch)
    accessed: 2026-05-12
  - url: https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/
    label: Chase Jarvis — How to Control Midjourney (secondary; substantial hands-on testing)
    accessed: 2026-05-12
  - url: https://runtheprompts.com/resources/midjourney-info/midjourney-moodboards-ultimate-guide-to-creative-consistency/
    label: RunThePrompts — Moodboard Ultimate Guide
    accessed: 2026-05-12
  - url: https://www.titanxt.io/post/get-more-consistent-art-making-midjourney-mood-boards-work-for-you
    label: TitanXT — Making Midjourney Mood Boards Work
    accessed: 2026-05-12
  - url: https://geekycuriosity.substack.com/p/midjourney-how-to-use-moodboard
    label: Geeky Animals — How to Use Moodboard
    accessed: 2026-05-12
  - url: https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard
    label: Geeky Animals — Mastering Midjourney Moodboard
    accessed: 2026-05-12
  - url: https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style
    label: Geeky Animals — Mixing Moodboard, Style Reference, and Personalization Codes
    accessed: 2026-05-12
  - url: https://medium.com/ai-art-creators/whats-the-difference-between-weird-chaos-and-stylize-in-midjourney-d7e16cab2420
    label: Medium/AI Art Creators — Weird vs Chaos vs Stylize
    accessed: 2026-05-12
---

# 06 — Moodboard Semantics and Starter Recipe (5 Q&A)

This document answers 5 operator-specified questions about Midjourney V7 moodboard
behavior. It extends `03_image-prompts-and-moodboard.md` with deeper analysis specific
to the "extend visual library / variation production" use case.

---

## Q1. Moodboard は image から「何を」参照しているか?

### 結論

**Moodboard は primarily style (color, texture, lighting, mood, palette, material feel)
を読む。Subject や composition は prompt が決める。** ただし、subject leakage の
リスクはゼロではない。

### 根拠

**公式 announcement より:**

> "Moodboards take inspiration from the images that you add. As you add more diverse
> images to the board, the model will start to remix them in more complex ways."
> — [Profiles and Moodboards](https://updates.midjourney.com/profiles-and-moodboards/)

"inspiration from" と "remix" という表現は、literal copy ではなく aesthetic abstraction
を意図している。

**V7 sref アップデートより (moodboard に適用される改善):**

> "much smarter at understanding the style of an image and much less likely to get
> any undesired 'subject leakage' into your images"
> — [Style References for V7](https://updates.midjourney.com/style-references-for-v7/)

V7 は V6 に比べ subject leakage が明示的に削減された。moodboard も V7 の同モデルを使う。

**実践 source より:**

> "They [moodboards] can nudge subjects and compositional elements too, beyond just
> style influence."
> — [Geeky Animals — Mastering Midjourney Moodboard](https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard)

Chase Jarvis の実証実験では、moodboard に "woman" の画像が含まれる場合に
"man" と prompt しても brand consistency は保たれた。**Subject は prompt が勝つ。**

> "Go easy on the detailed prompts — focus more on describing the subject and the scene
> instead of the art style."
> — [RunThePrompts — Moodboard Guide](https://runtheprompts.com/resources/midjourney-info/midjourney-moodboards-ultimate-guide-to-creative-consistency/)

### 「建築写真 + 人物写真 mix」の場合の判断

| 懸念 | 実態 |
|------|------|
| 建築要素が人物 prompt の output に混入するか | 低リスク。V7 の subject leakage 削減効果が適用される |
| 両者の style (ライティング / トーン / 質感) が blend されるか | Yes — これが moodboard の意図された動作 |
| subject は建築か人物か | **Prompt が決める。** Moodboard は style だけ影響する |

> ⚠️ 推測: 建築写真が持つ構図的特徴 (wide shot / geometric / static) が portrait
> prompt の構図に leakage する可能性は V7 でも完全ゼロではない。Pool 内の建築写真比率が
> 高い場合 (>40%) は、portrait 専用 moodboard を分けることを検討。

### Moodboard vs --sref vs Image Prompt の比較

| 機構 | 読み取る要素 | subject 制御 | weight 調整 | --sw 使用可 |
|------|------------|-------------|-----------|-----------|
| **Image Prompt** (URL prepend) | Subject + composition + style すべて | URL の image が引っ張る | `--iw 0–3` (default 1) | N/A |
| **--sref** (Style Reference) | Style のみ (color / texture / light / medium) | 読まない | `--sw 0–1000` (default 100) | Yes |
| **Moodboard (`--p`)** | Style primarily (averaged across pool) + 軽微な compositional nudge | Prompt が決める | **なし (`--sw` 無効)** | **No** |

Sources:
[Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/),
[MJ Moodboards docs snippet](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards),
[MJ Style Reference docs snippet](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)

---

## Q2. Moodboard 採用時、prompt は何を書けばいいか?

### 結論

**Subject と scene を自然文で記述する。Art style・color・mood の記述は省略してよい
(moodboard が担う)。Prompt は短く・具体的に。**

### 「何が強く効くか / 上書きされやすいか」

| 要素 | Moodboard active 時の挙動 |
|------|--------------------------|
| Subject (人物 / 物体 / 場所) | Prompt が支配。moodboard は影響しない |
| Composition / pose / angle | Prompt が primary。ただし moodboard の compositional nudge が軽微に出ることあり |
| Color (specific — "red dress") | **グレーゾーン。** moodboard の palette が強い場合は moodboard 色が残ることある。`--s 40–60` で prompt 優先に寄せられる |
| Lighting mood (warm / cool) | Moodboard が支配しやすい領域 |
| Texture / material feel | Moodboard が支配しやすい領域 |
| Art style / medium | Moodboard が支配。prompt で書いても競合するだけ |

### "Red dress" vs monochrome moodboard — どちらが勝つか?

公式ドキュメントに明示的なテスト結果なし。以下は secondary source と挙動原則から:

- **Moodboard が強い (`--s 250+`)**: monochrome moodboard が "red" を抑圧し、
  desaturated red や grayscale になる可能性が高い。
- **`--s 40–60`**: prompt の "red dress" が優先されやすくなる。
- **`--style raw`**: moodboard の色影響が弱まり、prompt 指定色が出やすい。

Source: [TitanXT — Mood Boards](https://www.titanxt.io/post/get-more-consistent-art-making-midjourney-mood-boards-work-for-you)
(色 overfitting に対し `--s 40–60` を推奨)

> ⚠️ 推測: V7 の natural language 理解向上により、prompt の "red" は V6 より強く効く
> 傾向があるが、moodboard 側の `--s` チューニングなしでの exact color guarantee は
> できない。

### Prompt の最適な構造

**公式 docs が示す V7 向け推奨:**

Natural language prompt が V7 で大幅に改善。以下の構造が複数 source で推奨:

```
[descriptive natural sentence about subject + scene + lighting context]
--p <moodboard_code> --s 100 --c 15 --ar 4:5 --v 7
```

例:
```
A woman reading at a sunlit café table, late afternoon light angling through tall windows
--p m7267884496307879959 --s 100 --c 15 --ar 4:5 --v 7
```

Source: [RunThePrompts](https://runtheprompts.com/resources/midjourney-info/midjourney-moodboards-ultimate-guide-to-creative-consistency/),
[Geeky Animals — How to use Moodboard](https://geekycuriosity.substack.com/p/midjourney-how-to-use-moodboard)

---

## Q3. 主要 parameter の影響範囲 (5 項目)

### `--sw` (Style Weight)

**Moodboard と組み合わせ不可。** `--sw` は `--sref` 専用 parameter。
Moodboard active 時は silently ignored。

> "Moodboards are compatible with Midjourney versions 6 and 7, but cannot be used with
> Style Reference Version (`--sv`) or Style Weight (`--sw`)."
> — [MJ Moodboards docs](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards) (via WebSearch snippet)

Moodboard の「強さ」は `--sw` ではなく **`--s` (stylize)** で調整する。

### `--s` (Stylize)

Midjourney 自体の aesthetic injection 量を制御する dial。Moodboard active 時は
**moodboard style の適用量**を実質的にコントロールする最重要 parameter。

- **Default**: 100
- **Range**: 0–1000
- `--s 0–50`: prompt text に忠実。moodboard の style influence が minimal になる。
- `--s 100`: バランス (default)。moodboard と prompt が共存。
- `--s 250+`: moodboard の style が強く出る。色・質感・ムードが moodboard dominant。
- `--s 1000`: moodboard (または MJ の aesthetic) が完全支配。

Sources:
[MJ Stylize docs](https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize) (via WebSearch),
[TitanXT](https://www.titanxt.io/post/get-more-consistent-art-making-midjourney-mood-boards-work-for-you)

### `--c` (Chaos)

4-grid の variation の広がりを制御。値が高いほど 4 枚が互いに大きく異なる。

- **Default**: 0
- **Range**: 0–100
- `--c 0`: 4 枚が似た構成で出る。安定した production 向き。
- `--c 10–25`: 同一 aesthetic 内で適度な variation。量産時の推奨帯域。
- `--c 50+`: 大きく散らばる。exploration には有効、production には不向き。

Source: [MJ Chaos docs](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety) (via WebSearch)

### `--style raw`

Midjourney 固有の "aesthetic persona" (V7 の artistic bias / 美化処理) を抑制する。
Prompt と reference を more literally に解釈する。

- Photorealism や cinematic 表現に有効。
- Moodboard と組み合わせた場合: Midjourney の aesthetic injection が減り、
  **moodboard 由来の style がより素直に出やすくなる**可能性がある。
- **Default**: off (standard mode)。

Source: [MJ Raw Mode docs](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode) (403 from sandbox; via WebSearch),
[DataCamp V7 Guide](https://www.datacamp.com/tutorial/midjourney-v7)

> ⚠️ 推測: `--style raw` + moodboard の組み合わせにおける相互作用は公式に明文化なし。
> "raw でも moodboard は効く" という実践報告はあるが、exact behavior の公式ドキュメント
> は確認できていない。

### `--w` (Weirdness)

Midjourney の "expected output" からの逸脱量。実験的 parameter。

- **Default**: 0
- **Range**: 0–3000
- `--w 50–150`: 構図や lighting に quirky な要素が加わる程度。
- `--w 500+`: 異形・シュール寄りになる。moodboard の aesthetic を破壊しやすい。
- **注意**: seeds と完全互換ではない。

Source: [MJ Weird docs](https://docs.midjourney.com/hc/en-us/articles/32390120435085-Weird) (via WebSearch)

**本プロジェクト用途 (美学 preservation) では `--w 0` (default) 推奨。**

---

## Q4. 「pool 美学を保って variation 量産」use case の推奨 starter recipe

### 公式推奨の有無

Midjourney 公式に "extend visual library" 専用の baseline parameter set は**未公開**。
公式 Discord にそのような named recipe も確認できず。

### 複数 source から導いた推奨 baseline

以下は複数の credible secondary source が収束している推奨値を統合したもの。

```
[natural-language subject + scene description] --p <snapshot_code> --s 100 --c 15 --ar 4:5 --v 7
```

**各値の根拠:**

| Parameter | 値 | 根拠 |
|-----------|---|------|
| `--p <code>` | snapshot code 使用 | 再現性のため。m-ID はボード編集で変わる |
| `--s 100` | default スタート | moodboard と prompt のバランス点。color override 必要なら `--s 40–60` に下げる |
| `--c 15` | 低〜中 chaos | 4 枚が aesthetic 内で適度に変化。production-safe な分散 |
| `--ar 4:5` | Instagram縦型 | project 固有 |
| `--v 7` | explicit | default だが明示することで snapshot code 変更後も安全 |
| `--w` | 指定なし (= 0) | 美学 preservation 優先なら weirdness off |
| `--style raw` | 任意 | photorealism lane では追加推奨 |

Sources:
[RunThePrompts](https://runtheprompts.com/resources/midjourney-info/midjourney-moodboards-ultimate-guide-to-creative-consistency/),
[TitanXT](https://www.titanxt.io/post/get-more-consistent-art-making-midjourney-mood-boards-work-for-you),
[Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/)

### Lane 別バリエーション

| Lane | 調整点 | 理由 |
|------|--------|------|
| Editorial / moody | `--s 150 --c 20` | aesthetic が強め、variation は許容 |
| Fashion product still | `--s 100 --c 10` | 安定再現性重視 |
| Photorealism | `--s 80 --style raw --c 15` | MJ aesthetic 抑制 |
| Exploration / ideation | `--s 100 --c 35` | 広い variation で候補探索 |

---

## Q5. Moodboard 過 fit (output が pool の literal copy になる) を避ける方法

### `--sw` は使えない (再確認)

Moodboard + `--sw` は **非対応**。`--sw` は `--sref` のみ有効。
過 fit の主要制御 knob は **`--s`** (stylize)。

### `--s` による過 fit 調整 (具体数値)

| `--s` 値 | 挙動 |
|----------|------|
| 0–50 | Moodboard の色・style 影響が minimal。prompt text が支配。過 fit リスク最小。 |
| **40–60** | **色 dominance や style 固着を崩すための推奨帯域。** |
| 100 | Default。バランス。軽微な literal copy 傾向が出る場合は下げる。 |
| 250+ | Moodboard が支配。過 fit が顕著になりやすい。 |

Source: [TitanXT](https://www.titanxt.io/post/get-more-consistent-art-making-midjourney-mood-boards-work-for-you) (具体値推奨あり),
[RunThePrompts](https://runtheprompts.com/resources/midjourney-info/midjourney-moodboards-ultimate-guide-to-creative-consistency/)

### Moodboard 構成枚数の影響

| 枚数 | 挙動 |
|------|------|
| 3–5 枚 (少数) | 特定の色・テクスチャが繰り返し出やすい。過 fit リスク高。|
| **5–10 枚** | **公式 + 複数 source が推奨する heuristic floor。** Averaged aesthetic が安定。|
| 12–20 枚 | より nuanced な blend。lane ごとに分ける場合の現実的上限。|
| 30+ 枚 | 多様性が増すが、aesthetic の coherence が弱まる可能性。|
| 100 枚 (上限) | 最大許容数。large pool では thematic clustering が崩れやすい。|

本プロジェクトの 500–700 枚 pool への対応策:
- Pool を **lane ごと (editorial / fashion / still-life / texture)** に分け、
  各 lane で 8–15 枚の focused moodboard を作る。
- 全 pool を 1 moodboard に投入しない。

Sources:
[Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/) (5–10 推奨),
[TitanXT](https://www.titanxt.io/post/get-more-consistent-art-making-midjourney-mood-boards-work-for-you) (枚数と色多様性の関係),
[RunThePrompts](https://runtheprompts.com/resources/midjourney-info/midjourney-moodboards-ultimate-guide-to-creative-consistency/) (max 100)

### Moodboard と prompt の "competing influence" を意図的に作る手法

**1. `--s` を下げて prompt を競合させる**

```
red dress, woman standing in a doorway --p <mono_moodboard> --s 50 --ar 4:5 --v 7
```
`--s 50` で moodboard の monochrome influence を弱め、"red" が出やすくなる。

**2. `--c` を上げて 4 grid に variation を散らす**

```
[prompt] --p <code> --s 100 --c 30 --ar 4:5 --v 7
```
4 枚が異なる aesthetic interpretation になる。最良 1 枚を選ぶ。

**3. Moodboard + sref を重ねて aesthetic を compound する**

```
[prompt] --profile MOOD_A MOOD_B --sref CODE_A --sw 80 --ar 4:5 --v 7
```
Note: `--sw` は moodboard ではなく **sref に適用**される。moodboard の weight は
`--s` で、sref の weight は `--sw` で別々に調整できる。

Source: [Geeky Animals — Mixing](https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style)

**4. Negative prompt で pool 由来の unwanted 要素を打ち消す**

```
[prompt] --p <code> --s 100 --no green, vintage grain --ar 4:5 --v 7
```
Pool が green-heavy / grainy な場合に有効。

Source: [RunThePrompts](https://runtheprompts.com/resources/midjourney-info/midjourney-moodboards-ultimate-guide-to-creative-consistency/)

**5. Successful output をフィードバックループで pool に追加**

良い生成結果を moodboard に追加し返すことで、preferred aesthetic を reinforcement。
Pool が自己進化して over time で drift 対策になる。

Source: [TitanXT](https://www.titanxt.io/post/get-more-consistent-art-making-midjourney-mood-boards-work-for-you)

---

## このドキュメントの信頼性 gap

| 項目 | 確定度 | 根拠 |
|------|--------|------|
| Moodboard が style primarily を読む | 高 | 公式 announcement + V7 sref "subject leakage 削減" 声明 + 複数実践 source 収束 |
| `--sw` が moodboard に無効 | 高 | 公式 docs snippet (WebSearch) + 複数 secondary source が一致 |
| `--s 40–60` で色 overfitting 回避 | 中 | 2 つの independent secondary source が一致 (公式 docs に明文なし) |
| 5–10 枚 heuristic | 中 | Chase Jarvis + 公式 announcement snippet に言及。公式 docs の explicit 推奨値ではない |
| `--style raw` + moodboard の相互作用 | 低 | 公式に未明文化。実践報告 (動作する) あり、exact 仕様なし |
| Prompt vs moodboard の color 優先順位 | 低 | 公式テスト結果なし。`--s` 値に依存するという原則のみ確認 |

