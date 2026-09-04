import os
import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)

COLOR_BURGUNDY = colors.HexColor('#7a3e4c')
COLOR_BURGUNDY_DARK = colors.HexColor('#5a2e38')
COLOR_GOLD = colors.HexColor('#b89050')
COLOR_GOLD_LIGHT = colors.HexColor('#dfc99f')
COLOR_BG_WARM = colors.HexColor('#fcfbf9')
COLOR_ROW_ALT = colors.HexColor('#fbf6f4')
COLOR_TEXT_MAIN = colors.HexColor('#2c2522')
COLOR_TEXT_MUTED = colors.HexColor('#6b5c57')
COLOR_BORDER = colors.HexColor('#e8d5d1')

SONGS_DATA = [
    {
        "id": 1,
        "title": "1. Entrée",
        "key": "Libre / Improvisation",
        "instruments": "Harmonium (Accompagnement)",
        "file": None,
        "target_page": 2
    },
    {
        "id": 2,
        "title": "2. Debout resplendis",
        "key": "Mi mineur (1#)",
        "instruments": "Chœur, Flûte, Saxo, Vcelle, Cajón",
        "file": "02 - Debout resplendis.pdf",
        "target_page": 3
    },
    {
        "id": 3,
        "title": "3. Messe St-Jean : Gloria",
        "key": "Ré mineur (1b)",
        "instruments": "Chœur, Harmonium",
        "file": "03 - Messe_Saint_Jean (Gloria+Agnus).pdf",
        "target_page": 4
    },
    {
        "id": 4,
        "title": "4. Psaume 148 (Louez le Seigneur)",
        "key": "Ré mineur (1b)",
        "instruments": "Chœur (A/B) + Solo (S), Vcelle",
        "file": "04 - louez-le-seigneur-Psaume 148.pdf",
        "target_page": 9
    },
    {
        "id": 5,
        "title": "5. Resucito",
        "key": "Sol mineur (2b) [capo 3]",
        "instruments": "Chœur, Saxo, Cajón, Guitare",
        "file": "05 - Resucito.pdf",
        "target_page": 12
    },
    {
        "id": 6,
        "title": "6. Esprit de lumière",
        "key": "Fa majeur (1b)",
        "instruments": "Chœur, Violon, Flûte, Vcelle",
        "file": "06 - Esprit_de_lumiere_esprit_createur.pdf",
        "target_page": 13
    },
    {
        "id": 7,
        "title": "7. Laudate Dominum (Taizé)",
        "key": "La mineur (0)",
        "instruments": "Chœur, Saxophone",
        "file": "07 - Laudate_Dominum_Taize.pdf",
        "target_page": 15
    },
    {
        "id": 8,
        "title": "8. Accueille au creux de tes mains",
        "key": "Mi mineur (1#)",
        "instruments": "Chœur, Violon, Violoncelle",
        "file": "08 - Accueille aux creux de tes mains - 4 voix mixtes.pdf",
        "target_page": 17
    },
    {
        "id": 9,
        "title": "9. Vivre d’amour",
        "key": "Mib majeur (3b)",
        "instruments": "Chœur & Voix solo, Violoncelle",
        "file": "09 - Vivre_d_amour.pdf",
        "target_page": 18
    },
    {
        "id": 10,
        "title": "10. Sanctus (Messe St-Paul)",
        "key": "La mineur (0) [éolien]",
        "instruments": "Chœur, Violon, Vcelle, Cajón",
        "file": "10 - sanctus_de_saint_paul.pdf",
        "target_page": 19
    },
    {
        "id": 11,
        "title": "11. Messe St-Jean : Agnus",
        "key": "Ré mineur (1b)",
        "instruments": "Chœur, Harmonium",
        "file": "11 - Messe_Saint_Jean (Gloria+Agnus).pdf",
        "target_page": 20,
        "agnus_page": 24
    },
    {
        "id": 12,
        "title": "12. Tu fais ta demeure en nous",
        "key": "Mi mineur (1#)",
        "instruments": "Chœur, Harmonium",
        "file": "12 - tu fais ta demeure en nous.pdf",
        "target_page": 25
    },
    {
        "id": 13,
        "title": "13. Marie, Mère de Dieu",
        "key": "Mi mineur (1#)",
        "instruments": "Chœur, Violon, Violoncelle",
        "file": "13 - Marie_Mere_de_Dieu.pdf",
        "target_page": 26
    },
    {
        "id": 14,
        "title": "14. Pour tes merveilles",
        "key": "Ré mineur (1b)",
        "instruments": "Chœur, Vlon, Vcelle, Sax, Cajón, Guit.",
        "file": "14 - Pour-tes-merveilles.pdf",
        "target_page": 27
    }
]

