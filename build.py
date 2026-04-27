#!/usr/bin/env python3
"""Build static multi-page site for Faith Pleases God from the design source."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = Path("/tmp/fpg-design/faith-pleases-god/project/site.html")
SYS = ROOT / "system"
SYS.mkdir(exist_ok=True)

# Cache-busting version — changes on every build so immutable CSS caches invalidate
import time
CSS_VER = str(int(time.time()))

raw = SRC.read_text()

# ---------- Extract the inline <style> block into system/site.css ----------
style_match = re.search(r"<style>(.*?)</style>", raw, re.DOTALL)

JP_CSS = """
/* ===========================================================
   JESUSPOD — brand-accurate: pure black + saturated red, no gold
   Brand refs: #0a0a0a bg, #DC2626 accent, rounded cards, pill filters
   =========================================================== */
.jp-scope {
  --jp-bg:        #0a0a0a;
  --jp-bg-2:      #141414;
  --jp-card:      #1c1c1c;
  --jp-card-2:    #242424;
  --jp-rule:      #2a2a2a;
  --jp-red:       #DC2626;
  --jp-red-dark:  #B91C1C;
  --jp-red-soft:  #EF4444;
  --jp-text:      #FAFAFA;
  --jp-text-2:    #C9C9C9;
  --jp-text-3:    #8A8A8A;
  --jp-font-ui:   'Inter', 'Geist', -apple-system, sans-serif;
}

/* ---------- HOME BAND (full-bleed) ------------------------- */
.jp-band {
  --jp-bg: #0a0a0a;
  --jp-red: #DC2626;
  --jp-text: #FAFAFA;
  --jp-text-2: #C9C9C9;
  --jp-text-3: #8A8A8A;
  background: var(--jp-bg);
  color: var(--jp-text);
  margin: 0 calc(-50vw + 50%);
  padding: var(--s-9) calc(50vw - 660px);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', 'Geist', sans-serif;
}
.jp-band::before {
  content: ""; position: absolute; inset: 0;
  background: radial-gradient(circle at 90% 10%, rgba(220,38,38,0.18), transparent 50%);
  pointer-events: none;
}
.jp-band__wrap {
  position: relative;
  display: grid; grid-template-columns: 1.25fr 1fr;
  gap: var(--s-8);
  align-items: center;
}
.jp-band__wordmark {
  display: inline-flex; align-items: center; gap: 10px;
  margin-bottom: var(--s-5);
  font-family: 'Inter', 'Geist', sans-serif;
  font-weight: 800; font-size: 18px; letter-spacing: -0.01em;
  color: var(--jp-text);
}
.jp-band__wordmark::before {
  content: ""; width: 26px; height: 26px;
  border-radius: 999px; background: var(--jp-red);
  flex-shrink: 0;
  box-shadow: 0 0 0 4px rgba(220,38,38,0.2);
}
.jp-band__wordmark span.pod { color: var(--jp-red); }
.jp-band__kicker {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px;
  background: rgba(220,38,38,0.12);
  color: var(--jp-red-soft);
  border: 1px solid rgba(220,38,38,0.3);
  border-radius: 999px;
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 12px; font-weight: 500; letter-spacing: 0.02em;
  margin-bottom: var(--s-5);
}
.jp-band__title {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: clamp(40px, 5.5vw, 76px);
  line-height: 1.02; letter-spacing: -0.035em;
  font-weight: 700; color: var(--jp-text);
}
.jp-band__title em { font-style: normal; color: var(--jp-red); font-weight: 700; }
.jp-band__lede {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: clamp(16px, 1.3vw, 18px); color: var(--jp-text-2);
  line-height: 1.55; max-width: 52ch;
  margin-top: var(--s-4);
}
.jp-band__cats {
  display: flex; flex-wrap: wrap; gap: 8px;
  margin-top: var(--s-6);
}
.jp-band__cats span {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 12px; font-weight: 500; letter-spacing: -0.005em;
  color: var(--jp-text-2);
  padding: 8px 16px;
  background: var(--jp-card);
  border: 1px solid var(--jp-rule);
  border-radius: 999px;
}
.jp-band__cats span.on {
  background: var(--jp-red); border-color: var(--jp-red); color: var(--jp-text);
}
.jp-band__actions {
  display: flex; flex-wrap: wrap; gap: 12px;
  margin-top: var(--s-6); align-items: center;
}
.jp-band__cta {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 14px 22px;
  background: var(--jp-red); color: var(--jp-text);
  border: 1px solid var(--jp-red);
  border-radius: 999px;
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 14px; font-weight: 600; letter-spacing: -0.005em;
  transition: background .15s, transform .15s;
}
.jp-band__cta:hover { background: var(--jp-red-dark); transform: translateY(-1px); }

