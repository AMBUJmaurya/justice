from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class OfflineAnswer:
    answer: str
    confidence: float = 0.6


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip().lower()


def answer_offline(question: str) -> OfflineAnswer:
    """
    Offline helper for court/case related general questions.
    Returns general information only (not legal advice).
    """
    q = _norm(question)

    disclaimer = (
        "Note: Ye general information hai, legal advice nahi. "
        "Case-specific guidance ke liye advocate se documents ke saath consult karein.\n\n"
    )

    # Simple keyword routing
    if any(k in q for k in ["bail", "जमानत", "anticipatory", "438", "439"]):
        return OfflineAnswer(
            disclaimer
            + "Bail ke liye commonly ye cheezein lagti hain (case par depend karta hai):\n"
            + "- FIR/Case details (FIR number, police station)\n"
            + "- Arrest memo / custody details (agar arrested)\n"
            + "- ID proof + address proof\n"
            + "- Medical papers (agar relevant)\n"
            + "- Surety details (surety ka ID/address proof, income proof as needed)\n"
            + "- Previous case history (agar koi ho)\n\n"
            + "Next step: Advocate aapke sections + stage (investigation/charge-sheet) dekh kar proper application draft karega.",
            0.8,
        )

    if any(k in q for k in ["fir", "एफआईआर", "complaint", "शिकायत", "nc r", "ncr"]):
        return OfflineAnswer(
            disclaimer
            + "FIR/Complaint ke liye general steps:\n"
            + "- Nearest police station / online portal (state specific) par complaint\n"
            + "- Facts: date/time/place, accused details (agar pata ho), witnesses\n"
            + "- Evidence: screenshots, call logs, documents, medical report, etc.\n\n"
            + "Agar FIR register nahi ho rahi: written complaint + receiving, then senior officer / magistrate route (facts par depend).",
            0.75,
        )

    if any(k in q for k in ["date", "hearing", "next date", "पेशी", "तारीख", "cause list", "causelist"]):
        return OfflineAnswer(
            disclaimer
            + "Next hearing/date check karne ke options:\n"
            + "- Court website/e-courts portal par case number se status\n"
            + "- Court cause list (daily list)\n"
            + "- Aapke advocate clerk/diary se confirm\n\n"
            + "Tip: Case number + court name + year ready rakhein.",
            0.7,
        )

    if any(k in q for k in ["vakalatnama", "वकालतनामा"]):
        return OfflineAnswer(
            disclaimer
            + "Vakalatnama (advocate authorization) me usually:\n"
            + "- Party details + case details\n"
            + "- Client signature/thumb impression\n"
            + "- Advocate details + enrollment\n"
            + "- Stamp/fees (court rules ke hisaab se)\n\n"
            + "Aapko ID/address proof aur passport photo (kabhi-kabhi) lag sakti hai.",
            0.7,
        )

    if any(k in q for k in ["affidavit", "हलफनामा", "notary", "notarize"]):
        return OfflineAnswer(
            disclaimer
            + "Affidavit ke liye general checklist:\n"
            + "- Facts clear, numbered paragraphs\n"
            + "- Supporting documents annexure\n"
            + "- Proper verification clause\n"
            + "- Notary/Oath commissioner attestation (local process)\n\n"
            + "Drafting me ek chhoti mistake bhi issue ban sakti hai—advocate/notary se verify karwa lein.",
            0.7,
        )

    if any(k in q for k in ["fees", "fee", "charges", "cost", "खर्च", "फीस"]):
        return OfflineAnswer(
            disclaimer
            + "Legal fees matter-to-matter vary karti hai (type, urgency, court, hearing count).\n"
            + "Best practice: pehle consultation me scope clear karein:\n"
            + "- Drafting only vs representation\n"
            + "- Filing + appearance count\n"
            + "- Out-of-station travel\n\n"
            + "Aap apna case type batayein (civil/criminal/family/NI-138) to ek rough range estimate ho sakta hai.",
            0.65,
        )

    if any(k in q for k in ["property", "mutation", "registry", "sale deed", "बैनामा", "नामांतरण", "खसरा", "खतौनी"]):
        return OfflineAnswer(
            disclaimer
            + "Property matters me commonly documents:\n"
            + "- Title chain documents (sale deed/gift deed/partition)\n"
            + "- Khatauni/Khasra/registry copy\n"
            + "- Encumbrance/loan details (agar ho)\n"
            + "- Site map/boundary info\n\n"
            + "Dispute ho to: notices, previous case orders, revenue/civil records bhi zaroori hote hain.",
            0.7,
        )

    if any(k in q for k in ["cheque", "138", "ni act", "चेक", "bounce"]):
        return OfflineAnswer(
            disclaimer
            + "Cheque bounce (NI Act 138) ka general flow:\n"
            + "- Cheque return memo\n"
            + "- Legal notice within limitation\n"
            + "- Notice service proof\n"
            + "- Complaint filing + evidence\n\n"
            + "Exact timelines limitation par depend karte hain—documents ke saath advocate se confirm karein.",
            0.75,
        )

    if any(k in q for k in ["divorce", "maintenance", "custody", "498a", "dv act", "domestic violence"]):
        return OfflineAnswer(
            disclaimer
            + "Family matters me usually:\n"
            + "- Marriage proof, address proof\n"
            + "- Child documents (agar custody)\n"
            + "- Income proof (maintenance cases)\n"
            + "- Communication/evidence (as applicable)\n\n"
            + "Aap bata dein: mutual consent hai ya contested, aur city/district—phir process ko step-by-step samjha dunga.",
            0.7,
        )

    # Default helpful response
    return OfflineAnswer(
        disclaimer
        + "Main aapki help kar sakta hoon. Please ye 3 cheezein bata dein:\n"
        + "1) Matter type: civil / criminal / family / property / NI-138 / other\n"
        + "2) Court/Authority: District court / family court / police / etc.\n"
        + "3) Stage: notice / FIR / investigation / filing / hearing / appeal\n\n"
        + "Phir main required documents + next steps ka clear checklist de dunga.",
        0.55,
    )

