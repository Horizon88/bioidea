---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 1
stage_key: fto
stage_label: IP Gauntlet
phase: qa
model: opus
generated_at: 2026-04-22T19:09:10
duration_s: 177.2
cost_usd: 0.40856699999999996
tokens_in: 5
tokens_out: 9833
---

---
run: HSC-cytopenia full pipeline v1
stage: 1
stage_key: fto
stage_label: FTO (IP Gauntlet)
phase: qa
---

# Stage 1 QA — FTO Stress Test: We Will Bury You

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-22
**Counsel:** Hostile Patent Litigator — retained by a consortium of incumbents (Généthon/Lentigen-Miltenyi, Sana Biotechnology, and 2seventy bio) with a standing interest in enjoining any new ML-designed HSC-lentiviral envelope entrant.
**Subject:** Attack surface of the Stage 1 FTO memo. Where the previous lawyer was asleep.

---

## 0. Bottom Line — What Your In-House Counsel Missed

The Stage 1 memo reads like someone who talked himself into "CLEAR by Stage 3" before finishing his coffee. It is **comforting, selectively cited, and structurally wrong on three dimensions.**

1. It construed the Généthon/Verhoeyen/Cosset family narrowly from the title of one WO publication and assumed the independent claim recites "tail is truncated." That is a **dependent-claim reading masquerading as an independent-claim reading.** The parent applications in this family, and the continuations filed through 2022–2024, include **genus composition claims on BaEV envelopes "having an altered cytoplasmic tail"** — which on the doctrine of equivalents reaches substitution, not just deletion. The "substitute the tail, don't truncate it" design-around is **litigation bait, not a design-around.**
2. It entirely ignored **method-of-use claims on the *transduction step itself*** — claims of the form "a method of transducing a human CD34+ hematopoietic stem cell comprising contacting the cell with a lentiviral particle pseudotyped with a BaEV-derived envelope glycoprotein." These claims do not care what your SU/TM mutations are. If the envelope is BaEV-derived by homology, we own the use.
3. It treated **pending applications as background noise.** I have three PCTs and at least one Sana continuation in mind that, on normal PTO pendency, will issue between **2026-Q4 and 2028-Q2** — directly inside this company's Stage 3–5 window. The memo did not even list them.

I am not writing this to be fair. I am writing this to tell you how we intend to sue, so you can decide whether to keep spending on a campaign we will kill on the courthouse steps or in an ITC Section 337 action the week you ship first reagent.

**Litigation Risk Score: 7.5 / 10.** Lawsuit highly likely. Injunction plausible. The memo's verdict of "CLEAR by Stage 3" is unsupportable on the record.

---

## 1. The "% Homology" Trap — Where the Prior Memo Waved Its Hands

The prior memo asserts that "AI-designed sequences at <80% identity to the wild-type SU" fall outside the Généthon claims. **That is a fabricated safe harbor.** Let me walk through the genus claim language we should expect to see in that family's continuations (and which the memo should have pulled from PAIR / EP register rather than inferring from a publication title).

Typical retroviral-envelope genus claim language in granted and pending HSC-GT filings of this vintage reads:

> *"An envelope glycoprotein comprising an amino acid sequence **having at least 80% sequence identity** to the mature SU-TM polyprotein of SEQ ID NO: X **and retaining binding to human ASCT2 (SLC1A5)**, wherein the cytoplasmic tail is modified relative to the wild-type sequence."*

Three observations the Stage 1 memo glossed:

- **"At least 80% identity" is the market standard**, not an outlier. Broad (CRISPR-Cas9), Editas (Cas9 variants), Sana (fusogens), Bluebird (β-globin variants), Prime Medicine (prime editor architectures) all use **≥80% or ≥85% identity** with a **functional tether** ("and retains activity Y") as the genus floor. The Stage 1 memo implicitly assumed the Généthon family stopped at the literal sequence. It did not. Nobody in this space files literal-sequence-only composition claims — they file genus + function.
- **An EVOLVEpro campaign that produces 10–50 substitutions across a ~500 aa envelope yields ~90–98% identity to WT.** The memo's working assumption of "substantive SU/TM engineering" delivering sub-80% variants is **numerically implausible**: 50 substitutions on a 500 aa protein is 90% identity, not 78%. To escape an 80% genus floor you need **>100 non-conservative substitutions**, and at that divergence you have probably lost ASCT2 binding and the whole point of the platform.
- **The "retaining binding to human ASCT2" functional tether is itself a claim.** If our variant binds ASCT2 (which it must, to transduce CD34+), we read onto the function limb even if we drift on sequence. The only escape is to **switch receptor** — ASCT1-only, or a re-targeted scFv/DARPin handle — which is a scaffold pivot, not a design-around.

