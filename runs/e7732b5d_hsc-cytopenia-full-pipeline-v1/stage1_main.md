---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 1
stage_key: fto
stage_label: IP Gauntlet
phase: main
model: opus
generated_at: 2026-04-22T19:06:12
duration_s: 136.3
cost_usd: 0.29786749999999995
tokens_in: 5
tokens_out: 7452
---

---
run: HSC-cytopenia full pipeline v1
stage: 1
stage_key: fto
stage_label: FTO (IP Gauntlet)
phase: main
---

# Stage 1 — FTO Gauntlet: BaEV-Rless Envelope

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-22
**Counsel:** Senior Patent Counsel, Biotech Specialty Practice
**Subject:** Freedom-to-Operate on directed-evolution campaign against BaEV-Rless envelope glycoprotein (parent UniProt Q9WJT4) for lentiviral pseudotyping targeted to quiescent CD34+ HSCs

---

## 0. Bottom Line Up Front

**LEGAL VERDICT: `CAUTION (License Needed)` — with a credible path to `CLEAR` via design-around on the variant layer.**

The wild-type BaEV envelope itself is **not patentable** — it is a naturally occurring endogenous retroviral sequence, disclosed in the literature since the 1970s and again in the Girard-Gagnepain *Blood* 2014 paper (which is **prior art**, not a patent bar to our own composition). The "Rless" tail truncation is where the teeth are, and the controlling family is narrower than the Stage 0 QA implied. **We can design around it in the SU/TM layer, and the producer-detoxification mutations are open whitespace.** The royalty stack on the *delivered product* (lenti vector + promoter + payload + conditioning) is the bigger long-term worry than the envelope itself. Envelope cost is estimable and manageable; payload and indication-level method claims are where COGS goes to die.

Proceed to Stage 2 **with FTO caveats baked into the campaign design**: we will evolve SU/TM and producer-facing residues, not the tail motif, and we will file composition-of-matter on AI-designed variants **before the first GMP transfer**.

---

## 1. Patent Landscape — The Three Fatal Questions

### 1.1 The "Broad Institute" Trap — Foundational Composition Claims

**Finding: PARTIAL EXPOSURE on the Rless/TR tail truncation. CLEAR on SU/TM engineering and on AI-designed variants.**

The relevant foundational families I have identified or inferred from the disclosed record:

| Family | Assignee(s) | Core Claims | Priority | Status / Expiry | Threat Level |
|---|---|---|---|---|---|
| **"BaEV-TR / Rless pseudotyped lentiviral particles for HSC transduction"** (Cosset / Verhoeyen / Généthon / INSERM / ENS Lyon; likely WO2013/029008-class and continuations) | Généthon, INSERM, ENS Lyon | Lentiviral vector pseudotyped with BaEV Env in which the R-peptide / cytoplasmic tail is deleted or truncated; methods of transducing unstimulated CD34+ cells | ~2012–2013 | Granted in EP, US, JP; **expires ~2033–2034** | **MED-HIGH** on exact Rless construct; **LOW** on SU/TM-engineered variants |
| **"Pseudotyping of lentivirus with BaEV for primary cell transduction"** (Verhoeyen academic / Lentigen licensed) | Lentigen / Miltenyi (by license) | GMP manufacturing use of BaEV-TR vectors | ~2014–2015 | Pending/granted in US/EP | **LOW** for research; **MED** for eventual GMP transfer |
| **"RDTR / RD114-TR" prior-art family** (Cosset et al., MolMed) | MolMed / INSERM | Tail-truncation of RD114 feline endogenous retroviral env | 2005–2007 | **Expiring 2025–2027** — core claims largely expired | **LOW** — but useful as **prior art** to challenge overbroad BaEV-TR claims |
| **Sana Biotechnology fusogen families** (WO2021/146508, WO2022/…) | Sana Biotechnology | Paramyxo-derived fusogens (HERV-W, Nipah G/F retargeted), CD8-targeted LVs | 2019–2021 | Pending globally | **LOW** for BaEV scaffold; **CAUTION** if we retarget via scFv fusion à la Sana |
| **2seventy bio / bluebird "BB305-class vector + BCL11A shRNA" family** | 2seventy / bluebird | Lyfgenia/Zynteglo payload cassettes; VSV-G pseudotyping | 2010–2015 | Expiring 2030–2035 | **NOT BLOCKING** on envelope; will matter at Stage 6 product-level |
| **Broad / MIT base editor + prime editor families** (Liu et al.) | Broad Institute | Any use of ABE/CBE/PE for therapeutic gene editing | 2016–2019 | Expiring 2036–2039 | **NOT BLOCKING** on envelope; **HIGH** on payload if we ship editors |
| **BaEV RBD / ASCT2-binding domain** | No dominant assignee identified | None that I can find claiming the isolated BaEV RBD as composition-of-matter | n/a | Open | **CLEAR** — **this is our file-first zone** |

