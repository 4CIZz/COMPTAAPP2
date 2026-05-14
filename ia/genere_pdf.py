"""
Générateur de PDF — Format officiel DCG
Gère les écritures journal, tableaux, sujet et corrigé.
"""

import re
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, KeepTogether,
)

# ─────────────────────────────────────────────
#  COULEURS
# ─────────────────────────────────────────────
DCG_BLEU    = colors.HexColor("#1a3a6b")
DCG_BLEU2   = colors.HexColor("#2d5a9e")
DCG_GRIS    = colors.HexColor("#f0f3f8")
DCG_BORDURE = colors.HexColor("#c8d4e8")
NOIR        = colors.HexColor("#1a1a1a")
GRIS_TEXTE  = colors.HexColor("#444444")
CORRIGE_BG  = colors.HexColor("#1a4a1a")
CORRIGE_COL = colors.HexColor("#0d4a0d")
VERT        = colors.HexColor("#1a5c1a")


# ─────────────────────────────────────────────
#  STYLES
# ─────────────────────────────────────────────
def creer_styles() -> dict:
    return {
        "entete_titre": ParagraphStyle("entete_titre", fontName="Helvetica-Bold", fontSize=10, textColor=colors.white, alignment=TA_CENTER, spaceAfter=2),
        "entete_sous":  ParagraphStyle("entete_sous",  fontName="Helvetica",      fontSize=8,  textColor=colors.white, alignment=TA_CENTER),
        "ue_titre":     ParagraphStyle("ue_titre",     fontName="Helvetica-Bold", fontSize=13, textColor=DCG_BLEU,    alignment=TA_CENTER, spaceAfter=5),
        "info_epreuve": ParagraphStyle("info_epreuve", fontName="Helvetica",      fontSize=9,  textColor=GRIS_TEXTE,  alignment=TA_CENTER, spaceAfter=3),
        "materiel":     ParagraphStyle("materiel",     fontName="Helvetica-Oblique", fontSize=8, textColor=GRIS_TEXTE, alignment=TA_CENTER, spaceAfter=2),
        "avertissement":ParagraphStyle("avertissement",fontName="Helvetica-Bold", fontSize=8,  textColor=DCG_BLEU,    alignment=TA_CENTER, spaceBefore=4, spaceAfter=4),
        "dossier_titre":ParagraphStyle("dossier_titre",fontName="Helvetica-Bold", fontSize=10, textColor=colors.white, alignment=TA_LEFT, leftIndent=6),
        "corrige_label":ParagraphStyle("corrige_label",fontName="Helvetica-Bold", fontSize=9,  textColor=colors.white, alignment=TA_LEFT, leftIndent=6),
        "question":     ParagraphStyle("question",     fontName="Helvetica-Bold", fontSize=9,  textColor=NOIR,        leftIndent=10, spaceBefore=6, spaceAfter=2),
        "corps":        ParagraphStyle("corps",        fontName="Helvetica",      fontSize=9,  textColor=NOIR,        alignment=TA_JUSTIFY, leading=14, spaceBefore=2, spaceAfter=2),
        "corps_indent": ParagraphStyle("corps_indent", fontName="Helvetica",      fontSize=9,  textColor=NOIR,        leftIndent=18, leading=13, spaceBefore=1, spaceAfter=2),
        "journal_titre":ParagraphStyle("journal_titre",fontName="Helvetica-Bold", fontSize=8.5,textColor=DCG_BLEU,    spaceBefore=8, spaceAfter=3),
        "calcul":       ParagraphStyle("calcul",       fontName="Courier",        fontSize=8,  textColor=colors.HexColor("#1a3a6b"), leftIndent=12, leading=12),
        "note_bas":     ParagraphStyle("note_bas",     fontName="Helvetica-Oblique", fontSize=7, textColor=colors.HexColor("#999999"), alignment=TA_CENTER),
        "section_sep":  ParagraphStyle("section_sep",  fontName="Helvetica-Bold", fontSize=12, textColor=colors.white, alignment=TA_CENTER),
    }


