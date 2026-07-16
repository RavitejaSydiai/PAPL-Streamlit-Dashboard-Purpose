"""Create a formatted Word report summarizing PAPL_National Insights.pptx."""

from __future__ import annotations

import html
import zipfile
from datetime import datetime, timezone
from pathlib import Path


OUTPUT = Path("docs/PAPL_National_Insights_Analysis.docx")


SLIDES = [
    ("1. Commercial Insights & Opportunity Assessment", [
        "Introduces the national commercial-intelligence and growth-opportunity assessment for Parle Agro."
    ]),
    ("2. Data caveats and coverage", [
        "Establishes that the source scope and limitations must be understood before interpreting the analysis."
    ]),
    ("3. Data basis, definitions and limitations", [
        "Retail-audit data covers April–September 2025 across 12 states and is filtered to Parle Agro and total-category rows.",
        "Sales values are retained in the source file's native units because the currency scale was not independently confirmed.",
        "ND gap equals category numeric distribution minus Parle numeric distribution. Store headroom applies this gap to category-carrying stores.",
        "Pack buckets were derived from ITEM descriptions; tetra is a separate lane and 80 ml tetra is called out independently.",
        "The deck acknowledges incomplete period and Q4 coverage."
    ]),
    ("4. NARTD × Parle Agro", ["Section divider introducing Parle Agro's position in the wider NARTD market."]),
    ("5. National category opportunity", [
        "The deck argues that Parle participates across a very large beverage opportunity but must concentrate investment rather than expand uniformly.",
        "Displayed opportunities include approximately ₹49K Cr RTD Sugar at 3.9% Parle share, ₹17K Cr Plain Water at 4.3%, approximately ₹17K Cr Mango at 39.5%, and approximately ₹2K Cr Milk at 26.0%.",
        "The strategic claim is that the next ₹500 Cr will come from becoming dominant in selected opportunities."
    ]),
    ("6. Executive summary", [
        "Parle's footprint is narrow but powerful where established.",
        "Distribution, rather than product demand, is presented as the main growth ceiling.",
        "Gujarat, Telangana, Punjab and Haryana are revenue-led; Tamil Nadu, Karnataka, West Bengal and Delhi are GTM-led."
    ]),
    ("7. Growth-prioritization matrix", [
        "States are assessed on revenue opportunity and right-to-win factors such as franchise strength, distribution, sales footprint and route-to-market capability.",
        "Leverage strengths: Gujarat, Telangana, Punjab and Haryana.",
        "Invest to win: Uttar Pradesh, Maharashtra, Rajasthan and Andhra Pradesh.",
        "Build the right to win: Tamil Nadu, Karnataka, West Bengal and Delhi.",
        "The key instruction is to assign each state a strategic role rather than treat all states equally."
    ]),
    ("8. Business scorecard and simulator", [
        "The framework combines category size, opportunity size, Parle value share, numeric and weighted distribution, and distribution gaps.",
        "Andhra Pradesh has the highest displayed priority score (70.4), followed by Tamil Nadu (57) and Uttar Pradesh (50).",
        "Prototype assumptions include 45,000 stores onboarded per quarter and 60% first-year new-store ROS ramp.",
        "The visual identifies 14 quick wins and estimates ₹688 Cr in first-year revenue."
    ]),
    ("9. National strengths", [
        "Frooti and Smoodh are presented as category leaders, with cited shares of 23.6% in Mango Drinks and 13.3% in Milk Drinks.",
        "Both brands appear to generate strong value relative to their distribution, indicating that consumer acceptance is proven and reach is the main issue."
    ]),
    ("10. Weaknesses and whitespace", [
        "Energy and Mixers are treated as portfolio whitespace.",
        "RTD Sugar is the largest category but Parle has a low share, making it the largest absolute value opportunity.",
        "Bailley's numeric distribution is cited at approximately 0.85% against about 14.7% category availability."
    ]),
    ("11. Parle Agro vs. competition", ["Section divider introducing competitive and category benchmarking."]),
    ("12. Strategic state segmentation", [
        "The four-zone framework recommends monetizing established strengths, investing in large revenue pools, building execution capability where route to market is weak, and protecting profitability in lower-priority markets."
    ]),
    ("13. Revenue-led states", ["Introduces Gujarat, Telangana, Punjab and Haryana as the revenue/RGM-led group."]),
    ("14. Revenue-led category size and share", [
        "Category values shown: Gujarat 19,987; Telangana 20,086; Punjab 17,813; Haryana 25,783.",
        "Parle value shares shown: Gujarat 2.51%; Telangana 4.29%; Punjab 2.05%; Haryana 6.94%.",
        "Haryana has the strongest current capture, while the other three states have wider untapped pools relative to current share."
    ]),
    ("15. Revenue-led distribution headroom", [
        "Average ND gaps: Gujarat 55.5pp; Telangana 52.8pp; Punjab 63.4pp; Haryana 55.0pp.",
        "Estimated store headroom: Gujarat 1.966M; Punjab 1.357M; Telangana 1.063M; Haryana 0.911M.",
        "Punjab has the widest percentage gap; Gujarat has the largest absolute store opportunity."
    ]),
    ("16. Revenue-led pack mix", [
        "Combined value mix: Family/Party 33.04%; Single-serve 16.27%; Sharing 16.01%; Tetra 15.91%; Individual/on-the-go 15.24%; 80 ml tetra 3.52%.",
        "Family packs are especially important in Haryana, Telangana and Punjab.",
        "The 80 ml tetra segment is almost entirely Smoodh: 887,363.6 source-value units versus 1,704.5 for Frooti, suggesting a Frooti format opportunity."
    ]),
    ("17. Category and price-pack simulation", [
        "The proposed portfolio architecture covers entry/tetra, individual consumption, value packs and family packs.",
        "Displayed price-band values are: under ₹10, ₹349 Cr; ₹10–15, ₹754 Cr; ₹15–20, ₹654 Cr; ₹20–30, ₹134 Cr; ₹30–50, ₹201 Cr; ₹50+, ₹104 Cr.",
        "The deck estimates ₹294 Cr potential from filling the weak ₹20–30 price band."
    ]),
    ("18. Revenue opportunity simulator", [
        "Closing 50% of the ND gap lifts modeled revenue from ₹2,195 Cr to ₹3,308 Cr, an increment of ₹1,113 Cr.",
        "Projected market share is 6.86%, up 2.31 percentage points.",
        "The model displays 1,36,23,420 stores to add; this unusually large figure requires validation.",
        "Portfolio-entry and ROS-uplift levers are zero, so all modeled growth comes from distribution."
    ]),
    ("19. RGM synthesis", [
        "Gujarat, Telangana and Punjab combine large category pools with low Parle capture.",
        "The 52.8–63.4pp distribution gap is identified as the principal cause.",
        "RGM states over-index on Family/Party packs (33.0% versus 23.6% in GTM states), while individual/on-the-go formats under-index.",
        "Recommended sequence: expand Frooti and Smoodh reach first, then consider RTD Sugar and Water."
    ]),
    ("20. GTM-led states", [
        "Introduces Tamil Nadu, Karnataka, West Bengal and Delhi, where execution rather than insufficient demand is considered the binding constraint."
    ]),
    ("21. Mango distribution gap", [
        "Tamil Nadu: category ND 76.7%, Parle Mango ND 14.2%, gap 62.5pp, 893K-store headroom.",
        "Karnataka: 68.1% versus 11.4%, gap 56.7pp, 646K stores.",
        "West Bengal: 51.9% versus 17.9%, gap 34.1pp, 628K stores.",
        "Delhi: 76.3% versus 52.0%, gap 24.4pp, 97K stores.",
        "Tamil Nadu and Karnataka have the largest reach problems; Delhi is the more developed benchmark."
    ]),
    ("22. Portfolio breadth and SKU depth", [
        "Active brands: Tamil Nadu 6, Karnataka 7, West Bengal 6, Delhi 8.",
        "Active SKUs: Tamil Nadu 84, Karnataka 82, West Bengal 58, Delhi 82.",
        "West Bengal combines the largest store opportunity with the weakest product activation; Delhi demonstrates stronger execution."
    ]),
    ("23. Execution simulator", [
        "The model separates direct-distribution reach (DDR), distribution quality (DQI), and out-of-stock recovery.",
        "At 50% DDR-gap closure, modeled revenue increases from ₹2,195 Cr to ₹3,308 Cr, with projected share of 6.86%.",
        "Average OOS is displayed at 5.79% and stock share at 26.4%; DQI and OOS levers contribute zero in the shown scenario."
    ]),
    ("24. State-category and portfolio sequencing", [
        "Contribution to NARTD opportunity: AP 30.9%, UP 24.5%, Maharashtra 10.2%, Rajasthan 8.3%, TN 7.3%, Haryana 5.7%, Delhi 5.2%, Telangana 3.6%, Gujarat 3.1%, Karnataka 1.2%.",
        "The slide compares recommended execution order with actual performance order.",
        "Bailley and Appy often need earlier activation based on category opportunity, while current performance remains dominated by Frooti and, in some states, Smoodh."
    ]),
    ("25. GTM synthesis", [
        "Tamil Nadu, Karnataka and West Bengal have meaningful category size but insufficient Parle reach.",
        "West Bengal is the clearest execution gap: 1.85M category stores but only 6 active brands and 58 SKUs.",
        "Delhi is the internal benchmark, with 8 active brands, the smallest Mango ND gap, and 8.7% overall Parle share.",
        "Channel-level data is unavailable; store-format and channel distribution data should be obtained before final RTM investment allocation."
    ]),
]