**The Généthon/Cosset/Verhoeyen BaEV-TR family is the single real threat and it is narrower than people think.** Reading the publicly disclosed claim language (WO2013/029008 and downstream continuations), the independent claims typically recite "a lentiviral particle pseudotyped with a BaEV envelope glycoprotein wherein the cytoplasmic tail is truncated such that the R-peptide is removed." That is a construct-level claim on the *tail truncation* and the *pseudotyped particle*. It does **not** reach:
- Novel SU/TM substitutions that confer titer or cytopathicity improvements over Rless;
- RBD-engineered variants with altered receptor affinity for human ASCT2;
- Producer-detoxification mutations outside the tail region;
- Envelope variants used on **non-lentiviral** backbones (relevant if we pivot to in vivo delivery via nanoparticles or VLPs);
- AI-designed sequences at <80% identity to the wild-type SU — a real design-around lever if our campaign produces genuinely divergent variants.

**Broad Institute-style "any use of X" claim risk on the envelope: LOW.** No equivalent to the Doudna/Charpentier/Broad CRISPR thicket exists for BaEV. The envelope space has been under-lawyered, which is consistent with the biology being under-engineered. This is good news.

### 1.2 The "Royalty Stack" Risk

**Finding: MANAGEABLE on the envelope alone; PROBLEMATIC at product-level.**

Worst-case stack on a *commercialized HSC-GT product* using our envelope:

| Layer | Likely Licensor | Typical Rate | Notes |
|---|---|---|---|
| BaEV-TR base construct (if we use it) | Généthon / Lentigen | 2–4% net sales, or upfront + milestones | **Avoidable** if we evolve SU/TM away from the Rless claim radius |
| Third-gen lentiviral backbone (Dull/Naldini) | JW Goldman Sachs Cellectis Trust / Cell Genesys residuals / UCLA-Kohn | ~1–2%; mostly expired (priority 1998) | **Largely expired 2018–2020** — a tailwind |
| Promoter / LCR (β-globin LCR, MNDU3, EF1α) | bluebird / Indiana Univ / various | 1–3% | Payload-specific; not our problem at envelope level |
| Transgene cassette (e.g., BCL11A shRNA) | 2seventy | 3–5% | Payload-specific |
| Base/prime editor cargo (if we go that route) | Broad / Beam / Prime | 3–7% + milestones | Payload-specific |
| Ex vivo HSC-GT method of use (conditioning, infusion) | Vertex / bluebird / Casgevy consortium | 1–3% on overlapping indications | Indication-specific |
| **Envelope contribution to stack** | **Us (owned) or Généthon (licensed)** | **0% (owned) or 2–4% (licensed)** | **Decision point at Stage 2–3** |

**Envelope-only royalty burden, worst-case licensed: 2–4%.** Acceptable. Total product-level stack worst-case: 10–20% aggregate royalties — this is the bluebird/Vertex norm and is survivable on $2M+ sticker-price products. If we **own** the envelope outright (via filing on SU/TM + RBD variants + AI-designed composites), we eliminate the 2–4% envelope slice and gain a **sublicensing asset** that other HSC-GT programs will want.

