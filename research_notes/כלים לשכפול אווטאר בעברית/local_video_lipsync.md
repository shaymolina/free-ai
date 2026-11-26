# Local open-source lip-sync and talking-head tools for a "digital twin" (as of Nov 2026)

Research note: WebFetch could not reach arxiv.org, ltx.io and instavar.com from this session (network block), so findings come from search-result summaries of those pages, not full reads. Numbers from vendor blogs (sync.so, ltx.io, creeta, pixazo, talking-avatar.dev) should be treated with caution.

## Which models look most real on real footage (teeth, mouth, identity)?

### Takeaway
For re-dubbing existing studio footage (keep the real person, change only the mouth), the 2026 frontier has moved to video-DiT "mask-free" dubbing models (X-Dub, TBDub, LipForcing, InfiniteTalk V2V, LTX Dub-It), but the most-cited proven local workhorse is still LatentSync 1.6, with MuseTalk 1.5 as the fast/lighter option and Wav2Lip clearly outdated for HD. Full audio-driven generators (Wan2.2-S2V, InfiniteTalk, HunyuanVideo-Avatar) regenerate the whole frame, which raises identity and consistency risk for a "must not look AI" goal.

### Cited Findings
Video-to-video lip-sync (re-dubbing):
- LatentSync is generally seen as the quality pick and MuseTalk as the speed pick; a practitioner test called LatentSync 1.6 "still the local model to beat" for short dubbing — [sync.so](https://sync.so/blog/the-best-free-open-source-lipsync-tools-2), [Instavar](https://instavar.com/research/ai-video/open-source-lip-sync-models)
- LatentSync 1.6 was trained on 512x512 video specifically to fix the blurry teeth and lips of 1.5; the only change from 1.5 is the training data — [ByteDance HF model card](https://huggingface.co/ByteDance/LatentSync-1.6), [GitHub](https://github.com/bytedance/LatentSync)
- The LatentSync paper itself admits flicker in high-frequency details (teeth, lips, facial hair) — [arXiv 2412.09262](https://arxiv.org/html/2412.09262v2)
- In the MuseTalk paper's own comparisons, LatentSync had the best LSE-C (7.90 on HDTF) and scored higher than MuseTalk in the user study on lip-sync quality (4.07 vs 3.77) — [MuseTalk arXiv](https://arxiv.org/html/2410.10122v3)
- MuseTalk works on a 256x256 face region via one-step latent inpainting, 30 FPS on a V100; a critical comparison says it does not preserve facial features well — [MuseTalk arXiv](https://arxiv.org/pdf/2410.10122), [sync.so](https://sync.so/blog/what-is-musetalk), [ltx.io](https://ltx.io/blog/open-source-lip-sync-models)
- Wav2Lip is still cited for sync accuracy but is soft/blurry on HD footage — [sync.so](https://sync.so/blog/the-best-free-open-source-lipsync-tools-2)
- X-Dub (Kling Team / Kuaishou, ICML 2026): mask-free visual dubbing with a DiT editor that takes the full video as input; code listed at github.com/KlingAIResearch/X-Dub; a third-party wiki says weights are on HF (KlingTeam/X-Dub), inference-only, and built on Wan2.2 (not verified) — [ICML poster](https://icml.cc/virtual/2026/poster/64235), [arXiv 2512.25066](https://arxiv.org/abs/2512.25066), [demo](https://hjrphoebus.github.io/X-Dub), [wiki](https://knowledge-space.pages.dev/image-generation/X-Dub)
- TBDub (Sept 2026) is a production-oriented extension of X-Dub; in MOS it beats X-Dub by +0.14 lip-sync, +0.95 identity, +0.90 visual quality; 2-step distilled student hits 7.13 effective FPS at 512x512 on an H20; weights on HF under Apache-2.0 (Release V1.1). Author-reported only, no independent replication found — [arXiv 2609.06144](https://arxiv.org/html/2609.06144v1), [HF TaoLiveAIGC/TBDub](https://huggingface.co/TaoLiveAIGC/TBDub), [InsightFace blog](https://www.insightface.ai/blog/september-2026-face-swapping-papers)
- InsightFace notes the 7.13 FPS covers only the generation core, not tracking, compositing, encoding or long-video stability — [InsightFace blog](https://www.insightface.ai/blog/september-2026-face-swapping-papers)
- LipForcing (KAIST, June 2026): first autoregressive diffusion V2V lip-sync, distilled from a 14B teacher into 2-step students; 1.3B student 31 FPS, 14B student 15.11 FPS; code and checkpoints released; needs Wan2.1 components and SyncNet; license not confirmed — [arXiv 2606.11180](https://arxiv.org/html/2606.11180v1), [GitHub](https://github.com/cvlab-kaist/LipForcing), [HF](https://huggingface.co/JinhyukJang/lipforcing)
- LTX Dub-It (LTX-2.5 IC-LoRA) is a mask-free option that keeps the whole video except the lip region; LTX-2.5 talking-head use needs 32GB+ VRAM per the guide — [ltx.io](https://ltx.io/blog/open-source-lip-sync-models)
- Newer research specifically targeting mouth interiors: "Beyond Lip Sync: Reference-Grounded Oral Refinement" (Sept 2026) and VidDub (Nov 2026); availability of code not checked — [arXiv 2609.38019](https://arxiv.org/html/2609.38019v1), [arXiv 2611.03404](https://arxiv.org/pdf/2611.03404)

Audio-driven full talking-head generation:
- InfiniteTalk (MeiGen-AI) does sparse-frame video dubbing: new video with lip sync plus aligned head, body and expressions, preserving identity, background and camera movement from the source video; has streaming mode for long video — [GitHub](https://github.com/MeiGen-AI/InfiniteTalk), [arXiv 2508.14033](https://arxiv.org/abs/2508.14033v1)
- An InfiniteTalk review says lip timing is usable for clear single-speaker audio but should be judged as lip-sync, not full facial acting — [infinitetalk.net review](https://www.infinitetalk.net/blog/infinitetalk-vs-lipforcing-review)
- Wan-S2V paper (Alibaba) claims to beat Hunyuan-Avatar and OmniHuman and says Hunyuan-Avatar often shows facial distortion and identity drift in large movements (developer claim) — [arXiv 2508.18621](https://arxiv.org/html/2508.18621v1)
- A hobbyist RTX 4090 test found S2V promising on audio reactivity but weak on FPS (locked 16 FPS) and long-term consistency; MultiTalk ran 25 FPS — [Civitai article](https://civitai.com/articles/18873)

### Inferences
- For "must not look AI" on real studio footage, mouth-only re-dubbing (LatentSync 1.6, TBDub/X-Dub, LipForcing) is safer than full-frame generators, since everything outside the mouth stays real pixels.
- Ranked shortlist for this user: 1) LatentSync 1.6 (proven, ComfyUI, but VRAM tight); 2) TBDub / X-Dub (newest, best reported identity, but heavy DiT and unproven on consumer GPUs); 3) InfiniteTalk V2V via Wan2GP (adds natural head/body motion, low-VRAM path, but license issue); 4) LipForcing 1.3B (fast, new); 5) MuseTalk 1.5 (fast, commercial-friendly, but 256px face is soft at 1080p); outdated: Wav2Lip, VideoReTalking, Diff2Lip.
- 1080p: all of these work on a face crop (256 or 512 px) and paste it back, so a 1080p frame with a close-up face upsamples the mouth crop; a face restorer (e.g. GFPGAN/CodeFormer) pass is commonly added but can look "AI-smooth".

### Gaps
- No independent head-to-head benchmark found of TBDub/X-Dub/LipForcing vs LatentSync 1.6 on consumer hardware.
- Could not read full pages (arxiv/ltx/instavar blocked), so exact tables were not extracted.
- Did not check Hallo2/Hallo3, EchoMimic v2/v3, FantasyTalking, Sonic, OmniAvatar, MiniMax H3; these are image-driven and less suited to re-dubbing existing footage.

## Do they run on RTX 5080 16GB (Blackwell)? Speed?

### Takeaway
Blackwell works once PyTorch cu128 builds with sm_120 are installed; the main hard limit is VRAM: LatentSync 1.6 lists 18GB minimum (over 16GB), LatentSync 1.5 needs 8GB, and Wan-based models (InfiniteTalk, S2V) need low-VRAM tricks (Wan2GP, quantization, offload).

### Cited Findings
- LatentSync minimum inference VRAM: 8GB for 1.5, 18GB for 1.6 — [GitHub README](https://github.com/bytedance/LatentSync), [creeta](https://news.creeta.com/en/open-source-lip-sync-models-2026/)
- A third-party table lists LatentSync 1.6 at about 6 FPS — [creeta via search summary](https://news.creeta.com/en/open-source-lip-sync-models-2026/)
- Blackwell "no kernel image" errors come from old PyTorch builds; fix is a cu128 build with sm_120 in `torch.cuda.get_arch_list()`; a MuseTalk user fixed it with PyTorch 2.9.1+cu128 and had to build mmcv 2.1.0 from source (mmdet 3.2.0, mmpose 1.1.0) — [PyTorch forum](https://discuss.pytorch.org/t/pytorch-support-for-sm120/216099), [NVIDIA forum](https://forums.developer.nvidia.com/t/im-facing-a-cuda-compatibility-issue-with-my-new-rtx-5080-in-deep-learning/347350)
- On Windows a separate "sm_120 is not defined for option gpu-name" error comes from Triton's ptxas and needs a Triton update — [PyTorch forum](https://discuss.pytorch.org/t/rtx-5070-ti-blackwell-pytorch-nightly-triton-still-getting-sm-120-is-not-defined-for-option-gpu-name-error/220460)
- ComfyUI has an official Blackwell support thread — [ComfyUI discussion #6643](https://github.com/Comfy-Org/ComfyUI/discussions/6643)
- InfiniteTalk has very-low-VRAM mode (persistent DiT params = 0), CPU offload and quantized models; Wan2GP integrated it optimized for low VRAM — [GitHub](https://github.com/MeiGen-AI/InfiniteTalk)
- InfiniteTalk v1.5 switched to Whisper-Large audio encoder and 8-step distillation; Audio CFG 3-5 recommended — [search summary of InfiniteTalk materials](https://github.com/MeiGen-AI/InfiniteTalk)
- MultiTalk (InfiniteTalk's predecessor) on RTX 4090: 24GB, 8GB possible with persistence=0; 1365 frames at 25 FPS (about 55s) took 12 minutes, roughly 13 min render per minute of video — [Civitai](https://civitai.com/articles/18873)
- An 8GB RTX 4070 user reported about 10+ min per InfiniteTalk lip-sync clip (different workflow) — [note.com](https://note.com/luta_ai/n/ne0898fa5faf9?hl=en)
- Wan2.2 official: 24GB+ (e.g. 4090); HunyuanVideo-Avatar: 24GB minimum, 96GB recommended — [Wan2.2 docs](https://docsearch.algolia.com/mcp/docs/repo/wan-video/wan2.2), [osrepos](https://osrepos.com/compare/tencent-hunyuan-hunyuanvideo-avatar-vs-wan-video-wan2.2)
- LatentSync ComfyUI wrapper exists (unofficial, Windows/WSL) — [ComfyUI-LatentSyncWrapper](https://github.com/ShmuelRonen/ComfyUI-LatentSyncWrapper)

### Inferences
- LatentSync 1.6 at 18GB will likely OOM on 16GB without fp16/VAE tiling tricks; worth testing, else fall back to 1.5.
- HunyuanVideo-Avatar is not realistic on 16GB; skip.
- With time not a constraint, Wan2GP InfiniteTalk at 480p-720p on a 5080 is plausible overnight for 10-20 min, based on the 4090 MultiTalk rate.

### Gaps
- No measured RTX 5080 timings found for any model.
- No confirmed 16GB run of TBDub/X-Dub/LipForcing 14B.

## Long videos (10-20 min lessons)

### Takeaway
InfiniteTalk is the only one explicitly designed for unlimited length (streaming mode); for the mouth-only models the practical approach is to split by scene/sentence and stitch.

### Cited Findings
- InfiniteTalk: `--mode streaming` for long video, `--mode clip` for single chunk — [GitHub](https://github.com/MeiGen-AI/InfiniteTalk)
- A user tested a 2.5-minute InfiniteTalk lip-sync at 480p (about an hour on A100 including setup) — [note.com Baku](https://note.com/bakushu/n/n6ca5649ac048?hl=en)
- Wan2.2-S2V struggles with long-term consistency — [Civitai](https://civitai.com/articles/18873)
- Long-video stability is a stated production concern even for TBDub — [InsightFace blog](https://www.insightface.ai/blog/september-2026-face-swapping-papers)

### Inferences
- Lesson edits naturally cut on sentences, so chunking into 20-60s pieces with cuts at camera/b-roll moments hides seams.

### Gaps
- No published LatentSync long-video tests found.

## Hebrew / non-English audio

### Takeaway
No Hebrew benchmark exists; evidence shows English-trained models degrade on other languages, so test on real Hebrew clips before committing.

### Cited Findings
- A 2024 MDPI study built a framework to evaluate two lip-sync models on Turkish, Persian and Arabic — [MDPI Computers 14(1):7](https://mdpi.com/2073-431X/14/1/7)
- Wav2Lip on non-English speech showed abrupt mouth closings and minimal movement — [arXiv 2205.06421](https://arxiv.org/pdf/2205.06421)
- A 2025 paper says talking-face models do well in English but give wrong mouth shapes and rigid expressions in other languages due to English-dominated data — [arXiv 2510.06612](https://arxiv.org/html/2510.06612v1)
- VoxDub (Oct 2026) is a new bilingual lip-synced dubbing dataset, showing this is still an open area — [arXiv 2610.25259](https://arxiv.org/pdf/2610.25259)

### Inferences
- Models using Whisper audio features (LatentSync, MuseTalk, InfiniteTalk v1.5) are likely more language-robust than Wav2Lip's mel/SyncNet setup, since Whisper is multilingual; this is not confirmed for Hebrew.

### Gaps
- No Hebrew-specific user reports found.

## Fine-tuning on the user's own footage

### Takeaway
LatentSync supports training (including its own SyncNet) on custom data, but needs about 20GB+ VRAM; diffusion lip-sync is designed to work without per-person fine-tuning.

### Cited Findings
- LatentSync stage-2 training of only temporal and audio cross-attention layers brings VRAM to about 20GB; repo includes a script to train SyncNet on your own dataset — [GitHub](https://github.com/bytedance/LatentSync)
- The paper says diffusion lip-sync generalizes across identities without per-identity fine-tuning — [arXiv 2412.09262](https://arxiv.org/html/2412.09262v2)
- X-Dub released inference-only (no training code), per third-party wiki — [wiki](https://knowledge-space.pages.dev/image-generation/X-Dub)

### Inferences
- 20GB training will not fit the 5080; renting a cloud GPU for a few hours is the cheap path if fine-tuning is wanted.

### Gaps
- No Reddit or community reports found on person-specific LatentSync fine-tuning results.

## Is the GTX 1050 useful?

### Takeaway
Not for generation.

### Cited Findings
- Smallest VRAM needs found: LatentSync 1.5 8GB, MultiTalk 8GB with persistence=0 — [GitHub LatentSync](https://github.com/bytedance/LatentSync), [Civitai](https://civitai.com/articles/18873)

### Inferences
- The GTX 1050 (2-4GB, Pascal) is below every minimum; at most it could run ffmpeg cutting/encoding or audio prep.

### Gaps
- No direct source tested these models on a GTX 1050.

## Licenses (paid course)

### Takeaway
MuseTalk and TBDub look commercial-friendly; LatentSync weights carry OpenRAIL++ use restrictions (usually still commercial-OK); InfiniteTalk's own page says outputs are academic-only, so it is risky for a paid course.

### Cited Findings
- LatentSync code Apache-2.0; 1.6 weights listed as OpenRAIL++ — [GitHub](https://github.com/bytedance/LatentSync), [HF model card](https://huggingface.co/ByteDance/LatentSync-1.6)
- MuseTalk: MIT per one comparison, with trained model allowed for any purpose including commercial; a Gitee mirror lists BSD-3-Clause — [sync.so](https://sync.so/blog/what-is-musetalk), [Gitee](https://gitee.com/singray/MuseTalk)
- InfiniteTalk: weights Apache-2.0 on HF, but the project page says generated content is for academic use only and commercial use is not permitted — [HF](https://huggingface.co/MeiGen-AI/InfiniteTalk), [project page](https://meigen-ai.github.io/InfiniteTalk)
- TBDub: Apache-2.0 on HF — [HF](https://huggingface.co/TaoLiveAIGC/TBDub)
- HunyuanVideo-Avatar: license unclear (NOASSERTION); Tencent Hunyuan community licenses exclude some territories — [osrepos](https://osrepos.com/compare/meigen-ai-infinitetalk-vs-tencent-hunyuan-hunyuanvideo-avatar), [deepwiki](https://deepwiki.com/Tencent/HunyuanVideo/5-license-and-legal)

### Gaps
- LipForcing and X-Dub licenses not confirmed.

## Easiest install for a non-programmer (Windows)

### Takeaway
Pinokio (one-click) with Wan2GP is the easiest path for InfiniteTalk; LatentSync is easiest through ComfyUI (Desktop/portable) plus the LatentSyncWrapper node.

### Cited Findings
- Pinokio installs AI apps locally in one click on Windows via Discover > Install — [Pinokio guide](https://pasqualepillitteri.it/en/news/9050/pinokio-ai-browser-install-guide)
- Wan2GP has a Pinokio listing and standalone Windows launchers; tip: short path without spaces, Defender may false-flag the installer — [Wan2GP desktop](https://github.com/GKartist75/wan2gp-desktop), [jdhodges guide](https://www.jdhodges.com/?p=11439)
- InfiniteTalk is integrated in Wan2GP — [GitHub](https://github.com/MeiGen-AI/InfiniteTalk)
- LatentSync ComfyUI wrapper for Windows/WSL needs access to the ByteDance HF repo for downloads — [ComfyUI-LatentSyncWrapper](https://github.com/ShmuelRonen/ComfyUI-LatentSyncWrapper)

### Gaps
- Could not confirm Pinokio listings for LatentSync, MuseTalk, TBDub or LipForcing.