# ─────────────────────────────────────────────
#  PARSING
# ─────────────────────────────────────────────
def detecter_ecriture_journal(bloc: str) -> bool:
    """Détecte si un bloc de texte contient une écriture journal."""
    patterns = [
        r"\|\s*\d{3,5}\s*\|",           # | 512 |
        r"\d{3,5}\s+\d{3,5}.*\d+[,.]?\d*",  # 512 411 ... 1000
        r"(?:débit|crédit)\s*:?\s*\d",  # Débit : 1000
        r"\d{3,5}\s+[A-ZÀ-Ü][a-zà-ü].*\d{3,}",  # 512 Banque 10 000
    ]
    return any(re.search(p, bloc, re.IGNORECASE) for p in patterns)


def parser_ecriture_pipe(bloc: str) -> list[list]:
    """Parse un tableau d'écriture au format | col | col | col |"""
    lignes = []
    for ligne in bloc.split("\n"):
        if "|" in ligne:
            cells = [c.strip() for c in ligne.split("|") if c.strip()]
            if cells:
                lignes.append(cells)
    return lignes


def parser_ecriture_libre(bloc: str) -> list[list]:
    """Parse une écriture comptable en texte libre → [date, compte, libellé, débit, crédit]"""
    rows = []
    for ligne in bloc.split("\n"):
        l = ligne.strip()
        if not l:
            continue
        # Ligne type: "512  Banque  10 000,00"  ou  "  401  Fournisseurs    10 000,00"
        m = re.match(
            r"^(\d{2}/\d{2}/\d{4})?\s*(\d{3,6})\s+(.+?)\s+([\d\s]+[,.]?\d*)\s*$",
            l,
        )
        if m:
            date   = m.group(1) or ""
            compte = m.group(2)
            libelle= m.group(3).strip()
            montant= m.group(4).replace(" ", "")
            # Détermine débit/crédit selon l'indentation
            if ligne.startswith("  ") or ligne.startswith("\t"):
                rows.append([date, compte, libelle, "", montant])
            else:
                rows.append([date, compte, libelle, montant, ""])
    return rows


def separer_sujet_corrige(texte: str) -> tuple[str, str]:
    """Sépare le texte en deux parties : sujet et corrigé."""
    patterns = [
        r"(?:PARTIE\s+2|══+\s*PARTIE\s+2|CORRIG[EÉ]\s+D[EÉ]TAILL[EÉ]|ÉLÉMENTS\s+DE\s+CORRIG[EÉ]|CORRIG[EÉ]\s*\n)",
    ]
    for p in patterns:
        m = re.search(p, texte, re.IGNORECASE)
        if m:
            return texte[:m.start()].strip(), texte[m.start():].strip()
    return texte.strip(), ""


def parser_dossiers(texte: str) -> list[dict]:
    """Extrait les dossiers et leur contenu."""
    pattern = re.compile(
        r"(DOSSIER\s+\d+[^\n]*)",
        re.IGNORECASE,
    )
    positions = [(m.start(), m.group(0)) for m in pattern.finditer(texte)]

    dossiers = []
    for i, (pos, titre) in enumerate(positions):
        fin = positions[i + 1][0] if i + 1 < len(positions) else len(texte)
        contenu = texte[pos + len(titre):fin].strip()
        dossiers.append({"titre": titre.strip(), "contenu": contenu})

    if not dossiers:
        dossiers = [{"titre": "TRAVAUX COMPTABLES", "contenu": texte.strip()}]

    return dossiers


