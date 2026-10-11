# 設計知識レコードのひな形

一つの主張についてコピーして利用する。これは学習資料用のテンプレートであり、Codexのスキルではない。

```yaml
id: CLAIM-0001
subject: OP-APPROVE
predicate: requiresPermission
object: PERM-APPROVE
qualifiers:
  environment: test
  design_revision: release-1
  condition: "適用条件を原文どおりに記録"
assertion_kind: asserted # asserted / derived / proposed
review_status: unreviewed # unreviewed / accepted / rejected
validity:
  status: unknown # current / future / expired / withdrawn / unknown
  valid_from: null # 原文で確認した適用開始日時
  valid_until: null # 終了日時。未確認ならnull
release_id: null # この主張を利用する公開版
sources:
  - document_id: DOC-001
    revision: "原本の版またはコミット"
    locator: "見出しID、表、セル範囲など"
    excerpt: "主張を裏付ける必要最小限の記述"
derivation:
  rule_id: null
  premise_claim_ids: []
extraction:
  method: manual # parser / llm など
  extractor_version: null
  extracted_at: null
review:
  reviewer_id: null
  reviewed_at: null
```

## 意味と確認事項

- 対象・関係の意味：
- 条件・例外：
- 同義語・同一性の判断：
- 不足・競合：
- 確認者・確認日：
- この主張に依存するテストや導出：

assertedは原文に明記、derivedは規則から導出、proposedは推測・提案の候補を表す。作成方法と承認状態、有効性は別に記録する。LLMで抽出した内容も、原文に明記されていればassertedとして記録できる。

derivedの場合は規則と前提主張を必須にする。proposedは根拠付きの確定事実として公開しない。取り込み日時を適用開始日時に代用せず、未確認の期間は未確認として残す。秘密情報や認証情報そのものは格納せず、テスト環境で取得する方法の参照を持たせる。