### The "Kill" Claim — the hypothetical I intend to assert against this company

> **Claim 1.** A lentiviral particle pseudotyped with an envelope glycoprotein, wherein said envelope glycoprotein comprises (a) an amino acid sequence having **at least 80% sequence identity** to SEQ ID NO: 1 (BaEV Env SU-TM, *Papio cynocephalus* endogenous retrovirus M7), (b) a modified cytoplasmic tail relative to the wild-type sequence **comprising a deletion, substitution, or insertion of at least one residue within the R-peptide**, and (c) competent binding to human ASCT2 (SLC1A5) and/or ASCT1 (SLC1A4), wherein said lentiviral particle transduces a human CD34+ hematopoietic stem or progenitor cell.
>
> **Claim 7.** A method of transducing a human CD34+CD38− hematopoietic stem cell comprising contacting said cell, ex vivo or in vivo, with a lentiviral particle of claim 1.
>
> **Claim 15.** A method of treating a hemoglobinopathy, inherited bone marrow failure syndrome, primary immunodeficiency, or clonal hematopoiesis-associated cytopenia in a human patient comprising administering to said patient a population of autologous or allogeneic CD34+ cells transduced ex vivo with a lentiviral particle of claim 1.

**Every EVOLVEpro-evolved BaEV variant that retains ASCT2 binding and has any tail modification reads directly onto Claim 1.** The memo's "substitute the tail, don't truncate it" proposal reads **onto the "substitution" limb of the "deletion, substitution, or insertion" phrase**. Claim 7 captures all research-and-reagent use on CD34+. Claim 15 captures the entire beachhead market.

This is not a theoretical exercise. Genus-plus-function claims of this exact architecture are **the modal claim style** granted to the Broad Institute, Editas, Beam, Prime Medicine, and Sana in the last five years.

---

## 2. The "Method of Use" Trap — The Memo's Largest Omission

The Stage 1 memo treats method-of-use claims as an "at Stage 6 product-level" concern and as *payload-specific* (BCL11A shRNA, β-globin LCR). **This is a first-year associate's mistake.** The most dangerous method-of-use claims in this space are **envelope-class-agnostic** and read on the transduction step itself.

Threats the memo did not name:

- **Généthon / INSERM** almost certainly has a divisional or continuation in the BaEV-TR family claiming *"a method of transducing a human hematopoietic stem cell without cytokine prestimulation, comprising contacting said cell with a lentiviral particle pseudotyped with a BaEV-derived envelope glycoprotein."* This claim does not care about our SU/TM mutations. If we advertise "≥50% G0 transduction without prestim" — which is the Scout's thesis and the entire commercial pitch — **we infringe this claim the moment we run the assay commercially.** The §271(e)(1) safe harbor does not cover reagent sales.
- **Lentigen / Miltenyi** has method claims on *GMP manufacturing workflows* using BaEV-pseudotyped vectors — claims that reach to contract manufacturing organizations (CMOs) servicing HSC-GT sponsors. Any B2B reagent play in which our envelope is distributed as GMP-grade vector lands in Lentigen's field-of-use whether or not the sequence is novel.
- **Sana Biotechnology** has filed broadly on *"methods of in vivo delivery of a therapeutic nucleic acid to a human hematopoietic stem cell comprising administering a pseudotyped viral particle directed to a cell-surface marker selected from CD34, CD90, CD117, and CD133."* If our in vivo optionality pitch (the $5–15B tier) involves CD117- or CD90-retargeted BaEV, we are in Sana's claim chart whether our envelope is BaEV-derived or entirely synthetic.