def build_front_matter():
    temp_pdf = "temp_front_matter.pdf"
    doc = SimpleDocTemplate(
        temp_pdf,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()

    style_super_header = ParagraphStyle(
        'SuperHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_GOLD,
        alignment=1,
        spaceAfter=3
    )

    style_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=COLOR_BURGUNDY,
        alignment=1,
        spaceAfter=4
    )

    style_subtitle = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=COLOR_TEXT_MAIN,
        alignment=1,
        spaceAfter=10
    )

    style_cell_num = ParagraphStyle(
        'CellNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_BURGUNDY,
        alignment=1
    )

    style_cell_title = ParagraphStyle(
        'CellTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_TEXT_MAIN
    )

    style_cell_key = ParagraphStyle(
        'CellKey',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=COLOR_GOLD
    )

    style_cell_inst = ParagraphStyle(
        'CellInst',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=COLOR_TEXT_MUTED
    )

    style_cell_page = ParagraphStyle(
        'CellPage',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_BURGUNDY,
        alignment=1
    )

    style_th = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    elements = []

    # --- PAGE 1: TABLE DES MATIÈRES ---
    elements.append(Paragraph("MESSE DE MARIAGE — COORDINATION MUSICALE", style_super_header))
    elements.append(Paragraph("Programme Musical & Partitions — Mariage de Marguerite & Antoine", style_title))
    elements.append(Paragraph("Samedi 5 Septembre 2026 — Morges", style_subtitle))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_GOLD, spaceBefore=0, spaceAfter=8))

    table_data = [[
        Paragraph("N°", style_th),
        Paragraph("Chant / Pièce", style_th),
        Paragraph("Tonalité", style_th),
        Paragraph("Pupitres & Rôles", style_th),
        Paragraph("Page", style_th)
    ]]

    for song in SONGS_DATA:
        p_str = f"p. {song['target_page']}"
        if song.get('agnus_page'):
            p_str = f"p. {song['target_page']}<br/><font size=6.5 color='#b89050'>(Agnus p. {song['agnus_page']})</font>"
        
        table_data.append([
            Paragraph(f"<b>{song['id']:02d}</b>", style_cell_num),
            Paragraph(song['title'], style_cell_title),
            Paragraph(song['key'], style_cell_key),
            Paragraph(song['instruments'], style_cell_inst),
            Paragraph(p_str, style_cell_page)
        ])

    toc_table = Table(
        table_data,
        colWidths=[26, 148, 104, 185, 60],
        repeatRows=1
    )

    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BURGUNDY),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
    ]

    for i in range(1, len(table_data)):
        bg = colors.white if i % 2 == 1 else COLOR_ROW_ALT
        t_style.append(('BACKGROUND', (0, i), (-1, i), bg))
        t_style.append(('TOPPADDING', (0, i), (-1, i), 3.8))
        t_style.append(('BOTTOMPADDING', (0, i), (-1, i), 3.8))

    toc_table.setStyle(TableStyle(t_style))
    elements.append(toc_table)

    elements.append(Spacer(1, 8))
    style_notice = ParagraphStyle(
        'Notice',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=9.5,
        textColor=COLOR_TEXT_MUTED,
        alignment=1
    )
    elements.append(Paragraph("★ <i>Astuce : Chaque ligne de cette table des matières et chaque signet PDF sont cliquables pour naviguer instantanément.</i>", style_notice))

    elements.append(Spacer(1, 10))

    # Musician Info Box at bottom of TOC
    style_info_h = ParagraphStyle(
        'InfoHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_BURGUNDY
    )
    style_info_body = ParagraphStyle(
        'InfoBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=COLOR_TEXT_MAIN
    )

    info_box = Table([
        [Paragraph("<b>Recommandations & Repères pour l'Équipe Musicale :</b>", style_info_h)],
        [Paragraph("• <b>Accordage & Diapason :</b> Diapason standard La 440 Hz pour l'ensemble des instruments (harmonium/orgue, cordes, flûte, saxo, guitare).<br/>"
                   "• <b>Équilibre acoustique :</b> Veiller au dosage délicat des percussions (cajón) et cuivres/bois pour laisser prédominer les voix et le texte liturgique.<br/>"
                   "• <b>Enchaînement clé :</b> L'entrée à l'harmonium (n° 01) prépare l'accord de départ (Mi mineur / Si7) pour l'entrée du chœur <i>Debout resplendis</i> (n° 02).<br/>"
                   "• <b>Fiches pupitres interactives :</b> Retrouvez le détail exact de vos interventions sur le portail web de coordination.", style_info_body)]
    ], colWidths=[523])

    info_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_WARM),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_GOLD_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_box)

    elements.append(PageBreak())

    # --- PAGE 2: INTRODUCTION CHANT 1 ---
    style_intro_badge = ParagraphStyle(
        'IntroBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=COLOR_GOLD,
        alignment=0,
        spaceAfter=4
    )

    style_intro_title = ParagraphStyle(
        'IntroTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=27,
        textColor=COLOR_BURGUNDY,
        alignment=0,
        spaceAfter=5
    )

    style_intro_sub = ParagraphStyle(
        'IntroSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=COLOR_TEXT_MAIN,
        alignment=0,
        spaceAfter=12
    )

    style_section_h = ParagraphStyle(
        'SectionH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=COLOR_BURGUNDY,
        spaceBefore=10,
        spaceAfter=4
    )

    style_body = ParagraphStyle(
        'IntroBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=COLOR_TEXT_MAIN,
        spaceAfter=6
    )

    style_body_bold = ParagraphStyle(
        'IntroBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=COLOR_BURGUNDY
    )

    elements.append(Paragraph("OUVERTURE LITURGIQUE — PIÈCE N° 01", style_intro_badge))
    elements.append(Paragraph("1. Entrée (Harmonium)", style_intro_title))
    elements.append(Paragraph("Mariage de Marguerite & Antoine — Célébration Liturgique", style_intro_sub))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_GOLD, spaceBefore=0, spaceAfter=12))

    card_data = [
        [Paragraph("<b>Instrument & Titulaire :</b>", style_body_bold), Paragraph("Harmonium / Orgue d'accompagnement", style_body)],
        [Paragraph("<b>Moment liturgique :</b>", style_body_bold), Paragraph("Accueil de l'assemblée, entrée du cortège puis entrée solennelle de la mariée", style_body)],
        [Paragraph("<b>Tonalité recommandée :</b>", style_body_bold), Paragraph("<b>Libre / Improvisation</b> (majeur, solennel, chaleureux et recueilli)", style_body)],
        [Paragraph("<b>Transition harmonique :</b>", style_body_bold), Paragraph("Prévoir une cadence ou modulation douce vers <b>Mi mineur</b> (Mim) pour enchaîner directement sur le chant d'entrée de l'assemblée <i>Debout resplendis</i> (pièce n° 02)", style_body)],
        [Paragraph("<b>Durée indicative :</b>", style_body_bold), Paragraph("Environ 3 à 5 minutes selon le temps de placement et la procession d'entrée", style_body)]
    ]
    card_table = Table(card_data, colWidths=[155, 368])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_WARM),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_GOLD_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(card_table)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Directives & Conseils d'Interprétation", style_section_h))
    elements.append(Paragraph("• <b>Phase 1 — Accueil & Recueillement :</b> Alors que les invités prennent place dans l'église, instaurer une atmosphère lumineuse, paisible et recueillie.", style_body))
    elements.append(Paragraph("• <b>Phase 2 — Entrée du cortège & de Marguerite :</b> À l'ouverture des portes et dès que le cortège s'élance, déployer un jeu plus ample, majestueux et jubilatoire pour accompagner la procession jusqu'à l'autel.", style_body))
    elements.append(Paragraph("• <b>Phase 3 — Résolution vers le chant 2 :</b> Lorsque les mariés sont installés, amener une cadence finale claire ou un accord tenu en <b>Mi mineur</b> (ou <b>Si7</b>) servant d'accord de départ parfait au chœur et aux instruments pour <i>Debout resplendis</i>.", style_body))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Espace Notes & Choix de Répertoire de l'Organiste", style_section_h))

    notes_box = Table([
        [Paragraph("<i>Pièce choisie / Thème :</i> ........................................................................................................................................", style_body)],
        [Paragraph("<i>Enregistrement / Jeux :</i> .............................................................................................................................................", style_body)],
        [Paragraph("<i>Notes de jeu :</i> ..........................................................................................................................................................", style_body)],
        [Paragraph(".....................................................................................................................................................................................", style_body)],
        [Paragraph(".....................................................................................................................................................................................", style_body)],
    ], colWidths=[523])
    notes_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fcfcfc')),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(notes_box)

    doc.build(elements)
    print("Front matter generated successfully.")