def run(text: str, *, bold: bool = False, size: int | None = None, color: str | None = None) -> str:
    props = []
    if bold:
        props.append("<w:b/>")
    if size:
        props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    safe = html.escape(text)
    return f'<w:r><w:rPr>{"".join(props)}</w:rPr><w:t xml:space="preserve">{safe}</w:t></w:r>'


def paragraph(text: str = "", *, style: str | None = None, bullet: bool = False, page_break: bool = False) -> str:
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if bullet:
        ppr.append('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>')
    content = '<w:r><w:br w:type="page"/></w:r>' if page_break else run(text)
    return f'<w:p><w:pPr>{"".join(ppr)}</w:pPr>{content}</w:p>'


def document_xml() -> str:
    body = [
        paragraph("PAPL National Insights", style="Title"),
        paragraph("Complete PowerPoint Analysis and Slide-by-Slide Summary", style="Subtitle"),
        paragraph("Prepared from: PAPL_National Insights.pptx"),
        paragraph("Scope: All 25 slides, including embedded charts, tables and simulator visuals"),
        paragraph(page_break=True),
        paragraph("Executive summary", style="Heading1"),
    ]
    for item in [
        "Parle Agro's strongest brands already perform well where distributed; store reach is the primary growth constraint.",
        "Revenue/RGM-led states are Gujarat, Telangana, Punjab and Haryana.",
        "GTM/execution-led states are Tamil Nadu, Karnataka, West Bengal and Delhi.",
        "Andhra Pradesh, Uttar Pradesh, Maharashtra and Rajasthan are positioned as invest-to-win markets.",
        "The fastest route to growth is expanding Frooti and Smoodh distribution before broad category expansion.",
        "RTD Sugar is the largest absolute category opportunity; Water has a severe Bailley distribution gap; Energy and Mixers represent whitespace.",
        "Delhi is the execution benchmark, while West Bengal is the clearest portfolio-activation gap.",
    ]:
        body.append(paragraph(item, bullet=True))
    body += [paragraph("Recommended strategic sequence", style="Heading2")]
    for item in [
        "Close numeric-distribution gaps for Frooti and Smoodh.",
        "Improve brand breadth, SKU depth and route-to-market execution by state.",
        "Correct pack and price-ladder gaps, particularly individual formats and the ₹20–30 band.",
        "Expand into RTD Sugar, Water, Mixers and Energy only after core distribution execution is strengthened.",
    ]:
        body.append(paragraph(item, bullet=True))
    body += [paragraph(page_break=True), paragraph("Slide-by-slide analysis", style="Heading1")]
    for title, bullets in SLIDES:
        body.append(paragraph(title, style="Heading2"))
        for item in bullets:
            body.append(paragraph(item, bullet=True))
    body += [
        paragraph(page_break=True),
        paragraph("Validation points before Python reproduction", style="Heading1"),
    ]
    for item in [
        "RTD Sugar share is displayed as 3.9% on one slide but described as 1.6% elsewhere.",
        "Mango and Milk national shares vary between slides.",
        "Some state-map share labels are materially higher than the shares used in later state analysis.",
        "Source percentage and distribution metrics above 100 suggest possible hierarchy-level aggregation issues.",
        "The simulator's store-addition figure is unusually large and must be confirmed.",
        "The ₹294 Cr price-ladder and ₹1,113 Cr distribution opportunities depend on modeling assumptions, not only observed source data.",
        "All commercial conclusions should be recreated from the Final Ver sheet after separating category totals, manufacturer totals and item-level records."
    ]:
        body.append(paragraph(item, bullet=True))
    body.append(paragraph("End of report"))
    sect = '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720"/></w:sectPr>'
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + "".join(body) + sect + '</w:body></w:document>'


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:spacing w:before="1800" w:after="240"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:color w:val="17365D"/><w:sz w:val="44"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:pPr><w:spacing w:after="480"/><w:jc w:val="center"/></w:pPr><w:rPr><w:color w:val="666666"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:keepNext/><w:spacing w:before="300" w:after="180"/></w:pPr><w:rPr><w:b/><w:color w:val="17365D"/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:color w:val="2F5597"/><w:sz w:val="26"/></w:rPr></w:style>
</w:styles>'''
    numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>'''
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>PAPL National Insights Analysis</dc:title><dc:creator>OpenAI Codex</dc:creator><dc:subject>PowerPoint analysis and slide summary</dc:subject><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created></cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office Word</Application></Properties>'''
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("word/document.xml", document_xml())
        archive.writestr("word/_rels/document.xml.rels", doc_rels)
        archive.writestr("word/styles.xml", styles)
        archive.writestr("word/numbering.xml", numbering)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)
    print(f"Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