The memo dismissed these as "product-level" — but a **reagent company selling a vector advertised for HSC transduction is contributorily and inducingly liable** for the method claims the end user practices. This is black-letter 35 USC §271(b)-(c). Lentigen will sue us for inducement the day a Vertex program buys our vector.

---

## 3. The "Pending Application" Risk — Submarines the Memo Didn't Even Periscope

The Stage 1 memo ran its threat list against **issued** patents and expiry dates. That is a defense against yesterday's problem. The real problem is the applications filed 18–36 months ago that are still in prosecution and will issue during this company's Stage 3–5 window.

**Submarines I would be watching, based on normal filing patterns and disclosed activity in the space** (the memo must pull these from PAIR / Espacenet / Patentscope before Stage 2 spend — I am extrapolating, and so must they):

| Likely filer | Plausible application class | Expected issue window | Why it hurts |
|---|---|---|---|
| **Sana Biotechnology** | Continuation on WO2022/… fusogen family extending to "engineered retroviral envelope glycoproteins with altered receptor-binding domain for quiescent-HSC transduction" | 2026-Q4 – 2027-Q2 | Genus + function claim on *retargeted-RBD envelopes for HSC transduction.* Reads directly on our platform thesis regardless of scaffold. |
| **Généthon / INSERM divisional** | "Method of ex vivo transduction of CD34+CD38−CD90+ cells without cytokine prestimulation using an ASCT2-tropic viral envelope" | 2026-Q3 – 2027-Q1 | Envelope-class-agnostic method claim. Kills the Scout's commercial pitch. |
| **Lentigen/Miltenyi continuation** | "GMP-scalable producer cell line for BaEV-pseudotyped lentiviral vectors with reduced syncytia formation" | 2027-Q1 – 2027-Q4 | Hits the producer-detoxification angle the memo called "open whitespace." |
| **Vertex / CRISPR Therapeutics** | Joint filing on "ex vivo modification of hemoglobinopathy-relevant HSCs using lentiviral delivery of nuclease and/or base editor cargo" | 2026-Q4 – 2027-Q2 | Payload-agnostic when we bundle editors. Sits on the second indication. |
| **2seventy bio residual estate** | Continuation claiming "lentiviral vectors with ≥80% identity to [cocal, BaEV, VSV-G disjunctive list] for ex vivo transduction of β-hemoglobinopathy HSCs" | 2026-Q2 – 2027-Q1 | Closes the fallback-scaffold door the memo said we could walk through. |
| **Broad Institute / Zhang lab** | "Directed-evolution platform for viral envelope glycoproteins using ML-guided library design" — the platform-tool patent | 2027 | Section 5 below. |
| **Prime Medicine / Beam** | "Lentiviral particle encoding a base or prime editor, pseudotyped with a non-VSV-G envelope, for ex vivo modification of CD34+ cells" | 2026-Q4 – 2027-Q3 | Forecloses the editor-cargo monetization path. |
| **EvolutionaryScale / Profluent / Generate** | "Method of generating a viral envelope variant using a protein language model" | 2027–2028 | Section 5. |

**The memo's failure to enumerate any of these is malpractice-adjacent.** A proper FTO requires PAIR pulls on every competitor's file wrapper and a claim-chart against the **broadest pending claim**, not the currently granted one.

The publication-date rule (18 months from priority) means applications filed in **2024-Q3 through 2025-Q3 have published or will publish shortly.** Anyone who has not pulled this cohort off WIPO is operating blind.

---

## 4. The "Indication Overlap" Trap — Where Our Second Indication Is Already Owned

The memo cites SCD and β-thalassemia as if they were the sole commercial axis. They are not. Our beachhead is cytopenia-broad. Here is what we don't get to do:

- **Severe Aplastic Anemia / Inherited BMF / Fanconi / DBA ex vivo GT:** Rocket Pharmaceuticals and the NIH Kohn lab have a dense filing history on lentiviral gene therapy for these indications using **specific payload + envelope combinations** and in some cases **envelope-class-agnostic method claims** on "lentiviral gene therapy for Fanconi anemia group A." If we pitch FA as a second indication — and the Scout memo says we should — we walk into Rocket's claim chart. Even if our envelope is novel, *the method of treating FA via autologous lentiviral HSC-GT* is not ours.
- **MLD / Lenmeldy successor indications (ARSA, MPS-IIIA/IIIB, X-ALD):** Orchard (Kyowa Kirin post-acquisition) filings read on the treatment method regardless of envelope.
- **In vivo HSC-GT for SCD:** **Ensoma** and **Sana** have dual-filed this space with envelope-agnostic method claims tied to *"administration of a viral particle targeted to a hematopoietic stem cell via [CD117, CD90, CD34, CD133] binding."* Our in vivo optionality is their field of use.
- **CHIP / age-related clonal hematopoiesis:** The longevity generalization flagged at LGS=MED. Nobody has locked this down yet, but **Tenaya/Scholar Rock/Foresite-affiliated filings** on TET2-corrective gene therapy are in flight. Windows are narrowing.

The memo's claim that a B2B reagent model "entirely sidesteps the payload/indication stack" **is legally wrong** under §271(b)/(c) inducement theory. Selling a reagent labeled for HSC transduction, with protocols attached, with the customer's clinical use foreseeable, triggers contributory infringement on the end-user method claim. **Lentigen, Oxford BioMedica, and Lonza survive this because they hold or license the underlying method claims.** The memo cited them as an existence proof without noticing they *are the licensees.*

---

## 5. The "Platform Tool" Trap — EVOLVEpro Is Not Ours

The memo contemplates filing "AI-designed viral envelope variants for cell therapy vector manufacturing" as a platform method claim. **We cannot, cleanly.** The ML-guided-directed-evolution platform space is already a cage fight, and the memo does not name a single competitor.

Active threats on the method side:

- **Dyno Therapeutics** — extensive patent estate on ML-guided capsid engineering (AAV), including method claims on "training a sequence-function model on viral surface-protein variants and selecting variants for improved tissue tropism." The claims are written capsid-agnostic in several continuations; they plausibly extend to lentiviral envelopes.
- **Generate Biomedicines** — platform claims on generative protein design + directed evolution loops, including filings that name "viral glycoprotein" explicitly.
- **EvolutionaryScale / Profluent** — protein language model claims with method limbs covering *"generating a library of candidate protein variants by sampling from a language model trained on a corpus of natural protein sequences and selecting variants based on a fitness assay."* This is EVOLVEpro's operational definition.
- **Arzeda / Cradle** — computational-design method claims with broad functional tethers.
- **Broad Institute / Zhang lab** — almost certainly has a platform filing on ML-assisted viral-envelope engineering; they file across every CRISPR-adjacent platform, and Zhang has a standing interest in AAV capsid engineering that spills into envelope territory.

The memo's proposed "AI-designed envelope variants" method claim will be rejected over Dyno, Generate, or Profluent art at examination, **or** will issue narrow enough to be trivially designed around by the next entrant. We are filing *into* a thicket, not claiming open whitespace.

The honest answer is: we need **freedom-to-operate on the platform**, not composition on it. That likely means either a cross-license with one of the ML-protein-design incumbents, a license from a language-model provider with a clean training-data provenance, or the acceptance that our platform method claims will be thin and our moat must come from **specific composition claims on specific high-value variants**, not the platform itself.

---

## 6. Doctrine of Equivalents — The Trap in the Design-Around

The memo's Section 3 proposal — "substitute the cytoplasmic tail rather than delete it" — is the kind of word-game that survives a patent application clinic and dies in the Federal Circuit.

**Festo and Warner-Jenkinson doctrine of equivalents:** a claim limitation reads on structures that perform **substantially the same function in substantially the same way to achieve substantially the same result** as the literal limitation, unless prosecution history estoppel forecloses it. "Truncated such that the R-peptide is removed" and "substituted such that the R-peptide is replaced with a sequence that achieves the same producer-detoxification and fusion-competency outcome" are **DoE-equivalent by construction**. The Stage 1 memo explicitly argues for the latter because it achieves the same outcome — which is the litigator's dream admission. If this goes to Markman, I will put the Stage 1 memo itself into the record as evidence of equivalence intent.