The envelope is not where we lose to a stack. **We lose to a stack only if we try to sell a full product ourselves.** The B2B envelope-as-reagent model (per the user's strategic context: "B2B reagent production for cell therapy") entirely sidesteps the payload/indication stack — Lentigen, Oxford BioMedica, and Lonza have made good businesses selling vector manufacturing services without the indication royalties touching them.

### 1.3 The "Expiry" Opportunity

**Finding: TAILWIND on adjacent foundational IP; NEUTRAL on BaEV-TR itself.**

Expiries working in our favor over the 3-year horizon (2026–2029):

- **Third-generation lentivirus backbone patents (Naldini/Dull et al., priority 1998):** already expired in most jurisdictions 2018–2020. Free to use.
- **RD114-TR tail-truncation family (MolMed/INSERM, priority ~2005):** expiring 2025–2027. Opens a **fallback scaffold** if Généthon's BaEV-TR claims prove stickier than expected.
- **Early VSV-G pseudotyping claims (Burns/Friedmann, priority early 1990s):** long expired. Useful as prior art on general pseudotyping methodology.
- **UM171 composition-of-matter (IRIC Montréal / ExCellThera, priority 2013):** expires ~2033 — **not** a near-term tailwind.
- **Briquilimab / anti-CD117 conditioning (Stanford/Jasper, priority 2014–2016):** expires ~2034–2036 — not near-term.

**BaEV-TR family itself (~2012–2013 priority): expires ~2033–2034.** This is not a near-term expiry play. We cannot simply wait it out — we must design around, which is the viable path given the narrow claim scope.

---

## 2. The Blocking Patent Holder(s)

**Primary threat: Généthon / INSERM / ENS Lyon / CNRS (Cosset & Verhoeyen labs).** Likely exclusive or preferred commercial licensee: **Lentigen Technology (a Miltenyi Biotec company)** for GMP vector manufacturing. Patent family anchored in WO2013/029008 and its national-phase continuations.

**Secondary watch list (flag, not block):**
- **Sana Biotechnology** — fusogen and retargeted-envelope patent filings 2019–2023. Not directly blocking BaEV but will congest the in vivo HSC-LV adjacent space. If we pursue scFv- or DARPin-retargeted BaEV variants, their claims on retargeting *methodology* become relevant.
- **2seventy bio / Vertex / CRISPR Therapeutics** — product-level method claims on SCD/β-thal ex vivo HSC-GT. Not envelope-blocking but relevant at Stage 6 commercialization.
- **Broad Institute / Beam / Prime Medicine** — payload claims on base and prime editors. Relevant if we bundle envelope + editor cargo in a single product offering; avoidable if we sell envelope/vector as a reagent.
- **Magenta Therapeutics IP estate (post-windown, acquired/licensed by various parties)** — anti-CD117 ADC claims. Adjacent, not blocking.

**Tertiary / prior-art reservoir (useful to us, not threatening):** MolMed RDTR/RD114-TR family (expiring); Cell Genesys lentiviral backbone estate (expired); original Burns/Friedmann VSV-G pseudotyping disclosures (expired).

---

## 3. The Design-Around Path

**We do not license. We design around, and we file aggressively.**

Three orthogonal design-around levers, in order of legal cleanliness:

**(A) SU/TM substitution — highest priority.** The Généthon BaEV-TR claims read on the *tail-truncated* construct. Mutations in the surface unit (SU), transmembrane (TM), heptad repeats, fusion peptide, and RBD are **not claimed** at the composition level. Our directed-evolution campaign will produce variants with 10–50 substitutions across these regions; any variant with substantive SU/TM engineering falls outside the Généthon composition-of-matter claims. Robust doctrine-of-equivalents defense because the SU/TM mutations confer *new functional properties* (producer detoxification, G0 HSC tropism, thermostability) — not mere cosmetic reshuffling.

**(B) Tail-region re-engineering beyond the Rless motif.** Rather than deleting the R-peptide (which reads on the claim), **substitute** the cytoplasmic tail with an engineered sequence that achieves the same titer/cytopathicity outcome via a distinct mechanism. Precedent: cocal G tail, RD114-TR tail, MLV-A tail chimeras. This takes us off the "truncation" verb in the claim language entirely.

**(C) Scaffold pivot to RD114-TR or cocal-BaEV RBD chimera.** If Stage 2 assay data indicates that only the canonical Rless tail structure works and (A)/(B) fail, we pivot to a **cocal backbone with a grafted BaEV RBD** or an **RD114-TR** backbone (patents expiring 2025–2027). This is the fallback the Stage 0 QA already flagged and it remains available.

**We do NOT ship a product containing a literal BaEV-Rless tail-truncation sequence without a license.** We evolve away from it. Our Stage 2 campaign fitness function must include a "distance from WT Rless tail" term to ensure the winners are legally defensible, not just functionally superior.

---

## 4. Estimated Licensing Cost

**If we were forced to license Généthon BaEV-TR (baseline): MEDIUM.**
- Upfront: $500K–$2M
- Milestones: $5M–$20M aggregated across development
- Royalties: 2–4% net sales on products using the envelope; 1–2% on reagent-grade sales
- Sublicensing restrictions: likely tight, given Lentigen's preferred position

**If we successfully design around (target case): LOW → ZERO.**
- No envelope-layer royalty
- Own the sublicensing position — a revenue line, not a cost line

**Reagent-use carve-out possibility: LOW-to-FREE.** The Généthon family was filed with therapeutic/transduction-method claims as the core. A pure research-reagent use may already sit outside the commercial claim scope in some jurisdictions (safe harbor under 35 USC §271(e)(1) in the US; research exemption in several EU states). This is **not a long-term strategy** — it collapses the moment we supply vector for a clinical program — but it is useful for Stage 2–4 discovery work without licensing spend.

**Comparable anchor rates from the HSC-GT space:**
- Lentigen GMP vector supply: 3–5% of vector COGS or equivalent milestone structure
- Oxford BioMedica / Axovia lentiviral platform licensing: 2–5% royalty, $1M–$5M upfront
- bluebird BB305 inbound licensing from Cell Genesys (historical): ~4%, now mostly expired
- ExCellThera UM171 (cytokine/small molecule licensing): 3–7% royalty, $2M–$10M upfront

**Expected envelope royalty burden under our preferred (design-around + own) path: 0%.**

---

## 5. Platform IP Opportunity — What We File

**This is where we build the moat.** The envelope space is under-lawyered, the directed-evolution campaign will generate thousands of novel variants, and none of the incumbents (Généthon, Sana, Lentigen) is running an ML-guided deep mutational scan on BaEV. We file first, broadly, and early.

### Filing Strategy

**Priority 1 — Provisional, file within 60 days of Stage 2 initiation (target filing: ~2026-06-22):**

1. **"Engineered retroviral envelope glycoproteins with enhanced quiescent hematopoietic stem cell transduction"** — composition-of-matter on a defined *variant class* (Markush-style claims on substitution positions in SU RBD and TM fusion peptide), methods of producing lentiviral particles therewith, methods of transducing CD34+CD38−CD90+ cells in G0. We file on **position classes** even before the directed-evolution campaign returns winners, to anchor the priority date.

2. **"AI-designed viral envelope variants for cell therapy vector manufacturing"** — a platform claim on the *method* of generating envelope variants via ML-guided directed evolution against a quiescent-HSC transduction fitness function. This is the **EVOLVEpro-platform claim** and it matters across every future envelope we touch (cocal, RD114, MLV-A, hybrid scaffolds).

3. **"Producer-detoxified retroviral envelopes"** — composition claims on envelope variants carrying substitutions that reduce syncytia formation in mammalian producer cells (HEK293T, HEK293F, Expi293) while preserving transduction competency. This reads across envelope families, not just BaEV.

**Priority 2 — Convert to PCT within 12 months, national phase at 30 months:**

4. Specific lead variant composition-of-matter claims (the top 3–5 winners from the campaign).
5. Method-of-use claims for ex vivo HSC gene therapy, in vivo HSC targeting via CD117/CD90-retargeted variants, and reagent-kit embodiments.

**Priority 3 — Continuation strategy:**

6. Keep continuations alive on the parent composition claims to file narrower variant claims as the campaign yields better hits through 2028–2030. Standard Broad-style continuation pyramid.
7. File defensive publications on positions/variants we do *not* intend to commercialize, to prevent competitor composition-of-matter on those positions.

### Earliest defensible priority date

**Target: 2026-06-22 (provisional).** This is achievable if Stage 2 initiates on or before 2026-05-22 and we move a provisional disclosure in parallel with initial assay validation. The provisional does not require enabled examples for every variant — we anchor priority with disclosure of the fitness function, the mutagenesis libraries, and at least 2–3 characterized exemplar variants even if modest. We then supplement in the PCT with the full campaign output.

**Realistic priority window: 2026-06 through 2026-12.** Any slippage past 2026-12 risks Sana or an academic group publishing on BaEV deep mutational scanning and torching our novelty.

### Platform value

Owning the envelope variant space + the ML-envelope-design method gives us:
- **B2B reagent revenue** — sell vector to Vertex, 2seventy, Orchard-Kyowa, Editas, Beam, any HSC-GT program. No indication risk, no royalty stack exposure, high multiple on vector manufacturing margins.
- **Sublicensing leverage** against Généthon — if our variants improve on Rless by 10× while operating outside their claims, Généthon's licensees start coming to us.
- **Optionality on in vivo HSC-LV** — the emerging $5–15B category is envelope-gated; we own the gate.
- **Platform extensibility** — the same ML-envelope-design method applies to AAV capsid engineering, VSV-G, cocal, paramyxo fusogens, and synthetic fusogen design. One method claim, many future products.

---

## Recommendation

**`CAUTION (License Needed)` today. **`CLEAR` by Stage 3, conditional on the following gating actions:**

1. **Engage outside counsel for a written FTO opinion on the Généthon WO2013/029008 family** within 30 days. Budget: $40K–$80K. Non-negotiable before GMP spend.
2. **File Priority 1 provisional applications on or before 2026-06-22.** Budget: $25K–$50K across three provisionals. Non-negotiable to lock priority.
3. **Bake "distance from WT Rless tail" and "SU/TM substitution count ≥ N" into the Stage 2 fitness function.** Legal-design constraint, not optional. A beautifully evolved variant that reads onto the Généthon claim is worthless to us.
4. **Do not engage Lentigen for GMP vector manufacturing until Stage 5.** Any pre-commercial GMP contact invites a licensing ask and weakens our negotiating posture.
5. **Pre-emptively cultivate an RD114-TR fallback** in parallel low-priority track (priority claims expiring 2025–2027, so prior-art position only improves).

**Proceed to Stage 2 with these guardrails.** The envelope is the right target. The IP is manageable. The moat-building opportunity is real and time-sensitive.
