# Hebrew Voice Cloning / TTS Options (as of 2026-11-26)

Research note: huggingface.co and elevenlabs.io could not be fetched directly from this session (blocked by the network allowlist). Facts about them come from search snippets, GitHub pages and third-party listings. Prices are as of November 2026, in USD.

Working assumption used below for "cost per hour": about 60,000 Hebrew characters per hour of narration. This comes from third-party ElevenLabs guides that equate 121,000 credits (1 credit = 1 character) with "about 121 minutes" of TTS ([BigVU / aggregators](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/)). It is an estimate, not a measurement on Hebrew.

## Which local open-source models actually sound good in Hebrew, and how do they handle nikud and stress?

### Takeaway
No open model in late 2026 clearly matches the top cloud voices in Hebrew. The strongest local candidates with voice cloning are QwenTTS-he (Apache 2.0, "clearest" in one tester's notes), Chatterbox Multilingual v3 (MIT), and the F5-TTS Hebrew v2 fine-tune (licence unclear). XTTS-v2 has no Hebrew, and CosyVoice, IndexTTS2, OmniVoice and VibeVoice are not trained for Hebrew or sound accented. Nikud and stress are the main failure point: models fed text without correct nikud and stress marks often stress the last syllable or misread words.

### Cited Findings
- A blind listening bake-off of Hebrew TTS (dated 2026-11-18) tested Phonikud+Piper, Piper `noa` (2026-10-26), Kokoro Hebrew (2026-07-05), BlueV3 v3.0.1 (2026-11-14), F5-TTS Hebrew v2 (Yzamari, 2026-03-28), ZONOS3-Mini, Chatterbox Multilingual v3 (v3 weights 2026-04-22), VoxCPM2, OmniVoice and Fish Audio S2 Pro, plus cloud APIs. — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- In that bake-off the arena winners were all cloud voices (Gemini 3.1 Flash TTS, Gemini 3.8 variants, ElevenLabs v4). Piper `noa` lost every match and was called "a preceding generation of TTS." — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- The bake-off says Chatterbox Multilingual v3's "built-in Dicta nikud step is broken." — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- Common screening failures were "wrong stress" (BlueV3, Kokoro with nikud, OmniVoice, Phonikud variants) and "mispronunciation" (Google Cloud, Inworld, Piper noa). The Phonikud voice stressed the last syllable of words like סֵפֶר because its nikud had no stress marks. — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- Nikud changes output: Kokoro-Hebrew read הספר as "ha-sefer" on plain text and "ha-sapar" with nikud; phonemes differed between inputs in 16 of 20 sentences. DictaBERT nikud needed 12 word corrections across 8 sentences. — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- Fish S2 Pro self-hosted in bf16 on an L4 took about 13 minutes per sentence, so the tester switched to Fish's API. — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- Hebrew Voice Studio (local multi-engine Hebrew TTS) lists these engines: LightBlue/BlueTTS v2 and Blue 2.5 (CPU, cloning), Kokoro Hebrew (CPU, no cloning), Chatterbox Multilingual (GPU, cloning), OmniVoice, Higgs Audio v3 ("some garbled words in testing"), QwenTTS-he ("clearest in testing"), Magpie-TTS Hebrew (fixed voices only), F5-TTS Hebrew (cloning required), VibeVoice 1.5B/7B ("Hebrew has an English accent"), Fish Audio Drama 3, ZONOS3-Mini, voxtream2-he, Zonos-Hebrew. — [hebrew-voice-studio](https://github.com/tm1981/hebrew-voice-studio)
- Hebrew fine-tunes on Hugging Face named there: notmax123/QwenTTS-he-1.7B (Qwen3-TTS 1.7B Base plus Hebrew LoRA), Yzamari/f5tts-hebrew-v2 (F5-TTS v1 Base fine-tune), notmax123/Zonos-Hebrew, flowty1/voxtream2-he, notmax123/magpie_tts_multilingual_357m-he, thewh1teagle/kokoro-hebrew-nc, bosonai/higgs-tts-3-4b. — [hebrew-voice-studio](https://github.com/tm1981/hebrew-voice-studio)
- F5-TTS Hebrew v2 was fine-tuned from F5-TTS v1 Base on 158 hours (per search snippet of the bake-off). — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- Chatterbox Multilingual officially lists Hebrew and has an `add_hebrew_diacritics` helper that uses the `dicta_onnx` package. Hebrew has no dedicated per-language checkpoint. — [Chatterbox HF README](https://huggingface.co/ResembleAI/chatterbox/blob/main/README.md); [Algolia docs index](https://docsearch.algolia.com/mcp/docs/repo/resemble-ai/chatterbox)
- Chatterbox guidance: use a reference clip in the target language; set `cfg_weight=0` if accent transfer happens. — [Mintlify docs mirror](https://www.mintlify.com/yocxy2/chatterboxyocxy/models/chatterbox-multilingual)
- An earlier Hebrew provider snapshot rated Chatterbox (via Replicate) "Poor": output sounded generic and the clone did not carry into Hebrew. The page says it is dated 22 March 2025, which conflicts with Chatterbox Multilingual's September 2025 release, so the date is likely wrong and it predates the v3 weights. — [Hebrew-TTS-Providers](https://github.com/danielrosehill/Hebrew-TTS-Providers)
- Phonikud is an open Hebrew G2P that outputs full IPA with vowels and stress; its authors report small local TTS models with Phonikud input approach large proprietary systems. — [Phonikud arXiv](https://arxiv.org/abs/2506.12311); [phonikud.github.io](https://phonikud.github.io/)
- Zonos-Hebrew fine-tunes Zonos-v0.1 on SASPEECH with a Phonikud phoneme front end and supports zero-shot cloning. — [Medium write-up](https://medium.com/@maxme006/zonos-hebrew-fine-tuning-zonos-on-saspeech-with-a-phonikud-phoneme-pipeline-397e6d5717c8)
- SASPEECH (OpenSLR 134) is the public single-speaker Hebrew corpus most of these fine-tunes use; Robo-Shaul is an older project on it. — [Sharoni et al. Interspeech 2023](https://www.isca-archive.org/interspeech_2023/sharoni23_interspeech.pdf); [roboshaul GitHub](https://github.com/Sharonio/roboshaul)
- XTTS-v2 supports 17 languages and Hebrew is not one of them. — [XTTS-v2 model card](https://huggingface.co/coqui/XTTS-v2/raw/v2.0.3/README.md)
- A Hebrew LoRA exists for NeuTTS Air (flowty1/neutts-air-he) with instant cloning. — [neutts-air-he](https://huggingface.co/flowty1/neutts-air-he)
- A Hebrew LoRA for Fish Audio S2-Pro exists, described by its author as early, non-commercial (CC BY-NC-SA 4.0). — [Fish-Audio-S2-Pro-He](https://huggingface.co/notmax123/Fish-Audio-S2-Pro-He)

### Inferences
- Realistic local ranking for this user (own-voice cloning, Hebrew, 16 GB): 1) QwenTTS-he 1.7B, 2) F5-TTS Hebrew v2, 3) Chatterbox Multilingual v3 with manual nikud, 4) Zonos-Hebrew. This ranking leans on one tester's notes ("clearest") and the absence of failures, not on a published blind test of cloned voices.
- Feeding text with corrected nikud (Dicta Nakdan, then hand-fixing) is likely the single biggest quality lever for any local model.
- CosyVoice 2/3, IndexTTS2 and OmniVoice are trained mainly on Chinese/English and are not worth testing for Hebrew.

### Gaps
- No independent blind test of cloned Hebrew voices (as opposed to stock voices) was found for any local model.
- Exact VRAM and quality of QwenTTS-he and F5-TTS Hebrew v2 model cards could not be read (huggingface.co was blocked).
- No information found on CosyVoice 3, IndexTTS2 or Higgs Audio Hebrew quality beyond the one "garbled words" note for Higgs v3.

## Can a model be fine-tuned on hours of the user's own voice, and does it fit 16 GB?

### Takeaway
Yes. F5-TTS, Chatterbox (via LoRA) and QwenTTS-style LoRAs all support fine-tuning; 30 minutes to a few hours of clean single-speaker audio is the range people use. Fine-tuning captures rhythm and pronunciation, not just timbre, which matters for sounding "exactly like" the user. All the candidate models are small enough (roughly 2.5 to 7 GB at inference) for an RTX 5080 16 GB; training VRAM was not documented.

### Cited Findings
- A Runpod tutorial fine-tunes F5-TTS on about 30 minutes of one person's speech and notes that fine-tuning also learns rhythm and pronunciation. — [Runpod blog](https://www.runpod.io/blog/clone-your-voice-f5-tts)
- Fine-tune pitfalls reported: models producing only noise, and a reference with no pauses leads to output with no pauses. — [Towards AI write-up](https://pub.towardsai.net/what-i-got-wrong-fine-tuning-f5-tts-for-a-new-writing-system-ce2576bddbb0); [F5-TTS discussion](https://github.com/SWivid/F5-TTS/discussions/1168)
- Chatterbox Multilingual has community LoRA fine-tunes (Amharic about 193 h, Uzbek 111 h, Estonian, Indic rank-32 on the T3 backbone). The base stays MIT; adapters inherit the licence of their training data. — [chatterbox-amharic](https://huggingface.co/gabar-tech/chatterbox-amharic); [Uzbek-tts-chatterbox](https://huggingface.co/UAzimov/Uzbek-tts-chatterbox); [chatterbox-indic-lora](https://huggingface.co/reenigne314/chatterbox-indic-lora); [DEV write-up](https://dev.to/pekisko/fine-tuning-chatterbox-on-a-low-resource-language-7-things-that-mattered-13e1)
- Approximate inference VRAM: Chatterbox about 4 GB, ZONOS3-Mini 3.4 GB, voxtream2-he 2.5 GB, VibeVoice 1.5B about 7 GB / 7B about 19 GB, Fish Drama 3 up to 21 GB. Hebrew Voice Studio was tested on RTX 5090 with the CUDA 12.8 PyTorch build, and its Docker image supports RTX 50xx. — [hebrew-voice-studio](https://github.com/tm1981/hebrew-voice-studio)
- Hebrew Voice Studio accepts up to five reference recordings per voice and can trim and level them. — [hebrew-voice-studio](https://github.com/tm1981/hebrew-voice-studio)
- Whisper large-v3-turbo Hebrew fine-tune from ivrit-ai is available for transcribing recordings (useful for building a training set of audio plus text). — [hebrew-voice-studio](https://github.com/tm1981/hebrew-voice-studio)

### Inferences
- Best plan for the user's many studio hours: cut 1 to 5 hours into 5 to 15 second clips, transcribe with ivrit-ai Whisper, add nikud, then fine-tune F5-TTS Hebrew v2 or a QwenTTS-he LoRA on that set. This is a mid-level technical job, not a non-programmer task.
- The GTX 1050 is only useful for CPU-class models (BlueTTS, Kokoro); it is not useful for cloning or training.
- Blackwell (RTX 50xx) needs CUDA 12.8 builds of PyTorch; older install guides for these models may fail on it.

### Gaps
- No source gave training VRAM or training time for any Hebrew fine-tune on a 16 GB card.
- No source gave a minimum hours figure for a single-speaker Hebrew voice fine-tune.

## How good is the voice conversion route (RVC / Seed-VC / OpenVoice) for Hebrew?

### Takeaway
No Hebrew-specific test was found. Voice conversion is language-agnostic in principle (it copies timbre onto existing speech), so pairing a good Hebrew TTS voice (cloud or local) with an RVC model trained on the user's hours could work, but accent, rhythm and stress come from the source speech, not the user.

### Cited Findings
- Seed-VC's own evaluation reports better intelligibility and speaker similarity than baselines, with slightly lower audio quality (DNSMOS) than RVCv2; the test set is English and singing. — [Seed-VC EVAL.md](https://raw.githubusercontent.com/Plachtaa/seed-vc/51383ef/EVAL.md)
- Seed-VC clones from a 1 to 30 second reference without training; RVCv2 baselines are trained per speaker. — [Seed-VC README](https://raw.githubusercontent.com/Plachtaa/seed-vc/main/README.md)

### Inferences
- RVC trained on 30 to 60 minutes of the user's studio audio is a strong timbre match and runs fine on 16 GB; it is likely the easiest fix if a TTS gets Hebrew prosody right but the voice is only "similar."
- The source voice should be the same gender and similar pitch range as the user for best results.

### Gaps
- No Hebrew listening tests for RVC, Seed-VC or OpenVoice were found.

## Cloud options: Hebrew quality, own-voice cloning, and cost per hour

### Takeaway
ElevenLabs is the safest cloud route for "my own voice in Hebrew": Professional Voice Cloning (from Creator $22/month) is trained on the user's hours, and ElevenLabs v3/v4 ranked near the top in the 2026 Hebrew bake-off. Estimated cost is about $5 to $10 per hour of narration. MiniMax and Fish are cheaper per hour but less proven for Hebrew cloning. Gemini TTS sounds best in Hebrew but offers preset voices, not own-voice cloning.

### Cited Findings
- ElevenLabs plans (Nov 2026): Free $0 / 10k credits, Starter $6 / 30k, Creator $22 / 121k ($11 first month), Pro $99 / 600k, Scale $299 / 1.8M, Business $990. Older guides list different numbers. — [ElevenLabs pricing (de)](https://elevenlabs.io/de/pricing); [DEV summary](https://dev.to/techsifted/elevenlabs-pricing-2026-plans-credits-and-api-costs-explained-1549)
- Multilingual v2/v3 cost 1 credit per character; API rate about $0.08 per 1,000 characters (Flash/Turbo about $0.04). — [ElevenLabs v3 cost help](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-much-does-it-cost-to-generate-using-eleven-v3-alpha); [BigVU](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/)
- PVC requires Creator or higher; Creator, Pro and legacy Scale have 1 PVC slot; PVC can only clone your own voice. Paid plans include a commercial licence; Free does not. — [ElevenLabs PVC slots help](https://elevenlabs.io/docs/help-center/product/voices/voice-cloning/how-many-professional-voice-clones-pv-cs-can-i-have); [BigVU](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/)
- PVC supports all languages in the Eleven v4 family (90+); a secondary source says that since 2026-11-02 PVCs can be fine-tuned on v4. Hebrew was not explicitly confirmed in the snippets. — [ElevenLabs PVC languages](https://elevenlabs.io/docs/help-center/product/voices/voice-cloning/what-languages-are-supported-with-professional-voice-cloning-pvc); [secondary blog via search](https://magichour.ai/blog/elevenlabs-pricing)
- ElevenLabs Hebrew needs `eleven_v3` with `language_code: "he"`; Multilingual v2 was "unintelligible" in Hebrew in an earlier snapshot. — [Hebrew-TTS-Providers](https://github.com/danielrosehill/Hebrew-TTS-Providers)
- ElevenLabs v4 (Rachel) was unbeaten in the 2026-11-18 Hebrew female arena; cost about $0.08 per 1,000 characters. — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- Gemini 3.1 Flash TTS won both Hebrew arena brackets (with nikud), about $0.033 per 1,000 characters; Gemini 3.8 Flash Lite about $0.010. — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- MiniMax was rated "Best" for Hebrew in the earlier snapshot, with cloned voices sounding natural in Hebrew. — [Hebrew-TTS-Providers](https://github.com/danielrosehill/Hebrew-TTS-Providers)
- MiniMax Speech 2.8: HD $100 / Turbo $60 per million characters (official pay-as-you-go); Hebrew is in the language list; rapid voice clone reported at $1.50 per voice (third-party, unverified). — [MiniMax pricing](https://platform.minimax.io/docs/guides/pricing-paygo.md); [fal.ai listing](https://fal.ai/models/fal-ai/minimax/speech-2.8-hd/llms.txt); [invideo](https://invideo.io/blog/minimax-ai-voice-models/)
- Fish Audio S2 Pro API: $15 per million UTF-8 bytes; instant clone from about 10 s, professional clone from 10 to 180 minutes of audio. — [OpenRouter](https://openrouter.ai/fish-audio/s2-pro/api); [usecarly](https://www.usecarly.com/blog/fish-audio/)
- Resemble AI: Hebrew preset voice "usable but limited"; custom clones "unintelligible without nekudot" in the earlier snapshot. — [Hebrew-TTS-Providers](https://github.com/danielrosehill/Hebrew-TTS-Providers)
- Google Cloud Instant Custom Voice about $60 per million characters; Hebrew support for Chirp 3 HD / instant custom voice could not be confirmed. Google Cloud TTS was flagged for mispronunciation in the bake-off. — [Google TTS pricing](https://cloud.google.com/text-to-speech/pricing); [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- Azure Professional custom neural voice is billed per minute or per character plus hourly endpoint hosting; actual figures and he-IL availability were not visible. — [Azure Speech pricing](https://azure.microsoft.com/pricing/details/speech/)
- Microsoft Edge TTS (Avri, Hila) rated "Good" and free, but no cloning. — [Hebrew-TTS-Providers](https://github.com/danielrosehill/Hebrew-TTS-Providers)

### Inferences (cost per hour, at about 60k characters per hour)
- ElevenLabs Pro $99 for 600k credits is about 10 hours, so roughly $10 per hour; Scale $299 for 1.8M is about 30 hours (about $10 per hour); API at $0.08 per 1k is about $4.80 per hour.
- A 20-hour course on ElevenLabs is roughly $100 to $200 total with retakes.
- MiniMax HD about $6 per hour, Turbo about $3.60 per hour.
- Fish S2 Pro: Hebrew letters are 2 bytes in UTF-8, so about $30 per million characters, about $1.80 per hour (but Hebrew clone quality unproven).
- Gemini 3.1 Flash TTS about $2 per hour, but stock voices only; could be paired with RVC for the user's timbre.

### Gaps
- No source tested ElevenLabs PVC (as opposed to stock voices) in Hebrew.
- Cartesia and Play.ht Hebrew support and prices were not researched within the tool budget.
- Azure he-IL custom voice price and availability unknown.

## Licences for commercial course use

### Takeaway
Commercially safe: ElevenLabs paid plans, MiniMax, Chatterbox (MIT), QwenTTS-he (Apache 2.0), BlueTTS (MIT), VibeVoice (MIT). Not safe for a paid course: Kokoro-Hebrew, Zonos-Hebrew, OmniVoice, Higgs Audio, Fish S2 Pro Hebrew LoRA, Fish Drama 3, Phonikud. F5-TTS Hebrew is unclear.

### Cited Findings
- Non-commercial: Kokoro (SASPEECH terms), OmniVoice (CC BY-NC), Higgs (research/non-commercial), Breeze TTS 2, Zonos-Hebrew (CC BY-NC 4.0). Drama 3: Fish Audio Community License (personal/non-commercial). F5-TTS Hebrew: Apache 2.0 but its base weights are CC BY-NC 4.0, so commercial use is unclear. voxtream2-he: GPL-3.0. MIT: LightBlue, Blue 2.5, VibeVoice, Ming. Apache 2.0: QwenTTS-he, ZONOS3-Mini, ivrit-ai Whisper. Magpie: NVIDIA Open Model License. — [hebrew-voice-studio](https://github.com/tm1981/hebrew-voice-studio)
- Phonikud, Kokoro-Hebrew, OmniVoice and Fish S2 Pro flagged non-commercial. — [Hebrew-TTS-Bakeoff-1126](https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126)
- Chatterbox base code and weights are MIT; adapters inherit their data licence. — [Uzbek-tts-chatterbox](https://huggingface.co/UAzimov/Uzbek-tts-chatterbox)

### Inferences
- Cloning one's own voice removes the consent issue; the remaining risk is the model licence and any SASPEECH-derived weights.
- QwenTTS-he's Qwen3-TTS base licence should be checked, since the LoRA is Apache 2.0 but the card could not be read.

### Gaps
- SASPEECH's own licence terms were not checked directly.

## Easiest setup for a non-programmer on Windows

### Takeaway
Easiest overall: ElevenLabs website (upload recordings, PVC, type text, download). Easiest local: Hebrew Voice Studio, which bundles QwenTTS-he, Chatterbox, F5-TTS Hebrew and others behind one web UI at http://localhost:8010, but setup still needs Miniconda or Docker commands.

### Cited Findings
- Hebrew Voice Studio Windows setup: install Miniconda and Git, create a conda env, `pip install` from a lock file, run `fetch_vendor.py`, optional per-engine envs, then `start.bat` and open `http://localhost:8010`. Docker alternative: one `docker run --gpus all` command with a 9.4 GB image; models about 75 GB with all engines. — [hebrew-voice-studio](https://github.com/tm1981/hebrew-voice-studio)
- Some models need accepting terms on Hugging Face and `hf auth login`. — [hebrew-voice-studio](https://github.com/tm1981/hebrew-voice-studio)

### Inferences
- Suggested path: 1) try ElevenLabs Creator ($11 first month) with PVC on 1 to 3 hours of the studio audio and judge Hebrew output; 2) in parallel test QwenTTS-he and F5 Hebrew in Hebrew Voice Studio on the RTX 5080 with zero-shot reference clips; 3) only if local is close, fine-tune; 4) use RVC trained on the user's voice as a fixer for any good-prosody but wrong-timbre output.
- Always prepare text with nikud and check stress on tricky words, whichever tool is used.

### Gaps
- No one-click Windows installer (like Pinokio) for the Hebrew fine-tunes was confirmed.
