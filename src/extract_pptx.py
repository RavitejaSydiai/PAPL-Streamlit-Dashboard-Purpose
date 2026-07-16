"""Extract slide text, notes, tables, and chart caches from a PPTX using stdlib only."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


PPTX = Path(r"C:\Users\RavitejaKamsali\Downloads\PAPL_National Insights.pptx")
OUTPUT = Path("docs/papl_national_insights_extract.json")
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def natural_key(name: str) -> tuple:
    return tuple(int(part) if part.isdigit() else part for part in re.split(r"(\d+)", name))


def xml_text(root: ET.Element) -> list[str]:
    return [node.text.strip() for node in root.findall(".//a:t", NS) if node.text and node.text.strip()]


def relationships(archive: zipfile.ZipFile, rel_path: str) -> dict[str, str]:
    if rel_path not in archive.namelist():
        return {}
    root = ET.fromstring(archive.read(rel_path))
    return {
        rel.attrib["Id"]: rel.attrib.get("Target", "")
        for rel in root.findall("pr:Relationship", NS)
    }


def chart_data(root: ET.Element) -> dict:
    series = []
    for node in root.findall(".//c:ser", NS):
        text = xml_text(node)
        categories = []
        values = []
        for point in node.findall(".//c:cat//c:pt", NS):
            value = point.find("c:v", NS)
            if value is not None and value.text is not None:
                categories.append(value.text)
        for point in node.findall(".//c:val//c:pt", NS):
            value = point.find("c:v", NS)
            if value is not None and value.text is not None:
                values.append(value.text)
        series.append({"text": text, "categories": categories, "values": values})
    return {"text": xml_text(root), "series": series}


def main() -> None:
    with zipfile.ZipFile(PPTX) as archive:
        names = archive.namelist()
        slide_paths = sorted(
            (name for name in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
            key=natural_key,
        )
        charts = {
            name: chart_data(ET.fromstring(archive.read(name)))
            for name in names
            if re.fullmatch(r"ppt/charts/chart\d+\.xml", name)
        }
        slides = []
        for number, slide_path in enumerate(slide_paths, 1):
            root = ET.fromstring(archive.read(slide_path))
            rel_path = slide_path.replace("slides/", "slides/_rels/") + ".rels"
            rels = relationships(archive, rel_path)
            linked_charts = []
            for chart in root.findall(".//c:chart", NS):
                target = rels.get(chart.attrib.get(f"{{{NS['r']}}}id", ""), "")
                chart_name = "ppt/" + target.replace("../", "")
                if chart_name in charts:
                    linked_charts.append({"path": chart_name, **charts[chart_name]})

            linked_images = []
            for picture in root.findall(".//p:pic", NS):
                blip = picture.find(".//a:blip", NS)
                if blip is None:
                    continue
                target = rels.get(blip.attrib.get(f"{{{NS['r']}}}embed", ""), "")
                if target:
                    linked_images.append("ppt/" + target.replace("../", ""))

            note_path = f"ppt/notesSlides/notesSlide{number}.xml"
            notes = xml_text(ET.fromstring(archive.read(note_path))) if note_path in names else []
            slides.append(
                {
                    "slide": number,
                    "text": xml_text(root),
                    "notes": notes,
                    "charts": linked_charts,
                    "images": linked_images,
                    "shape_count": len(root.findall(".//p:sp", NS)),
                    "table_count": len(root.findall(".//a:tbl", NS)),
                    "image_count": len(root.findall(".//p:pic", NS)),
                }
            )

        payload = {
            "file": str(PPTX),
            "slide_count": len(slides),
            "slides": slides,
            "media": [name for name in names if name.startswith("ppt/media/")],
            "embedded_files": [name for name in names if name.startswith("ppt/embeddings/")],
        }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Extracted {len(slides)} slides to {OUTPUT}")


if __name__ == "__main__":
    main()