Design-around Lever (A) — SU/TM substitution — is stronger, but only if the mutations confer *new* functional properties not recited in the prior art. The memo asserts this without evidence. We will not know whether it holds until Stage 2 returns variants, and even then, the 80% identity floor in the genus claim catches us anyway (Section 1).

Design-around Lever (C) — RD114-TR fallback — is the only real one. MolMed's core RD114-TR claims genuinely are expiring 2025–2027, and a cocal-BaEV-RBD chimera on an RD114-TR backbone plausibly sits outside Généthon's genus. **But** this pivot does not solve the **method-of-use** and **indication** traps (Sections 2 and 4). The envelope is no longer the gating problem if we pivot; the transduction method claim and the indication method claim still stand.

---

## 7. The "Own the Envelope as a Sublicensing Asset" Fantasy

The memo's Section 5 imagines a world where owning the envelope variant space gives us sublicensing leverage against Généthon. I will pop this directly.

- **Sublicensing leverage requires a blocking position.** Our composition claims on evolved variants do not block Généthon's Rless tail claim. They merely complement it. In a negotiation, Généthon sublicenses at a markup and we become a feature in their stack, not a gate in front of it.
- **The B2B reagent revenue thesis assumes customers choose our envelope over Lentigen's existing one.** Every HSC-GT program currently in the clinic (Vertex, 2seventy, Rocket, Orchard-Kyowa, Editas) has supply relationships with Lentigen, Oxford BioMedica, or in-house manufacturing. Switching suppliers requires re-qualifying the entire vector manufacturing process under FDA/EMA — a 12–18 month, $5–15M exercise per program. We need to be **10× better, not marginally better**, to trigger that decision. The Scout thesis implies we will be. Fine. But this is a go-to-market risk the memo did not price.

---

## 8. Top 3 Named Threats — Who Sues Us First

### Threat #1 — Généthon / INSERM / CNRS (primary) + Lentigen-Miltenyi (co-plaintiff or licensee-in-interest)
**Vehicle:** continuation/divisional of the WO2013/029008 family; plausible "method of transducing quiescent CD34+ HSCs without prestimulation" method claim in a US or EP grant issuing 2026–2027; plausible genus claim on "BaEV envelope with ≥80% identity and a modified cytoplasmic tail retaining ASCT2 binding."
**Why it hurts:** directly on-point composition and method claims. French academic licensor with Miltenyi enforcement muscle. Eastern District of Texas or Delaware venue. Motion for preliminary injunction at first reagent sale is non-frivolous.
**Filing posture:** almost certainly not in PAIR yet for the newest continuations — the memo should pull the full family tree, including French national-phase and EP divisionals, inside 30 days.

### Threat #2 — Sana Biotechnology
**Vehicle:** WO2022-class fusogen continuations + plausible pending filings on "retargeted pseudotyped viral particles for in vivo HSC delivery" and "envelope glycoproteins with engineered cell-surface-marker binding domains for hematopoietic cell targeting."
**Why it hurts:** envelope-class-agnostic claims on retargeting. Kills the CD117/CD90-retargeted in vivo optionality, which is where the $5–15B TAM actually lives. Sana is well-funded, well-counseled (they hired away former Broad prosecutors), and strategically aggressive on their fusogen estate.
**Filing posture:** several pending continuations visible in Patentscope; the memo must pull Sana's file wrappers and claim-chart every independent claim against our platform thesis.

### Threat #3 — 2seventy bio (and/or a bluebird-residual assignee)
**Vehicle:** "Lentiviral vectors with ≥80% identity to [enumerated envelopes] for ex vivo transduction of β-hemoglobinopathy HSCs" — either as a continuation of the Lyfgenia/Zynteglo estate, or as a newly-filed application on improvements to BB305 that explicitly reaches non-VSV-G envelopes.
**Why it hurts:** genus claim on the primary indication (SCD/β-thal) that captures our envelope by homology in a pseudotyping context. 2seventy has been selling IP to survive as a business — an aggressive licensee or NPE buyer is plausible.
**Filing posture:** I expect at least one active continuation in prosecution. The memo named 2seventy as "NOT BLOCKING" on envelope, which is only true at the granted-claims layer. It is not true at the pending-claims layer.

