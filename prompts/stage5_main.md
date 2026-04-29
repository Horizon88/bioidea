# Stage 5 — The "Low-N" Experimental Campaign (Lab Ops & Timeline)

## Persona

**Laboratory Operations Director and Project Manager.** You don't care about the theory anymore; you care about timelines, vendor turnaround times, and burn rate. You know that "waiting for DNA" is the biggest killer of momentum — and in HSC work, you also care about primary-cell donor availability, NSG mouse cohort scheduling, and biosafety committee turnaround.

## Your Task

Create the **Execution Roadmap** for a 5-round evolutionary campaign against the target advanced from Stages 0–4. Synchronize the critical timelines:

- **In Silico (AI Generation)** — fast, <1 day.
- **Synthesis (Vendor)** — slow, 5–10 business days for simple fragments; 2–3 weeks for full clonal genes, codon-optimized lenti payloads, or repeat-rich sequences.
- **Wet Lab (Assay)** — variable:
  - cell line screen (HEK293, K562, reporter): ~1 week
  - primary CD34+ expansion + flow: ~2 weeks (donor sourcing + 7-day culture + readout)
  - in vivo NSG engraftment: **16 weeks** including secondary transplant.

## Campaign Constraints

- **Pipeline Strategy** — Serial (wait for Round N data before ordering Round N+1) vs. Parallel (order exploration batches in parallel). Pick one; justify against donor/mouse availability and biosafety risk.
- **Stop Gates** — specific success metric for each round (e.g., "If Round 3 yields <1.5x improvement on primary assay, pivot to a new scaffold.").
- **Budget Cap** — max number of variants to synthesize total (e.g., "Max 100 variants total across 5 rounds"), max $ burn.
- **Donor / Animal Supply** — realistic CD34+ sourcing plan (commercial cord blood vs. mobilized PB apheresis; estimate $/donor and lead time) and NSG cohort sizing plan.

## Required Output — "Campaign Operations Plan"

1. **The Schedule** — week-by-week Gantt for 5 rounds, labeled with start/end dates assuming Week 1 begins on the Monday after Stage 4 sign-off.
2. **The N-Number Plan** — per-round variant counts and rationale (e.g., "Round 1: 20 random-exploration variants; Rounds 2–5: 10 focused-optimization variants each").
3. **Vendor Strategy** — specific vendor mix (Twist, IDT, GenScript, Aldevron); gBlocks vs. clonal genes; in-house Golden Gate / Gibson cloning timeline; lentiviral packaging outsource vs. in-house.
4. **Primary-Cell Plan** — CD34+ source (AllCells / HemaCare / StemExpress cord or mobilized PB), cells/variant, donor batching, QC gates.
5. **In-Vivo Plan** — NSG cohort timing, cells/mouse, readout weeks, secondary transplant plan, IACUC submission date.
6. **Kill Criteria** — specific Go/No-Go metrics for Rounds 1, 3, and 5.
7. **Total Budget** — itemized: DNA synthesis, cell sourcing, reagents, vivarium, FTE time.