# ─────────────────────────────────────────────
#  RENDU DES ÉCRITURES JOURNAL
# ─────────────────────────────────────────────
def construire_tableau_journal(rows: list[list], styles: dict) -> Table:
    """Construit un tableau ReportLab pour les écritures journal."""
    if not rows:
        return None

    # Normalise toutes les lignes à 5 colonnes : Date | Compte | Libellé | Débit | Crédit
    normalized = []
    for row in rows:
        while len(row) < 5:
            row.append("")
        normalized.append(row[:5])

    header = [
        Paragraph("<b>Date</b>",    ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=7.5, textColor=colors.white, alignment=TA_CENTER)),
        Paragraph("<b>Compte</b>",  ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=7.5, textColor=colors.white, alignment=TA_CENTER)),
        Paragraph("<b>Libellé</b>", ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=7.5, textColor=colors.white, alignment=TA_CENTER)),
        Paragraph("<b>Débit</b>",   ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=7.5, textColor=colors.white, alignment=TA_RIGHT)),
        Paragraph("<b>Crédit</b>",  ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=7.5, textColor=colors.white, alignment=TA_RIGHT)),
    ]

    cell_style_left  = ParagraphStyle("td_l", fontName="Helvetica", fontSize=8, textColor=NOIR)
    cell_style_right = ParagraphStyle("td_r", fontName="Courier",   fontSize=8, textColor=NOIR, alignment=TA_RIGHT)
    cell_style_num   = ParagraphStyle("td_n", fontName="Courier-Bold", fontSize=8, textColor=DCG_BLEU)

    data = [header]
    for row in normalized:
        data.append([
            Paragraph(str(row[0]), cell_style_left),
            Paragraph(str(row[1]), cell_style_num),
            Paragraph(str(row[2]), cell_style_left),
            Paragraph(str(row[3]), cell_style_right),
            Paragraph(str(row[4]), cell_style_right),
        ])

    col_widths = [2.2*cm, 1.8*cm, 8.5*cm, 2.5*cm, 2.5*cm]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  DCG_BLEU),
        ("BACKGROUND",   (0,1), (-1,-1), colors.white),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, colors.HexColor("#f5f8ff")]),
        ("GRID",         (0,0), (-1,-1), 0.4, DCG_BORDURE),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("LINEBELOW",    (0,0), (-1,0),  1, DCG_BLEU2),
    ]))
    return table


# ─────────────────────────────────────────────
#  RENDU D'UN BLOC DE CONTENU
# ─────────────────────────────────────────────
def rendre_contenu(contenu: str, styles: dict, is_corrige: bool = False) -> list:
    """Transforme un bloc de texte en éléments ReportLab."""
    elements = []
    lignes = contenu.split("\n")
    i = 0

    while i < len(lignes):
        l = lignes[i].strip()

        if not l:
            elements.append(Spacer(1, 0.12*cm))
            i += 1
            continue

        # ── Détection bloc d'écriture journal (lignes avec |) ──
        if "|" in l and re.search(r"\d{3}", l):
            bloc_pipe = []
            while i < len(lignes) and ("|" in lignes[i] or lignes[i].strip() == ""):
                if lignes[i].strip():
                    bloc_pipe.append(lignes[i])
                i += 1
            rows = parser_ecriture_pipe("\n".join(bloc_pipe))
            if rows:
                elements.append(Spacer(1, 0.15*cm))
                t = construire_tableau_journal(rows, styles)
                if t:
                    elements.append(t)
                elements.append(Spacer(1, 0.15*cm))
            continue

        # ── Titre de question (1. ou 1) ──
        if re.match(r"^\d+[\.\)]\s+.{5,}", l):
            elements.append(Paragraph(l, styles["question"]))
            i += 1
            continue

        # ── Ligne de calcul (commence par =, contient =, formule) ──
        if re.match(r"^[=\-\+×÷\*]|.*=\s*\d", l) and is_corrige:
            elements.append(Paragraph(l, styles["calcul"]))
            i += 1
            continue

        # ── Lignes indentées (sous-éléments) ──
        if lignes[i].startswith("   ") or lignes[i].startswith("\t"):
            elements.append(Paragraph(l, styles["corps_indent"]))
            i += 1
            continue

        # ── Texte normal ──
        elements.append(Paragraph(l, styles["corps"]))
        i += 1

    return elements


