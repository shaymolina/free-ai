# Cloud services for a realistic AI video twin (Hebrew course, 5-10 hours)

Access date for all sources: 2026-11-26. Research method: web search only. Direct page fetches were blocked in this session for help.heygen.com, sync.so, fal.ai and arcade.software, so most figures come from search snippets of those pages and from third-party blogs. Anything marked UNVERIFIED was not confirmed on a vendor page.

## Q1. Comparison table: realism, Hebrew, custom avatar, length, prices, cost per hour, watermark, rights, API

### Takeaway
The cheapest realistic paths are video-to-video lip-sync on the user's own studio footage (Kling LipSync about $50/hour, LatentSync about $18/hour hosted or free locally), while full avatar platforms (HeyGen, Synthesia) land around $60-180/hour on subscriptions and $290-430/hour via API. Premium lip-sync (sync.so lipsync-2-pro, sync-3) costs $240-480/hour.

### Cited Findings

Summary table (effective cost per hour of finished video is computed in Inferences; "?" = not found):

| Service / model | Type | Price basis | Effective $/hour finished | Hebrew | Max length / res | Watermark | API |
|---|---|---|---|---|---|---|---|
| HeyGen Creator ($29/mo, 600 credits) | Avatar platform, digital twin | Avatar V 48 cr/min (help center) or 20 cr/min (HeyGen blog); Avatar IV video look 31 cr/min | ~$58-139 | 175+ languages claimed, no Hebrew-specific test found | 30 min/video, 1080p | Removed from Creator up | Separate API pricing |
| HeyGen Pro ($49/mo, 1,000 credits) | same | same | similar per-min, adds 4K | same | 30 min, 4K | No | - |
| HeyGen Business ($149/mo, 1,500 credits) | same | same | - | same | - | No | - |
| HeyGen API | API | Avatar IV Digital Twin $4.83/min; Avatar V Digital Twin $7.20/min | ~$290 / ~$432 | same | ? | No | Yes |
| HeyGen Avatar 5 Digital Twin via fal.ai | API | $0.10/sec | ~$360 | ? | ? | ? | Yes |
| Synthesia Starter ($29/mo, 10 min) / Creator ($89/mo, 30 min) | Avatar platform | ~100 credits per finished min | ~$174-178 | ? (not confirmed) | ? | Logo removal from Starter | API on Creator |
| Synthesia Studio Express-1 avatar | Studio avatar add-on | $1,000/year, annual plans only, up to 10 days processing | add-on on top | ? | ? | - | - |
| sync.so lipsync-2-pro | Video-to-video lip-sync | $0.067-0.083/sec at 25 fps | ~$241-300 | any language when you supply audio | ? | ? | Yes |
| sync.so sync-3 | Video-to-video lip-sync | $0.107-0.133/sec at 25 fps (Atlas Cloud: $0.22/sec) | ~$385-479 (Atlas ~$792) | 95+ languages, any language with own audio | free tier 15 s clips | ? | Yes |
| Kling LipSync (fal.ai, audio-to-video) | Video-to-video lip-sync | $0.014 per input-video second, rounded to 5 s | ~$50 | ? | ? | ? | Yes |
| LatentSync (fal.ai) | Video-to-video lip-sync, open source | $0.20 up to 40 s, then $0.005/sec | ~$18 | language-agnostic (audio-driven) | ? | ? | Yes; also runs locally |
| MuseTalk (fal.ai) | Video-to-video lip-sync, open source | price not readable | ? | - | - | - | Yes |
| Kling AI Avatar v2 (fal.ai) | Photo to talking video | Standard $0.0562/sec, Pro $0.115/sec | ~$202 / ~$414 | ? | ? | ? | Yes |
| OmniHuman (fal.ai) | Photo to talking video | $0.14/sec (other blog: $0.16 for v1.5) | ~$504-576 | ? | ? | ? | Yes |
| Hedra Character-3 | Photo to talking video | 6 credits/sec at 720p; ~$2-3 per finished minute | ~$120-180 | ? | 720p | ? | ? |
| D-ID | Avatar platform | Lite ~$5.90/mo (watermark), Basic ~$29, Advanced ~$96 or ~$299 (conflict) | ? | ? | ? | Lite has watermark | Advanced |
| DeepBrain AI Studios | Avatar platform | $24-29/mo; custom avatar needs Enterprise | ? | 80+ langs, Hebrew unconfirmed | ? | ? | ? |
| Colossyan | Avatar platform (training) | $19-59/mo (conflict) | ? | ? | ? | ? | ? |
| Argil | Avatar platform | Pro/Studio/Enterprise, no public price found | ? | ? | ? | ? | ? |
| Akool | Avatar platform | ~$5-9/mo entry | ? | ? | ? | ? | ? |
| Tavus | Real-time conversational video | $59/mo 100 min, $397/mo 1,250 min | not a fit (conversational) | ? | ? | ? | Yes |
| Captions / Mirage | Avatar app + API | only found API "Add Captions" $0.15/min | ? | ? | ? | ? | Yes |
| ElevenLabs (voice only) | Hebrew voice clone | Creator $22/mo for Professional Voice Clone; API $0.08 per 1,000 chars | voice only, see Inferences | Hebrew TTS page exists; PVC on v3 for Hebrew unconfirmed | - | - | Yes |

