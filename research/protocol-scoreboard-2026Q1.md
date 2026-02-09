# Protocol Scoreboard (2026 Q1)

Last verified: 2026-02-09

## Summary Table

| Protocol / Program | Launch Signal | Current Status | Usage Signal | Confidence | Primary Source |
| --- | --- | --- | --- | --- | --- |
| x402 | V2 post dated Dec 11, 2025 | Live | Homepage counters show 75.41M tx, $24.24M volume, 94.06K buyers, 22K sellers | high | https://www.x402.org, https://www.x402.org/writing/x402-v2-launch |
| A2A (Google) | Launch announcement | Live as open interoperability protocol | "More than 50 technology partners" | high | https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ |
| AP2 (Google) | Payments expansion announcement | Early deployment | "More than 60 partners" and "single trusted protocol" framing | high | https://developers.googleblog.com/en/google-expands-agent2agent-protocol-for-payments/ |
| UCP (Google / partners) | Under-the-hood technical launch post | Early rollout | Explicitly described as open-source standard; includes AP2 compatibility and partner set (Shopify, Etsy, Wayfair, Target, Walmart, 20+ ecosystem partners) | high | https://developers.googleblog.com/en/under-the-hood-universal-commerce-protocol-ucp/ |
| TAP (Visa) | Trusted Agent Program press release | Pilot / sandbox stage | 100+ innovation partners, 30+ pilot participants, 20+ live integrations | high | https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21476.html |
| Agent Pay (Mastercard) | Agentic payments program press release | Announced / rollout path | Partner examples disclosed; no robust production-volume disclosure | high | https://www.mastercard.com/news/press/2025/april/mastercard-unveils-agentic-payments-program-mastercard-agent-pay/ |
| PayPal Agent Toolkit | October 2025 newsroom announcement | Announced | Product launch statement; no public transaction-volume disclosure | high | https://newsroom.paypal-corp.com/2025-10-15-PayPal-Jumps-Into-Agentic-Commerce-with-PayPal-Agent-Toolkit |
| Stripe agentic commerce stack | Sessions 2025 press | Announced and integrated into Stripe stack | AI-foundation-model partnerships and checkout stack references | high | https://stripe.com/newsroom/news/stripe-sessions-2025 |

## Notes

1. Cross-protocol volume comparability is currently low because disclosures are heterogeneous.
2. x402 has the strongest publicly visible transaction counters; card/fiat incumbents disclose mostly partner/distribution milestones.
3. UCP now uses a parse-stable canonical source page (`developers.googleblog.com`) for repeatable extraction.

## Next Data Pull

1. Add quarterly `merchant_count_live`, `monthly_tx_disclosed`, and `dispute_coverage` columns.
2. Separate "enabled accounts" from "active monthly usage" in all protocol rows.