# ─────────────────────────────────────────────
#  CONSTRUCTION DES SECTIONS
# ─────────────────────────────────────────────
def construire_entete(styles: dict, session: str) -> list:
    elements = []

    data = [[
        Paragraph("MINISTÈRE DE L'ÉDUCATION NATIONALE", styles["entete_sous"]),
        Paragraph("DIPLÔME DE COMPTABILITÉ ET DE GESTION", styles["entete_titre"]),
        Paragraph(f"SESSION {session}", styles["entete_sous"]),
    ]]
    t = Table(data, colWidths=[5*cm, 9*cm, 4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), DCG_BLEU),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0), (-1,-1), 10),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.35*cm))
    elements.append(Paragraph("UE 9 — INTRODUCTION À LA COMPTABILITÉ", styles["ue_titre"]))

    info = [[
        Paragraph("Durée : 4 heures", styles["info_epreuve"]),
        Paragraph("Coefficient : 1", styles["info_epreuve"]),
        Paragraph("Calculatrice autorisée", styles["info_epreuve"]),
    ]]
    ti = Table(info, colWidths=[6*cm, 4.5*cm, 7.5*cm])
    ti.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), DCG_GRIS),
        ("BOX",          (0,0), (-1,-1), 0.5, DCG_BORDURE),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ]))
    elements.append(ti)
    elements.append(Spacer(1, 0.15*cm))
    elements.append(Paragraph(
        "Matériel autorisé : une calculatrice de poche à fonctionnement autonome sans imprimante "
        "et sans aucun moyen de transmission, à l'exclusion de tout autre élément matériel ou documentaire.",
        styles["materiel"],
    ))
    elements.append(Spacer(1, 0.15*cm))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=DCG_BLEU))
    elements.append(Spacer(1, 0.1*cm))
    elements.append(Paragraph(
        "AVERTISSEMENT : Si le sujet vous semble ne pas correspondre à votre épreuve, "
        "vous devez immédiatement avertir le surveillant qui préviendra le chef de centre.",
        styles["avertissement"],
    ))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=DCG_BLEU))
    elements.append(Spacer(1, 0.3*cm))
    return elements


def construire_bandeau_dossier(titre: str, points: int, styles: dict, is_corrige: bool = False) -> list:
    bg = VERT if is_corrige else DCG_BLEU
    label = f"{titre.upper()}"
    if points:
        label += f"  ({points} points)"
    if is_corrige:
        label = "✦ CORRIGÉ — " + label

    data = [[Paragraph(label, styles["dossier_titre"])]]
    t = Table(data, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), bg),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return [KeepTogether([t]), Spacer(1, 0.2*cm)]


def construire_separateur_corrige(styles: dict) -> list:
    data = [[Paragraph("CORRIGÉ DÉTAILLÉ", styles["section_sep"])]]
    t = Table(data, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), VERT),
        ("TOPPADDING",   (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0), (-1,-1), 10),
    ]))
    return [
        PageBreak(),
        t,
        Spacer(1, 0.4*cm),
    ]


def construire_pied(styles: dict, session: str) -> list:
    return [
        Spacer(1, 0.3*cm),
        HRFlowable(width="100%", thickness=0.5, color=DCG_BORDURE),
        Spacer(1, 0.1*cm),
        Paragraph(
            f"DCG UE9 — Session {session} — Annale générée par IA — Document non officiel",
            styles["note_bas"],
        ),
    ]


# ─────────────────────────────────────────────
#  FONCTION PRINCIPALE
# ─────────────────────────────────────────────
def generer_pdf(texte: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=2*cm,
    )

    styles  = creer_styles()
    annee   = re.search(r"20\d{2}", texte)
    session = annee.group(0) if annee else datetime.now().strftime("%Y")

    # Parse uniquement le sujet (pas de corrigé)
    dossiers = parser_dossiers(texte)

    # Répartition des points
    nb = len(dossiers) or 1
    pts_base = 100 // nb
    pts_list = [pts_base] * nb
    pts_list[-1] += 100 - sum(pts_list)

    elements = []

    # ── EN-TÊTE ──
    elements += construire_entete(styles, session)

    # ── DOSSIERS ──
    for dossier, pts in zip(dossiers, pts_list):
        elements += construire_bandeau_dossier(dossier["titre"], pts, styles)
        elements += rendre_contenu(dossier["contenu"], styles, is_corrige=False)
        elements.append(Spacer(1, 0.3*cm))

    # ── PIED ──
    elements += construire_pied(styles, session)

    doc.build(elements)
    return output_path


# ─────────────────────────────────────────────
#  USAGE DIRECT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage : python genere_pdf.py fichier.txt")
        sys.exit(1)
    texte = Path(sys.argv[1]).read_text(encoding="utf-8")
    nom = f"annale_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    out = Path("annales_generees") / nom
    generer_pdf(texte, out)
    print(f"PDF généré : {out}")