/* App-store / Play-store pills (brand neutral, not gold) */
.jp-store {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 10px 20px; min-height: 52px;
  background: var(--jp-text); color: #000;
  border: 1px solid var(--jp-text);
  border-radius: 999px;
  transition: transform .15s, box-shadow .15s, background .15s;
  font-family: 'Inter', 'Geist', sans-serif;
}
.jp-store svg { width: 22px; height: 22px; flex-shrink: 0; }
.jp-store span { display: flex; flex-direction: column; line-height: 1.1; text-align: left; }
.jp-store small { font-family: 'Inter', 'Geist', sans-serif; font-size: 10px; font-weight: 500; color: #555; letter-spacing: 0; text-transform: none; }
.jp-store span > :not(small) { font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }
.jp-store:hover { transform: translateY(-2px); box-shadow: 0 8px 20px -4px rgba(220,38,38,0.5); }

/* Phone illustration — JesusPod brand dark + red accents */
.jp-band__right { display: grid; place-items: center; }
.jp-phone {
  width: 300px; aspect-ratio: 9 / 18;
  background: #000;
  border: 1px solid #1f1f1f;
  border-radius: 40px;
  padding: 12px;
  box-shadow: 0 50px 100px -30px rgba(220,38,38,0.3), 0 40px 80px -30px rgba(0,0,0,0.9), inset 0 0 0 1px rgba(255,255,255,0.04);
  position: relative;
}
.jp-phone::before {
  content: ""; position: absolute; top: 22px; left: 50%; transform: translateX(-50%);
  width: 90px; height: 22px; border-radius: 999px; background: #000; z-index: 2;
}
.jp-phone__screen {
  background: #0a0a0a;
  width: 100%; height: 100%;
  border-radius: 28px;
  padding: 52px 14px 14px;
  display: flex; flex-direction: column; gap: 12px;
  color: var(--jp-text);
  overflow: hidden;
}
.jp-phone__header {
  display: flex; align-items: center; justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid #1c1c1c;
}
.jp-phone__logo {
  font-family: 'Inter', 'Geist', sans-serif;
  font-weight: 800; font-size: 14px; letter-spacing: -0.01em;
  color: var(--jp-text);
}
.jp-phone__logo em { font-style: normal; color: var(--jp-red); }
.jp-phone__signin {
  background: var(--jp-red); color: var(--jp-text);
  padding: 4px 10px; border-radius: 999px;
  font-size: 10px; font-weight: 600;
}
.jp-phone__pills {
  display: flex; gap: 6px; flex-wrap: nowrap; overflow: hidden;
}
.jp-phone__pills span {
  font-size: 10px; font-weight: 500;
  padding: 4px 10px; border-radius: 999px;
  background: #1c1c1c; color: var(--jp-text-2);
  white-space: nowrap;
}
.jp-phone__pills span.on { background: var(--jp-red); color: var(--jp-text); }
.jp-phone__feature {
  position: relative;
  border-radius: 10px; overflow: hidden;
  aspect-ratio: 16 / 10;
  background: linear-gradient(135deg, #2a1a1a 0%, #0a0a0a 100%);
  display: grid; place-items: end start;
  padding: 10px;
}
.jp-phone__feature::after {
  content: "1h 5m"; position: absolute; top: 8px; right: 8px;
  background: var(--jp-red); color: var(--jp-text);
  font-size: 9px; font-weight: 600;
  padding: 2px 8px; border-radius: 999px;
}
.jp-phone__feature strong { font-size: 12px; font-weight: 700; letter-spacing: -0.01em; }
.jp-phone__sectitle { font-size: 11px; font-weight: 600; color: var(--jp-text); margin-top: 4px; }
.jp-phone__grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;
}
.jp-phone__grid > div {
  aspect-ratio: 1; border-radius: 8px;
  position: relative;
  background: linear-gradient(135deg, #2a1515 0%, #0a0a0a 100%);
}
.jp-phone__grid > div:nth-child(2) { background: linear-gradient(135deg, #1a1a2a 0%, #0a0a0a 100%); }
.jp-phone__grid > div:nth-child(3) { background: linear-gradient(135deg, #2a2015 0%, #0a0a0a 100%); }
.jp-phone__grid > div::after {
  content: ""; position: absolute; top: 4px; right: 4px;
  width: 18px; height: 8px; border-radius: 999px;
  background: var(--jp-red); opacity: 0.9;
}

/* ---------- DEDICATED PAGE: /jesuspod --------------------- */
.jp-hero {
  background: #0a0a0a; color: #FAFAFA;
  padding: var(--s-9) 0 var(--s-8);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', 'Geist', sans-serif;
}
.jp-hero::before {
  content: ""; position: absolute; inset: 0;
  background:
    radial-gradient(circle at 85% 15%, rgba(220,38,38,0.28), transparent 50%),
    radial-gradient(circle at 10% 85%, rgba(220,38,38,0.15), transparent 45%);
  pointer-events: none;
}
.jp-hero__wrap {
  position: relative;
  max-width: 1320px; margin: 0 auto;
  padding: 0 var(--s-7);
}
.jp-hero__wordmark {
  display: inline-flex; align-items: center; gap: 12px;
  margin-bottom: var(--s-6);
  font-family: 'Inter', 'Geist', sans-serif;
  font-weight: 800; font-size: 22px; letter-spacing: -0.015em;
  color: #FAFAFA;
}
.jp-hero__wordmark::before {
  content: ""; width: 32px; height: 32px;
  border-radius: 999px; background: #DC2626;
  flex-shrink: 0;
  box-shadow: 0 0 0 6px rgba(220,38,38,0.2);
}
.jp-hero__wordmark em { font-style: normal; color: #DC2626; }
.jp-hero__meta {
  display: inline-flex; align-items: center; gap: 10px; flex-wrap: wrap;
  padding: 8px 16px;
  background: rgba(220,38,38,0.12);
  border: 1px solid rgba(220,38,38,0.3);
  border-radius: 999px;
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 12px; font-weight: 500; color: #EF4444;
  margin-bottom: var(--s-6);
}
.jp-hero__meta .tick { width: 8px; height: 8px; background: #DC2626; border-radius: 999px; box-shadow: 0 0 0 3px rgba(220,38,38,0.3); }
.jp-hero__meta .sep { color: rgba(255,255,255,0.25); }
.jp-hero__title {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: clamp(44px, 7vw, 108px);
  line-height: 1.02; letter-spacing: -0.04em;
  font-weight: 700; color: #FAFAFA;
  max-width: 16ch;
}
.jp-hero__title em { font-style: normal; color: #DC2626; font-weight: 700; }
.jp-hero__lede {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: clamp(17px, 1.4vw, 20px); line-height: 1.55;
  color: #C9C9C9; max-width: 58ch;
  margin-top: var(--s-5); font-weight: 400;
}
.jp-hero__actions {
  display: flex; flex-wrap: wrap; gap: 12px;
  margin-top: var(--s-7); align-items: center;
}
.jp-hero__web {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 24px;
  background: transparent; color: #FAFAFA;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 999px;
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 14px; font-weight: 500;
  transition: background .15s, border-color .15s;
}
.jp-hero__web:hover { background: rgba(255,255,255,0.05); border-color: #DC2626; }

/* Category grid */
.jp-cats {
  background: #141414; color: #FAFAFA;
  padding: var(--s-9) 0;
  font-family: 'Inter', 'Geist', sans-serif;
}
.jp-cats__wrap { max-width: 1320px; margin: 0 auto; padding: 0 var(--s-7); }
.jp-cats__hd {
  display: grid; grid-template-columns: 1fr 2fr;
  gap: var(--s-7);
  margin-bottom: var(--s-7);
  align-items: end;
}
.jp-cats__label {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px;
  background: rgba(220,38,38,0.12);
  border: 1px solid rgba(220,38,38,0.3);
  border-radius: 999px;
  font-size: 12px; font-weight: 500; color: #EF4444;
  width: fit-content;
}
.jp-cats__kicker { font-size: 13px; font-weight: 500; color: #8A8A8A; margin-top: 10px; }
.jp-cats__title {
  font-size: clamp(36px, 4.5vw, 64px);
  line-height: 1.02; letter-spacing: -0.03em;
  font-weight: 700; color: #FAFAFA;
}
.jp-cats__title em { font-style: normal; color: #DC2626; font-weight: 700; }
.jp-cats__lede {
  font-size: 17px; line-height: 1.55;
  color: #C9C9C9; max-width: 56ch; margin-top: var(--s-4);
}

.jp-cat-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
  margin-top: var(--s-6);
}
.jp-cat {
  padding: var(--s-6);
  background: #1c1c1c;
  border: 1px solid #2a2a2a;
  border-radius: 18px;
  display: flex; flex-direction: column; gap: var(--s-3);
  transition: background .15s, border-color .15s, transform .15s;
  min-height: 220px;
  position: relative;
  overflow: hidden;
}
.jp-cat::before {
  content: ""; position: absolute; top: 0; right: 0;
  width: 120px; height: 120px;
  background: radial-gradient(circle, rgba(220,38,38,0.18) 0%, transparent 70%);
  opacity: 0; transition: opacity .25s;
}
.jp-cat:hover { background: #242424; border-color: rgba(220,38,38,0.4); transform: translateY(-3px); }
.jp-cat:hover::before { opacity: 1; }
.jp-cat__num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 32px; height: 32px; border-radius: 999px;
  background: rgba(220,38,38,0.15);
  color: #EF4444;
  font-size: 12px; font-weight: 700;
}
.jp-cat h3 {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 24px; line-height: 1.1; letter-spacing: -0.02em;
  font-weight: 700; color: #FAFAFA;
  margin-top: 6px;
}
.jp-cat h3 em { font-style: normal; color: #DC2626; }
.jp-cat p { font-size: 14px; line-height: 1.55; color: #9A9A9A; margin-top: auto; font-family: 'Inter', 'Geist', sans-serif; }

/* FPG channel card — sits on bone surface, uses JP red */
.jp-channel { display: grid; }
.jp-channel__card {
  display: grid; grid-template-columns: 280px 1fr;
  gap: var(--s-7);
  border: 1px solid var(--bone-rule);
  background: var(--bone-2);
  padding: var(--s-7);
  border-radius: 20px;
  align-items: center;
  font-family: 'Inter', 'Geist', sans-serif;
}
.jp-channel__logo {
  aspect-ratio: 1;
  background:
    radial-gradient(circle at 30% 30%, rgba(220,38,38,0.45), transparent 55%),
    linear-gradient(165deg, #0a0a0a 0%, #1c1c1c 100%);
  display: grid; place-items: center;
  color: #FAFAFA;
  border-radius: 16px;
  border: 1px solid #1c1c1c;
}
.jp-channel__logo svg { width: 50%; color: #DC2626; }
.jp-channel__kicker {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px;
  background: rgba(220,38,38,0.1);
  color: #DC2626;
  border: 1px solid rgba(220,38,38,0.25);
  border-radius: 999px;
  font-size: 12px; font-weight: 500;
  margin-bottom: var(--s-3);
}
.jp-channel__name {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: clamp(30px, 2.8vw, 44px); line-height: 1.05; letter-spacing: -0.025em;
  font-weight: 700; margin-bottom: var(--s-4); color: var(--ink);
}
.jp-channel__name em { color: #DC2626; font-style: normal; }
.jp-channel__body { font-family: 'Inter', 'Geist', sans-serif; font-size: 16px; line-height: 1.55; color: var(--ink-2); max-width: 56ch; }
.jp-channel__stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--s-5); margin-top: var(--s-6); padding-top: var(--s-5); border-top: 1px solid var(--bone-rule); }
.jp-channel__stats strong {
  display: block;
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 28px; font-weight: 700; letter-spacing: -0.02em; color: var(--ink);
}
.jp-channel__stats strong em { color: #DC2626; font-style: normal; }
.jp-channel__stats span { font-family: 'Inter', 'Geist', sans-serif; font-size: 12px; font-weight: 500; color: var(--muted); margin-top: 4px; display: block; }
.jp-channel__actions { margin-top: var(--s-6); display: flex; gap: 12px; flex-wrap: wrap; }
.jp-channel__cta {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 13px 22px;
  background: #DC2626; color: #FAFAFA;
  border: 1px solid #DC2626;
  border-radius: 999px;
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 14px; font-weight: 600;
  transition: background .15s, transform .15s;
}
.jp-channel__cta:hover { background: #B91C1C; transform: translateY(-1px); }
.jp-channel__cta--ghost { background: transparent; color: var(--ink); border-color: var(--bone-rule); }
.jp-channel__cta--ghost:hover { background: var(--ink); color: var(--bone); border-color: var(--ink); transform: translateY(-1px); }

/* Why + CTA card */
.jp-why p { font-family: 'Inter', 'Geist', sans-serif; font-size: 17px; line-height: 1.6; color: var(--ink-2); margin-bottom: var(--s-5); max-width: 56ch; }
.jp-why p em { color: #DC2626; font-style: normal; font-weight: 600; }
.jp-cta-card {
  background: #0a0a0a; color: #FAFAFA;
  padding: var(--s-7);
  border-radius: 20px;
  border: 1px solid #1c1c1c;
  display: flex; flex-direction: column; gap: var(--s-4);
  font-family: 'Inter', 'Geist', sans-serif;
  position: relative;
  overflow: hidden;
}
.jp-cta-card::before {
  content: ""; position: absolute; top: -40px; right: -40px;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(220,38,38,0.25), transparent 60%);
  pointer-events: none;
}
.jp-cta-card__kicker {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px;
  background: rgba(220,38,38,0.15);
  color: #EF4444;
  border: 1px solid rgba(220,38,38,0.3);
  border-radius: 999px;
  font-size: 12px; font-weight: 500;
  width: fit-content;
  position: relative;
}
.jp-cta-card__title {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: clamp(36px, 3.6vw, 56px); line-height: 1.02; letter-spacing: -0.03em;
  font-weight: 700;
  position: relative;
}
.jp-cta-card__title em { color: #DC2626; font-style: normal; }
.jp-cta-card__body {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 17px; line-height: 1.5;
  color: #C9C9C9; max-width: 40ch;
  margin-bottom: var(--s-3);
  position: relative;
}
.jp-cta-card__web {
  font-family: 'Inter', 'Geist', sans-serif;
  font-size: 14px; font-weight: 500;
  color: #C9C9C9; margin-top: var(--s-3);
  padding: 14px 0;
  border-top: 1px solid rgba(255,255,255,0.08);
  display: inline-flex; justify-content: space-between; align-items: center; width: 100%;
  position: relative;
  transition: color .15s;
}
.jp-cta-card__web:hover { color: #DC2626; }
.jp-cta-card__web strong { color: #FAFAFA; font-weight: 700; }
.jp-cta-card .jp-store { position: relative; }

@media (max-width: 1040px) {
  .jp-band__wrap { grid-template-columns: 1fr; }
  .jp-phone { width: 240px; }
  .jp-cat-grid { grid-template-columns: repeat(2, 1fr); }
  .jp-channel__card { grid-template-columns: 1fr; padding: var(--s-5); gap: var(--s-5); }
  .jp-channel__logo { max-width: 200px; justify-self: center; }
  .jp-cats__hd { grid-template-columns: 1fr; gap: var(--s-3); }
}
@media (max-width: 860px) {
  .jp-band { padding: var(--s-7) var(--s-5); }
  .jp-band__title { font-size: clamp(32px, 9vw, 48px); }
  .jp-band__lede { font-size: 16px; }
  .jp-band__actions { gap: 10px; width: 100%; }
  .jp-store, .jp-band__cta { width: 100%; justify-content: center; padding: 14px 18px; }
  .jp-band__cats span { font-size: 11px; padding: 6px 12px; }
  .jp-hero { padding: var(--s-7) 0 var(--s-6); }
  .jp-hero__wrap { padding: 0 var(--s-5); }
  .jp-hero__title { font-size: clamp(36px, 11vw, 60px); }
  .jp-hero__lede { font-size: 16px; }
  .jp-hero__web { width: 100%; justify-content: center; }
  .jp-cats { padding: var(--s-7) 0; }
  .jp-cats__wrap { padding: 0 var(--s-5); }
  .jp-cats__title { font-size: 32px; }
  .jp-cats__lede { font-size: 15px; }
  .jp-cat-grid { grid-template-columns: 1fr; }
  .jp-cat { padding: var(--s-5); min-height: 0; }
  .jp-channel__stats { grid-template-columns: 1fr; }
  .jp-channel__actions .jp-channel__cta { width: 100%; justify-content: center; }
  .jp-cta-card { padding: var(--s-5); }
  .jp-cta-card__title { font-size: 32px; }
}

/* Nav 'on' state for current page */
.site-nav__links a.on { color: var(--ink); border-bottom-color: var(--valley-red); }

/* ===========================================================
   WELCOME BANNER — "New here?" strip below the nav
   =========================================================== */
.welcome-banner {
  position: sticky;
  top: 80px;
  z-index: 55;
  display: flex; align-items: center; justify-content: center;
  gap: 14px; flex-wrap: wrap;
  padding: 11px var(--s-7);
  background: linear-gradient(90deg, #F3E4DA 0%, #E6E8DC 55%, #DCE8E4 100%);
  border-bottom: 1px solid #D9CEBD;
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 13px;
  text-align: center;
  transition: background .2s;
}
.welcome-banner:hover { background: linear-gradient(90deg, #EEDBCC 0%, #DDE0D0 55%, #D0DED8 100%); }
.welcome-banner__kicker {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--valley-red-dark);
  font-weight: 700;
  white-space: nowrap;
}
.welcome-banner__msg {
  color: var(--ink-2);
  font-size: 13px;
  letter-spacing: -0.005em;
}
.welcome-banner__cta {
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--ink);
  font-weight: 600;
  border-bottom: 1px solid var(--valley-red);
  padding-bottom: 1px;
  white-space: nowrap;
}
.welcome-banner:hover .welcome-banner__cta { color: var(--valley-red); }

/* Hero anchors can now start higher */
section { scroll-margin-top: 128px; }

@media (max-width: 860px) {
  .welcome-banner {
    padding: 9px var(--s-5);
    gap: 8px;
    font-size: 12px;
    top: 60px;
  }
  .welcome-banner__kicker { font-size: 9px; letter-spacing: 0.14em; }
  .welcome-banner__msg { display: none; }
  .welcome-banner__cta { font-size: 12px; }
}

/* ===========================================================
   SPRING REVIVAL HERO SIDE — pastel mint + coral (matches
   official fpgchurch.com revival banner; features the pastor)
   =========================================================== */
.hero__side {
  /* Consolidated base — supersedes the earlier .hero__side rule in the
     extracted design CSS (kept flex layout carried over from there). */
  background:
    radial-gradient(ellipse at 8% 95%, rgba(243, 201, 179, 0.9) 0%, transparent 55%),
    radial-gradient(ellipse at 100% 15%, #EE8060 0%, rgba(234, 163, 121, 0.5) 35%, transparent 65%),
    linear-gradient(155deg, #E4F0EC 0%, #BBDFDE 42%, #A8CDBB 78%, #EBCAB6 100%);
  color: #2B2A28;
  border: 1px solid #E8C4B0;
  padding: var(--s-6) var(--s-6) 0;
  min-height: 560px;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.hero__side::before {
  background-image: radial-gradient(rgba(255,255,255,0.35) 1px, transparent 1px);
  background-size: 14px 14px;
  opacity: 0.25;
  z-index: 1;
}
.hero__side-pastor {
  display: block;
  position: absolute;
  right: -20%;
  bottom: 0;
  width: 135%;
  max-width: 135%;
  height: auto;
  z-index: 2;
  pointer-events: none;
  filter: drop-shadow(0 20px 35px rgba(139, 74, 46, 0.25));
}
.hero__side > *:not(.hero__side-pastor) { position: relative; z-index: 3; }
.hero__side-tag {
  color: #A84A2E;
  font-weight: 600;
  letter-spacing: 0.16em;
  margin-bottom: var(--s-6);
}
.hero__side-tag span:first-child { color: #C9623F; }
.hero__side-dates {
  grid-template-columns: 1fr;
  margin-top: 0;
  max-width: 58%;
  gap: var(--s-3);
}
.hero__side-big {
  color: #C65A3E;
  font-size: clamp(56px, 9vw, 120px);
  line-height: 0.9;
  font-weight: 300;
  padding-top: 0.12em;
}
.hero__side-big em { color: #4A8A83; font-style: italic; }
.hero__side-list {
  color: #2B1E17;
  opacity: 1;
  margin-top: var(--s-3);
  font-size: 11px;
  letter-spacing: 0.08em;
  line-height: 1.45;
  font-weight: 500;
  width: 100%;
  padding: 16px 18px;
  background:
    linear-gradient(135deg, rgba(255,253,248,0.34), rgba(255,253,248,0.18)) padding-box,
    linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.35) 45%, rgba(255,255,255,0.15) 100%) border-box;
  backdrop-filter: blur(14px) saturate(1.15);
  -webkit-backdrop-filter: blur(14px) saturate(1.15);
  border: 1px solid transparent;
  border-radius: 10px;
  box-shadow:
    0 14px 34px -12px rgba(139, 74, 46, 0.28),
    inset 0 1px 0 rgba(255,255,255,0.55),
    inset 0 -1px 0 rgba(168, 74, 46, 0.08);
}
.hero__side-list li {
  border-bottom-color: rgba(168, 74, 46, 0.18);
  color: #2B1E17;
  padding: 6px 0;
  overflow-wrap: anywhere;
}
.hero__side-list li:last-child { border-bottom: none; padding-bottom: 0; }
.hero__side-list li:first-child { padding-top: 0; }
.hero__side-cta {
  margin-top: auto;
  margin-bottom: var(--s-5);
  max-width: max-content;
  justify-content: flex-start;
  gap: 14px;
  padding: 14px 18px;
  border: 1px solid transparent;
  color: #A84A2E;
  background:
    linear-gradient(135deg, rgba(255,253,248,0.38), rgba(255,253,248,0.2)) padding-box,
    linear-gradient(135deg, rgba(168,74,46,0.55) 0%, rgba(168,74,46,0.22) 50%, rgba(168,74,46,0.4) 100%) border-box;
  backdrop-filter: blur(12px) saturate(1.1);
  -webkit-backdrop-filter: blur(12px) saturate(1.1);
  border-radius: 8px;
  font-weight: 600;
  box-shadow:
    0 10px 24px -10px rgba(139, 74, 46, 0.22),
    inset 0 1px 0 rgba(255,255,255,0.5);
}
.hero__side-cta:hover {
  background: #C65A3E;
  color: #FFFDF8;
  border-color: #C65A3E;
}

@media (max-width: 1040px) {
  .hero__side { min-height: 540px; padding: var(--s-5) var(--s-5) 0; }
  .hero__side-pastor { width: 115%; right: -15%; }
  .hero__side-dates, .hero__side-list, .hero__side-cta { max-width: 55%; }
}
@media (max-width: 860px) {
  .hero__side { min-height: 520px; padding: var(--s-5) var(--s-5) 0; }
  .hero__side-pastor { width: 90%; right: -8%; }
  .hero__side-dates, .hero__side-list, .hero__side-cta { max-width: 58%; }
  .hero__side-list { max-width: 58%; }
}
@media (max-width: 540px) {
  .hero__side { min-height: 560px; }
  .hero__side-pastor { width: 68%; right: -8%; opacity: 1; }
  .hero__side-dates, .hero__side-list { max-width: 72%; }
  .hero__side-list { max-width: 72%; font-size: 10px; letter-spacing: 0.04em; padding: 12px 14px; line-height: 1.35; }
  .hero__side-cta { max-width: max-content; font-size: 10px; padding: 12px 14px; }
}

/* ===========================================================
   HERO TEXT — reduce sizes for better desktop+mobile density
   =========================================================== */
.hero { padding: var(--s-8) 0 var(--s-7); }
.hero__title {
  font-size: clamp(44px, 7vw, 112px);
  line-height: 0.92;
  letter-spacing: -0.03em;
}
.hero__lede {
  font-size: clamp(17px, 1.6vw, 22px);
  line-height: 1.4;
  max-width: 30ch;
  margin-top: var(--s-5);
}
.hero__side-big { font-size: clamp(52px, 8vw, 104px); }
.hero__side-tag { font-size: 10px; letter-spacing: 0.14em; }

@media (max-width: 860px) {
  .hero { padding: var(--s-6) 0 var(--s-5); gap: var(--s-5); }
  .hero__title { font-size: clamp(38px, 11vw, 66px); line-height: 0.95; }
  .hero__lede { font-size: 16px; margin-top: var(--s-4); }
  .hero__actions { margin-top: var(--s-5); }
  .hero__actions .btn { padding: 13px 18px; font-size: 13px; }
  .hero__side-tag span:nth-child(3) { display: none; }
}
@media (max-width: 440px) {
  .hero { padding: var(--s-5) 0 var(--s-4); }
  .hero__title { font-size: clamp(34px, 12vw, 52px); }
  .hero__lede { font-size: 15px; }
}

/* ===========================================================
   BOOKS — real-image cover cards (replaces designed covers)
   =========================================================== */
.book {
  background: var(--bone-2);
  border: 1px solid var(--bone-rule);
  display: flex; flex-direction: column;
  transition: transform .2s, box-shadow .2s;
  position: relative;
}
.book:hover { transform: translate(-3px, -3px); box-shadow: 6px 6px 0 var(--valley-red); }
.book__cover-link {
  display: block; position: relative;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  background: var(--bone-3);
}
.book__cover-img {
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
  transition: transform .4s ease;
}
.book:hover .book__cover-img { transform: scale(1.03); }
.book__corner {
  position: absolute; top: 12px; right: 12px;
  width: 38px; height: 38px;
  background: var(--bone); color: var(--ink);
  border-radius: 999px;
  display: grid; place-items: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.35);
  z-index: 2;
  transition: transform .15s, background .15s, color .15s;
}
.book__corner svg { width: 16px; height: 16px; }
.book__cover-link:hover .book__corner { transform: scale(1.08); background: var(--valley-red); color: var(--bone); }
.book__body { padding: var(--s-5); display: flex; flex-direction: column; gap: 10px; flex: 1; }
.book__meta {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.14em;
  text-transform: uppercase; color: var(--valley-red);
}
.book__title {
  font-family: var(--font-display);
  font-size: 22px; line-height: 1.12; letter-spacing: -0.015em;
  font-weight: 400; color: var(--ink);
}
.book__title em { color: var(--valley-red); font-style: italic; }
.book__sub {
  font-family: var(--font-display); font-style: italic;
  font-size: 14px; line-height: 1.35;
  color: var(--ink-2);
}
.book__desc { font-size: 13.5px; line-height: 1.55; color: var(--ink-3); flex: 1; }
.book__author {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.14em;
  text-transform: uppercase; color: var(--muted);
  padding-top: 10px;
  border-top: 1px solid var(--bone-rule);
}
.book__pill {
  display: inline-flex; align-items: center; justify-content: center; gap: 10px;
  padding: 12px 16px;
  background: var(--ink); color: var(--bone);
  border: 1px solid var(--ink);
  border-radius: 999px;
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase;
  font-weight: 500;
  transition: all .15s;
  align-self: stretch;
}
.book__pill svg { width: 13px; height: 13px; }
.book__pill:hover { background: var(--valley-red); border-color: var(--valley-red); }

/* Grid: 4 books on books page, 2-col on tablet, 1-col on phone */
.books { grid-template-columns: repeat(4, 1fr); gap: var(--s-5); }
@media (max-width: 1200px) { .books { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px)  { .books { grid-template-columns: 1fr; } }

/* ===========================================================
   HOME BOOKS TEASER — 4 compact covers with download pill
   =========================================================== */
.home-books { padding-top: var(--s-6); padding-bottom: var(--s-7); }
.home-books__grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: var(--s-5);
}
.home-book {
  position: relative; display: block;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  border: 1px solid var(--bone-rule);
  background: var(--bone-2);
  transition: transform .2s, box-shadow .2s;
}
.home-book img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform .4s ease; }
.home-book:hover { transform: translate(-3px, -3px); box-shadow: 6px 6px 0 var(--valley-red); }
.home-book:hover img { transform: scale(1.04); }
.home-book__pill {
  position: absolute; left: 12px; bottom: 12px;
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 14px;
  background: var(--ink); color: var(--bone);
  border-radius: 999px;
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;
  font-weight: 500;
  transition: background .15s;
}
.home-book__pill svg { width: 12px; height: 12px; }
.home-book:hover .home-book__pill { background: var(--valley-red); }
.home-books__footer { margin-top: var(--s-6); display: flex; justify-content: center; }

@media (max-width: 860px) {
  .home-books__grid { grid-template-columns: repeat(2, 1fr); gap: var(--s-4); }
  .home-book__pill { font-size: 9px; padding: 6px 10px; letter-spacing: 0.08em; }
  .home-books__footer .btn { width: 100%; justify-content: space-between; }
}

/* ===========================================================
   WATCH PAGE ACCESSIBILITY — filter chips on dark background
   Fixes browser-default button bg bleed-through; ensures text
   meets WCAG AA contrast on the ink surface.
   =========================================================== */
.watch__filter-label {
  color: #C9C9C9;
  font-weight: 500;
}
.watch .chip {
  background: rgba(255, 255, 255, 0.06);
  color: #F0EEE8;
  border: 1px solid rgba(255, 255, 255, 0.28);
  font-weight: 500;
  min-height: 40px;
  border-radius: 999px;
  padding: 9px 16px;
  transition: background .15s, border-color .15s, color .15s, transform .15s;
}
.watch .chip:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: var(--gold-leaf);
  color: #FFFFFF;
}
.watch .chip.on {
  background: var(--valley-red);
  border-color: var(--valley-red);
  color: #FFFFFF;
  font-weight: 600;
}
.watch .chip:focus-visible {
  outline: 2px solid var(--gold-leaf);
  outline-offset: 3px;
}

/* Global focus-visible improvements (accessibility) */
a:focus-visible,
button:focus-visible {
  outline: 2px solid var(--valley-red);
  outline-offset: 3px;
  border-radius: 2px;
}
.watch a:focus-visible,
.watch button:focus-visible,
.jp-band a:focus-visible,
.jp-hero a:focus-visible,
.jp-cats a:focus-visible {
  outline-color: var(--gold-leaf);
}
.give__form *:focus-visible {
  outline: 2px solid var(--bone);
  outline-offset: 2px;
}

/* ===========================================================
   MOBILE HAMBURGER + MENU
   =========================================================== */
.site-nav__burger {
  display: none;
  width: 44px; height: 44px;
  background: transparent;
  border: 1px solid var(--bone-rule);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  padding: 0;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  grid-column: -1;
  justify-self: end;
}
.site-nav__burger span {
  display: block;
  width: 20px; height: 2px;
  background: var(--ink);
  border-radius: 2px;
  transition: transform .25s, opacity .2s;
}
.site-nav__burger[aria-expanded="true"] span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}
.site-nav__burger[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
.site-nav__burger[aria-expanded="true"] span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

.mobile-menu {
  position: fixed;
  inset: 0;
  background: color-mix(in oklab, var(--bone) 98%, transparent);
  backdrop-filter: blur(8px);
  z-index: 80;
  overflow-y: auto;
  padding: 96px var(--s-5) var(--s-7);
  animation: mobileMenuIn .2s ease-out;
}
.mobile-menu[hidden] { display: none; }
@keyframes mobileMenuIn {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.mobile-menu__inner {
  max-width: 720px;
  margin: 0 auto;
  display: flex; flex-direction: column;
  gap: var(--s-6);
}
.mobile-menu nav {
  display: flex; flex-direction: column;
  border-top: 1px solid var(--bone-rule);
}
.mobile-menu nav a {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 400;
  letter-spacing: -0.02em;
  color: var(--ink);
  padding: 18px 0;
  border-bottom: 1px solid var(--bone-rule);
  transition: color .15s;
}
.mobile-menu nav a:hover { color: var(--valley-red); }
.mobile-menu__lang {
  display: flex;
  border: 1px solid var(--bone-rule);
  border-radius: 2px;
  align-self: flex-start;
}
.mobile-menu__lang button {
  background: transparent;
  border: 0;
  padding: 14px 22px;
  min-height: 44px;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink-3);
  cursor: pointer;
}
.mobile-menu__lang button.on { background: var(--ink); color: var(--bone); }
.mobile-menu__cta {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 24px;
  background: var(--valley-red);
  color: var(--bone);
  font-family: var(--font-sans);
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.02em;
  transition: background .15s;
}
.mobile-menu__cta:hover { background: var(--valley-red-dark); }

body.menu-open { overflow: hidden; }

/* Show hamburger + hide nav CTA/lang at narrow widths */
@media (max-width: 1040px) {
  .site-nav__inner { grid-template-columns: 1fr auto !important; }
  .site-nav__burger {
    display: inline-flex !important;
    justify-self: end;
    background: var(--bone-2) !important;
    border-color: var(--ink-3) !important;
  }
  .site-nav__links { display: none !important; }
  .site-nav__cta { display: none !important; }
  .site-nav__lang { display: none !important; }
}
@media (max-width: 860px) {
  .site-nav__inner { padding: 12px var(--s-5); grid-template-columns: 1fr auto; gap: var(--s-4); }
  .site-nav__brand-sub { display: none; }
  .site-nav__brand { font-size: 17px; gap: 10px; }
  .site-nav__brand svg { width: 24px; height: 24px; }
  .mobile-menu { padding: 88px var(--s-5) var(--s-6); }
  .mobile-menu nav a { font-size: 24px; padding: 14px 0; }
}

/* ===========================================================
   .field--group — fieldset with no default chrome, matches .field
   =========================================================== */
.field.field--group {
  border: 0;
  padding: 0;
  margin: 0;
  min-inline-size: auto;
}
.field.field--group legend {
  padding: 0;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: var(--s-3);
}

/* ===========================================================
   Pastors grid — shown on /about below the beliefs block
   =========================================================== */
.pastors__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--s-6);
  margin-top: var(--s-5);
}
.pastor {
  background: var(--bone-2);
  border: 1px solid var(--bone-rule);
  padding: var(--s-6);
  display: flex;
  flex-direction: column;
  gap: var(--s-3);
}
.pastor__kicker {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--valley-red-dark);
  font-weight: 600;
}
.pastor__name {
  font-family: var(--font-display);
  font-size: clamp(26px, 2.4vw, 32px);
  line-height: 1.05;
  letter-spacing: -0.02em;
  font-weight: 300;
  color: var(--ink);
  margin: 0;
}
.pastor__name em { font-style: italic; color: var(--valley-red); font-weight: 400; }
.pastor__tag {
  font-family: var(--font-display);
  font-style: italic;
  font-size: 17px;
  color: var(--ink-2);
  line-height: 1.35;
  margin: 0;
  padding-bottom: var(--s-3);
  border-bottom: 1px solid var(--bone-rule);
}
.pastor__bio {
  font-size: 14.5px;
  line-height: 1.55;
  color: var(--ink-2);
  margin: 0;
}
.pastor__bio em { font-style: italic; color: var(--ink); }
@media (max-width: 1040px) {
  .pastors__grid { grid-template-columns: repeat(2, 1fr); }
  .pastor:last-child { grid-column: 1 / -1; }
}
@media (max-width: 640px) {
  .pastors__grid { grid-template-columns: 1fr; gap: var(--s-5); }
  .pastor:last-child { grid-column: auto; }
  .pastor { padding: var(--s-5); }
}

/* ===========================================================
   .sermon when rendered as an anchor — keep block-level card layout
   and inherit text color from ink context (watch page is dark).
   =========================================================== */
a.sermon { display: block; color: inherit; text-decoration: none; }
a.sermon:hover { text-decoration: none; }
a.feat__play { display: inline-flex; align-items: center; justify-content: center; color: inherit; text-decoration: none; }

/* ===========================================================
   Real YouTube thumbnails — fill the thumb box behind the badges
   =========================================================== */
.sermon__thumb { position: relative; overflow: hidden; }
.sermon__thumb img {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
  z-index: 0;
  transition: transform .3s ease;
}
.sermon:hover .sermon__thumb img { transform: scale(1.04); }
.sermon__thumb::after {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0) 40%, rgba(0,0,0,0.72) 100%);
  z-index: 1;
  pointer-events: none;
}
.sermon__series, .sermon__dur { position: relative; z-index: 2; }
/* Featured background image */
.feat { position: relative; overflow: hidden; }
.feat__bg {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  z-index: 0;
  opacity: 0.5;
}
.feat::after {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.75) 100%);
  z-index: 1;
  pointer-events: none;
}
.feat__label, .feat__caption, .feat__play { position: relative; z-index: 2; }

/* ===========================================================
   .min cards — only show pointer when they are actual links.
   Non-anchor usage (/ministries) should not lie about interactivity.
   =========================================================== */
article.min { cursor: default; }
article.min:hover { background: inherit; color: inherit; transform: none; }
article.min:hover .min__icon,
article.min:hover .min__kicker,
article.min:hover .min__name,
article.min:hover .min__name em,
article.min:hover .min__body { color: inherit; }

/* ===========================================================
   #fbi anchor — land with headroom below sticky nav
   =========================================================== */
#fbi { scroll-margin-top: 120px; }

/* ===========================================================
   TAP TARGETS — enforce 44px minimum on interactive controls
   =========================================================== */
.site-nav__lang button {
  padding: 12px 16px !important;
  min-height: 44px;
  font-size: 11px;
}
.site-nav__burger {
  min-width: 44px;
  min-height: 44px;
}

/* ===========================================================
   FOCUS VISIBLE — ensure keyboard users see focus everywhere
   =========================================================== */
:focus-visible {
  outline: 2px solid var(--valley-red);
  outline-offset: 2px;
  border-radius: 2px;
}
.watch :focus-visible,
.jp-scope :focus-visible,
.jp-band :focus-visible {
  outline-color: var(--gold-leaf);
}

/* ===========================================================
   SKIP LINK — visible on keyboard focus only
   =========================================================== */
.skip-link {
  position: absolute;
  top: -40px;
  left: var(--s-4);
  z-index: 100;
  background: var(--ink);
  color: var(--bone);
  padding: 10px 16px;
  font-family: var(--font-sans);
  font-size: 14px;
  text-decoration: none;
  border-radius: var(--r-1);
  transition: top 0.15s;
}
.skip-link:focus { top: var(--s-4); outline: 2px solid var(--valley-red); outline-offset: 2px; }
"""

(SYS / "site.css").write_text(style_match.group(1).strip() + "\n" + JP_CSS)

# ---------- Pull out reusable section HTML by comment markers --------------
def section(label):
    """Return the HTML of a <section> whose preceding comment contains `label`."""
    pattern = rf"<!--[^>]*{re.escape(label)}[^>]*-->\s*(<section[\s\S]*?</section>)"
    m = re.search(pattern, raw)
    if not m:
        raise ValueError(f"section not found: {label}")
    return m.group(1)

HERO    = section("HERO")
ABOUT   = section("ABOUT")
WATCH   = section("WATCH")

# ---------- Real sermon data from YouTube channel --------------------------
SERMON_DATA_PATH = ROOT.parent / "sermon-data.json"
SERMONS = json.loads(SERMON_DATA_PATH.read_text()) if SERMON_DATA_PATH.exists() else []

def _clean_sermon_title(t):
    """Strip the `| MM.DD.YYYY` stamp + leading speaker prefix for a cleaner title."""
    t = re.sub(r'\s*\|\s*\d{2}\.\d{2}\.\d{4}\s*$', '', t)
    t = re.sub(r'^(Pastor |Pastora |Kevin Ortiz - |Rey Mejia - |Veronica Ortiz - )', '', t)
    return t.strip().rstrip('!')

def _sermon_card(i, s):
    title = _clean_sermon_title(s['title'])
    series = s.get('series', 'Sermon')
    dur = s.get('duration', '')
    speaker = s.get('speaker', '')
    lang = s.get('language', 'English')
    speaker_line = f"Pastor {speaker}" + (" · Español" if lang == 'Español' else "")
    thumb = s.get('thumbnail', '')
    return f'''<a href="{s['url']}" target="_blank" rel="noopener noreferrer" class="sermon sermon--s{i}">
      <div class="sermon__thumb">
        <img src="{thumb}" alt="{title} — {speaker_line}" loading="lazy" />
        <span class="sermon__series">{series}</span>
        <span class="sermon__dur">{dur}</span>
      </div>
      <div class="sermon__meta"><h3>{title}</h3><p>{speaker_line}</p></div>
    </a>'''

def _featured_block(s):
    if not s:
        return None
    title = _clean_sermon_title(s['title'])
    speaker = s.get('speaker', '')
    lang = s.get('language', 'English')
    speaker_line = f"Pastor {speaker}" + (" · Español" if lang == 'Español' else "")
    dur_human = s.get('duration', '').split(':')
    dur_label = f"{int(dur_human[0])}h {dur_human[1]}m" if len(dur_human) == 3 else f"{dur_human[0]}:{dur_human[1]}" if len(dur_human) == 2 else ''
    series = s.get('series', '')
    return f'''<div class="watch__featured">
    <div class="feat">
      <img class="feat__bg" src="{s['thumbnail']}" alt="" aria-hidden="true" />
      <div class="feat__label"><span class="rec"></span> Latest upload</div>
      <div class="feat__caption">
        <h4>{title}</h4>
        <p>{speaker_line} · {dur_label}</p>
      </div>
      <a class="feat__play" href="{s['url']}" target="_blank" rel="noopener noreferrer" aria-label="Watch this sermon on YouTube (opens in new tab)">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M4 2 L18 10 L4 18 Z"/></svg>
      </a>
    </div>
    <div class="feat-meta">
      <h5>{series}</h5>
      <p>The most recent message from Faith Pleases God — watch full-length on our YouTube channel.</p>
      <dl>
        <dt>Speaker</dt><dd>{speaker_line}</dd>
        <dt>Series</dt><dd>{series}</dd>
        <dt>Length</dt><dd>{dur_label}</dd>
        <dt>Published</dt><dd>{s.get('published', '')}</dd>
      </dl>
    </div>
  </div>'''
# Accessibility: give the filter group proper ARIA + initial aria-pressed state
WATCH = (WATCH
    .replace(
        '<div class="watch__filter">\n      <span class="watch__filter-label">Filter by pastor:</span>',
        '<div class="watch__filter" role="group" aria-label="Filter sermons by pastor">\n      <span id="watch-filter-label" class="watch__filter-label">Filter by pastor:</span>')
    .replace('<button class="chip on" type="button">All</button>',
             '<button class="chip on" type="button" aria-pressed="true">All</button>')
    .replace('<button class="chip" type="button">Pastor Kevin Ortiz</button>',
             '<button class="chip" type="button" aria-pressed="false">Pastor Kevin Ortiz</button>')
    .replace('<button class="chip" type="button">Pastora Veronica Ortiz</button>',
             '<button class="chip" type="button" aria-pressed="false">Pastora Veronica Ortiz</button>')
    .replace('<button class="chip" type="button">Pastor Rey Mejia</button>',
             '<button class="chip" type="button" aria-pressed="false">Pastor Rey Mejia</button>')
    .replace('<button class="chip" type="button">Guest Speakers</button>',
             '<button class="chip" type="button" aria-pressed="false">Guest Speakers</button>')
    # Wire the featured play button to the YouTube channel
    .replace('<button class="feat__play" type="button" aria-label="Play sermon">',
             '<a class="feat__play" href="https://www.youtube.com/@faithpleasesgod" target="_blank" rel="noopener noreferrer" aria-label="Watch sermons on YouTube (opens in new tab)">')
    .replace('</svg>\n      </button>',
             '</svg>\n      </a>'))
# Replace the placeholder featured block + sermon grid with real YouTube data.
if SERMONS:
    new_sermons_html = "\n    ".join(_sermon_card(i+1, s) for i, s in enumerate(SERMONS[:8]))
    new_featured = _featured_block(SERMONS[0]) or ''
    # Replace from "<div class="watch__featured">" up to just before "</section>"
    # (this covers both the featured block and the sermons grid in one shot)
    WATCH = re.sub(
        r'<div class="watch__featured">.*?</div>\s*</section>',
        f'{new_featured}\n  <div class="sermons">\n    {new_sermons_html}\n  </div>\n</section>',
        WATCH,
        count=1,
        flags=re.DOTALL
    )
else:
    # Fallback: keep placeholder articles but wire to channel
    WATCH = re.sub(
        r'<article class="(sermon sermon--s\d+)">(.*?)</article>',
        r'<a href="https://www.youtube.com/@faithpleasesgod" target="_blank" rel="noopener noreferrer" class="\1">\2</a>',
        WATCH,
        flags=re.DOTALL
    )
EVENTS  = section("EVENTS")
VISIT   = section("LOCATIONS")
MINS    = section("MINISTRIES")
CONNECT = section("CONNECT")
GIVE    = section("GIVE")
CONTACT = section("CONTACT")

# ---------- Rewrite placeholder anchors to real routes --------------------
BREEZE_REVIVAL = "https://fpgchurch.breezechms.com/form/f098b0"

HERO = (HERO
    .replace('<a href="#" class="btn btn--red">Register for Spring Revival',
             f'<a href="{BREEZE_REVIVAL}" target="_blank" rel="noopener noreferrer" class="btn btn--red">Register for Spring Revival')
    .replace('Six nights. Six voices. One Valley, gathered to seek Him with everything we have — and leave different than we came.',
             'Five nights. One Valley, gathered to seek Him with everything we have — and leave different than we came.')
    .replace('href="#about"', 'href="/about"')
    .replace('<a href="#" class="hero__side-cta">',
             f'<a href="{BREEZE_REVIVAL}" target="_blank" rel="noopener noreferrer" class="hero__side-cta">')
    .replace('<aside class="hero__side" aria-label="Spring Revival details">',
             '<aside class="hero__side" aria-label="Spring Revival details">'
             '<img class="hero__side-pastor" src="/assets/pastor-revival.png" alt="" aria-hidden="true"/>')
    .replace(
        '<li>Wed · Opening Night</li>\n'
        '          <li>Thu · Pastor Kevin Ortiz</li>\n'
        '          <li>Fri · Pastora Veronica Ortiz</li>\n'
        '          <li>Sat · Worship &amp; Testimony</li>\n'
        '          <li>Sun · Pastor Rey Mejia · Español</li>\n'
        '          <li>Closing Service · 7 PM nightly</li>',
        '<li>Wed · Opening · Ps Kevin + Ev Troy</li>\n'
        '          <li>Thu · Ps Marvin</li>\n'
        '          <li>Fri · Ps Kevin + Ev Troy</li>\n'
        '          <li>Sat · KBF 10 AM · Ps Marvin + Ev Troy</li>\n'
        '          <li>Sun · 8:30 ES Marvin · 11 EN Troy</li>'))

EVENTS = (EVENTS
    .replace('<a href="#" class="event__cta">Más info</a>',
             '<a href="/visit" class="event__cta">Más info</a>')
    .replace('<a href="#" class="event__cta">Plan visit</a>',
             '<a href="/visit" class="event__cta">Plan visit</a>')
    .replace('<a href="#" class="event__cta">More info</a>',
             '<a href="/visit" class="event__cta">More info</a>')
    .replace('<a href="#" class="event__cta">I\'m in</a>',
             '<a href="/visit" class="event__cta">I&rsquo;m in</a>'))

MINS = (MINS
    .replace('<a href="#" class="btn">Enroll for Fall',
             '<a href="/visit" class="btn">Enroll for Fall')
    .replace('<a href="#" class="btn btn--ghost">Course catalog</a>',
             '<a href="/contact" class="btn btn--ghost">Course catalog</a>')
    .replace('<article class="min fbi">', '<article id="fbi" class="min fbi">'))

TICKER = re.search(r'<div class="ticker"[\s\S]*?</div>\s*</div>', raw).group(0)

# ---------- Nav + footer templates ----------------------------------------
def nav(current):
    """Render nav HTML with `current` link marked active (current=home|about|...)."""
    links = [
        ("about",      "/about",      "About"),
        ("watch",      "/watch",      "Watch"),
        ("jesuspod",   "/jesuspod",   "JesusPod"),
        ("events",     "/events",     "Events"),
        ("visit",      "/visit",      "Visit"),
        ("ministries", "/ministries", "Ministries"),
        ("books",      "/books",      "Books"),
        ("give",       "/give",       "Give"),
    ]
    rendered = "\n      ".join(
        f'<a href="{href}"{" class=\"on\" aria-current=\"page\"" if key == current else ""}>{label}</a>'
        for key, href, label in links
    )
    # Hide welcome banner on /visit (it self-links) and /connect (already planning).
    welcome_banner = "" if current in ("visit", "connect") else '''<a class="welcome-banner" href="/visit">
  <span class="welcome-banner__kicker">★ New here?</span>
  <span class="welcome-banner__msg">We&rsquo;d love to meet you. Here&rsquo;s what to expect on your first visit.</span>
  <span class="welcome-banner__cta">Plan your visit <span aria-hidden="true">→</span></span>
</a>
'''
    return f'''<a class="skip-link" href="#main">Skip to main content</a>
<nav class="site-nav" aria-label="Primary">
  <div class="site-nav__inner">
    <a href="/" class="site-nav__brand" aria-label="Faith Pleases God Church — home">
      <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">
          <line x1="6" y1="44" x2="58" y2="44"/>
          <path d="M 18 44 A 14 14 0 0 1 46 44"/>
          <line x1="32" y1="10" x2="32" y2="18"/>
          <line x1="14" y1="18" x2="19" y2="23"/>
          <line x1="50" y1="18" x2="45" y2="23"/>
          <line x1="8"  y1="32" x2="14" y2="32"/>
          <line x1="50" y1="32" x2="56" y2="32"/>
        </g>
      </svg>
      <span class="site-nav__brand-lock">
        <span class="site-nav__brand-name">Faith <em>Pleases</em> God</span>
        <span class="site-nav__brand-sub">Harlingen, Texas</span>
      </span>
    </a>
    <div class="site-nav__links">
      {rendered}
    </div>
    <div class="site-nav__lang" role="group" aria-label="Language">
      <button class="on" type="button" aria-pressed="true">EN</button>
      <button type="button" aria-pressed="false">ES</button>
    </div>
    <a href="/events" class="site-nav__cta">Register <span aria-hidden="true">→</span></a>
    <button class="site-nav__burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>
<div id="mobile-menu" class="mobile-menu" hidden>
  <div class="mobile-menu__inner">
    <nav aria-label="Mobile navigation">
      <a href="/about">About</a>
      <a href="/watch">Watch</a>
      <a href="/jesuspod">JesusPod</a>
      <a href="/events">Events</a>
      <a href="/visit">Plan a Visit</a>
      <a href="/ministries">Ministries</a>
      <a href="/books">Books</a>
      <a href="/give">Give</a>
      <a href="/contact">Contact</a>
    </nav>
    <div class="mobile-menu__lang" role="group" aria-label="Language">
      <button class="on" type="button" aria-pressed="true">English</button>
      <button type="button" aria-pressed="false">Español</button>
    </div>
    <a href="https://fpgchurch.breezechms.com/form/f098b0" target="_blank" rel="noopener noreferrer" class="mobile-menu__cta">Register for Spring Revival <span aria-hidden="true">→</span></a>
  </div>
</div>
{welcome_banner}'''

FOOTER = '''<footer>
  <div class="foot-mark">Faith<br/><em>pleases</em> God.</div>
  <div class="foot-grid">
    <div class="foot-col">
      <h6>Faith Pleases God Church</h6>
      <p>A family of believers in the Rio Grande Valley, pressing on together since 2004. English &amp; Español. All are welcome.</p>
    </div>
    <div class="foot-col">
      <h6>Explore</h6>
      <ul>
        <li><a href="/about">About</a></li>
        <li><a href="/watch">Watch &amp; listen</a></li>
        <li><a href="/jesuspod">JesusPod app</a></li>
        <li><a href="/events">Events</a></li>
        <li><a href="/ministries">Ministries</a></li>
        <li><a href="/ministries#fbi">Faith Bible Institute</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h6>Visit</h6>
      <ul>
        <li><a href="/visit">Plan a visit</a></li>
        <li><a href="/visit#online">Watch online</a></li>
        <li><a href="/books">Books</a></li>
        <li><a href="/give">Give</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h6>Follow</h6>
      <ul>
        <li><a href="https://instagram.com/fpgharlingen" target="_blank" rel="noopener noreferrer">Instagram</a></li>
        <li><a href="https://www.youtube.com/@faithpleasesgod" target="_blank" rel="noopener noreferrer">YouTube</a></li>
        <li><a href="https://www.facebook.com/FaithPleasesGodChurch" target="_blank" rel="noopener noreferrer">Facebook</a></li>
        <li><a href="/books">Books on Google Play</a></li>
        <li><a href="https://www.fpgfamily.com/" target="_blank" rel="noopener noreferrer">FPG Family · sermons</a></li>
      </ul>
    </div>
  </div>
  <div class="foot-bottom">
    <div>© 2026 Faith Pleases God Church · 4501 W Expressway 83, Harlingen, TX 78552 · 501(c)(3)</div>
    <div>Made with love in the Valley</div>
  </div>
</footer>
'''

SCRIPT = '''<script>
  // Hamburger mobile menu
  (function(){
    const burger = document.querySelector('.site-nav__burger');
    const menu = document.getElementById('mobile-menu');
    if (!burger || !menu) return;
    const setOpen = (open) => {
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open) {
        menu.removeAttribute('hidden');
        document.body.classList.add('menu-open');
      } else {
        menu.setAttribute('hidden', '');
        document.body.classList.remove('menu-open');
      }
    };
    burger.addEventListener('click', () => setOpen(menu.hasAttribute('hidden')));
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
  })();

  // Language toggle — visual only
  document.querySelectorAll('.site-nav__lang button, .mobile-menu__lang button').forEach(b => {
    b.addEventListener('click', () => {
      const container = b.parentElement;
      container.querySelectorAll('button').forEach(x => {
        x.classList.remove('on');
        x.setAttribute('aria-pressed', 'false');
      });
      b.classList.add('on');
      b.setAttribute('aria-pressed', 'true');
    });
  });
  // Sermon filter chips — only bind on /watch
  if (document.querySelector('.watch__filter')) {
    document.querySelectorAll('.watch__filter .chip').forEach(c => {
      c.addEventListener('click', () => {
        document.querySelectorAll('.watch__filter .chip').forEach(x => {
          x.classList.remove('on');
          x.setAttribute('aria-pressed', 'false');
        });
        c.classList.add('on');
        c.setAttribute('aria-pressed', 'true');
      });
    });
  }
  // Give amounts — only bind on /give
  if (document.querySelector('.give__amount')) {
    document.querySelectorAll('.give__amount').forEach(a => {
      a.addEventListener('click', () => {
        document.querySelectorAll('.give__amount').forEach(x => x.classList.remove('on'));
        a.classList.add('on');
      });
    });
  }
</script>
'''

# ---------- Page-template helpers ------------------------------------------
def HEAD(title, desc): return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} — Faith Pleases God Church</title>
<meta name="description" content="{desc}"/>
<meta property="og:type" content="website"/>
<meta property="og:title" content="{title} — Faith Pleases God Church"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:image" content="https://fpg-church.vercel.app/system/mark.svg"/>
<meta property="og:url" content="https://fpg-church.vercel.app/"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{title} — Faith Pleases God Church"/>
<meta name="twitter:description" content="{desc}"/>
<meta name="theme-color" content="#D03E21"/>
<link rel="icon" type="image/svg+xml" href="/system/mark.svg"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"/>
<link rel="stylesheet" href="/system/tokens.css?v={CSS_VER}"/>
<link rel="stylesheet" href="/system/site.css?v={CSS_VER}"/>
</head>
<body>
'''

def page(slug, title, desc, body_inner, current):
    """Write a full HTML page to slug.html (or index.html for slug == 'index')."""
    # Inject id="main" tabindex="-1" onto the first <main> or <section>.
    def _inject_main(src):
        m = re.search(r'<(main|section)\b([^>]*)>', src)
        if not m:
            return src
        attrs = m.group(2)
        if 'id="main"' in attrs or "id='main'" in attrs:
            return src
        return src[:m.start()] + f'<{m.group(1)} id="main" tabindex="-1"{attrs}>' + src[m.end():]
    # Ensure exactly one <h1> per page: promote first heading only if no h1 exists.
    def _promote_h1(src):
        if re.search(r'<h1\b', src):
            return src  # already has an h1 (home hero, jesuspod hero)
        # Try h2.sec-hd__title first (most pages)
        promoted = re.sub(
            r'<h2(\s+class="sec-hd__title"[^>]*>.*?)</h2>',
            r'<h1\1</h1>',
            src,
            count=1,
            flags=re.DOTALL
        )
        if promoted != src:
            return promoted
        # Fall back to promoting the first h3 (contact page pattern)
        return re.sub(r'<h3(\b[^>]*>.*?)</h3>', r'<h1\1</h1>', src, count=1, flags=re.DOTALL)
    body = _inject_main(_promote_h1(body_inner))
    html = HEAD(title, desc) + nav(current) + body + FOOTER + SCRIPT + "</body></html>\n"
    (ROOT / f"{slug}.html").write_text(html)

# wrap() — sections that sit inside .wrap container
def wrap(*inner):
    return '<main class="wrap">\n' + "\n".join(inner) + "\n</main>\n"

# ---------- HOME — hero + ticker + teaser cards ----------------------------
HOME_TEASERS = '''<main class="wrap">
  <section class="sec" style="border-top:0;">
    <header class="sec-hd">
      <div><div class="sec-hd__num">§ Explore</div><div class="sec-hd__kicker">Find your place</div></div>
      <div><h2 class="sec-hd__title">Come as you are.<br/><em>Find</em> where you belong.</h2></div>
    </header>
    <div class="mins">
      <a class="min" href="/about" style="text-decoration:none;">
        <svg class="min__icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M 8 30 L 20 8 L 32 30 Z"/></svg>
        <div class="min__kicker">§ 02 · Our story</div>
        <h3 class="min__name">About <em>FPG.</em></h3>
        <p class="min__body">Rooted in the Word, planted in the Valley. A family that&rsquo;s been pressing on together since 2004.</p>
      </a>
      <a class="min" href="/watch" style="text-decoration:none;">
        <svg class="min__icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="20" cy="20" r="14"/><path d="M 17 14 L 26 20 L 17 26 Z" fill="currentColor"/></svg>
        <div class="min__kicker">§ 03 · Watch</div>
        <h3 class="min__name">Sermons <em>on demand.</em></h3>
        <p class="min__body">Every sermon, every series. Sundays, revival nights, studies — all in one library.</p>
      </a>
      <a class="min" href="/events" style="text-decoration:none;">
        <svg class="min__icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="6" y="10" width="28" height="24" rx="1"/><path d="M 6 18 L 34 18 M 14 6 L 14 14 M 26 6 L 26 14"/></svg>
        <div class="min__kicker">§ 04 · Upcoming</div>
        <h3 class="min__name">What&rsquo;s <em>happening.</em></h3>
        <p class="min__body">Revival, studies, outreach, gatherings — come to any of them.</p>
      </a>
      <a class="min" href="/visit" style="text-decoration:none;">
        <svg class="min__icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M 20 6 C 12 6 8 12 8 18 C 8 26 20 34 20 34 C 20 34 32 26 32 18 C 32 12 28 6 20 6 Z"/><circle cx="20" cy="18" r="4"/></svg>
        <div class="min__kicker">§ 05 · Visit</div>
        <h3 class="min__name">Find a <em>seat.</em></h3>
        <p class="min__body">Harlingen campus, online worldwide. First-time visitor? We&rsquo;ll save you a spot.</p>
      </a>
      <a class="min" href="/ministries" style="text-decoration:none;">
        <svg class="min__icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="14" cy="18" r="5"/><circle cx="26" cy="18" r="5"/><path d="M 6 32 Q 14 26, 20 28 Q 26 26, 34 32"/></svg>
        <div class="min__kicker">§ 06 · Get rooted</div>
        <h3 class="min__name">Ministries &amp; <em>FBI.</em></h3>
        <p class="min__body">Kids, youth, young adults, small groups — plus Faith Bible Institute.</p>
      </a>
      <a class="min" href="/give" style="text-decoration:none;">
        <svg class="min__icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M 20 34 C 12 28 6 22 6 14 C 6 10 10 8 13 8 C 16 8 18 10 20 12 C 22 10 24 8 27 8 C 30 8 34 10 34 14 C 34 22 28 28 20 34 Z"/></svg>
        <div class="min__kicker">§ 08 · Give</div>
        <h3 class="min__name">Sow in <em>faith.</em></h3>
        <p class="min__body">Secure, tax-deductible giving. Tithes, missions, building, benevolence.</p>
      </a>
    </div>
  </section>
</main>
'''

HERO_WRAP = '<main class="wrap">\n' + HERO + '\n</main>\n'

# ---------- BOOKS — real cover images from fpgchurch.com -------------------
BOOK_ITEMS = [
    {
        "slug": "stand",
        "cover": "/assets/book-stand.jpg",
        "category": "Devotional · 30-day",
        "title": "Stand in the <em>Fire</em>",
        "subtitle": "How to trust God when everything is against you.",
        "author": "Veronica Ortiz",
        "url": "https://play.google.com/store/books/details?id=0vHFEQAAQBAJ",
        "desc": "A 30-day devotional built to anchor you when pressure mounts, voices rise, and everything says bow down. Practical, scripture-grounded, and written for the moment you need it most.",
    },
    {
        "slug": "wind",
        "cover": "/assets/book-wind.jpg",
        "category": "Pentecost · Revival history",
        "title": "Wind and <em>Fire</em>",
        "subtitle": "Pentecost and the Great Men &amp; Women God Used.",
        "author": "A JesusPOD Production",
        "url": "https://play.google.com/store/books/details/Wind_and_Fire_Pentecost_and_the_Great_Men_and_Wome?id=w5_EEQAAQBAJ",
        "desc": "A story-driven journey from the upper room in Jerusalem to canvas revival tents and open fields under African and Latin American skies — where wind and flame turned fearful disciples into fearless witnesses.",
    },
    {
        "slug": "faithful",
        "cover": "/assets/book-faithful.jpg",
        "category": "Stewardship · Discipleship",
        "title": "Faithful With Your <em>Now</em>",
        "subtitle": "Steward every area of your life for God&rsquo;s increase.",
        "author": "Veronica Ortiz",
        "url": "https://play.google.com/store/books/details?id=Hye7EQAAQBAJ",
        "desc": "A bold, practical call to stop making excuses and start stewarding every area of your life God&rsquo;s way. Your &ldquo;little things&rdquo; are the key to the &ldquo;more&rdquo; you&rsquo;ve been praying for.",
    },
    {
        "slug": "voice",
        "cover": "/assets/book-voice.jpg",
        "category": "Prayer · Spiritual growth",
        "title": "Hearing the <em>Voice</em> of Jesus",
        "subtitle": "Living every day led by His voice.",
        "author": "Kevin Ortiz",
        "url": "https://play.google.com/store/books/details?id=AiW7EQAAQBAJ",
        "desc": "What if the greatest need of your life is not more money, opportunities, or influence — but the ability to clearly hear the voice of Jesus? Move from empty religion to a loving relationship where His voice becomes your daily guide.",
    },
]

def book_card(b):
    # Strip HTML tags + entities from title for alt/aria text
    clean_title = re.sub(r'<[^>]+>', '', b['title']).replace('&rsquo;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"')
    return f'''<article class="book">
        <a class="book__cover-link" href="{b["url"]}" target="_blank" rel="noopener noreferrer" aria-label="{clean_title} by {b['author']} — download on Google Play (opens in new tab)">
          <img class="book__cover-img" src="{b['cover']}" alt="{clean_title} by {b['author']} — book cover" loading="lazy"/>
          <div class="book__corner" aria-hidden="true">
            <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M 10 3 L 10 14 M 5 9 L 10 14 L 15 9 M 4 17 L 16 17"/></svg>
          </div>
        </a>
        <div class="book__body">
          <div class="book__meta">{b["category"]}</div>
          <h3 class="book__title">{b["title"]}</h3>
          <p class="book__sub">{b["subtitle"]}</p>
          <p class="book__desc">{b["desc"]}</p>
          <div class="book__author">by {b["author"]}</div>
          <a class="book__pill" href="{b["url"]}" target="_blank" rel="noopener noreferrer">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M 8 2 L 8 11 M 4 7 L 8 11 L 12 7 M 3 14 L 13 14"/></svg>
            Download on Google Play
          </a>
        </div>
      </article>'''

BOOKS = f'''<section id="books" class="sec">
  <header class="sec-hd">
    <div>
      <div class="sec-hd__num">§ 04b</div>
      <div class="sec-hd__kicker">Books &amp; Resources</div>
    </div>
    <div>
      <h2 class="sec-hd__title">The teaching<br/>you can <em>take home.</em></h2>
      <p class="sec-hd__lede">Books from our pastors — on Google Play. Tap the cover or the download pill to get your copy.</p>
    </div>
  </header>
  <div class="books">
    {chr(10).join(book_card(b) for b in BOOK_ITEMS)}
  </div>
</section>
'''

# Home-page books teaser (compact — covers only, click to open book page)
HOME_BOOKS = f'''<main class="wrap">
  <section class="sec home-books" style="border-top: 0;">
    <header class="sec-hd">
      <div>
        <div class="sec-hd__num">§ Read</div>
        <div class="sec-hd__kicker">Books by our pastors</div>
      </div>
      <div>
        <h2 class="sec-hd__title">Teaching you can <em>take home.</em></h2>
        <p class="sec-hd__lede">Four books on Google Play — devotionals, revival history, stewardship, hearing His voice. Tap any cover to download.</p>
      </div>
    </header>
    <div class="home-books__grid">
      {"".join(
        f'''<a class="home-book" href="{b["url"]}" target="_blank" rel="noopener noreferrer" aria-label="Download {b['slug']}">
          <img src="{b['cover']}" alt="{b['slug']}" loading="lazy"/>
          <div class="home-book__pill"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M 8 2 L 8 11 M 4 7 L 8 11 L 12 7"/></svg> Download</div>
        </a>'''
        for b in BOOK_ITEMS
      )}
    </div>
    <div class="home-books__footer">
      <a href="/books" class="btn btn--ghost">See all books &amp; resources <span aria-hidden="true">→</span></a>
    </div>
  </section>
</main>
'''

# ---------- JESUSPOD — full-bleed dark feature band -----------------------
JESUSPOD_LINKS = {
    "web":  "https://jesuspod.com/",
    "ios":  "https://apps.apple.com/us/app/jesuspod-christian-medias/id6642658345",
    "and":  "https://play.google.com/store/apps/details?id=com.jesuspod.app",
}

# Home-page teaser band (condensed version, full-bleed dark w/ JesusPod brand colors)
JESUSPOD_BAND = f'''<section class="jp-band" id="jesuspod-band">
  <div class="jp-band__wrap">
    <div class="jp-band__left">
      <div class="jp-band__wordmark">Jesus<span class="pod">POD</span></div>
      <div class="jp-band__kicker">● A global thrust from Faith Pleases God</div>
      <h2 class="jp-band__title">All your favorite Christian content, <em>in one place.</em></h2>
      <p class="jp-band__lede">JesusPod brings the world&rsquo;s best sermons, podcasts, movies, radio, books and 24/7 live streams into a single app. Free to download — and FPG has its own channel inside.</p>
      <div class="jp-band__cats">
        <span class="on">All</span><span>Live</span><span>Podcast</span><span>Radio</span><span>Channels</span><span>Movies</span><span>Books</span>
      </div>
      <div class="jp-band__actions">
        <a href="/jesuspod" class="jp-band__cta">Explore JesusPod <span aria-hidden="true">→</span></a>
        <a href="{JESUSPOD_LINKS['ios']}" target="_blank" rel="noopener noreferrer" class="jp-store jp-store--app">
          <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M14.94 10.52c-.02-2.03 1.66-3 1.73-3.05-.94-1.38-2.41-1.57-2.93-1.59-1.25-.13-2.44.73-3.07.73-.64 0-1.61-.71-2.65-.69-1.36.02-2.62.79-3.32 2-1.42 2.45-.36 6.08 1.02 8.07.68.98 1.48 2.07 2.52 2.03 1.02-.04 1.4-.65 2.63-.65s1.58.65 2.65.63c1.09-.02 1.78-.99 2.45-1.97.77-1.13 1.09-2.23 1.11-2.29-.02-.01-2.13-.82-2.14-3.22zM12.94 4.69c.56-.68.94-1.63.84-2.57-.81.03-1.79.54-2.37 1.22-.52.6-.97 1.56-.85 2.49.9.07 1.82-.46 2.38-1.14z"/></svg>
          <span><small>Download on the</small>App Store</span>
        </a>
        <a href="{JESUSPOD_LINKS['and']}" target="_blank" rel="noopener noreferrer" class="jp-store jp-store--play">
          <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M3.5 2.2v15.6c0 .4.5.7.9.4l11.2-7.8c.3-.2.3-.7 0-.9L4.4 1.7c-.4-.2-.9.1-.9.5z"/></svg>
          <span><small>Get it on</small>Google Play</span>
        </a>
      </div>
    </div>
    <div class="jp-band__right" aria-hidden="true">
      <div class="jp-phone">
        <div class="jp-phone__screen">
          <div class="jp-phone__header">
            <div class="jp-phone__logo">Jesus<em>POD</em></div>
            <div class="jp-phone__signin">Sign in</div>
          </div>
          <div class="jp-phone__pills">
            <span class="on">All</span><span>Live</span><span>Podcast</span><span>Radio</span>
          </div>
          <div class="jp-phone__feature">
            <strong>FPG · Latest sermon</strong>
          </div>
          <div class="jp-phone__sectitle">Popular &amp; Trending</div>
          <div class="jp-phone__grid">
            <div></div><div></div><div></div>
            <div></div><div></div><div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

JESUSPOD_PAGE = f'''<section class="jp-hero">
  <div class="jp-hero__wrap">
    <div class="jp-hero__wordmark">Jesus<em>POD</em></div>
    <div class="jp-hero__meta">
      <span class="tick"></span>
      <span>Available worldwide · Free</span>
      <span class="sep">·</span>
      <span>iOS · Android · Web</span>
    </div>
    <h1 class="jp-hero__title">All your favorite Christian content, <em>in one place.</em></h1>
    <p class="jp-hero__lede">JesusPod is a global home for the world&rsquo;s best Christian content — sermons, podcasts, 24/7 live streams, radio, films and books. Hundreds of thousands of hours in one app, gathered from ministries all over the earth. It&rsquo;s one of the biggest thrusts in the reach of Faith Pleases God, and FPG has its own channel inside.</p>
    <div class="jp-hero__actions">
      <a href="{JESUSPOD_LINKS['ios']}" target="_blank" rel="noopener noreferrer" class="jp-store jp-store--app">
        <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M14.94 10.52c-.02-2.03 1.66-3 1.73-3.05-.94-1.38-2.41-1.57-2.93-1.59-1.25-.13-2.44.73-3.07.73-.64 0-1.61-.71-2.65-.69-1.36.02-2.62.79-3.32 2-1.42 2.45-.36 6.08 1.02 8.07.68.98 1.48 2.07 2.52 2.03 1.02-.04 1.4-.65 2.63-.65s1.58.65 2.65.63c1.09-.02 1.78-.99 2.45-1.97.77-1.13 1.09-2.23 1.11-2.29-.02-.01-2.13-.82-2.14-3.22zM12.94 4.69c.56-.68.94-1.63.84-2.57-.81.03-1.79.54-2.37 1.22-.52.6-.97 1.56-.85 2.49.9.07 1.82-.46 2.38-1.14z"/></svg>
        <span><small>Download on the</small>App Store</span>
      </a>
      <a href="{JESUSPOD_LINKS['and']}" target="_blank" rel="noopener noreferrer" class="jp-store jp-store--play">
        <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M3.5 2.2v15.6c0 .4.5.7.9.4l11.2-7.8c.3-.2.3-.7 0-.9L4.4 1.7c-.4-.2-.9.1-.9.5z"/></svg>
        <span><small>Get it on</small>Google Play</span>
      </a>
      <a href="{JESUSPOD_LINKS['web']}" target="_blank" rel="noopener noreferrer" class="jp-hero__web">Open on the web <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

<section class="jp-cats">
  <div class="jp-cats__wrap">
    <header class="jp-cats__hd">
      <div>
        <div class="jp-cats__label">● What&rsquo;s inside</div>
        <div class="jp-cats__kicker">8 ways to grow</div>
      </div>
      <div>
        <h2 class="jp-cats__title">A single app, <em>every kind</em> of teaching.</h2>
        <p class="jp-cats__lede">Instead of hopping between sites, everything you need to stay encouraged and connected to the Word — gathered, curated, and always with you.</p>
      </div>
    </header>
    <div class="jp-cat-grid">
      <article class="jp-cat">
        <div class="jp-cat__num">01</div>
        <h3>Popular &amp; <em>Trending</em></h3>
        <p>What the global church is pressing into right now — updated daily.</p>
      </article>
      <article class="jp-cat">
        <div class="jp-cat__num">02</div>
        <h3>Live <em>streams</em></h3>
        <p>24/7 worship, prayer rooms, services and broadcasts from ministries around the world.</p>
      </article>
      <article class="jp-cat">
        <div class="jp-cat__num">03</div>
        <h3><em>Radio</em></h3>
        <p>Christian stations in English, Español, Portuguese, French and more — one tap away.</p>
      </article>
      <article class="jp-cat">
        <div class="jp-cat__num">04</div>
        <h3>Movies &amp; <em>films</em></h3>
        <p>Feature-length Christian cinema, documentaries, and revival-history retellings.</p>
      </article>
      <article class="jp-cat">
        <div class="jp-cat__num">05</div>
        <h3><em>Podcasts</em></h3>
        <p>Sermons and teaching shows from pastors, authors and missionaries — bookmark, resume, download.</p>
      </article>
      <article class="jp-cat">
        <div class="jp-cat__num">06</div>
        <h3>Video <em>channels</em></h3>
        <p>Ministry channels with full sermon libraries. FPG has its own channel inside.</p>
      </article>
      <article class="jp-cat">
        <div class="jp-cat__num">07</div>
        <h3><em>Books</em></h3>
        <p>Classics and new releases — from Moody and Hagin to today&rsquo;s voices.</p>
      </article>
      <article class="jp-cat">
        <div class="jp-cat__num">08</div>
        <h3>Your <em>growth</em></h3>
        <p>Save, like, queue and revisit — a quiet daily habit, not another scroll.</p>
      </article>
    </div>
  </div>
</section>

<main class="wrap">
  <section class="sec" style="border-top: 1px solid var(--bone-rule);">
    <header class="sec-hd">
      <div><div class="sec-hd__num">§ FPG on JesusPod</div><div class="sec-hd__kicker">Our channel</div></div>
      <div><h2 class="sec-hd__title">Faith Pleases God,<br/><em>inside</em> the app.</h2>
        <p class="sec-hd__lede">Our full sermon library lives on JesusPod — search &ldquo;Faith Pleases God Church&rdquo; or tap below to open our channel in the app.</p>
      </div>
    </header>
    <div class="jp-channel">
      <div class="jp-channel__card">
        <div class="jp-channel__logo" aria-hidden="true">
          <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">
              <line x1="6" y1="44" x2="58" y2="44"/>
              <path d="M 18 44 A 14 14 0 0 1 46 44"/>
              <line x1="32" y1="10" x2="32" y2="18"/>
              <line x1="14" y1="18" x2="19" y2="23"/>
              <line x1="50" y1="18" x2="45" y2="23"/>
              <line x1="8" y1="32" x2="14" y2="32"/>
              <line x1="50" y1="32" x2="56" y2="32"/>
            </g>
          </svg>
        </div>
        <div class="jp-channel__meta">
          <div class="jp-channel__kicker">● Featured channel · Harlingen, TX</div>
          <h3 class="jp-channel__name">Faith Pleases God Church on <em>JesusPOD</em></h3>
          <p class="jp-channel__body">Every Sunday service, every revival night, every teaching series — English and Español — in one searchable library. Listen on the drive, in the kitchen, on the job site.</p>
          <div class="jp-channel__stats">
            <div><strong>200+</strong><span>Sermons &amp; series</span></div>
            <div><strong><em>EN</em> · ES</strong><span>Bilingual library</span></div>
            <div><strong>Free</strong><span>No paywall, ever</span></div>
          </div>
          <div class="jp-channel__actions">
            <a href="{JESUSPOD_LINKS['web']}" target="_blank" rel="noopener noreferrer" class="jp-channel__cta">Open our channel <span aria-hidden="true">→</span></a>
            <a href="/watch" class="jp-channel__cta jp-channel__cta--ghost">Watch on fpgchurch.com</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="sec">
    <header class="sec-hd">
      <div><div class="sec-hd__num">§ Why it matters</div><div class="sec-hd__kicker">A vision, not a platform</div></div>
      <div><h2 class="sec-hd__title">The Gospel goes where<br/><em>the algorithm</em> won&rsquo;t.</h2></div>
    </header>
    <div class="about">
      <div class="jp-why">
        <p>JesusPod isn&rsquo;t another social feed fighting for your attention. It&rsquo;s a <em>sanctuary</em> — a place where the only thing surfacing to the top is teaching that builds faith, testimonies that lift your head, and worship that moves your heart.</p>
        <p>Faith Pleases God Church believes that what God is doing in the Rio Grande Valley belongs to the whole world. JesusPod is how a sermon preached on a Sunday night in Harlingen ends up in headphones in Lagos, in São Paulo, in Manila, in Madrid — in the hand of someone who just needed to hear it.</p>
        <p>That&rsquo;s why we&rsquo;re all in. Download the app. Share it with a friend. Find your corner of the global family.</p>
      </div>
      <aside class="jp-cta-card">
        <div class="jp-cta-card__kicker">● Download free</div>
        <h3 class="jp-cta-card__title">Get <em>JesusPOD.</em></h3>
        <p class="jp-cta-card__body">Built for believers around the world. No subscription, no ads interrupting the sermon, no dark patterns. Just grow.</p>
        <a href="{JESUSPOD_LINKS['ios']}" target="_blank" rel="noopener noreferrer" class="jp-store jp-store--app">
          <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M14.94 10.52c-.02-2.03 1.66-3 1.73-3.05-.94-1.38-2.41-1.57-2.93-1.59-1.25-.13-2.44.73-3.07.73-.64 0-1.61-.71-2.65-.69-1.36.02-2.62.79-3.32 2-1.42 2.45-.36 6.08 1.02 8.07.68.98 1.48 2.07 2.52 2.03 1.02-.04 1.4-.65 2.63-.65s1.58.65 2.65.63c1.09-.02 1.78-.99 2.45-1.97.77-1.13 1.09-2.23 1.11-2.29-.02-.01-2.13-.82-2.14-3.22zM12.94 4.69c.56-.68.94-1.63.84-2.57-.81.03-1.79.54-2.37 1.22-.52.6-.97 1.56-.85 2.49.9.07 1.82-.46 2.38-1.14z"/></svg>
          <span><small>Download on the</small>App Store</span>
        </a>
        <a href="{JESUSPOD_LINKS['and']}" target="_blank" rel="noopener noreferrer" class="jp-store jp-store--play">
          <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M3.5 2.2v15.6c0 .4.5.7.9.4l11.2-7.8c.3-.2.3-.7 0-.9L4.4 1.7c-.4-.2-.9.1-.9.5z"/></svg>
          <span><small>Get it on</small>Google Play</span>
        </a>
        <a href="{JESUSPOD_LINKS['web']}" target="_blank" rel="noopener noreferrer" class="jp-cta-card__web">or visit <strong>jesuspod.com</strong> <span aria-hidden="true">→</span></a>
      </aside>
    </div>
  </section>
</main>
'''


# ---------- Write pages ----------------------------------------------------
page("index", "Home",
     "A family of believers in Harlingen, Texas — English & Español. Spring Revival April 22–26, 2026. All are welcome.",
     HERO_WRAP + TICKER + HOME_BOOKS + JESUSPOD_BAND + HOME_TEASERS, current="home")

page("jesuspod", "JesusPod",
     "All your favorite Christian content in one place. JesusPod is a global home — hundreds of thousands of hours of sermons, podcasts, 24/7 live streams, radio, films and books. FPG has its own channel inside.",
     JESUSPOD_PAGE, current="jesuspod")

PASTORS_SECTION = '''<section class="sec pastors" data-screen-label="Pastors">
  <header class="sec-hd">
    <div>
      <div class="sec-hd__num">§ Pastors</div>
      <div class="sec-hd__kicker">The people in the room</div>
    </div>
    <div>
      <h2 class="sec-hd__title">Meet <em>the family.</em></h2>
      <p class="sec-hd__lede">Teaching, preaching, and shepherding FPG in English and Español.</p>
    </div>
  </header>
  <div class="pastors__grid">
    <article class="pastor">
      <div class="pastor__kicker">Senior Pastor · English</div>
      <h3 class="pastor__name">Pastor Kevin <em>Ortiz</em></h3>
      <p class="pastor__tag">Helping believers hear the voice of Jesus and walk in Spirit-led, faith-filled authority every day.</p>
      <p class="pastor__bio">Pastor Kevin Ortiz is the senior pastor of Faith Pleases God Church in Harlingen, Texas, serving alongside his wife, Pastora Veronica Ortiz. Together they have been in full-time ministry for 18 years and have relaunched the media legacy of late founding pastor Carlos Ortiz — preaching the gospel on international TV in the UK and Africa. Pastor, evangelist, and teacher; author of <em>Hearing the Voice of Jesus</em>, <em>Stand Your Ground</em>, <em>ANOTHER MAN</em>, <em>A Spirit of Prayer</em>, and <em>Power &amp; Authority</em>.</p>
    </article>
    <article class="pastor">
      <div class="pastor__kicker">Co-Pastor · English</div>
      <h3 class="pastor__name">Pastora Veronica <em>Ortiz</em></h3>
      <p class="pastor__tag">Bold, practical, faith-filled teaching that strengthens believers in every area of life.</p>
      <p class="pastor__bio">Pastora Veronica Ortiz serves as co-pastor of Faith Pleases God Church alongside her husband, Pastor Kevin Ortiz. She ministers the Word with a bold, faith-filled, practical preaching style, carrying a passion to see believers strengthened spiritually, physically, mentally, socially, and financially so they can walk fully in God&rsquo;s purpose. Author of <em>Faithful With Your Now</em>, <em>Stand in the Fire</em>, and the children&rsquo;s book <em>This Little Light of Mine</em>.</p>
    </article>
    <article class="pastor">
      <div class="pastor__kicker">Español Pastor</div>
      <h3 class="pastor__name">Pastor Rey <em>Mejia</em></h3>
      <p class="pastor__tag">Carrying the gospel of faith to the Spanish-speaking Rio Grande Valley and beyond.</p>
      <p class="pastor__bio">Pastor Rey Mejia leads the Spanish-language ministry at Faith Pleases God Church, serving alongside his wife, Pastora Julie Mejia. Together they shepherd FPG Church Español, preaching weekly at the Sunday 8:30 AM and Tuesday 7:00 PM Spanish services in Harlingen — and producing FPG&rsquo;s weekly Spanish-language messages that reach a growing audience across the Valley and beyond.</p>
    </article>
  </div>
</section>
'''
page("about", "About",
     "Founded in the Valley, rooted in the Word. Meet Faith Pleases God Church — pastors Kevin & Veronica Ortiz (English) and Rey Mejia (Español), pressing on together in Harlingen since 2004.",
     wrap(ABOUT + PASTORS_SECTION), current="about")

# Watch is full-bleed (no wrap)
page("watch", "Watch & Sermons",
     "Every sermon, every series, on demand. Sundays, revival nights, teaching — caught up or rewinding, it's all here.",
     WATCH, current="watch")

EVENTS_FIXED = (EVENTS
    # Featured revival card: put the start day "22" in .day slot (was "Spring")
    .replace('<div class="event__date">Apr 22 – 26<span class="day">Spring</span><span class="yr">2026 · Every night 7pm</span></div>',
             '<div class="event__date">Apr 22 – 26<span class="day">22</span><span class="yr">Wed – Sun · 7 PM nightly</span></div>')
    # Standardize CTA labels: Register | Details (was a mix of 5 different labels)
    .replace('<a href="/visit" class="event__cta">Más info</a>',
             '<a href="/visit" class="event__cta">Details</a>')
    .replace('<a href="/visit" class="event__cta">Plan visit</a>',
             '<a href="/visit" class="event__cta">Details</a>')
    .replace('<a href="/visit" class="event__cta">More info</a>',
             '<a href="/visit" class="event__cta">Details</a>')
    .replace('<a href="/visit" class="event__cta">I&rsquo;m in</a>',
             '<a href="/visit" class="event__cta">Details</a>'))

page("events", "Events",
     "What's happening at the church — revival, studies, outreach, gatherings. All welcome, most free.",
     wrap(EVENTS_FIXED), current="events")

def _fieldset_wrap(src):
    """Convert a .field div containing a group label + .field__check into fieldset/legend."""
    pattern = re.compile(
        r'<div class="field">\s*<label>([^<]+)</label>\s*(<div class="field__check">.*?</div>)\s*</div>',
        re.DOTALL
    )
    return pattern.sub(
        r'<fieldset class="field field--group"><legend>\1</legend>\2</fieldset>',
        src
    )

VISIT_MERGED = wrap(
    VISIT
        .replace('4501 W Expressway 83<br/>',
                 '<a href="https://maps.google.com/?q=4501+W+Expressway+83,+Harlingen,+TX+78552" target="_blank" rel="noopener noreferrer">4501 W Expressway 83<br/>')
        .replace('Harlingen, TX 78552<br/>',
                 'Harlingen, TX 78552</a><br/>')
        .replace('(956) 412-5600',
                 '<a href="tel:+19564125600">(956) 412-5600</a>'),
    _fieldset_wrap(CONNECT
        .replace('<section id="connect" class="sec" data-screen-label="07 Connect">',
                 '<section id="plan" class="sec" data-screen-label="Plan your visit">')
        .replace('Apr 27 · 10 AM', 'Apr 27 · 11 AM')
        .replace('English · 10 AM', 'English · 11 AM')
        .replace('Español · 12 PM', 'Español · 8:30 AM')
        # Form semantics: add name/value to submit real data; mark required fields
        .replace('<input id="cn-name" type="text"',
                 '<input id="cn-name" name="name" type="text" autocomplete="name" required')
        .replace('<input id="cn-email" type="email"',
                 '<input id="cn-email" name="email" type="email" autocomplete="email" required')
        .replace('<input id="cn-date" type="text"',
                 '<input id="cn-date" name="date" type="text"')
        .replace('<label><input type="checkbox" /> Spouse</label>',
                 '<label><input type="checkbox" name="coming[]" value="spouse" /> Spouse</label>')
        .replace('<label><input type="checkbox" /> Kids (0–5)</label>',
                 '<label><input type="checkbox" name="coming[]" value="kids-0-5" /> Kids (0–5)</label>')
        .replace('<label><input type="checkbox" /> Kids (K–12)</label>',
                 '<label><input type="checkbox" name="coming[]" value="kids-k-12" /> Kids (K–12)</label>')
        .replace('<label><input type="checkbox" /> Friend</label>',
                 '<label><input type="checkbox" name="coming[]" value="friend" /> Friend</label>')
        .replace('<label><input type="checkbox" /> Just me</label>',
                 '<label><input type="checkbox" name="coming[]" value="just-me" /> Just me</label>')
        .replace('<input type="radio" name="cn-lang" checked />',
                 '<input type="radio" name="lang" value="en" checked />')
        .replace('<input type="radio" name="cn-lang" />',
                 '<input type="radio" name="lang" value="es" />'))
)

page("visit", "Plan a Visit",
     "Find a seat at the table. Harlingen campus — first-time visitors get a parking spot, a warm welcome, and exactly what to expect on Sunday.",
     VISIT_MERGED, current="visit")

page("ministries", "Ministries",
     "A place for everyone in the house — kids, youth, young adults, small groups, plus Faith Bible Institute.",
     wrap(MINS), current="ministries")

page("books", "Books & Resources",
     "Books from our pastors — available on Google Play. Wind and Fire, Faithful With Your Now, Hearing the Voice of Jesus.",
     wrap(BOOKS), current="books")

# /connect retained as alias so old links don't break, but routes to same content
page("connect", "Plan a Visit",
     "Walking into a new church is hard. Here's what to expect — and a way to say hi before you do.",
     VISIT_MERGED, current="visit")

# Give is full-bleed (no wrap)
page("give", "Give",
     "Sow into the work of the Kingdom. Secure, tax-deductible giving. Tithes, missions, building fund, benevolence.",
     GIVE, current="give")

CONTACT_TAPPABLE = (CONTACT
    .replace('(956) 412-5600', '<a href="tel:+19564125600">(956) 412-5600</a>')
    .replace('4501 W Expressway 83, Harlingen, TX 78552',
             '<a href="https://maps.google.com/?q=4501+W+Expressway+83,+Harlingen,+TX+78552" target="_blank" rel="noopener noreferrer">4501 W Expressway 83, Harlingen, TX 78552</a>'))
page("contact", "Contact",
     "Every email answered within 48 hours, by a person on staff. Phone, email, prayer requests, service times.",
     wrap(CONTACT_TAPPABLE), current="contact")

print("Built pages:")
for p in sorted(ROOT.glob("*.html")):
    print(f"  /{p.stem}")