Sources per row:
- HeyGen Avatar IV Video Look 31 credits/min, Photo Look 16, Avatar III 4 — [HeyGen help center (search snippet)](https://help.heygen.com/en/articles/15125761)
- HeyGen API: Avatar IV Digital Twin $4.83/min (97 credits), Avatar V Digital Twin $7.20/min (144 credits) — [HeyGen API plans (Intercom help)](https://intercom.help/heygen/en/articles/10060327-new-heygen-api-plans)
- HeyGen Avatar V 48 credits/min for Photo and Video Looks — [HeyGen help center](https://help.heygen.com/es/articles/9204682-heygen-pricing-plans-and-subscriptions-explained-what-you-need-to-know); contradicted by HeyGen's own blog saying Avatar IV/V cost 20 credits/min and 30 min of Avatar V on Creator at $0.97/min (as summarized by [Rework](https://resources.rework.com/tools/ai-video/best-ai-avatar-generators-2026)) and by [Creatify](https://creatify.ai/blog/heygen-pricing-(2026)-plans-and-what-you-ll-actually-pay)
- HeyGen Creator $29/600 credits, Pro $49/1,000 credits — [Arcade](https://www.arcade.software/post/heygen-pricing); Business $149/1,500 credits, extra seats $20 — [Creatify](https://creatify.ai/blog/heygen-pricing-(2026)-plans-and-what-you-ll-actually-pay); older guide lists Pro at $99 — [dev.to](https://dev.to/2gelbuy/heygen-pricing-2026-all-plans-from-0-to-149mo-compared-2dff)
- HeyGen 30-minute max video on Creator and Pro; Creator 1080p, Pro 4K; watermark only on free — [Capterra](https://www.capterra.com/p/10015133/HeyGen/pricing/); 4K under higher Pro tiers — [HeyGen help](https://help.heygen.com/en/articles/15125761-heygen-credit-based-pricing-explained)
- HeyGen Avatar 5 digital twin on fal.ai $0.10/sec — [fal.ai listing (search snippet)](https://fal.ai/models/fal-ai/heygen/avatar5/digital-twin/llms.txt)
- Synthesia Starter $29/10 min/3 Personal Avatars, Creator $89/30 min/5 Personal Avatars + API, Enterprise custom; Studio Express-1 $1,000/yr annual only, up to 10 days — [Synthesia pricing](https://synthesia.io/pricing), [Arcade](https://www.arcade.software/post/synthesia-pricing); ~100 credits per finished minute — [Rework](https://resources.rework.com/tools/ai-video/best-ai-avatar-generators-2026); older/promo prices ($18/$64 annual) also appear on Synthesia affiliate pages
- sync.so lipsync-2-pro $0.067-0.083/sec at 25 fps, billed per output frame; Hobbyist $0.08325/sec; up to 20% discount on higher tiers — [sync.so pricing](https://sync.so/pricing), [sync.so billing docs](https://sync.so/docs/billing); Runware $0.0733/sec — [Runware](https://runware.ai/models/lipsync-2-pro); WaveSpeed $0.08/sec of audio — [WaveSpeed](https://wavespeed.ai/docs-api/sync/sync-lipsync-2-pro); fal.ai $5/min (possibly outdated) — [fal.ai](https://fal.ai/models/fal-ai/sync-lipsync/v2)
- sync-3 $0.107-0.133/sec at 25 fps, 95+ languages, own audio in any language, free tier 3 videos/month max 15 s — [sync.so sync-3 docs](https://sync.so/docs/models/sync-3); Atlas Cloud $0.22/sec — [Atlas Cloud](https://www.atlascloud.ai/models/sync/lipsync-v3)
- Kling LipSync audio-to-video $0.014 per input-video second rounded to 5 s — [fal.ai docs](https://fal.ai/docs/model-api-reference/video-generation-api/kling-video-lipsync); Kling LipSync cheapest for a 10 s clip ($0.14) among ten models — [fal.ai lip sync roundup](https://fal.ai/learn/tools/ai-lip-sync-generators)
- LatentSync $0.20 up to 40 s, then $0.005/sec — [fal.ai LatentSync](https://fal.ai/models/fal-ai/latentsync)
- Kling AI Avatar v2 Standard $0.0562/sec, Pro $0.115/sec — [fal.ai standard](https://fal.ai/models/fal-ai/kling-video/ai-avatar/v2/standard), [fal.ai pro](https://fal.ai/models/fal-ai/kling-video/ai-avatar/v2/pro)
- OmniHuman $0.14/sec — [fal.ai OmniHuman](https://fal.ai/models/fal-ai/bytedance/omnihuman); $0.16/sec for v1.5 — [PicassoIA blog](https://blog.picassoia.com/omnihuman-1-5-api-pricing-lip-sync-and-avatar-videos); OmniHuman 2.0 released Oct 2026 via BytePlus, photo-based — [PixVerse roundup](https://pixverse.ai/en/blog/best-ai-lip-sync-video-generators-2026)
- Hedra Character-3 6 credits/sec (360/min) at 720p; ~$3/min or ~$2/min on Creator; plan prices conflict ($15/$30/$75 vs $20/$50/$75/$100; Creator dropped Sept 2026) — [Activepieces](https://www.activepieces.com/blog/hedra-pricing-2026-plans-credits-and-cost-per-video.md), [Fluxnote](https://fluxnote.io/guides/hedra-ai-review), [UsagePricing](https://www.usagepricing.com/blueprint/activity/hedra-2026-07-29-character-3-hailuo-lineup)
- D-ID Lite ~$5.90 with watermark, Basic ~$29, Advanced ~$96 or ~$299 — [Argil blog on D-ID pricing](https://www.argil.ai/blog/d-id-pricing) (competitor-written), [Rework](https://resources.rework.com/tools/ai-video/best-ai-avatar-generators-2026)
- DeepBrain custom avatar needs Enterprise; $24-29/mo; 80+ languages — [HeyGen comparison](https://www.heygen.com/blog/best-talking-avatars-video-maker) (competitor-written), [HeyGen Hebrew blog](https://www.heygen.com/he-il/blog/best-free-ai-avatar-generators)
- Tavus $59/100 min, $397/1,250 min, 30 s minimum per conversation — [DailyAIFixs](https://dailyaifixs.com/blog/tavus-pricing-2026-the-per-minute-catch) (UNVERIFIED on vendor page)
- Captions API Add Captions $0.15/min, billed on input length rounded up — [Captions API docs](https://captions.ai/help/docs/api/pricing)
- ElevenLabs PVC from Creator $22/mo, needs 30+ min clean samples, own voice only; API $0.08/1,000 chars on Multilingual v2/v3 — [Fora Soft](https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/elevenlabs-pricing-voice-cloning-no-fakes-act), [ElevenLabs API pricing](https://elevenlabs.io/hi/pricing/api); PVC works with Multilingual model across its languages — [ElevenLabs Hebrew TTS](https://elevenlabs.io/zh/text-to-speech/hebrew)

### Inferences
- Cost per hour math: HeyGen Creator at 48 cr/min = 12.5 min/month = ~$2.32/min = ~$139/hour; at 31 cr/min (Avatar IV) = ~$91/hour; at 20 cr/min = ~$58/hour. 5-10 hours on Creator would need 24-48 months of credits, so in practice it means Business plan or buying extra credits; the real bill for 5-10 hours is roughly $300-1,400 on subscriptions vs $1,450-4,300 via API.
- sync.so lipsync-2-pro: $4.0-5.0/min, so 5-10 hours = ~$1,200-3,000. sync-3: ~$1,900-4,800.
- Kling LipSync: $0.84/min, so 5-10 hours = ~$250-500. LatentSync hosted: $0.30/min, 5-10 hours = ~$90-180, or near free locally on the RTX 5080.
- The "~$200 per hour" the user saw matches Synthesia (~$174-178/hour) and HeyGen at Avatar V rates.
- Voice: a Hebrew hour of speech is very roughly 40-60k characters (my estimate, not sourced), so ElevenLabs API voice is ~$3-5/hour; voice is a minor cost next to video.

### Gaps
- Could not open HeyGen, sync.so or fal.ai pages directly (blocked hosts), so all their numbers are from search snippets.
- No HeyGen Business/Enterprise credit price for top-up packs found.
- Commercial rights terms not verified for any service.
- Synthesia, Colossyan, Argil, Akool, Vidnoz, Elai: no verified per-minute price or Hebrew lip-sync confirmation.
- Veo and Hailuo lip-sync features: not researched (ran out of budget).

## Q2. Video-to-video dubbing (own footage + new audio) vs generated avatars, and which looks most real

### Takeaway
For a person with real studio footage, video-to-video lip-sync keeps the real body, lighting and gestures and only changes the mouth, which is the most likely route to "looks real"; avatar platforms like HeyGen Avatar V also build from a short clip but generate the whole performance.

### Cited Findings
- sync.so models re-sync lips of existing video to a new audio track, working on footage you provide — [sync.so blog](https://sync.so/blog/what-is-lipdub-ai), [sync.so sync-3 docs](https://sync.so/docs/models/sync-3)
- A 2026 roundup names sync-3 and HeyGen Lipsync Precision as top picks for existing footage — [PixVerse roundup](https://pixverse.ai/en/blog/best-ai-lip-sync-video-generators-2026)
- Video-to-video options found: sync.so (lipsync-2-pro, sync-3), Kling LipSync, LatentSync, MuseTalk, HeyGen lip-sync tool — [fal.ai roundup](https://fal.ai/learn/tools/ai-lip-sync-generators), [HeyGen Hebrew lip-sync tool](https://www.heygen.com/he-il/tool/create-ai-lip-sync-videos)
- Photo-driven generators: OmniHuman, Hedra Character-3, Kling AI Avatar — [PixVerse roundup](https://pixverse.ai/en/blog/best-ai-lip-sync-video-generators-2026), [Fluxnote](https://fluxnote.io/guides/hedra-ai-review)
- HeyGen Avatar V builds a twin from a single ~15 s clip (another HeyGen post says ~30 s) and combines footage and consent into one recording where the subject reads a security code — [HeyGen community FAQ](https://community.heygen.com/public/resources/avatar-v-live-webinar-recap-top-questions-answered-2026-04-16), [HeyGen blog](https://www.heygen.com/blog/how-to-create-digital-twin-avatar), [HeyGen consent docs](https://developers.heygen.com/docs/avatar-consent)
- Both HeyGen and Synthesia require recorded consent for custom avatars — [Eneba](https://www.eneba.com/hub/ai-tools/best-ai-avatar-video-generators/)
- Vendor-run test (VEED) ranks its own Fabric 1.0 first, HeyGen runner-up, Hedra cheapest — [VEED](https://www.veed.io/learn/best-lipsync-api) (biased)

### Inferences
- With hours of studio footage, the user can loop or cut segments of real footage and lip-sync new Hebrew audio onto them, which avoids generated hands and bodies.
- Lip-sync models only change the mouth region, so long static talking shots work best; head turns and hand-over-mouth moments are where artifacts are likely.

### Gaps
- No independent, Hebrew-specific realism test found for any tool.
- No head-to-head of sync-3 vs Kling LipSync vs LatentSync on the same footage found.

## Q3. Cheapest way to 5-10 hours of realistic video, and hidden limits

### Takeaway
Cheapest realistic plan: clone the voice (ElevenLabs, ~$22/month), then lip-sync onto the user's own footage with Kling LipSync (~$50/hour) or LatentSync (~$18/hour hosted, or local on the RTX 5080), and pay for premium sync.so only on close-up or hero segments.

### Cited Findings
- Kling LipSync is the cheapest of ten lip-sync models on fal.ai for a 10 s clip ($0.14) — [fal.ai roundup](https://fal.ai/learn/tools/ai-lip-sync-generators)
- LatentSync $0.005/sec after the first 40 s — [fal.ai LatentSync](https://fal.ai/models/fal-ai/latentsync)
- Hidden limits: HeyGen 30-minute cap per video, 4K only on Pro — [Capterra](https://www.capterra.com/p/10015133/HeyGen/pricing/); HeyGen lip-sync uses extra credits, one source says one lip-synced minute uses two minutes of credit — [HeyGen G2/Capterra review summaries via search](https://www.capterra.co.il/software/1059360/heygen) (UNVERIFIED); Synthesia Studio avatar $1,000/year extra, annual only — [Arcade](https://www.arcade.software/post/synthesia-pricing); sync.so bills per output frame at 25 fps, so higher fps costs more — [sync.so billing docs](https://sync.so/docs/billing); Kling LipSync rounds up to 5 s — [fal.ai docs](https://fal.ai/docs/model-api-reference/video-generation-api/kling-video-lipsync); Hedra Character-3 is 720p at the quoted rate — [Activepieces](https://www.activepieces.com/blog/hedra-pricing-2026-plans-credits-and-cost-per-video.md)
- Lip sync quality complaints on HeyGen: "sometimes gets off", "makes video quality bad sometimes" — [G2 HeyGen reviews](https://www.g2.com/products/HeyGen/reviews), [Capterra IL](https://www.capterra.co.il/software/1059360/heygen)
- HeyGen lip sync accurate in English and major European languages, weaker in Japanese in one test — [Coda review](https://coda.io/@rohan-mac/heygen-avatar-iv-review/heygen-multilingual-test-lipsync-translation-and-accent-quality-7)

### Inferences
- Hybrid plan for 5-10 hours: ElevenLabs voice ~$22-99 total; Kling LipSync ~$250-500 or LatentSync local ~$0; optional sync.so lipsync-2-pro for 10-20% of footage adds ~$120-600. Total likely ~$300-1,000 vs ~$870-1,780 on Synthesia or ~$1,450-4,300 on HeyGen API.
- Test 1-2 minutes of Hebrew on each candidate before committing, since no Hebrew realism data exists.

### Gaps
- No verified Hebrew lip-sync quality data for Kling LipSync, LatentSync or sync.so.
- Real cost of re-renders (failed takes) not quantified anywhere reliable.
