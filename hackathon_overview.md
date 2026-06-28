# Hackathon Overview: "Local AI"

🧠 **THE CPU-FIRST HACKATHON**
_Build AI that runs anywhere._

GPUs are scarce, costly and online. Most computing isn't. This is a demonstration that *the CPU is enough* — and the best apps keep working when the network doesn't.

*Your mission:* turn unstructured input (docs, images, audio, video, text) into clean *structured data*. Build it as a *CLI* app. Run inference on *CPU*. Make it work *offline*.

## ⚙️ THE RULES
• **CPU-first** — no GPU/CUDA. Declare your model + runtime (faster-whisper, llama.cpp CPU).
• **Offline-first** — core feature works with *no cloud calls*. Demo must show it running with the network OFF.
• **Free and Open Source Software** LICENSE file. Must be strong copyleft (e.g. GPLv3).

## 📋 PHASE 1 — Plan & Spec (Submit Before 10AM)
GitLab/Swecha repo with:
• README with your idea
• Spec kit
• Issues w/ assignee + estimate + due date
• Work-division plan

## 🚀 PHASE 2 — MVP (Submit before lunch Break)
Working demo on real records:
• CLI → submit CLI build version.

## 🔍 PHASE 3 — Repo Audit (all green) (Submit before 3PM)
Metadata + README, CONTRIBUTING, CHANGELOG + pre-commit & CI: formatting, lint, type-check, security scan, semantic commits etc. At least 10 checks, all run on local gitlab runner.

⚠️ *Faking the checklist = malpractice.* Stub jobs (echo/print, exit 0, disabled steps) that look green without real checks → *disqualification or penalty.*

Pick a hard, real problem. Make it run on a laptop with the Wi-Fi off. 🚀
