# Apex Omega Violation 3 closed, Surg Co B postal block

Date: 2026-05-07
Branch: claude/apex-omega-audit-repair-gG9mM
File modified: M67400-FO-M13020 3D MED BN-22NOV2024.xlsx
Sheet: MISSION STATEMENT
Cells touched: B208, B210, B211 (Surg Co B address block)

================================================================
What changed
================================================================

  Cell    Before                                                          After
  ----    ------------------------------------------------------------    -----------------------
  B208    FOSTER BUILDING TBD                                             UNIT XXXXX
  B210    OKINAWA, JAPAN (MCB Camp Butler / Camp Foster post-relocation)  FPO, AP   96604XXXX
  B211    Country: US                                                     Country: JP

================================================================
Why
================================================================

The prior session populated Surg Co B's postal block with placeholders
that violated Apex Omega rule 1 (facts only, no invented values):
"FOSTER BUILDING TBD" is not a postal field; "OKINAWA, JAPAN ..." is
descriptive text not an FPO line; "Country: US" is plainly wrong for a
unit relocating to Japan.

User-supplied deep research (Claude Sonnet 4.6 Thinking, 2026-05-07)
confirmed:

  - Surg Co A (UIC M28263) carries an Okinawa TFSMS address
    UNIT 38448 / FPO, AP 96604-8448 / Country: JP, verified.
  - Surg Co B (UIC M28262) currently carries a Hawaii address
    in every published postal directory because the unit has not
    physically relocated yet. Its post-consolidation Okinawa UNIT
    number does not exist in any unclassified document because
    MCB Camp Butler G-1 Postal has not assigned it.
  - FPO, AP 96604 is confirmed as the Camp Butler postal series
    used by all 3d MLG subordinate units in Okinawa.

Per Apex Omega rule 4 (mark TBD if not verifiable, never guess to
fill): the UNIT number and ZIP+4 suffix are honestly placeholdered
as `XXXXX`, pending MCB Camp Butler G-1 Postal assignment upon
execution of the consolidation per the CG signed letter dated
2 February 2026.

Per the user-binding A=B rule, Surg Co B mirrors Surg Co A's
FPO base (96604) and country code (JP). Only the UNIT number
and ZIP+4 differ, both pending assignment.

================================================================
Format note
================================================================

The cell format matches the rest of the MISSION STATEMENT sheet
(H&S Co at row 9 reads "FPO, AP   963734500" with three spaces and
no hyphen between the 5-digit FPO and the 4-digit ZIP+4 suffix;
Surg Co A at row 109 reads "FPO, AP   966048448"). The Surg Co B
entry follows the same convention as "FPO, AP   96604XXXX" so the
final value, once G-1 Postal assigns the suffix, will substitute
4 digits in place of XXXX.

================================================================
Apex Omega application
================================================================

Rule 1 (facts only): no invented values. The XXXXX placeholders
are explicit unknowns.

Rule 4 (TBD where unverifiable): the unknowns are marked with
the source/action that would resolve them (G-1 Postal assignment
upon consolidation execution per CG signed letter 2 Feb 2026).

Rule 5 (time-stamp at point of citation): the CG signed letter
date 2 February 2026 is the time-stamped reference; the user's
deep research conducted 2026-05-07.

Rule 8 (no placeholder crap in workbook): no bracketed TBD text
or AI-style hedging inside the cell. The annotation lives here
in this audit report and in the commit message, not in the
workbook.

================================================================
Validator
================================================================

Pre-fix: 8 PASS / 0 FAIL.
Post-fix: 8 PASS / 0 FAIL (no validator regression).

================================================================
Reversal
================================================================

If MCB Camp Butler G-1 Postal assigns Surg Co B a UNIT number,
update B208 to "UNIT NNNNN" and B210 to "FPO, AP   96604NNNN"
substituting the assigned digits. No other changes required.

If Surg Co B is later directed to share Surg Co A's UNIT 38448
(rather than receiving its own designator), the cells become:
  B208 = UNIT 38448
  B210 = FPO, AP   966048448
  B211 = Country: JP

================================================================
Apex Omega Violation 3 status: CLOSED with TBD honest placeholder.
================================================================