def assemble_complete_booklet(output_pdf="Livret_Partitions_Mariage.pdf"):
    build_front_matter()

    final_doc = pymupdf.open()
    front_doc = pymupdf.open("temp_front_matter.pdf")

    # Insert page 1 (TOC) and page 2 (Harmonium)
    final_doc.insert_pdf(front_doc)

    partition_files = [
        "02 - Debout resplendis.pdf",
        "03 - Messe_Saint_Jean (Gloria+Agnus).pdf",
        "04 - louez-le-seigneur-Psaume 148.pdf",
        "05 - Resucito.pdf",
        "06 - Esprit_de_lumiere_esprit_createur.pdf",
        "07 - Laudate_Dominum_Taize.pdf",
        "08 - Accueille aux creux de tes mains - 4 voix mixtes.pdf",
        "09 - Vivre_d_amour.pdf",
        "10 - sanctus_de_saint_paul.pdf",
        "11 - Messe_Saint_Jean (Gloria+Agnus).pdf",
        "12 - tu fais ta demeure en nous.pdf",
        "13 - Marie_Mere_de_Dieu.pdf",
        "14 - Pour-tes-merveilles.pdf"
    ]

    for pf in partition_files:
        src = pymupdf.open(pf)
        final_doc.insert_pdf(src)

    print(f"Total pages assembled: {len(final_doc)}")

    # Add GoTo links on Page 1 (TOC)
    toc_page = final_doc[0]

    for song in SONGS_DATA:
        target_idx = song["target_page"] - 1 # 0-indexed
        
        # Search for the song title on the TOC page
        title_term = song["title"]
        rects = toc_page.search_for(title_term)
        if rects:
            r = rects[0]
            # Link across the full row from x=36 to x=500
            row_rect = pymupdf.Rect(36, r.y0 - 3, 500, r.y1 + 3)
            toc_page.insert_link({
                "kind": pymupdf.LINK_GOTO,
                "page": target_idx,
                "from": row_rect
            })
            # Also link the page number specifically
            page_term = f"p. {song['target_page']}"
            p_rects = toc_page.search_for(page_term)
            for pr in p_rects:
                if abs(pr.y0 - r.y0) < 6:
                    toc_page.insert_link({
                        "kind": pymupdf.LINK_GOTO,
                        "page": target_idx,
                        "from": pymupdf.Rect(pr.x0 - 2, pr.y0 - 2, pr.x1 + 2, pr.y1 + 2)
                    })

        # Special link for Agnus p. 24 on song 11
        if song.get("agnus_page"):
            agnus_rects = toc_page.search_for(f"Agnus p. {song['agnus_page']}")
            if agnus_rects:
                ar = agnus_rects[0]
                toc_page.insert_link({
                    "kind": pymupdf.LINK_GOTO,
                    "page": song["agnus_page"] - 1,
                    "from": pymupdf.Rect(ar.x0 - 2, ar.y0 - 2, ar.x1 + 2, ar.y1 + 2)
                })

    # Add PDF Outlines (Signets / Bookmarks)
    toc_outlines = [
        [1, "Programme & Table des matières", 1],
        [1, "01. Entrée — Harmonium [Libre / Impr.]", 2],
        [1, "02. Debout resplendis [Mi mineur]", 3],
        [1, "03. Messe St-Jean : Gloria [Ré mineur]", 4],
        [1, "04. Psaume 148 (Louez le Seigneur) [Ré mineur]", 9],
        [1, "05. Resucito [Sol mineur]", 12],
        [1, "06. Esprit de lumière [Fa majeur]", 13],
        [1, "07. Laudate Dominum (Taizé) [La mineur]", 15],
        [1, "08. Accueille au creux de tes mains [Mi mineur]", 17],
        [1, "09. Vivre d’amour [Mib majeur]", 18],
        [1, "10. Sanctus — Messe St-Paul [La mineur]", 19],
        [1, "11. Messe St-Jean : Agnus [Ré mineur]", 20],
        [2, "Agnus Dei (Partie chantée)", 24],
        [1, "12. Tu fais ta demeure en nous [Mi mineur]", 25],
        [1, "13. Marie, Mère de Dieu [Mi mineur]", 26],
        [1, "14. Pour tes merveilles [Ré mineur]", 27]
    ]

    final_doc.set_toc(toc_outlines)

    final_doc.save(output_pdf, garbage=4, deflate=True)
    print(f"Livret generated successfully: {output_pdf}")

if __name__ == "__main__":
    assemble_complete_booklet()
