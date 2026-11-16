#!/usr/bin/env python3
"""Surgical fix for QR-2026-1116-R TOC (rewrite, single pass, robust):
1. In the _Toc1 hyperlink entry, put cached page number '1' between the
   PAGEREF field's separate and end fldChars (idempotent).
2. Remove the plain duplicate paragraph with texts ['1. Executive Summary','1'].
"""
import re, shutil, zipfile, os

DOCX = "/home/z/my-project/download/QR-2026-1116-R_CRO_Remediation_Verification.docx"
TMP = DOCX + ".fixwork"

shutil.rmtree(TMP, ignore_errors=True)
os.makedirs(TMP)
with zipfile.ZipFile(DOCX) as z:
    z.extractall(TMP)

xml_path = os.path.join(TMP, "word", "document.xml")
xml = open(xml_path, encoding="utf-8").read()

CACHED = ('<w:fldChar w:fldCharType="separate"/>'
          '<w:r><w:rPr><w:noProof/></w:rPr><w:t xml:space="preserve">1</w:t></w:r>'
          '<w:fldChar w:fldCharType="end"/>')
EMPTY = ('<w:fldChar w:fldCharType="separate"/>'
         '<w:fldChar w:fldCharType="end"/>')

if CACHED not in xml:
    assert EMPTY in xml, "empty PAGEREF cache not found"
    xml = xml.replace(EMPTY, CACHED, 1)
    print("step 1: cached page number injected")
else:
    print("step 1: already cached, skipped")

# remove the plain duplicate paragraph
removed = False
for m in re.finditer(r'<w:p[ >].*?</w:p>', xml, re.S):
    seg = m.group(0)
    texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', seg)
    if texts == ["1. Executive Summary", "1"] and "<w:hyperlink" not in seg and "fldChar" not in seg:
        xml = xml[:m.start()] + xml[m.end():]
        removed = True
        break
assert removed, "plain duplicate paragraph not found"
print("step 2: duplicate paragraph removed")

open(xml_path, "w", encoding="utf-8").write(xml)

out = DOCX
os.remove(out)
zf = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(TMP):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, TMP)
        zf.write(full, rel)
zf.close()
shutil.rmtree(TMP)
print("fixed and rezipped")
