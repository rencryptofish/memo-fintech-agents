# URL Remediation Log

Date: 2026-02-09

## Remediated Links

| Legacy URL | HTTP | Replacement URL(s) | Replacement HTTP | Resolution |
| --- | ---: | --- | ---: | --- |
| https://www.frbservices.org/news/communications/120425-fednow-service-marks-strong-growth-2025.html | 404 | https://www.frbservices.org/news/communications/120425-general-announcing-2026-fees | 200 | Replaced with current FRB communication that contains FedNow participation and limit updates |
| https://www.fdic.gov/news/financial-institution-letters/2025/notification-process-supervised-institutions-engage | 404 | https://www.fdic.gov/news/financial-institution-letters/2025/notice-proposed-rulemaking-establish-genius-act-application ; https://www.fdic.gov/news/press-releases/2026/fdic-extends-comment-period-proposal-establish-genius-act-application | 200 ; 200 | Replaced with active NPR notice page and extension announcement |

## Files Updated to Reflect Remediation

1. `research/source-registry.md`
2. `research/regulatory-tracker-us-2026.md`
3. `research/memo-citation-backfill-matrix.csv`

## Guardrail

Any URL returning `404` must be replaced by a current primary-source URL in the same working session and recorded in this log.