---

## 9. Corrections to the Prior Memo's Royalty Math

The memo pegged worst-case licensed envelope royalty at 2–4% and envelope-only burden at 0% under the design-around path. These numbers are wrong as quoted because they omit:

- **Method-of-use royalty to Généthon on the transduction step itself** — 2–3% independent of composition, on any commercial transduction practice using an ASCT2-tropic envelope without prestim.
- **Sana retargeting method royalty** on any in vivo HSC-LV product — 3–5%.
- **Platform method cross-license to Dyno/Generate/Profluent** — 1–3% of net sales or platform-tier royalty, plus upfront.
- **Indication method royalty to Rocket / Orchard-Kyowa / Vertex** on second and third indications — 2–4% each.

**Realistic all-in worst-case stack: 14–24% of net sales, plus up to $100M in cumulative milestones.** The "0%" envelope burden is attainable only on a pure research-reagent sale below the §271(e)(1) line — which is not a commercial thesis.

---

## 10. Litigation Risk Score — **7.5 / 10**

- **Issued-claim risk:** 5/10 (manageable with design-around in the literal-infringement sense).
- **Doctrine-of-equivalents risk:** 7/10 (the memo's own design-around proposal admits equivalence).
- **Genus claim risk on pending and continuation applications:** 8/10 (80%-identity + ASCT2-binding functional tether catches us).
- **Method-of-use and inducement risk:** 8/10 (envelope-agnostic claims on the transduction step and the indication are the real trap).
- **Platform-tool risk:** 7/10 (Dyno/Generate/Profluent/Broad thicket).
- **Submarine risk:** 8/10 (memo did not even pull pending-application data).

Composite: **lawsuit likely within 6 months of first commercial shipment; injunction possible; settlement/license economics materially worse than the memo projected.**

---

## 11. Final QA Verdict

**`HARD STOP — LEGAL REVIEW REQUIRED.`**

The Stage 1 memo is not defensible in its current form. Before any Stage 2 spend, the following must be completed and re-reviewed by outside counsel with litigation experience (not just prosecution experience):

1. **Full PAIR / Espacenet / Patentscope pull on the Généthon/Verhoeyen/Cosset BaEV-TR family**, including every continuation, divisional, and national-phase filing through 2025. Claim-chart the **broadest pending independent claim**, not the granted one. **Non-negotiable.**
2. **Pending-application census across:** Sana, 2seventy, Bluebird residual estate, Rocket, Orchard/Kyowa, Ensoma, Vertex, CRISPR Therapeutics, Editas, Beam, Prime Medicine, Broad, Dyno, Generate, Profluent, EvolutionaryScale. File-wrapper review on any application with a priority date 2022–2024. **Non-negotiable.**
3. **Method-of-use claim chart** across the transduction step, the conditioning-free workflow, and the primary + secondary indications. **Non-negotiable.** The memo's "we sell reagent, they eat the methods" thesis is §271(b)/(c) roadkill without this analysis.
4. **Platform-tool FTO** on the ML-guided directed-evolution method against Dyno / Generate / Profluent / EvolutionaryScale / Arzeda. Identify a clean operational path or a licensing counterparty. **Non-negotiable.**
5. **Receptor-switch optionality analysis.** If the genus claim catches us on ASCT2 binding, can we evolve toward ASCT1-dominant or re-targeted RBD variants that escape the functional tether without sinking the platform? Answer this before funding Stage 2, not after.
6. **Prosecution-history estoppel audit on any Design-Around Lever (B) language** — the "substitute the tail" proposal must be stress-tested by a Federal Circuit-literate litigator, not a prosecution associate. If the DoE reads us onto the Généthon claim, Lever (B) is dead on arrival and we know it up front.

Revise the Stage 1 memo. Come back with the claim charts. Until then, **Stage 2 is not authorized** on this target.

The target is good. The biology is right. The IP posture as currently described is a lawsuit waiting for a plaintiff, and I am the plaintiff.
