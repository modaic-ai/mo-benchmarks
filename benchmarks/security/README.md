# Security benchmarks

- [Access Recommendation — Test](access_recommendation_test/README.md)
- [Access Recommendation — Validation](access_recommendation_validation/README.md)
- [Access Continuation — Test](access_continuation_test/README.md)
- [Access Continuation — Validation](access_continuation_validation/README.md)

The complete dataset is private: [`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/f1617a20780cef96be15eb6e345e003e976cf292). This repository contains exactly three representative rows in [`examples.jsonl`](examples.jsonl).

Example task shapes include a review snapshot mapped to `approve` or `revoke`, and a time-bounded access record mapped to `retain` or `revoke`. The linked representative file shows three complete payloads.
