---
title: "Step-by-step explanation of Oracle HCM Cloud HDL Transformation Fast Formula — OPERATION routing, METADATA arrays, MAP steps, WSA caching, LINEREPEATNO, MultipleEntryCount, and ElementEntry output. Part 1 of 3."
pubDate: 2026-03-25
description: "Step-by-step explanation of Oracle HCM Cloud HDL Transformation Fast Formula — OPERATION routing, METADATA arrays, MAP steps, WSA caching,..."
tags: ["Fast Formula", "HDL", "Oracle HCM Cloud"]
author: "Abhishek Mohanty"
draft: false
---

<style>
@media (prefers-color-scheme: dark) {
.hdl-blog { background: #12131A !important; color: #C8C9D4 !important; }
.hdl-blog p, .hdl-blog li { color: #C8C9D4 !important; }
.hdl-blog strong { color: #EAEBF0 !important; }
.hdl-blog em { color: #C8C9D4 !important; }
.hdl-blog code { background: #1E1F2B !important; color: #D4D5DE !important; }
.hdl-blog hr { border-color: #2A2B38 !important; }

.hdl-blog [style*="background:linear-gradient(135deg,#1B4965"] { background: linear-gradient(135deg,#0D2B3E,#081C2B) !important; box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important; }
.hdl-blog [style*="font-size:17px"][style*="font-weight:700"] { color: #EAEBF0 !important; }
.hdl-blog [style*="font-size:15px"][style*="font-weight:700"][style*="border-left"] { color: #D4D5DE !important; }

.hdl-blog [style*="background:#fff"] { background: #1A1B26 !important; }
.hdl-blog [style*="background:#F5F3EF"] { background: #16171F !important; }
.hdl-blog [style*="background:#FDF5ED"] { background: #1C1812 !important; border-color: #3D3224 !important; }
.hdl-blog [style*="background:#FCF0F0"] { background: #1C1414 !important; }
.hdl-blog [style*="background:#EDE8E0"] { background: #1E1F2B !important; }

.hdl-blog [style*="#DDD8D0"] { border-color: #2A2B38 !important; }
.hdl-blog td, .hdl-blog th, .hdl-blog tr { border-color: #2A2B38 !important; }

.hdl-blog td { color: #C8C9D4 !important; }
.hdl-blog th { color: #fff !important; }
.hdl-blog td[style*="font-weight:700"] { color: #EAEBF0 !important; }
.hdl-blog td[style*="font-weight:600"] { color: #D4D5DE !important; }
.hdl-blog td[style*="font-weight:800"] { color: #EAEBF0 !important; }

.hdl-blog [style*="color:#D4622B"] { color: #E89060 !important; }
.hdl-blog td[style*="color:#D4622B"] { color: #E89060 !important; }
.hdl-blog [style*="background:#D4622B"], .hdl-blog [style*="background:linear-gradient(135deg,#D4622B"] { color: #fff !important; }

.hdl-blog [style*="color:#2D8B6F"] { color: #5CC4A0 !important; }
.hdl-blog [style*="background:#2D8B6F"] { background: #1A5C47 !important; }

.hdl-blog [style*="color:#C13B3B"] { color: #F08080 !important; }
.hdl-blog [style*="background:#C13B3B"] { background: #8B2020 !important; }
.hdl-blog [style*="border"][style*="#C13B3B"] { border-color: #5C1A1A !important; }

.hdl-blog [style*="color:#8B8FA8"] { color: #6B6F88 !important; }

.hdl-blog pre { background: #0D0E14 !important; border-color: #1E1F2B !important; }

.hdl-blog [style*="background:#1E1E1E"] { background: #0D0E14 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#8B8FA8"] { color: #6B6F88 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#B5CEA8"] { color: #B5CEA8 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#CE9178"] { color: #CE9178 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#2D8B6F"] { color: #5CC4A0 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#C13B3B"] { color: #F08080 !important; }

.hdl-blog [style*="background:#1B4965"] { background: #0D2B3E !important; }

.hdl-blog [style*="font-size:28px"][style*="color:#C13B3B"] { color: #F08080 !important; }
.hdl-blog [style*="font-size:28px"][style*="color:#D4622B"] { color: #E89060 !important; }

.hdl-blog [style*="background:#eee"] { background: #2A2B38 !important; color: #8B8FA8 !important; }

.hdl-blog span[style*="border-radius:10px"] { color: #fff !important; }
.hdl-blog span[style*="border-radius:12px"] { color: #fff !important; }

.hdl-blog [style*="font-size:30px"][style*="font-weight:800"] { color: #F0F1F5 !important; }

.hdl-blog td[style*="font-family:monospace"] { color: #C8C9D4 !important; }

.hdl-blog [style*="color:#1A1A2E"] { color: #EAEBF0 !important; }
.hdl-blog [style*="color:#3D3D5C"] { color: #C8C9D4 !important; }
}

<style>
.hdl-blog table { min-width: 400px; }

.hdl-blog .block-table { font-size: 11px !important; }
.hdl-blog .block-table td, .hdl-blog .block-table th { padding: 5px 6px !important; font-size: 11px !important; white-space: nowrap !important; }
.hdl-blog .db-table { font-size: 11px !important; }
.hdl-blog .db-table td, .hdl-blog .db-table th { padding: 5px 6px !important; font-size: 11px !important; white-space: nowrap !important; }

.hdl-blog div[style*="overflow:hidden"] { overflow-x: auto !important; }
</style>
</style>
<div class="hdl-blog" style="font-family:'Open Sans',sans-serif;color:#3D3D5C;line-height:1.85;max-width:760px;margin:0 auto;background:#FCFBF9;">

<span style="display:inline-block;background:#D4622B;color:#fff;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:5px;margin-bottom:8px;margin-right:8px;box-shadow:0 2px 4px rgba(212,98,43,0.2);">Fast Formula</span>
<span style="display:inline-block;background:#D4622B;color:#fff;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:5px;margin-bottom:8px;margin-right:8px;box-shadow:0 2px 4px rgba(212,98,43,0.2);">HCM Data Loader</span>
<span style="display:inline-block;background:#D4622B;color:#fff;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:5px;margin-bottom:8px;margin-right:8px;box-shadow:0 2px 4px rgba(212,98,43,0.2);">Transformation Formula</span>
<span style="display:inline-block;background:#D4622B;color:#fff;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:5px;margin-bottom:8px;margin-right:8px;box-shadow:0 2px 4px rgba(212,98,43,0.2);">WSA</span>
<span style="display:inline-block;background:#1A1A2E;color:#fff;padding:5px 16px;font-size:11px;letter-spacing:1.5px;font-weight:700;letter-spacing:2px;text-transform:uppercase;border-radius:2px;margin-bottom:6px;margin-right:6px;">Series Part 1 of 3</span>

<div style="font-size:30px;font-weight:800;color:#1A1A2E;margin:24px 0 10px;line-height:1.25;letter-spacing:-0.8px;">HDL Transformation Formula Deep Dive — Part 1: Pure Concepts</div>

<div style="font-size:15px;color:#8B8FA8;margin-bottom:6px;letter-spacing:0.5px;">Vendor Deduction Interface | ElementEntry + ElementEntryValue</div>
<div style="font-size:13px;color:#8B8FA8;margin-bottom:25px;letter-spacing:0.5px;">March 2026 • 25 min read • Oracle HCM Cloud</div>

<div style="font-size:15px;color:#3D3D5C;line-height:1.7;margin-bottom:30px;font-style:italic;border-left:4px solid #D4622B;padding-left:18px;">
This is <strong>Part 1</strong> of a 3-part series on HDL Transformation Formulas. This post covers the concepts end-to-end — what each section of the formula does and why. No code to copy-paste here. Just the understanding you need before writing a single line.
</div>

<!-- SERIES ROADMAP -->
<div style="margin:0 0 35px;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;color:#fff;padding:14px 20px;font-weight:700;font-size:15px;">HDL Transformation Formula Series</div>
<div style="padding:0;">

<div style="display:flex;align-items:center;gap:16px;padding:16px 20px;border-bottom:1px solid #DDD8D0;background:#FDF5ED;">
<div style="background:#D4622B;color:#fff;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;box-shadow:0 2px 8px rgba(212,98,43,0.25);">1</div>
<div>
<div style="font-weight:700;font-size:15px;color:#D4622B;">Pure Concepts <span style="font-size:13px;font-weight:400;color:#8B8FA8;margin-left:6px;">← You are here</span></div>
<div style="font-size:13px;color:#8B8FA8;">What each section of the formula does. INPUTS, OPERATION, METADATA, MAP (5 steps), WSA, LINEREPEATNO, RETURN. Zero code to memorize — just understanding.</div>
</div>
</div>

<div style="display:flex;align-items:center;gap:16px;padding:16px 20px;border-bottom:1px solid #DDD8D0;">
<div style="background:#eee;color:#8B8FA8;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;">2</div>
<div>
<div style="font-weight:700;font-size:15px;color:#3D3D5C;">Code Walkthrough <span style="font-size:13px;font-weight:400;color:#8B8FA8;margin-left:6px;">Coming soon</span></div>
<div style="font-size:13px;color:#8B8FA8;">The actual formula code, explained line-by-line. Value set definitions, WSA implementation, date conversions, ISNULL patterns, ESS_LOG_WRITE debugging. Moderate complexity — you'll be able to read any HDL formula after this.</div>
</div>
</div>

<div style="display:flex;align-items:center;gap:16px;padding:16px 20px;">
<div style="background:#eee;color:#8B8FA8;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;">3</div>
<div>
<div style="font-weight:700;font-size:15px;color:#3D3D5C;">Build Your Own <span style="font-size:13px;font-weight:400;color:#8B8FA8;margin-left:6px;">Coming soon</span></div>
<div style="font-size:13px;color:#8B8FA8;">Full implementation guide. Setting up the formula in Oracle, creating the value sets, configuring the HDL integration, testing with real data, debugging production issues. Copy-paste ready.</div>
</div>
</div>

</div>
</div>

<div style="display:flex;align-items:center;gap:14px;padding:20px 0;border-top:1px solid #DDD8D0;border-bottom:2px solid #DDD8D0;margin-bottom:35px;">
<div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#D4622B,#E8944F);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;flex-shrink:0;">AM</div>
<div>
<div style="font-weight:700;font-size:15px;">Abhishek Mohanty</div>
<div style="font-size:13px;color:#8B8FA8;">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant</div>
</div>
</div>

<!-- ==================== BIG PICTURE FLOW ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">The Big Picture</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Before we go section by section, here's what this formula does end to end:</p>

<!-- VISUAL: END-TO-END PIPELINE -->
<div style="display:flex;align-items:center;gap:0;margin:20px 0;flex-wrap:wrap;">
<div style="background:#D4622B;color:#fff;padding:8px 10px;border-radius:8px 0 0 8px;font-weight:700;font-size:13px;text-align:center;min-width:100px;">
Vendor CSV File<br><span style="font-size:13px;font-weight:400;opacity:0.7;">SSN, Date, Code, Amounts</span>
</div>
<div style="width:0;height:0;border-top:24px solid transparent;border-bottom:24px solid transparent;border-left:14px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;min-width:120px;">
HDL Transformation<br><span style="font-size:13px;font-weight:400;opacity:0.7;">This Formula</span>
</div>
<div style="width:0;height:0;border-top:24px solid transparent;border-bottom:24px solid transparent;border-left:14px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;border-radius:0 8px 8px 0;font-weight:700;font-size:13px;text-align:center;min-width:120px;">
ElementEntry .dat<br><span style="font-size:13px;font-weight:400;opacity:0.7;">Header + Value rows</span>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">A third-party benefits administration vendor (BenAdmin) sends a CSV with deduction and employer contribution amounts. This formula transforms each row into Oracle HDL format — resolving SSNs to Assignment Numbers, mapping vendor codes to Oracle Element Names, managing MultipleEntryCount, and generating both ElementEntry (header) and ElementEntryValue (detail) rows.</p>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 1: VENDOR FILE ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 1: The Vendor Inbound File — What We Receive</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The vendor manages employee benefit enrollments — medical, dental, vision, life insurance, FSA, HSA, loans. Every pay period, they send a flat CSV file with deduction details to load into Oracle as Element Entries.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The Raw Input File Layout</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Each row in the vendor file maps to one set of delimited columns. The HDL engine reads these into POSITION variables:</p>

<div style="overflow-x:auto;margin:18px 0;border:1px solid #DDD8D0;border-radius:8px;">
<table style="width:100%;border-collapse:collapse;font-size:11px;min-width:700px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;">Column</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;">Position</th>
<th style="padding:6px 8px;text-align:left;font-size:10px;">Description</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;">Example</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">SSN</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION1</td>
<td style="padding:5px 8px;">Employee Social Security Number</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">123-45-6789</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">EFFECTIVE_DATE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION2</td>
<td style="padding:5px 8px;">Date the deduction applies (YYYY-MM-DD)</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">2024-01-15</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">BENEFIT_PLAN_CODE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION3</td>
<td style="padding:5px 8px;">Vendor’s internal code for the benefit plan</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">DENTAL01</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">DEDUCTION_TYPE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION4</td>
<td style="padding:5px 8px;">Controls LINEREPEATNO branches and how many input values are loaded</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">LOAN, PRE, POST, CU</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">AMOUNT</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION5</td>
<td style="padding:5px 8px;">Deduction amount (InputValueName = ‘Amount’)</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">150.00</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">PERIOD_TYPE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION6</td>
<td style="padding:5px 8px;">Period type for the deduction</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(varies)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">PERCENTAGE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION7</td>
<td style="padding:5px 8px;">Percentage for PRE/POST type deductions</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(blank or value)</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">LOAN_NUMBER</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION8</td>
<td style="padding:5px 8px;">Loan number (LOAN type only)</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(blank or value)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;color:#8B8FA8;">POSITION9–10</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION9–10</td>
<td style="padding:5px 8px;color:#8B8FA8;">Reserved / additional fields</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(varies)</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">STATUS</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION11</td>
<td style="padding:5px 8px;">C = Cancel/End-date, blank = Active/New</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(blank)</td>
</tr>
</tbody></table>
</div>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-left:4px solid #D4622B;padding:14px 18px;margin:18px 0;border-radius:0 6px 6px 0;">
<p style="margin:0;font-size:14px;color:#3D3D5C;"><strong>Key point:</strong> POSITION4 (Deduction Type) is the most important field after SSN and Date. It controls the formula's branching logic — which LINEREPEATNO passes execute, which input values get loaded (Amount, Period Type, Percentage, Loan Number, Total Owed, Deduction Amount), and even whether the formula generates output on certain passes. A LOAN type deduction goes through 7 passes. A regular deduction goes through fewer.</p>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How One Vendor Row Becomes Multiple Input Values</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">A single vendor row carries multiple amounts for the same deduction. The formula uses LINEREPEATNO to load each input value in a separate pass. For a LOAN type deduction, one source row generates up to 7 output rows:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* One vendor row: */</span>
<span style="color:#CE9178;">123-45-6789,2024-01-15,DENTAL01,LOAN,150.00,Monthly,5.5,LN-001,,,,</span>

<span style="color:#57A64A;font-style:italic;">/* Formula generates (up to 7 passes): */</span>
<span style="color:#C8C8C8;">Pass 1 (LINEREPEATNO=1):</span> <span style="color:#CE9178;">ElementEntry header</span>
<span style="color:#C8C8C8;">Pass 2 (LINEREPEATNO=2):</span> <span style="color:#CE9178;">ElementEntryValue → Amount = 150.00</span>
<span style="color:#C8C8C8;">Pass 3 (LINEREPEATNO=3):</span> <span style="color:#CE9178;">ElementEntryValue → Period Type = Monthly</span>
<span style="color:#C8C8C8;">Pass 4 (LINEREPEATNO=4):</span> <span style="color:#CE9178;">ElementEntryValue → Loan Number = LN-001</span>
<span style="color:#C8C8C8;">Pass 5 (LINEREPEATNO=5):</span> <span style="color:#CE9178;">ElementEntryValue → Total Owed = ...</span>
<span style="color:#C8C8C8;">Pass 6 (LINEREPEATNO=6):</span> <span style="color:#CE9178;">ElementEntryValue → Percentage = 5.5</span>
<span style="color:#C8C8C8;">Pass 7 (LINEREPEATNO=7):</span> <span style="color:#CE9178;">ElementEntryValue → Deduction Amount = ...</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Not every deduction type needs all 7 passes. The formula checks POSITION4 on each pass — if the type doesn't apply (e.g. Percentage only runs for PRE/POST types), it returns <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code> with no output, effectively skipping that pass.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Understanding MultipleEntryCount</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Oracle HCM draws a fundamental distinction between <strong>recurring</strong> and <strong>non-recurring</strong> elements when it comes to MultipleEntryCount:</p>

<!-- VISUAL: Recurring vs Non-Recurring -->
<div style="display:flex;gap:20px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:300px;border-radius:10px;overflow:hidden;border:1px solid #DDD8D0;border-left:4px solid #D4622B;">
<div style="background:#fff;padding:12px 18px;border-bottom:1px solid #DDD8D0;">
<div style="font-weight:800;font-size:14px;color:#D4622B;">RECURRING ELEMENTS</div>
<div style="font-size:13px;color:#D4622B;">Monthly salary, standing allowance</div>
</div>
<div style="padding:14px 18px;background:#fff;">
<p style="margin:0 0 8px;font-size:14px;color:#3D3D5C;">MultipleEntryCount is <strong>not required</strong> as a key when using SourceSystemId.</p>
<div style="background:#fff;border-radius:6px;padding:6px 8px;font-size:13px;color:#D4622B;"><em>"You don't need to supply the MultipleEntryCount attribute as source keys to uniquely identify the records."</em> — Oracle Docs</div>
</div>
</div>
<div style="flex:1;min-width:300px;border-radius:10px;overflow:hidden;border:1px solid #DDD8D0;border-left:4px solid #D4622B;">
<div style="background:#fff;padding:12px 18px;border-bottom:1px solid #DDD8D0;">
<div style="font-weight:800;font-size:14px;color:#D4622B;">NON-RECURRING ELEMENTS</div>
<div style="font-size:13px;color:#D4622B;">Benefits deductions (our vendor elements)</div>
</div>
<div style="padding:14px 18px;background:#fff;">
<p style="margin:0 0 8px;font-size:14px;color:#3D3D5C;">MultipleEntryCount <strong>must be incremented</strong> for each entry of the same assignment + element within the same payroll period.</p>
<div style="background:#fff;border-radius:6px;padding:6px 8px;font-size:13px;color:#D4622B;"><em>"You must increment the value of MultipleEntryCount for each entry of the same assignment and element."</em> — Oracle Docs</div>
</div>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The vendor interface loads <strong>non-recurring elements that allow multiple entries</strong>. This means the formula must query the cloud for the current highest MultipleEntryCount before assigning the next one — and track assigned values across rows within the same batch using WSA.</p>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#D4622B;"><strong>Key Takeaway:</strong> Three benefit plan rows (Dental, Medical, Vision) for the same employee map to three <strong>different elements</strong>, so they each get independent entries with their own MultipleEntryCount. MultipleEntryCount is needed when the <strong>same non-recurring element</strong> requires <strong>multiple entries</strong> for the <strong>same assignment within the same payroll period</strong>.</p>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 2: VALUE SETS ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 2: Why Value Sets? Understanding Each GET_VALUE_SET Call</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The vendor file gives us an <strong>SSN</strong> and an <strong>Vendor Deduction Code</strong>. Oracle HCM needs an <strong>Assignment Number</strong> and an <strong>Oracle Element Name</strong>. These are completely different identifiers in completely different systems. Value Sets act as the bridge — SQL-backed lookup functions that run inside the Fast Formula engine.</p>

<!-- VISUAL: Translation bridge -->
<div style="display:flex;align-items:center;gap:0;margin:20px 0;flex-wrap:wrap;">
<div style="background:#fff;border:1px solid #DDD8D0;padding:14px 18px;border-radius:8px 0 0 8px;text-align:center;min-width:160px;">
<div style="font-size:13px;color:#D4622B;font-weight:700;letter-spacing:1px;">VENDOR ENVIRONMENT</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;margin-top:6px;">SSN: 123-45-6789</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">Code: DENTAL01</div>
</div>
<div style="background:#D4622B;color:#fff;padding:14px 18px;text-align:center;min-width:120px;">
<div style="font-size:13px;opacity:0.7;font-weight:700;letter-spacing:1px;">VALUE SETS</div>
<div style="font-size:20px;margin-top:4px;">→</div>
</div>
<div style="background:#fff;border:1px solid #DDD8D0;padding:14px 18px;border-radius:0 8px 8px 0;text-align:center;min-width:180px;">
<div style="font-size:13px;color:#D4622B;font-weight:700;letter-spacing:1px;">ORACLE WORLD</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;margin-top:6px;">Asg#: E12345</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">Element: Dental EE Deduction</div>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula uses 11 value sets. Here's what each one does:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:center;width:30px;">#</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Value Set</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">What It Does</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Returns</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">1</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">XXVA_DEDUCTION_CODES</td>
<td style="padding:6px 8px;">Maps vendor plan code (DENTAL01) to Oracle Element Name</td>
<td style="padding:6px 8px;">Element Name</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">2</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">XXVA_DEDUCTION_CODES_INPUT</td>
<td style="padding:6px 8px;">Gets Input Value Name for the element (e.g. Amount)</td>
<td style="padding:6px 8px;">Input Value Name</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">3</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">XXVA_GET_LATEST_ASSIGNMENT_NUMBER</td>
<td style="padding:6px 8px;">Resolves SSN + date → Assignment Number</td>
<td style="padding:6px 8px;">Assignment# (E12345)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">4</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">XXVA_GET_PERSON_NUMBER</td>
<td style="padding:6px 8px;">Resolves SSN → Person Number</td>
<td style="padding:6px 8px;">Person# (100045)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">5</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">MAX_MULTI_ENTRY_COUNT</td>
<td style="padding:6px 8px;">Gets highest existing MultipleEntryCount for Person+Element+Date</td>
<td style="padding:6px 8px;">Max count (or NULL)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">6–7</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;">GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID / _OWNER</td>
<td style="padding:6px 8px;">Retrieves existing SourceSystemId/Owner for MERGE key reuse</td>
<td style="padding:6px 8px;">Existing SSID/SSO</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">8–9</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;">GET_ELEMENT_ENTRY_VALUE_SOURCE_SYSTEM_ID / _OWNER</td>
<td style="padding:6px 8px;">Same but at Element Entry Value level</td>
<td style="padding:6px 8px;">ElementEntryValue-level SSID/SSO</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">10</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">GET_ELEMENT_ENTRY_START_DATE</td>
<td style="padding:6px 8px;">For Cancel rows — gets original start date</td>
<td style="padding:6px 8px;">Original start date</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">11</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">GET_ELEMENT_ENTRY_INPUT_START_DATE</td>
<td style="padding:6px 8px;">Same but at ElementEntryValue level (date-tracked scenarios)</td>
<td style="padding:6px 8px;">ElementEntryValue original start date</td>
</tr>
</tbody></table>

<!-- VISUAL: Code vs Person lookup split -->
<div style="display:flex;gap:16px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:250px;background:#fff;border:1px solid #DDD8D0;border-top:3px solid #D4622B;border-radius:8px;padding:16px;">
<div style="font-weight:800;font-size:13px;color:#D4622B;margin-bottom:8px;">CODE-BASED LOOKUPS (#1–2)</div>
<p style="margin:0;font-size:13px;color:#3D3D5C;">Translate vendor codes → Oracle element names. Called once per row regardless. No caching benefit.</p>
</div>
<div style="flex:1;min-width:250px;background:#fff;border:1px solid #DDD8D0;border-top:3px solid #D4622B;border-radius:8px;padding:16px;">
<div style="font-weight:800;font-size:13px;color:#D4622B;margin-bottom:8px;">PERSON-BASED LOOKUPS (#3–11)</div>
<p style="margin:0;font-size:13px;color:#3D3D5C;">Resolve SSN/Person data. Same SSN appears across multiple rows — <strong>WSA caching saves significant performance here.</strong></p>
</div>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 3: INPUTS ARE ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 3: INPUTS ARE — Declaring Formula Input Variables</div>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">INPUTS ARE</span> <span style="color:#C8C8C8;">OPERATION</span> (<span style="color:#CC7832;">TEXT</span>),
<span style="color:#C8C8C8;">LINEREPEATNO</span> (<span style="color:#CC7832;">NUMBER</span>),
<span style="color:#C8C8C8;">LINENO</span> (<span style="color:#CC7832;">NUMBER</span>),
<span style="color:#C8C8C8;">POSITION1</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION2</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION3</span> (<span style="color:#CC7832;">TEXT</span>),
<span style="color:#C8C8C8;">POSITION4</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION5</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION6</span> (<span style="color:#CC7832;">TEXT</span>),
<span style="color:#C8C8C8;">POSITION7</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION8</span> (<span style="color:#CC7832;">TEXT</span>),
<span style="color:#C8C8C8;">POSITION9</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION10</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION11</span> (<span style="color:#CC7832;">TEXT</span>)

<span style="color:#fff;font-weight:700;">DEFAULT FOR</span> <span style="color:#C8C8C8;">LINENO</span> <span style="color:#fff;font-weight:700;">IS</span> <span style="color:#DCDCAA;">1</span>
<span style="color:#fff;font-weight:700;">DEFAULT FOR</span> <span style="color:#C8C8C8;">LINEREPEATNO</span> <span style="color:#fff;font-weight:700;">IS</span> <span style="color:#DCDCAA;">1</span>
<span style="color:#fff;font-weight:700;">DEFAULT FOR</span> <span style="color:#C8C8C8;">POSITION1</span> <span style="color:#fff;font-weight:700;">IS</span> <span style="color:#CE9178;">'NO DATA'</span>
<span style="color:#fff;font-weight:700;">DEFAULT FOR</span> <span style="color:#C8C8C8;">POSITION2</span> <span style="color:#fff;font-weight:700;">IS</span> <span style="color:#CE9178;">'NO DATA'</span>
<span style="color:#57A64A;font-style:italic;">/* ... same for POSITION3 through POSITION11 ... */</span></pre>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;width:130px;">Variable</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">What It Does</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;color:#000;width:130px;white-space:nowrap;">OPERATION</td>
<td style="padding:6px 8px;font-size:13px;">The HDL engine calls the formula multiple times with different values: FILETYPE, DELIMITER, READ, NUMBEROFBUSINESSOBJECTS, METADATALINEINFORMATION, then MAP per row. The formula is a router.</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;color:#000;width:130px;white-space:nowrap;">LINEREPEATNO</td>
<td style="padding:6px 8px;font-size:13px;">The repeat counter. When formula sets <code>LINEREPEAT = 'Y'</code>, HDL re-invokes for the same row with incremented LINEREPEATNO. One input row can generate up to 7 HDL output rows: 1 ElementEntry header (pass 1) + up to 6 ElementEntryValue rows (passes 2–7), one per input value (Amount, Period Type, Loan Number, Total Owed, Percentage, Deduction Amount). The deduction type (POSITION4) controls how many passes run.</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;color:#000;width:130px;white-space:nowrap;">LINENO</td>
<td style="padding:6px 8px;font-size:13px;">Line number from the source file (1-based). Useful for error tracing.</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;color:#000;width:130px;white-space:nowrap;">POSITION1–11</td>
<td style="padding:6px 8px;font-size:13px;">Map directly to CSV columns in order. HDL engine splits each line by delimiter and populates these.</td>
</tr>
</tbody></table>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#D4622B;"><strong>Why DEFAULT FOR is required:</strong> When HDL calls the formula for non-MAP operations (like FILETYPE), the POSITION variables aren't populated — no source row is being processed. Without defaults, the formula throws a null reference error at runtime.</p>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 4: OPERATIONS ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 4: OPERATION — The Setup Handshake</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">This section does NOT touch the vendor data — it configures the HDL engine</div>
<div style="padding:14px 16px;font-size:12px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;width:30%;">Input</td>
<td style="padding:6px 0;">HDL engine asks: "What file type? What delimiter? How many objects?"</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;">Formula returns</td>
<td style="padding:6px 0;font-family:monospace;">DELIMITED, comma, NONE, 2</td>
</tr>
<tr>
<td style="padding:6px 0;font-weight:700;">HDL output</td>
<td style="padding:6px 0;color:#8B8FA8;">Nothing written to .dat yet — engine is just being configured</td>
</tr>
</table>
</div>
</div>


<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'FILETYPE'</span> <span style="color:#fff;font-weight:700;">THEN</span>
    <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'DELIMITED'</span>
<span style="color:#fff;font-weight:700;">ELSE IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'DELIMITER'</span> <span style="color:#fff;font-weight:700;">THEN</span>
    <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">','</span>
<span style="color:#fff;font-weight:700;">ELSE IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'READ'</span> <span style="color:#fff;font-weight:700;">THEN</span>
    <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'NONE'</span>
<span style="color:#fff;font-weight:700;">ELSE IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'NUMBEROFBUSINESSOBJECTS'</span> <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'2'</span>
    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">OUTPUTVALUE</span>
)</pre>

<!-- VISUAL: Setup handshake flow -->
<div style="display:flex;align-items:center;gap:0;margin:20px 0;flex-wrap:wrap;">
<div style="background:#D4622B;color:#fff;padding:8px 10px;border-radius:6px 0 0 6px;font-weight:700;font-size:13px;text-align:center;">FILETYPE<br><span style="color:#fff;">DELIMITED</span></div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;">DELIMITER<br><span style="color:#fff;">,</span></div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;">READ<br><span style="color:#fff;">NONE</span></div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;">OBJECTS<br><span style="color:#fff;">2</span></div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;">METADATA</div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;border-radius:0 6px 6px 0;font-weight:700;font-size:13px;text-align:center;">MAP<br><span style="font-size:9px;font-weight:400;">(per row)</span></div>
</div>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Operation</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Engine Asks</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Our Answer</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Why</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;">FILETYPE</td>
<td style="padding:8px 10px;">"What kind of file?"</td>
<td style="padding:8px 10px;font-family:monospace;">DELIMITED</td>
<td style="padding:8px 10px;">Only valid option for HDL transformation</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;">DELIMITER</td>
<td style="padding:8px 10px;">"What separates values?"</td>
<td style="padding:8px 10px;font-family:monospace;">,</td>
<td style="padding:8px 10px;">the vendor sends CSV. Default is pipe (|), so we override.</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;">READ</td>
<td style="padding:8px 10px;">"Skip header rows?"</td>
<td style="padding:8px 10px;font-family:monospace;">NONE</td>
<td style="padding:8px 10px;">vendor file has no header row — process every line.</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;">NUMBEROF...</td>
<td style="padding:8px 10px;">"How many HDL objects?"</td>
<td style="padding:8px 10px;font-family:monospace;">2</td>
<td style="padding:8px 10px;">ElementEntry (header) + ElementEntryValue (detail with amount)</td>
</tr>
</tbody></table>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 5: METADATA ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 5: METADATA — Generating the .dat File Headers</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">This section generates the .dat HEADER rows (not data rows)</div>
<div style="padding:14px 16px;font-size:12px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;width:30%;">Input</td>
<td style="padding:6px 0;">HDL engine asks: "What columns does each object have?"</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;">Formula returns</td>
<td style="padding:6px 0;font-family:monospace;">METADATA1[ ] array, METADATA2[ ] array</td>
</tr>
<tr>
<td style="padding:6px 0;font-weight:700;">HDL writes to .dat</td>
<td style="padding:6px 0;font-family:monospace;font-size:12px;"><span style="color:#D4622B;font-weight:700;">METADATA</span>|ElementEntry|LegislativeDataGroupName|EffectiveStartDate|...<br><span style="color:#D4622B;font-weight:700;">METADATA</span>|ElementEntryValue|LegislativeDataGroupName|EffectiveStartDate|...</td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After the setup handshake, the HDL engine calls the formula with <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">OPERATION = 'METADATALINEINFORMATION'</code>. This is where the formula defines the <strong>column headers</strong> for the .dat output file. These become the METADATA rows you see at the top of each block in the .dat file.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The .dat File Has Two METADATA Header Rows</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Since we told the engine <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">NUMBEROFBUSINESSOBJECTS = 2</code> (ElementEntry + ElementEntryValue), the formula must define two METADATA arrays — one per object. These become the two header rows in the .dat file:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* This header row in the .dat file: */</span>
<span style="color:#CE9178;">METADATA|ElementEntry|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|CreatorType|EffectiveEndDate|EntryType|MultipleEntryCount</span>

<span style="color:#57A64A;font-style:italic;">/* Is generated by this code: */</span></pre>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The Code — METADATA1 (ElementEntry Header)</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula uses an <strong>array variable</strong> called <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">METADATA1</code>. Each array position maps to a column in the .dat header. Positions [1] and [2] are reserved by the HDL engine for FileName and FileDiscriminator — the formula starts filling from position [3].</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">ELSE IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'METADATALINEINFORMATION'</span> <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* ================================================= */</span>
    <span style="color:#57A64A;font-style:italic;">/* METADATA1 — ElementEntry column definitions        */</span>
    <span style="color:#57A64A;font-style:italic;">/* [1] = FileName (auto-filled by HDL engine)         */</span>
    <span style="color:#57A64A;font-style:italic;">/* [2] = FileDiscriminator (auto-filled by HDL engine)*/</span>
    <span style="color:#57A64A;font-style:italic;">/* [3] onwards = we define                            */</span>
    <span style="color:#57A64A;font-style:italic;">/* ================================================= */</span>

    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">3</span>]  = <span style="color:#CE9178;">'LegislativeDataGroupName'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">4</span>]  = <span style="color:#CE9178;">'EffectiveStartDate'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">5</span>]  = <span style="color:#CE9178;">'ElementName'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">6</span>]  = <span style="color:#CE9178;">'AssignmentNumber'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">7</span>]  = <span style="color:#CE9178;">'CreatorType'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">8</span>]  = <span style="color:#CE9178;">'EffectiveEndDate'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">9</span>]  = <span style="color:#CE9178;">'EntryType'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">10</span>] = <span style="color:#CE9178;">'MultipleEntryCount'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">11</span>] = <span style="color:#CE9178;">'SourceSystemOwner'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">12</span>] = <span style="color:#CE9178;">'SourceSystemId'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">13</span>] = <span style="color:#CE9178;">'ReplaceLastEffectiveEndDate'</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The HDL engine reads this array and writes the following row to the .dat file:</p>

<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Generated .dat header row (ElementEntry)</div>
<div style="background:#1E1E1E;border-radius:8px;padding:16px 20px;overflow-x:auto;margin:4px 0;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#D4622B;font-weight:700;">METADATA</span>|<span style="color:#D4622B;font-weight:700;">ElementEntry</span>|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|CreatorType|EffectiveEndDate|EntryType|MultipleEntryCount|SourceSystemOwner|SourceSystemId|ReplaceLastEffectiveEndDate</pre>
</div>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The Code — METADATA2 (ElementEntryValue Header)</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Same pattern. <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">METADATA2</code> array defines the columns for the ElementEntryValue block:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">    <span style="color:#57A64A;font-style:italic;">/* ================================================= */</span>
    <span style="color:#57A64A;font-style:italic;">/* METADATA2 — ElementEntryValue column definitions   */</span>
    <span style="color:#57A64A;font-style:italic;">/* ================================================= */</span>

    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">3</span>]  = <span style="color:#CE9178;">'LegislativeDataGroupName'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">4</span>]  = <span style="color:#CE9178;">'EffectiveStartDate'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">5</span>]  = <span style="color:#CE9178;">'ElementName'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">6</span>]  = <span style="color:#CE9178;">'AssignmentNumber'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">7</span>]  = <span style="color:#CE9178;">'InputValueName'</span>              <span style="color:#57A64A;font-style:italic;">/* ← changes per pass */</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">8</span>]  = <span style="color:#CE9178;">'EffectiveEndDate'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">9</span>]  = <span style="color:#CE9178;">'EntryType'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">10</span>] = <span style="color:#CE9178;">'MultipleEntryCount'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">11</span>] = <span style="color:#CE9178;">'ScreenEntryValue'</span>            <span style="color:#57A64A;font-style:italic;">/* ← the actual value */</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">12</span>] = <span style="color:#CE9178;">'"ElementEntryId(SourceSystemId)"'</span>  <span style="color:#57A64A;font-style:italic;">/* parent link */</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">13</span>] = <span style="color:#CE9178;">'SourceSystemOwner'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">14</span>] = <span style="color:#CE9178;">'SourceSystemId'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">15</span>] = <span style="color:#CE9178;">'ReplaceLastEffectiveEndDate'</span>

    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">METADATA1</span>, <span style="color:#B5CEA8;">METADATA2</span>
)</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">This generates the second header row in the .dat file:</p>

<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Generated .dat header row (ElementEntryValue)</div>
<div style="background:#1E1E1E;border-radius:8px;padding:16px 20px;overflow-x:auto;margin:4px 0;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#D4622B;font-weight:700;">METADATA</span>|<span style="color:#D4622B;font-weight:700;">ElementEntryValue</span>|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|<span style="color:#D4622B;font-weight:700;">InputValueName</span>|EffectiveEndDate|EntryType|MultipleEntryCount|<span style="color:#D4622B;font-weight:700;">ScreenEntryValue</span>|ElementEntryId(SSID)|SourceSystemOwner|SourceSystemId|ReplaceLastEffectiveEndDate</pre>
</div>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How METADATA Links to RETURN in Sections 7 and 8</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The column names in the METADATA arrays directly map to the <strong>named output variables</strong> in the formula's RETURN statement. Here's the connection:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* METADATA defines the column header: */</span>
<span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">5</span>] = <span style="color:#CE9178;">'ElementName'</span>

<span style="color:#57A64A;font-style:italic;">/* In the MAP block, the formula assigns the named variable: */</span>
<span style="color:#B5CEA8;">ElementName</span>  = <span style="color:#B5CEA8;">l_ElementName</span>              <span style="color:#57A64A;font-style:italic;">/* = 'Dental EE Deduction' */</span>

<span style="color:#57A64A;font-style:italic;">/* And includes it in the RETURN: */</span>
<span style="color:#fff;font-weight:700;">RETURN</span> ..., <span style="color:#B5CEA8;">ElementName</span>, ...

<span style="color:#57A64A;font-style:italic;">/* Result in .dat file:                                                */</span>
<span style="color:#57A64A;font-style:italic;">/* METADATA |ElementEntry|...|ElementName                    |...      */</span>
<span style="color:#57A64A;font-style:italic;">/* MERGE    |ElementEntry|...|Dental EE Deduction   |...      */</span>
<span style="color:#57A64A;font-style:italic;">/*                             ↑ matched by variable name             */</span></pre>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0 0 8px;font-size:14px;color:#3D3D5C;"><strong>The mapping rule:</strong></p>
<p style="margin:0;font-size:14px;color:#3D3D5C;">
<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">METADATA1[N]</code> defines column N header name for object 1 (ElementEntry)<br>
In the MAP block, you assign a variable with <strong>that exact same name</strong> and include it in the RETURN statement<br><br>
The HDL engine matches the RETURN variable name to the METADATA column name and writes the value into the correct position in the .dat file. The <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator</code> value (<code>'ElementEntry'</code> vs <code>'ElementEntryValue'</code>) tells the engine which METADATA block to use.
</p>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 6: MAP ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 6: OPERATION: MAP — The Core Transformation</div>

<p style="font-size:15px;margin-bottom:6px;color:#3D3D5C;">The reference vendor row used in all examples below:</p>

<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;padding:10px 16px;font-weight:700;font-size:13px;color:#fff;">Vendor Input Row</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;width:25%;">POSITION1</td>
<td style="padding:8px 14px;font-weight:600;width:30%;">SSN</td>
<td style="padding:8px 14px;font-family:monospace;">123-45-6789</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION2</td>
<td style="padding:8px 14px;font-weight:600;">Effective Date</td>
<td style="padding:8px 14px;font-family:monospace;">2024-01-15</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION3</td>
<td style="padding:8px 14px;font-weight:600;">Benefit Plan</td>
<td style="padding:8px 14px;font-family:monospace;">DENTAL01</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION4</td>
<td style="padding:8px 14px;font-weight:600;">Deduction Type</td>
<td style="padding:8px 14px;font-family:monospace;">PRE</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION5</td>
<td style="padding:8px 14px;font-weight:600;">Amount</td>
<td style="padding:8px 14px;font-family:monospace;">150.00</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION6</td>
<td style="padding:8px 14px;font-weight:600;">Period Type</td>
<td style="padding:8px 14px;font-family:monospace;">Monthly</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION7</td>
<td style="padding:8px 14px;font-weight:600;">Percentage</td>
<td style="padding:8px 14px;font-family:monospace;">5.5</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION8</td>
<td style="padding:8px 14px;font-weight:600;">Loan Number</td>
<td style="padding:8px 14px;font-family:monospace;">LN-001</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION11</td>
<td style="padding:8px 14px;font-weight:600;">Status</td>
<td style="padding:8px 14px;font-family:monospace;color:#8B8FA8;">(blank = Active)</td>
</tr>
</table>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">This is the heart of the formula. When the HDL engine reaches a source row, it calls <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">OPERATION = 'MAP'</code>. The formula receives the raw CSV data in POSITION1–11 and must return Oracle HDL attributes. Five steps run in sequence.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's what the formula needs to figure out for each row:</p>

<!-- VISUAL: What the formula needs to answer -->
<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Question</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Vendor Gives Us</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Oracle Needs</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Step</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;">What type of deduction?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">POSITION4 (Deduction Type)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">PRE / POST / LOAN / CU</td>
<td style="padding:8px 10px;font-weight:700;">Step 1</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;">Which Oracle Element?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">DENTAL01</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">Dental EE Deduction</td>
<td style="padding:8px 10px;font-weight:700;">Step 2</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;">Which employee?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">123-45-6789 (SSN)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">E12345 (Assignment#)</td>
<td style="padding:8px 10px;font-weight:700;">Step 3</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;">How many entries already exist?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">(doesn't know)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">MultipleEntryCount = 2</td>
<td style="padding:8px 10px;font-weight:700;">Step 4</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;">New or existing entry?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">(doesn't know)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">SourceSystemId for MERGE</td>
<td style="padding:8px 10px;font-weight:700;">Step 5</td>
</tr>
</tbody></table>

<!-- VISUAL: 5 Step pipeline -->
<div style="display:flex;gap:8px;margin:20px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 1<br><span style="font-weight:400;font-size:13px;">Element Type</span></div>
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 2<br><span style="font-weight:400;font-size:13px;">Element Lookup</span></div>
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 3<br><span style="font-weight:400;font-size:13px;">Person / Assignment</span></div>
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 4<br><span style="font-weight:400;font-size:13px;">MultipleEntryCount</span></div>
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 5<br><span style="font-weight:400;font-size:13px;">SourceSystemId</span></div>
</div>

<!-- STEP 1 -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 1: Read Input Values from POSITION Fields</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 1 reads: POSITION4, POSITION5, POSITION6, POSITION7, POSITION8</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;width:50%;color:#8B8FA8;">POSITION4 = <span style="color:#3D3D5C;font-weight:700;">PRE</span></td>
<td style="padding:6px 0;">→ l_DeductionType = <span style="color:#D4622B;font-weight:700;">'PRE'</span></td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION5 = <span style="color:#3D3D5C;font-weight:700;">150.00</span></td>
<td style="padding:6px 0;">→ l_Amount = <span style="color:#D4622B;font-weight:700;">'150.00'</span></td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION6 = <span style="color:#3D3D5C;font-weight:700;">Monthly</span></td>
<td style="padding:6px 0;">→ l_PeriodType = <span style="color:#D4622B;font-weight:700;">'Monthly'</span></td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION7 = <span style="color:#3D3D5C;font-weight:700;">5.5</span></td>
<td style="padding:6px 0;">→ l_Percentage = <span style="color:#D4622B;font-weight:700;">'5.5'</span></td>
</tr>
<tr style="font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION8 = <span style="color:#3D3D5C;font-weight:700;">LN-001</span></td>
<td style="padding:6px 0;">→ l_LoanNumber = <span style="color:#D4622B;font-weight:700;">'LN-001'</span></td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula reads the deduction type from POSITION4 and the amount from POSITION5. It also captures other input values (Period Type, Percentage, Loan Number) from their respective positions for later LINEREPEATNO passes:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Read the key fields from the vendor row */</span>
<span style="color:#B5CEA8;">l_DeductionType</span>    = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION4</span>)     <span style="color:#57A64A;font-style:italic;">/* 'PRE', 'POST', 'LOAN', 'CU' */</span>
<span style="color:#B5CEA8;">l_Amount</span>           = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION5</span>)     <span style="color:#57A64A;font-style:italic;">/* '150.00' */</span>
<span style="color:#B5CEA8;">l_PeriodType</span>       = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION6</span>)     <span style="color:#57A64A;font-style:italic;">/* 'Monthly' */</span>
<span style="color:#B5CEA8;">l_Percentage</span>       = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION7</span>)     <span style="color:#57A64A;font-style:italic;">/* '5.5' (PRE/POST only) */</span>
<span style="color:#B5CEA8;">l_LoanNumber</span>       = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION8</span>)     <span style="color:#57A64A;font-style:italic;">/* 'LN-001' (LOAN only) */</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After this step: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_DeductionType = 'PRE'</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_Amount = '150.00'</code></p>

<!-- STEP 2 -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 2: Resolve Element Name from Benefit Plan Code</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 2 reads: POSITION3 (benefit plan code)</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 0;font-family:monospace;color:#8B8FA8;width:40%;">POSITION3 = <span style="color:#3D3D5C;font-weight:700;">DENTAL01</span></td>
<td style="padding:8px 0;font-family:monospace;">→ Value Set lookup</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 0;color:#8B8FA8;"></td>
<td style="padding:8px 0;font-family:monospace;">→ l_ElementName = <span style="color:#D4622B;font-weight:700;">'Dental EE Deduction'</span></td>
</tr>
<tr>
<td style="padding:8px 0;color:#8B8FA8;"></td>
<td style="padding:8px 0;font-family:monospace;">→ l_InputValueName = <span style="color:#D4622B;font-weight:700;">'Amount'</span></td>
</tr>
</table>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The vendor uses its own benefit plan codes (DENTAL01, MEDICAL01, VISION01). Oracle doesn't know these codes. The formula passes the vendor code to two value sets that translate it into Oracle terms:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Step 2: Translate vendor plan code → Oracle Element Name */</span>

<span style="color:#B5CEA8;">L_VendorPayCode</span> = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION3</span>)
<span style="color:#57A64A;font-style:italic;">/* e.g. 'DENTAL01' */</span>

<span style="color:#57A64A;font-style:italic;">/* Value set 1: vendor code → Oracle Element Name */</span>
<span style="color:#B5CEA8;">l_ElementName</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_DEDUCTION_CODES'</span>,
    <span style="color:#CE9178;">'|=P_PAY_CODE='''</span> || <span style="color:#B5CEA8;">L_VendorPayCode</span> || <span style="color:#CE9178;">''''</span>)
<span style="color:#57A64A;font-style:italic;">/* 'DENTAL01' → 'Dental EE Deduction' */</span>

<span style="color:#57A64A;font-style:italic;">/* Value set 2: vendor code → Input Value Name */</span>
<span style="color:#B5CEA8;">l_InputValueName</span> = <span style="color:#DCDCAA;">INITCAP</span>(<span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_DEDUCTION_CODES_INPUT'</span>,
    <span style="color:#CE9178;">'|=P_PAY_CODE='''</span> || <span style="color:#B5CEA8;">L_VendorPayCode</span> || <span style="color:#CE9178;">''''</span>))
<span style="color:#57A64A;font-style:italic;">/* 'DENTAL01' → 'Amount' */</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">These are <strong>code-based</strong> lookups — the value set definition maps each vendor code to its Oracle element. No person data is involved, so no WSA caching is needed here.</p>

<!-- VISUAL: Translation flow -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;color:#fff;padding:10px 16px;font-weight:700;font-size:13px;">Value Set Translation</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<thead><tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-weight:700;color:#3D3D5C;">Vendor Code (POSITION3)</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-weight:700;color:#3D3D5C;">Oracle Element Name</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-weight:700;color:#3D3D5C;">Input Value Name</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-weight:700;">DENTAL01</td>
<td style="padding:6px 8px;color:#D4622B;font-weight:700;">Dental EE Deduction</td>
<td style="padding:6px 8px;">Amount</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-weight:700;">MEDICAL01</td>
<td style="padding:6px 8px;color:#D4622B;font-weight:700;">Medical EE Deduction</td>
<td style="padding:6px 8px;">Amount</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-family:monospace;font-weight:700;">VISION01</td>
<td style="padding:6px 8px;color:#D4622B;font-weight:700;">Vision EE Deduction</td>
<td style="padding:6px 8px;">Amount</td>
</tr>
</tbody></table>
<p style="margin:10px 0 0;font-size:13px;color:#8B8FA8;">This mapping is defined in the value set configuration — not in the formula code. Adding a new benefit plan just means adding a row to the value set.</p>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After Step 2: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_ElementName = 'Dental EE Deduction'</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_InputValueName = 'Amount'</code></p>

<!-- STEP 3 -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 3: Resolve Person & Assignment</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 3 reads: POSITION1 (SSN) + POSITION2 (Date)</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;width:50%;color:#8B8FA8;">POSITION1 = <span style="color:#3D3D5C;font-weight:700;">123-45-6789</span></td>
<td style="padding:6px 0;">→ GET_VALUE_SET → L_PersonNumber = <span style="color:#D4622B;font-weight:700;">'100045'</span></td>
</tr>
<tr style="font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION2 = <span style="color:#3D3D5C;font-weight:700;">2024-01-15</span></td>
<td style="padding:6px 0;">→ GET_VALUE_SET → l_AssignmentNumber = <span style="color:#D4622B;font-weight:700;">'E12345'</span></td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Oracle HDL doesn't understand SSN. It needs two things: <strong>Person Number</strong> and <strong>Assignment Number</strong>. Step 3 translates one into the other.</p>

<!-- VISUAL: Simple translation -->
<div style="margin:18px 0;padding:16px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;">
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:center;">
<div style="background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:10px 18px;text-align:center;">
<div style="font-size:13px;color:#D4622B;font-weight:700;letter-spacing:1px;">VENDOR FILE GIVES US</div>
<div style="font-family:monospace;font-size:14px;font-weight:700;color:#D4622B;margin-top:4px;">123-45-6789</div>
<div style="font-size:13px;color:#8B8FA8;">SSN (POSITION1)</div>
</div>
<div style="text-align:center;">
<div style="font-size:22px;color:#D4622B;">→</div>
<div style="font-size:13px;color:#8B8FA8;">Value Set<br>calls DB</div>
</div>
<div style="background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:10px 18px;text-align:center;">
<div style="font-size:13px;color:#D4622B;font-weight:700;letter-spacing:1px;">ORACLE HDL NEEDS</div>
<div style="font-family:monospace;font-size:14px;font-weight:700;color:#D4622B;margin-top:4px;">Person# 100045</div>
<div style="font-family:monospace;font-size:14px;font-weight:700;color:#D4622B;">Assignment# E12345</div>
</div>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Two value sets do this translation:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;font-weight:700;color:#D4622B;">XXVA_GET_PERSON_NUMBER</td>
<td style="padding:8px 10px;">Takes SSN + Date → returns Person Number (100045)</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;font-weight:700;color:#D4622B;">XXVA_GET_LATEST_ASSIGNMENT_NUMBER</td>
<td style="padding:8px 10px;">Takes SSN + Date → returns Assignment Number (E12345)</td>
</tr>
</tbody></table>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">That's the simple version. But there's a performance problem.</p>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Problem: Same SSN, Three Rows, Three Identical DB Calls</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">One employee can have multiple rows in the vendor file — one per benefit plan. If an employee has 3 benefit plans (Dental, Medical, Vision), the file has 3 rows with the <strong>same SSN</strong>. Without optimization, the formula calls the value set 3 times for the exact same SSN and gets the exact same answer 3 times.</p>

<!-- VISUAL: The waste -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#fff;padding:10px 16px;border-bottom:1px solid #DDD8D0;font-weight:700;font-size:13px;color:#D4622B;">Without caching — 3 rows, same SSN</div>
<div style="padding:14px 16px;background:#fff;font-size:13px;line-height:2;">
<strong>Row 1 (DENTAL01):</strong> SSN 123-45-6789 → <span style="color:#D4622B;">call DB</span> → Person# 100045 <span style="color:#2D8B6F;font-weight:700;">[OK]</span><br>
<strong>Row 2 (MEDICAL01):</strong> SSN 123-45-6789 → <span style="color:#D4622B;">call DB again</span> → Person# 100045 <span style="color:#D4622B;">← same SSN, wasted call</span><br>
<strong>Row 3 (VISION01):</strong> SSN 123-45-6789 → <span style="color:#D4622B;">call DB again</span> → Person# 100045 <span style="color:#D4622B;">← same SSN, wasted call</span>
</div>
</div>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Fix: Cache with WSA</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula uses WSA to remember the answer (explained in the WSA Deep Dive after Step 4). The logic is simple:</p>

<div style="display:flex;gap:12px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:220px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:14px;text-align:center;">
<div style="background:#D4622B;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;margin:0 auto 4px;box-shadow:0 2px 8px rgba(212,98,43,0.25);">1</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">Did I already look up this SSN?</div>
<div style="font-family:monospace;font-size:13px;color:#8B8FA8;margin-top:6px;">WSA_EXISTS('PER_123-45-6789_2024-01-15')</div>
</div>
<div style="flex:1;min-width:220px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:14px;text-align:center;">
<div style="background:#D4622B;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;margin:0 auto 4px;">2a</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">YES → Read from cache</div>
<div style="font-family:monospace;font-size:13px;color:#8B8FA8;margin-top:6px;">WSA_GET('PER_123-45-6789_2024-01-15', ' ')<br>→ 100045. Done. No DB call.</div>
</div>
<div style="flex:1;min-width:220px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:14px;text-align:center;">
<div style="background:#D4622B;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;margin:0 auto 4px;">2b</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">NO → Call DB, then save to cache</div>
<div style="font-family:monospace;font-size:13px;color:#8B8FA8;margin-top:6px;">GET_VALUE_SET(...) → 100045<br>WSA_SET('PER_123-45-6789_2024-01-15', 100045)</div>
</div>
</div>

<!-- VISUAL: After caching — 3 rows -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#fff;padding:10px 16px;border-bottom:1px solid #DDD8D0;font-weight:700;font-size:13px;color:#D4622B;">With WSA caching — same 3 rows, same SSN</div>
<div style="padding:14px 16px;background:#fff;font-size:13px;line-height:2;">
<strong>Row 1 (DENTAL01):</strong> WSA_EXISTS? <strong>NO</strong> → <span style="color:#D4622B;">call DB</span> → 100045 → <span style="color:#D4622B;">WSA_SET (save it)</span> <span style="color:#2D8B6F;font-weight:700;">[OK]</span><br>
<strong>Row 2 (MEDICAL01):</strong> WSA_EXISTS? <strong>YES</strong> → <span style="color:#D4622B;">WSA_GET → 100045. Zero DB calls.</span> <span style="color:#2D8B6F;font-weight:700;">[OK]</span><br>
<strong>Row 3 (VISION01):</strong> WSA_EXISTS? <strong>YES</strong> → <span style="color:#D4622B;">WSA_GET → 100045. Zero DB calls.</span> <span style="color:#2D8B6F;font-weight:700;">[OK]</span>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's what the actual code looks like:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Build a unique WSA key from SSN + Date */</span>
<span style="color:#57A64A;font-style:italic;">/* e.g. 'PER_123-45-6789_2024-01-15' */</span>

<span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">WSA_EXISTS</span>(<span style="color:#CE9178;">'PER_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* Cache hit — read stored values */</span>
    <span style="color:#B5CEA8;">L_PersonNumber</span>     = <span style="color:#DCDCAA;">WSA_GET</span>(<span style="color:#CE9178;">'PER_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#CE9178;">' '</span>)
    <span style="color:#B5CEA8;">l_AssignmentNumber</span> = <span style="color:#DCDCAA;">WSA_GET</span>(<span style="color:#CE9178;">'ASG_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#CE9178;">' '</span>)
)
<span style="color:#fff;font-weight:700;">ELSE</span>
(
    <span style="color:#57A64A;font-style:italic;">/* Cache miss — call value sets (hits DB) */</span>
    <span style="color:#B5CEA8;">l_AssignmentNumber</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_GET_LATEST_ASSIGNMENT_NUMBER'</span>, ...)
    <span style="color:#B5CEA8;">L_PersonNumber</span>     = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_GET_PERSON_NUMBER'</span>, ...)

    <span style="color:#57A64A;font-style:italic;">/* Save to WSA — next row with same SSN skips DB */</span>
    <span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#CE9178;">'PER_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#B5CEA8;">L_PersonNumber</span>)
    <span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#CE9178;">'ASG_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#B5CEA8;">l_AssignmentNumber</span>)
)</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After Step 3: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">L_PersonNumber = '100045'</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_AssignmentNumber = 'E12345'</code></p>

<!-- STEP 4 -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 4: MultipleEntryCount</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 4 uses: L_PersonNumber + l_ElementName + POSITION2 (Date)</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;width:50%;color:#8B8FA8;">Person <span style="color:#3D3D5C;font-weight:700;">100045</span> + Element <span style="color:#3D3D5C;font-weight:700;">Dental EE Deduction</span> + Date <span style="color:#3D3D5C;font-weight:700;">2024-01-15</span></td>
<td style="padding:6px 0;">→ l_MultipleEntryCount = <span style="color:#D4622B;font-weight:700;">1</span> (or 2, 3... if entries already exist)</td>
</tr>
</table>
</div>
</div>


<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">What Is It?</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">When the same person has multiple entries of the <strong>same element</strong> in the <strong>same payroll period</strong>, Oracle needs a sequence number to tell them apart. That number is MultipleEntryCount.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">When does this happen in the vendor interface? Each pay period, the vendor sends a new deduction file. If person 100045 already has a Dental EE Deduction entry from a previous load, and this batch sends another one (maybe a mid-period adjustment), the new entry needs a higher count.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">If you know SQL, it's this:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#DCDCAA;">ROW_NUMBER</span>() <span style="color:#fff;font-weight:700;">OVER</span> (<span style="color:#fff;font-weight:700;">PARTITION BY</span> <span style="color:#C8C8C8;">person</span>, <span style="color:#C8C8C8;">element</span>, <span style="color:#C8C8C8;">payroll_period</span>)  =  MultipleEntryCount</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's what it looks like in <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PAY_ELEMENT_ENTRIES_F</code> after multiple loads:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:6px 8px;">Person#</th>
<th style="padding:6px 8px;">Element</th>
<th style="padding:6px 8px;">EffectiveStartDate</th>
<th style="padding:6px 8px;">Amount</th>
<th style="padding:6px 8px;">MultipleEntryCount</th>
<th style="padding:6px 8px;">Source</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;">100045</td>
<td style="padding:6px 8px;">Dental EE Deduction</td>
<td style="padding:6px 8px;font-family:monospace;">2024-01-15</td>
<td style="padding:6px 8px;font-family:monospace;">$150.00</td>
<td style="padding:6px 8px;text-align:center;font-weight:800;font-size:18px;color:#D4622B;">1</td>
<td style="padding:6px 8px;font-size:13px;color:#8B8FA8;">January batch</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;">100045</td>
<td style="padding:6px 8px;">Dental EE Deduction</td>
<td style="padding:6px 8px;font-family:monospace;">2024-01-20</td>
<td style="padding:6px 8px;font-family:monospace;">$25.00</td>
<td style="padding:6px 8px;text-align:center;font-weight:800;font-size:18px;color:#D4622B;">2</td>
<td style="padding:6px 8px;font-size:13px;color:#8B8FA8;">Mid-period adjustment</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;">100045</td>
<td style="padding:6px 8px;font-weight:700;color:#D4622B;">Medical EE Deduction</td>
<td style="padding:6px 8px;font-family:monospace;">2024-01-15</td>
<td style="padding:6px 8px;font-family:monospace;">$200.00</td>
<td style="padding:6px 8px;text-align:center;font-weight:800;font-size:18px;color:#D4622B;">1</td>
<td style="padding:6px 8px;font-size:13px;color:#8B8FA8;">← different element, count resets to 1</td>
</tr>
</tbody></table>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The partition key is <strong>Person + Element + Payroll Period</strong>. Same person + same element = same group, count increments. Different element = new group, count resets to 1. If two entries in the same group get the <strong>same</strong> count, Oracle overwrites the first one — data is lost.</p>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Problem: Fast Formula Has No Memory</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">In PL/SQL, you'd do this in a loop. The counter variable lives across iterations:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">-- PL/SQL: variable persists across loop iterations</span>
<span style="color:#B5CEA8;">l_counter</span> := <span style="color:#DCDCAA;">0</span>;
<span style="color:#fff;font-weight:700;">FOR</span> <span style="color:#B5CEA8;">rec</span> <span style="color:#fff;font-weight:700;">IN</span> <span style="color:#C8C8C8;">cursor</span> <span style="color:#fff;font-weight:700;">LOOP</span>
    <span style="color:#B5CEA8;">l_counter</span> := <span style="color:#B5CEA8;">l_counter</span> + <span style="color:#DCDCAA;">1</span>;
    <span style="color:#57A64A;font-style:italic;">-- Row 1: l_counter = 1</span>
    <span style="color:#57A64A;font-style:italic;">-- Row 2: l_counter = 2  ← remembers what happened in Row 1</span>
<span style="color:#fff;font-weight:700;">END LOOP</span>;</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Fast Formula is <strong>not</strong> a loop. The HDL engine calls the formula once per row as a <strong>separate, independent invocation</strong>. All local variables are destroyed after each call. It's like calling a standalone function 10,000 times — each call starts from zero with no memory of the previous call.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">So the formula has to ask the database: <em>"What's the highest count that already exists?"</em> The value set runs something like this behind the scenes against <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PAY_ELEMENT_ENTRIES_F</code>:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">SELECT</span> <span style="color:#DCDCAA;">MAX</span>(<span style="color:#C8C8C8;">pee.MULTIPLE_ENTRY_COUNT</span>) 
<span style="color:#fff;font-weight:700;">FROM</span>   <span style="color:#C8C8C8;">PAY_ELEMENT_ENTRIES_F</span>  <span style="color:#B5CEA8;">pee</span>
      ,<span style="color:#C8C8C8;">PAY_ELEMENT_TYPES_F</span>    <span style="color:#B5CEA8;">pet</span>
      ,<span style="color:#C8C8C8;">PER_ALL_ASSIGNMENTS_M</span>  <span style="color:#B5CEA8;">paam</span>
<span style="color:#fff;font-weight:700;">WHERE</span>  <span style="color:#B5CEA8;">pee</span>.<span style="color:#C8C8C8;">ELEMENT_TYPE_ID</span>  = <span style="color:#B5CEA8;">pet</span>.<span style="color:#C8C8C8;">ELEMENT_TYPE_ID</span>
<span style="color:#fff;font-weight:700;">AND</span>    <span style="color:#B5CEA8;">pee</span>.<span style="color:#C8C8C8;">PERSON_ID</span>         = <span style="color:#B5CEA8;">paam</span>.<span style="color:#C8C8C8;">PERSON_ID</span>
<span style="color:#fff;font-weight:700;">AND</span>    <span style="color:#B5CEA8;">pet</span>.<span style="color:#C8C8C8;">ELEMENT_NAME</span>      = <span style="color:#CE9178;">'Dental EE Deduction'</span>
<span style="color:#fff;font-weight:700;">AND</span>    <span style="color:#B5CEA8;">paam</span>.<span style="color:#C8C8C8;">PERSON_NUMBER</span>    = <span style="color:#CE9178;">'100045'</span>
<span style="color:#fff;font-weight:700;">AND</span>    <span style="color:#CE9178;">'2024-10-15'</span> <span style="color:#fff;font-weight:700;">BETWEEN</span> <span style="color:#B5CEA8;">pee</span>.<span style="color:#C8C8C8;">EFFECTIVE_START_DATE</span> <span style="color:#fff;font-weight:700;">AND</span> <span style="color:#B5CEA8;">pee</span>.<span style="color:#C8C8C8;">EFFECTIVE_END_DATE</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">This works fine when each batch has only one row per person+element. But what if the batch has two?</p>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Bug: Two Rows Read the Same Stale MAX</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's what's already in <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PAY_ELEMENT_ENTRIES_F</code> from last month's load:</p>

<!-- EXISTING DATA IN TABLE -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">PAY_ELEMENT_ENTRIES_F — existing data in cloud</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<thead><tr style="background:#F5F3EF;">
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;font-weight:700;color:#D4622B;">ELEMENT_ENTRY_ID</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">PERSON_ID</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">ELEMENT_TYPE_ID</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">EFFECTIVE_START_DATE</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">MULTIPLE_ENTRY_COUNT</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">ENTRY_TYPE</th>
</tr></thead>
<tbody>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-family:monospace;">300000012345</td>
<td style="padding:8px 10px;font-family:monospace;">100045</td>
<td style="padding:8px 10px;font-family:monospace;">50001 <span style="color:#8B8FA8;font-size:13px;">(Dental EE Deduction)</span></td>
<td style="padding:8px 10px;font-family:monospace;">01-Oct-2024</td>
<td style="padding:8px 10px;font-weight:800;font-size:15px;color:#D4622B;text-align:center;">1</td>
<td style="padding:8px 10px;font-family:monospace;">E</td>
</tr>
</tbody></table>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Now our vendor batch has two new Dental EE Deduction rows for the same person. The formula runs <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">SELECT MAX(MULTIPLE_ENTRY_COUNT)</code> for each — but the problem is Row 5's INSERT hasn't reached the table yet when Row 8 queries it:</p>

<!-- RED: Without WSA -->
<div style="margin:18px 0;border-radius:10px;overflow:hidden;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);">
<div style="background:#C13B3B;padding:12px 20px;color:#fff;font-weight:800;font-size:15px;"><span style="background:#fff;color:#C13B3B;padding:2px 8px;border-radius:4px;font-size:13px;margin-right:6px;">FAIL</span> WITHOUT WSA</div>
<div style="padding:20px;background:#fff;">

<div style="font-weight:700;font-size:14px;color:#3D3D5C;margin-bottom:10px;">Row 5 processes — formula queries the table:</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">SELECT</span> <span style="color:#DCDCAA;">MAX</span>(<span style="color:#C8C8C8;">MULTIPLE_ENTRY_COUNT</span>) <span style="color:#fff;font-weight:700;">FROM</span> <span style="color:#C8C8C8;">PAY_ELEMENT_ENTRIES_F</span>
<span style="color:#fff;font-weight:700;">WHERE</span> PERSON_ID = <span style="color:#DCDCAA;">100045</span> <span style="color:#fff;font-weight:700;">AND</span> ELEMENT_TYPE_ID = <span style="color:#DCDCAA;">50001</span>  <span style="color:#57A64A;font-style:italic;">→ Returns 1</span></pre>
<p style="font-size:14px;margin:0 0 16px;">Formula assigns: 1 + 1 = <span style="background:#C13B3B;color:#fff;padding:3px 12px;border-radius:12px;font-weight:800;font-size:15px;">2</span>   <span style="color:#8B8FA8;font-size:13px;">← this row is still in the HDL batch, NOT yet inserted into PAY_ELEMENT_ENTRIES_F</span></p>

<div style="font-weight:700;font-size:14px;color:#3D3D5C;margin-bottom:10px;">Row 8 processes — formula queries the SAME table:</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">SELECT</span> <span style="color:#DCDCAA;">MAX</span>(<span style="color:#C8C8C8;">MULTIPLE_ENTRY_COUNT</span>) <span style="color:#fff;font-weight:700;">FROM</span> <span style="color:#C8C8C8;">PAY_ELEMENT_ENTRIES_F</span>
<span style="color:#fff;font-weight:700;">WHERE</span> PERSON_ID = <span style="color:#DCDCAA;">100045</span> <span style="color:#fff;font-weight:700;">AND</span> ELEMENT_TYPE_ID = <span style="color:#DCDCAA;">50001</span>  <span style="color:#57A64A;font-style:italic;">→ STILL returns 1!</span></pre>
<p style="font-size:14px;margin:0 0 16px;">Formula assigns: 1 + 1 = <span style="background:#C13B3B;color:#fff;padding:3px 12px;border-radius:12px;font-weight:800;font-size:15px;">2</span>   <span style="color:#C13B3B;font-size:13px;font-weight:700;">← SAME count as Row 5!</span></p>

<p style="font-size:14px;margin:0 0 12px;">What the generated .dat file looks like — both rows got the same count:</p>

<div style="border:1px solid #DDD8D0;border-radius:6px;overflow:hidden;">
<div style="background:#1B4965;color:#fff;padding:8px 14px;font-weight:700;font-size:12px;">ElementEntry.dat — FAIL output</div>
<div style="background:#1E1E1E;padding:8px 10px;">
<div style="font-size:12px;color:#8E8680;margin-bottom:8px;">Existing entry (already in Oracle):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:5px 10px;color:#8E8680;width:35%;">ElementName</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:5px 10px;color:#8B8FA8;">MultipleEntryCount</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">1</td>
</tr>
</table>

<div style="font-size:12px;color:#C13B3B;margin-bottom:8px;font-weight:700;">Row 5 output ($175.00):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:5px 10px;color:#8E8680;width:35%;">ElementName</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:5px 10px;color:#8B8FA8;">MultipleEntryCount</td><td style="padding:5px 10px;color:#C13B3B;font-family:monospace;font-weight:700;font-size:16px;">2</td>
</tr>
</table>

<div style="font-size:12px;color:#C13B3B;margin-bottom:8px;font-weight:700;">Row 8 output ($200.00) — SAME count!</div>
__DARK_0__
</div>
</div>

<div style="background:#FCF0F0;border:1px solid #DDD8D0;border-radius:8px;padding:12px 18px;text-align:center;margin-top:12px;">
<span style="font-size:15px;font-weight:800;color:#C13B3B;"><strong>BUG:</strong> Two rows in the .dat file with MultipleEntryCount = 2. When Oracle loads this file, Row 8 overwrites Row 5. $175.00 entry is lost.</span>
</div>

</div>
</div>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Fix: WSA Tracks What the Table Can't See Yet</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">WSA acts as an in-memory counter that survives between formula calls. Row 5 saves its assigned count to WSA. When Row 8 runs, it reads from WSA instead of querying the table:</p>

<!-- GREEN: With WSA -->
<div style="margin:18px 0;border-radius:10px;overflow:hidden;border:1px solid #D4622B;box-shadow:0 2px 8px rgba(212,98,43,0.1);">
<div style="background:#D4622B;padding:12px 20px;color:#fff;font-weight:800;font-size:15px;"><span style="background:#fff;color:#2D8B6F;padding:2px 8px;border-radius:4px;font-size:13px;margin-right:6px;">PASS</span> WITH WSA</div>
<div style="padding:20px;background:#fff;">

<table style="width:100%;border-collapse:collapse;font-size:12px;">
<thead><tr style="background:#F5F3EF;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;font-weight:700;">Row</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;font-weight:700;">WSA has data?</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Source of MAX</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Assigns</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Saves to WSA</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">Row 5</td>
<td style="padding:8px 10px;">NO</td>
<td style="padding:8px 10px;font-size:13px;">PAY_ELEMENT_ENTRIES_F → MAX = 1</td>
<td style="padding:8px 10px;"><span style="background:#D4622B;color:#fff;padding:3px 12px;border-radius:12px;font-weight:800;">2</span></td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;color:#D4622B;">WSA_SET(2)</td>
</tr>
<tr>
<td style="padding:8px 10px;font-weight:700;">Row 8</td>
<td style="padding:8px 10px;font-weight:700;color:#D4622B;">YES → 2</td>
<td style="padding:8px 10px;font-size:13px;color:#D4622B;">WSA memory (skips table)</td>
<td style="padding:8px 10px;"><span style="background:#D4622B;color:#fff;padding:3px 12px;border-radius:12px;font-weight:800;">3</span></td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;color:#D4622B;">WSA_SET(3)</td>
</tr>
</tbody></table>

<p style="font-size:14px;margin:12px 0 0;">What the .dat file looks like — each row gets a unique count:</p>

<div style="border:1px solid #DDD8D0;border-radius:6px;overflow:hidden;margin-top:8px;">
<div style="background:#1B4965;color:#fff;padding:8px 14px;font-weight:700;font-size:12px;">ElementEntry.dat — PASS output</div>
<div style="background:#1E1E1E;padding:8px 10px;">
<div style="font-size:12px;color:#8E8680;margin-bottom:8px;">Existing entry (already in Oracle):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:5px 10px;color:#8E8680;width:35%;">ElementName</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:5px 10px;color:#8B8FA8;">MultipleEntryCount</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">1</td>
</tr>
</table>

<div style="font-size:12px;color:#2D8B6F;margin-bottom:8px;font-weight:700;">Row 5 output ($175.00):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:5px 10px;color:#8E8680;width:35%;">ElementName</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:5px 10px;color:#8B8FA8;">MultipleEntryCount</td><td style="padding:5px 10px;color:#2D8B6F;font-family:monospace;font-weight:700;font-size:16px;">2 <span style="font-size:12px;font-weight:400;color:#2D8B6F;">[OK]</span></td>
</tr>
</table>

<div style="font-size:12px;color:#2D8B6F;margin-bottom:8px;font-weight:700;">Row 8 output ($200.00):</div>
__DARK_1__
</div>
</div>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-radius:8px;padding:12px 18px;text-align:center;margin-top:12px;">
<span style="font-size:15px;font-weight:800;color:#D4622B;"><span style="background:#2D8B6F;color:#fff;padding:2px 8px;border-radius:4px;font-size:12px;margin-right:4px;">PASS</span> Three unique MultipleEntryCount values (1, 2, 3) in the .dat file. Oracle loads all three entries successfully.</span>
</div>

</div>
</div>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Fast Formula Code</div>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Check: did a previous row already assign a count for this combo? */</span>
<span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">WSA_EXISTS</span>(<span style="color:#CE9178;">'MEC_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* YES — read last assigned count and add 1 */</span>
    <span style="color:#B5CEA8;">l_MultipleEntryCount</span> = <span style="color:#DCDCAA;">WSA_GET</span>(<span style="color:#CE9178;">'MEC_'</span> || ..., <span style="color:#DCDCAA;">0</span>) + <span style="color:#DCDCAA;">1</span>
)
<span style="color:#fff;font-weight:700;">ELSE</span>
(
    <span style="color:#57A64A;font-style:italic;">/* NO — first row for this combo. Ask the database. */</span>
    <span style="color:#B5CEA8;">l_db_max</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'MAX_MULTI_ENTRY_COUNT'</span>, ...)

    <span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">ISNULL</span>(<span style="color:#B5CEA8;">l_db_max</span>) = <span style="color:#CE9178;">'N'</span> <span style="color:#fff;font-weight:700;">THEN</span>
        <span style="color:#B5CEA8;">l_MultipleEntryCount</span> = <span style="color:#DCDCAA;">1</span>              <span style="color:#57A64A;font-style:italic;">/* Nothing in cloud → start at 1 */</span>
    <span style="color:#fff;font-weight:700;">ELSE</span>
        <span style="color:#B5CEA8;">l_MultipleEntryCount</span> = <span style="color:#B5CEA8;">l_db_max</span> + <span style="color:#DCDCAA;">1</span>  <span style="color:#57A64A;font-style:italic;">/* Cloud has 1 → assign 2 */</span>
)

<span style="color:#57A64A;font-style:italic;">/* Save what we assigned — next row reads this instead of hitting DB */</span>
<span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#CE9178;">'MEC_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#B5CEA8;">l_MultipleEntryCount</span>)</pre>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#D4622B;"><strong>Summary in one line:</strong> WSA is a working storage area that persists across formula invocations — like a PL/SQL package variable. The formula writes the assigned count to WSA, so the next row with the same combo reads from memory instead of hitting a stale database. The formula writes the assigned count to WSA, so the next row with the same combo reads from memory instead of hitting a stale database.</p>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After Step 4: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_MultipleEntryCount = 2</code> (cloud had 1, so we assigned 1 + 1)</p>

<!-- ==================== WSA BRIDGE ==================== -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">WSA in This Formula — Connecting Step 3 and Step 4</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">You've now seen WSA used twice in the MAP block, but for <strong>two completely different reasons</strong>. Let's connect them before moving to Step 5.</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:15%;">Step</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:25%;">WSA Key</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:25%;">What It Stores</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:15%;">Why</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:20%;">What Breaks Without It</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">Step 3</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">PER_<SSN>_<Date><br>ASG_<SSN>_<Date></td>
<td style="padding:8px 10px;">Person Number<br>Assignment Number</td>
<td style="padding:8px 10px;font-weight:700;color:#D4622B;">Performance</td>
<td style="padding:8px 10px;font-size:13px;">Same SSN queried 3x instead of 1x. Slow but correct.</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-weight:700;">Step 4</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">MEC_<Person>_<Element>_<Date></td>
<td style="padding:8px 10px;">Last assigned MultipleEntryCount</td>
<td style="padding:8px 10px;font-weight:700;color:#C13B3B;">Correctness</td>
<td style="padding:8px 10px;font-size:13px;color:#C13B3B;font-weight:600;">Duplicate MULTIPLE_ENTRY_COUNT in PAY_ELEMENT_ENTRIES_F. Data lost.</td>
</tr>
</tbody></table>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">This is the key distinction:</p>

<div style="display:flex;gap:16px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:280px;border:1px solid #DDD8D0;border-left:4px solid #D4622B;border-radius:0 8px 8px 0;padding:16px;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#D4622B;margin-bottom:8px;">Step 3 WSA = Cache</div>
<p style="margin:0 0 6px;font-size:12px;">Removes WSA from Step 3 → formula still <strong>works correctly</strong></p>
<p style="margin:0;font-size:12px;">It just runs <strong>slower</strong> (3 DB calls instead of 1 per SSN group)</p>
</div>
<div style="flex:1;min-width:280px;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);border-radius:8px;padding:16px;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#C13B3B;margin-bottom:8px;">Step 4 WSA = Required for Correct Data</div>
<p style="margin:0 0 6px;font-size:12px;">Remove WSA from Step 4 → formula <strong>produces wrong output</strong></p>
<p style="margin:0;font-size:12px;">Duplicate counts → rows overwrite each other in PAY_ELEMENT_ENTRIES_F</p>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Both use the same WSA methods (<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">WSA_EXISTS</code>, <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">WSA_GET</code>, <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">WSA_SET</code>), same pattern (check → hit or miss → store), but different purposes. Step 3 is optional optimization. Step 4 is mandatory for data integrity.</p>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== WSA DEEP DIVE ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">WSA Deep Dive — Working Storage Area</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">You've now seen WSA used in Step 3 and Step 4. Let's go deeper into how it works, what this formula caches, and one critical deployment rule you can't skip.</p>

<!-- WHAT IS WSA -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">What Is WSA?</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">WSA (Working Storage Area) is, per Oracle documentation, <strong>a mechanism for storing global values across formulas</strong>. Local variables die after each formula invocation, but WSA values persist across calls within the same session. You write a value on Row 1, and you can read it back on Row 500. WSA names are <strong>case-independent</strong> — <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'PER_123'</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'per_123'</code> refer to the same item.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">In PL/SQL terms: WSA is a package-level associative array (<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">TABLE OF VARCHAR2 INDEX BY VARCHAR2</code>). It persists across function calls within the same session.</p>

<!-- THE API -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The API — Four Methods</div>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Method</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">PL/SQL Equivalent</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">What It Does</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;font-family:monospace;font-weight:700;color:#D4622B;white-space:nowrap;font-size:10px;">WSA_EXISTS(item [, type])</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">g_cache.EXISTS(key)</td>
<td style="padding:8px 10px;">Tests whether item exists in the storage area. Optional <code>type</code> parameter restricts to a specific data type (TEXT, NUMBER, DATE, TEXT_TEXT, TEXT_NUMBER, etc.)</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;font-family:monospace;font-weight:700;color:#D4622B;white-space:nowrap;font-size:10px;">WSA_GET(item, default-value)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">l_val := g_cache(key)</td>
<td style="padding:8px 10px;">Retrieves the stored value. If item doesn't exist, returns the <strong>default-value</strong> instead. The data type of default-value determines the expected data type.</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;font-family:monospace;font-weight:700;color:#D4622B;white-space:nowrap;font-size:10px;">WSA_SET(item, value)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">g_cache(key) := val</td>
<td style="padding:8px 10px;">Sets the value for item. Any existing item of the same name is <strong>overwritten</strong>.</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:4px 5px;font-family:monospace;font-weight:700;color:#D4622B;white-space:nowrap;font-size:10px;">WSA_DELETE([item])</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">g_cache.DELETE(key)</td>
<td style="padding:8px 10px;">Deletes item from storage. If no name specified, <strong>all storage area data is deleted</strong>. Not used in this vendor formula, but important for cleanup scenarios.</td>
</tr>
</tbody></table>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#3D3D5C;"><strong>Key detail from Oracle docs:</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">WSA_GET</code> always requires a <strong>default-value</strong> parameter. The formula always calls <code>WSA_EXISTS</code> first and only calls <code>WSA_GET</code> when the item is known to exist — so the default is never actually used, but it must still be provided. The data type of the default tells the engine what data type to expect.</p>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Every WSA usage in this formula follows the same pattern. You already saw it twice:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* THE PATTERN — same in Step 3, Step 4, and everywhere else */</span>

<span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">WSA_EXISTS</span>(<span style="color:#B5CEA8;">l_key</span>) <span style="color:#fff;font-weight:700;">THEN</span>            <span style="color:#57A64A;font-style:italic;">/* 1. Check memory */</span>
    <span style="color:#B5CEA8;">l_value</span> = <span style="color:#DCDCAA;">WSA_GET</span>(<span style="color:#B5CEA8;">l_key</span>, <span style="color:#CE9178;">' '</span>)    <span style="color:#57A64A;font-style:italic;">/* 2a. HIT  — read from memory (default never used) */</span>
<span style="color:#fff;font-weight:700;">ELSE</span>
    <span style="color:#B5CEA8;">l_value</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(...)      <span style="color:#57A64A;font-style:italic;">/* 2b. MISS — call the database */</span>
    <span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#B5CEA8;">l_key</span>, <span style="color:#B5CEA8;">l_value</span>)          <span style="color:#57A64A;font-style:italic;">/* 3.  SAVE — store for next row */</span></pre>

<!-- WHERE YOU ALREADY SAW THIS -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Where You Already Saw This Pattern</div>

<div style="display:flex;gap:16px;margin:18px 0;flex-wrap:wrap;">
<!-- STEP 3 RECAP -->
<div style="flex:1;min-width:300px;border:1px solid #DDD8D0;border-left:4px solid #D4622B;border-radius:0 8px 8px 0;padding:16px;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#D4622B;margin-bottom:10px;">Step 3 — Person & Assignment Lookup</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:8px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Key:</td>
<td style="padding:4px 0;font-family:monospace;">'PER_123-45-6789_2024-01-15'</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Stores:</td>
<td style="padding:4px 0;">Person Number (100045)</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">DB call saved:</td>
<td style="padding:4px 0;">GET_VALUE_SET('XXVA_GET_PERSON_NUMBER')</td>
</tr>
<tr>
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Purpose:</td>
<td style="padding:4px 0;font-weight:700;color:#D4622B;">Performance — same SSN in 3 rows, only 1 DB call</td>
</tr>
</table>
</div>
<!-- STEP 4 RECAP -->
<div style="flex:1;min-width:300px;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);border-radius:8px;padding:16px;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#C13B3B;margin-bottom:10px;">Step 4 — MultipleEntryCount</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:8px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Key:</td>
<td style="padding:4px 0;font-family:monospace;">'MEC_100045_Dental EE Deduction_2024-01-15'</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Stores:</td>
<td style="padding:4px 0;">Last assigned count (2, then 3, then 4...)</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">DB call saved:</td>
<td style="padding:4px 0;">GET_VALUE_SET('MAX_MULTI_ENTRY_COUNT')</td>
</tr>
<tr>
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Purpose:</td>
<td style="padding:4px 0;font-weight:700;color:#C13B3B;">Correctness — prevents duplicate MULTIPLE_ENTRY_COUNT</td>
</tr>
</table>
</div>
</div>

<!-- ALL WSA KEYS -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">All WSA Keys This Formula Uses</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Steps 3 and 4 are the two main ones, but the formula caches more. Here's the complete list:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">WSA Key</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Stores</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Used In</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Type</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">PER_<SSN>_<Date></td>
<td style="padding:8px 10px;">Person Number</td>
<td style="padding:8px 10px;font-weight:700;">Step 3</td>
<td style="padding:8px 10px;color:#D4622B;font-weight:600;">Performance</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">ASG_<SSN>_<Date></td>
<td style="padding:8px 10px;">Assignment Number</td>
<td style="padding:8px 10px;font-weight:700;">Step 3</td>
<td style="padding:8px 10px;color:#D4622B;font-weight:600;">Performance</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">MEC_<Person>_<Element>_<Date></td>
<td style="padding:8px 10px;">Last assigned MultipleEntryCount</td>
<td style="padding:8px 10px;font-weight:700;">Step 4</td>
<td style="padding:8px 10px;color:#C13B3B;font-weight:700;">Correctness</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">SSID_, SSO_, EEVID_, EEVO_</td>
<td style="padding:8px 10px;">SourceSystemId/Owner lookups</td>
<td style="padding:8px 10px;font-weight:700;">Step 5</td>
<td style="padding:8px 10px;color:#D4622B;font-weight:600;">Performance</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">HDR_<Person>_<Element>_<Date></td>
<td style="padding:8px 10px;">Flag: ElementEntry header already generated</td>
<td style="padding:8px 10px;font-weight:700;">Section 7</td>
<td style="padding:8px 10px;color:#C13B3B;font-weight:700;">Correctness</td>
</tr>
</tbody></table>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#D4622B;"><strong>Pattern:</strong> Performance keys (PER_, ASG_, SSID_) can be removed and the formula still works — just slower. Correctness keys (MEC_, HDR_) cannot be removed — the formula produces wrong data without them.</p>
</div>

<!-- TRACED EXAMPLE -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Traced Example: 3 Benefit Plan Rows, Same Employee</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Watch Step 3 and Step 4 WSA caching in action across three rows for SSN 123-45-6789:</p>

<!-- SOURCE ROWS REFERENCE -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;color:#fff;padding:12px 18px;font-weight:700;font-size:13px;">Vendor Input File — 3 rows for the same employee (SSN 123-45-6789)</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<thead><tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#3D3D5C;width:15%;">Row</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS1 (SSN)</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS2 (Date)</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS3 (Plan)</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS4 (Type)</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS5 (Amt)</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-weight:800;color:#D4622B;">Row 1</td>
<td style="padding:8px 14px;font-family:monospace;">123-45-6789</td>
<td style="padding:8px 14px;font-family:monospace;">2024-01-15</td>
<td style="padding:8px 14px;font-family:monospace;font-weight:700;">DENTAL01</td>
<td style="padding:8px 14px;font-family:monospace;">PRE</td>
<td style="padding:8px 14px;font-family:monospace;">150.00</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-weight:800;color:#D4622B;">Row 2</td>
<td style="padding:8px 14px;font-family:monospace;">123-45-6789</td>
<td style="padding:8px 14px;font-family:monospace;">2024-01-15</td>
<td style="padding:8px 14px;font-family:monospace;font-weight:700;">MEDICAL01</td>
<td style="padding:8px 14px;font-family:monospace;">PRE</td>
<td style="padding:8px 14px;font-family:monospace;">75.50</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 14px;font-weight:800;color:#D4622B;">Row 3</td>
<td style="padding:8px 14px;font-family:monospace;">123-45-6789</td>
<td style="padding:8px 14px;font-family:monospace;">2024-01-15</td>
<td style="padding:8px 14px;font-family:monospace;font-weight:700;">VISION01</td>
<td style="padding:8px 14px;font-family:monospace;">PRE</td>
<td style="padding:8px 14px;font-family:monospace;">12.30</td>
</tr>
</tbody></table>
<div style="padding:10px 18px;background:#FDF5ED;font-size:13px;color:#8B8FA8;">
Same SSN, same date — but <strong style="color:#3D3D5C;">different benefit plans</strong>. This is typical: one employee enrolled in Dental + Medical + Vision.
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Now let's trace what happens when the formula processes each row:</p>

<!-- ==================== ROW 1 ==================== -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:12px 18px;font-weight:800;font-size:12px;">ROW 1 — DENTAL01, PRE, $150.00</div>
<div style="padding:0;">

<!-- Step 3 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 3</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">Person & Assignment Lookup</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('PER_123-45-6789_2024-01-15')</td>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;width:15%;text-align:center;">MISS</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;" colspan="2">Call DB → Person# = <strong>100045</strong>, Asg# = <strong>E12345</strong></td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">WSA Save</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;color:#D4622B;" colspan="2">WSA_SET('PER_...', 100045)   WSA_SET('ASG_...', E12345)</td>
</tr>
</table>
</div>

<!-- Step 4 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 4</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">MultipleEntryCount</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('MEC_100045_Dental EE Deduction_2024')</td>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;width:15%;text-align:center;">MISS</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;" colspan="2">Call DB → MAX = NULL (no existing entry)</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Result</td>
<td style="padding:6px 8px;" colspan="2">MultipleEntryCount = <span style="background:#D4622B;color:#fff;padding:2px 10px;border-radius:10px;font-weight:800;">1</span>   → WSA_SET('MEC_...Dental...', 1)</td>
</tr>
</table>
</div>

<!-- Summary -->
<div style="padding:10px 18px;background:#FDF5ED;font-size:13px;color:#8B8FA8;">
DB calls: <strong style="color:#3D3D5C;">11</strong> — all cache misses (first time seeing this SSN)
</div>

</div>
</div>

<!-- ==================== ROW 2 ==================== -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:12px 18px;font-weight:800;font-size:12px;">ROW 2 — MEDICAL01, PRE, $75.50</div>
<div style="padding:0;">

<!-- Step 3 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 3</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">Person & Assignment Lookup</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('PER_123-45-6789_2024-01-15')</td>
<td style="padding:6px 8px;font-weight:700;color:#2D8B6F;width:15%;text-align:center;">HIT!</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;color:#2D8B6F;font-weight:600;" colspan="2">WSA_GET → Person# 100045, Asg# E12345 — zero DB calls</td>
</tr>
</table>
</div>

<!-- Step 4 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 4</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">MultipleEntryCount</span>
<span style="font-size:12px;color:#8B8FA8;font-style:italic;">— different element name = new WSA key</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('MEC_100045_<strong>Medical</strong> EE Deduction_2024')</td>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;width:15%;text-align:center;">MISS</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;" colspan="2">Call DB → MAX = NULL</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Result</td>
<td style="padding:6px 8px;" colspan="2">MultipleEntryCount = <span style="background:#D4622B;color:#fff;padding:2px 10px;border-radius:10px;font-weight:800;">1</span>   → WSA_SET('MEC_...Medical...', 1)</td>
</tr>
</table>
</div>

<!-- Summary -->
<div style="padding:10px 18px;background:#FDF5ED;font-size:13px;color:#8B8FA8;">
DB calls: <strong style="color:#3D3D5C;">4</strong> — Step 3 saved 2 calls (cache hit), Step 4 missed (different element)
</div>

</div>
</div>

<!-- ==================== ROW 3 ==================== -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:12px 18px;font-weight:800;font-size:12px;">ROW 3 — VISION01, PRE, $12.30</div>
<div style="padding:0;">

<!-- Step 3 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 3</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">Person & Assignment Lookup</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('PER_123-45-6789_2024-01-15')</td>
<td style="padding:6px 8px;font-weight:700;color:#2D8B6F;width:15%;text-align:center;">HIT!</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;color:#2D8B6F;font-weight:600;" colspan="2">WSA_GET → Person# 100045, Asg# E12345 — zero DB calls</td>
</tr>
</table>
</div>

<!-- Step 4 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 4</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">MultipleEntryCount</span>
<span style="font-size:12px;color:#8B8FA8;font-style:italic;">— yet another element = yet another WSA key</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('MEC_100045_<strong>Vision</strong> EE Deduction_2024')</td>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;width:15%;text-align:center;">MISS</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;" colspan="2">Call DB → MAX = NULL</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Result</td>
<td style="padding:6px 8px;" colspan="2">MultipleEntryCount = <span style="background:#D4622B;color:#fff;padding:2px 10px;border-radius:10px;font-weight:800;">1</span></td>
</tr>
</table>
</div>

<!-- Summary -->
<div style="padding:10px 18px;background:#FDF5ED;font-size:13px;color:#8B8FA8;">
DB calls: <strong style="color:#3D3D5C;">4</strong> — same pattern as Row 2
</div>

</div>
</div>

<!-- KEY INSIGHT -->
<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0 0 10px;font-size:14px;color:#3D3D5C;font-weight:700;">The Pattern:</p>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;width:20%;"></td>
<td style="padding:6px 0;font-weight:700;width:40%;">Step 3 (Person lookup)</td>
<td style="padding:6px 0;font-weight:700;">Step 4 (MEC)</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;">Row 1</td>
<td style="padding:6px 0;color:#C13B3B;">MISS — call DB</td>
<td style="padding:6px 0;color:#C13B3B;">MISS — call DB</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;">Row 2</td>
<td style="padding:6px 0;color:#2D8B6F;font-weight:700;">HIT — zero DB calls</td>
<td style="padding:6px 0;color:#C13B3B;">MISS — different element</td>
</tr>
<tr>
<td style="padding:6px 0;font-weight:700;">Row 3</td>
<td style="padding:6px 0;color:#2D8B6F;font-weight:700;">HIT — zero DB calls</td>
<td style="padding:6px 0;color:#C13B3B;">MISS — different element</td>
</tr>
</table>
<p style="margin:10px 0 0;font-size:13px;color:#8B8FA8;">Step 3 always hits after Row 1 (same SSN = same key). Step 4 always misses here because each row maps to a different element. Step 4 WSA becomes critical when the batch has multiple rows for the <strong>same person + same element</strong>.</p>
</div>

<!-- PERFORMANCE -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Performance at Scale</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">For 10,000 vendor rows where employees average 3 benefit plans each:</p>

<div style="display:flex;gap:16px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:250px;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);border-radius:8px;padding:16px;text-align:center;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#C13B3B;margin-bottom:8px;">WITHOUT WSA</div>
<div style="font-size:28px;font-weight:800;color:#C13B3B;letter-spacing:-0.5px;">~110,000</div>
<div style="font-size:13px;color:#8B8FA8;">value set calls (10K × 11 per row)</div>
</div>
<div style="flex:1;min-width:250px;border:1px solid #D4622B;box-shadow:0 2px 8px rgba(212,98,43,0.1);border-radius:8px;padding:16px;text-align:center;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#D4622B;margin-bottom:8px;">WITH WSA</div>
<div style="font-size:28px;font-weight:800;color:#D4622B;letter-spacing:-0.5px;">~40,000</div>
<div style="font-size:13px;color:#8B8FA8;">63% reduction — Step 3 caching saves ~7 calls per duplicate SSN</div>
</div>
</div>

<!-- SINGLE THREAD -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Critical Rule: Set Threads = 1</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">There's one deployment rule for WSA that you absolutely cannot skip:</p>

<div style="margin:18px 0;border-radius:10px;overflow:hidden;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);">
<div style="background:#C13B3B;padding:12px 20px;color:#fff;font-weight:800;font-size:15px;"><span style="background:#fff;color:#C13B3B;padding:2px 8px;border-radius:4px;font-size:13px;margin-right:6px;">WARNING</span> WSA memory is per-thread. Multi-thread = broken.</div>
<div style="padding:20px;background:#fff;">

<p style="font-size:14px;margin:0 0 12px;color:#3D3D5C;">If "Load Data from File" runs with 4 threads, each thread gets its <strong>own independent WSA</strong>:</p>

<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;width:25%;">Step 3 breaks:</td>
<td style="padding:6px 8px;">Thread 1 caches Person# for SSN 123. Thread 2 gets a different row for the same SSN — but Thread 2's WSA is empty. It calls the value set again. <span style="color:#8B8FA8;">(Wastes performance, but data is still correct.)</span></td>
</tr>
<tr>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;">Step 4 breaks:</td>
<td style="padding:6px 8px;color:#C13B3B;">Thread 1 assigns MultipleEntryCount = 2 and saves to its WSA. Thread 2 gets another row for the same person+element — but Thread 2's WSA is empty. It queries the DB, gets MAX = 1, assigns count = 2. <strong>Duplicate. Data lost.</strong></td>
</tr>
</table>

</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;"><strong>The fix:</strong></p>

<div style="margin:18px 0;padding:16px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;">
<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px;font-weight:600;">
<span style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;">My Client Groups</span>
<span style="color:#8B8FA8;">→</span>
<span style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;">Payroll</span>
<span style="color:#8B8FA8;">→</span>
<span style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;">Payroll Process Configuration</span>
<span style="color:#8B8FA8;">→</span>
<span style="background:#C13B3B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-weight:800;">Threads = 1</span>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Set thread count to 1 before running "Load Data from File." All rows process sequentially in one thread. WSA works as a true shared cache across every row.</p>

<hr style="border:none;border-top:1px dashed #DDD8D0;margin:30px 0;">
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 5: SourceSystemId Resolution</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 5 uses: l_AssignmentNumber + L_PersonNumber + l_ElementName + POSITION2</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="font-family:monospace;">
<td style="padding:6px 0;width:50%;color:#8B8FA8;">All resolved values from Steps 1–4</td>
<td style="padding:6px 0;">→ l_SourceSystemId = <span style="color:#D4622B;font-weight:700;">'HDL_XXVA_E12345_EE_100045_Dental EE Deduction_20240115'</span></td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Oracle HDL uses SourceSystemId as the MERGE key. If an entry already exists in cloud, the formula reuses its SourceSystemId (so HDL updates it). If not, it constructs one:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* For active employees — construct using PersonNumber */</span>
<span style="color:#CE9178;">'HDL_XXVA'</span> || <span style="color:#B5CEA8;">l_AssignmentNumber</span> || <span style="color:#CE9178;">'_EE_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>

<span style="color:#57A64A;font-style:italic;">/* For terminated employees (PersonNumber unavailable) — use SSN */</span>
<span style="color:#CE9178;">'HDL_XXVA'</span> || <span style="color:#B5CEA8;">l_AssignmentNumber</span> || <span style="color:#CE9178;">'_EE_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After all five steps, the formula has everything it needs: Element Name, Assignment Number, Person Number, MultipleEntryCount, SourceSystemId, and the dollar amount. Now it generates the HDL output rows (Sections 7 and 8).</p>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 7: LINEREPEATNO = 1 ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 7: LINEREPEATNO Passes — How Output Rows Are Generated</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">LINEREPEATNO = 1 generates the ElementEntry row</div>
<div style="padding:14px 16px;">
<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin-bottom:8px;">Vendor Input (what the formula receives):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;width:30%;">POSITION1</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;width:25%;">SSN</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">123-45-6789</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION2</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Date</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">2024-01-15</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION3</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Plan Code</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">DENTAL01</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION4</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Ded Type</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">PRE</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION5</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Amount</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">150.00</td>
</tr>
<tr style="background:#fff;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION11</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Status</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;color:#8B8FA8;">(blank = Active)</td>
</tr>
</table>

<div style="text-align:center;font-size:18px;color:#D4622B;font-weight:700;margin:10px 0;">↓ Formula transforms (Steps 1–5 + LINEREPEATNO=1) ↓</div>

<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin:10px 0 8px;">HDL .dat Output (ElementEntry):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;width:35%;">BusinessOperation</td>
<td style="padding:4px 5px;white-space:nowrap;color:#fff;font-weight:700;font-family:monospace;">MERGE</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">FileDiscriminator</td>
<td style="padding:4px 5px;white-space:nowrap;color:#CE9178;font-family:monospace;">ElementEntry</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">LegislativeDataGroupName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">570</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">EffectiveStartDate</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">2024/01/15</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">ElementName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">AssignmentNumber</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">E12345</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">CreatorType</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">H</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">EntryType</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">E</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">MultipleEntryCount</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">1</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">SourceSystemOwner</td>
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;font-family:monospace;">HDL_XXVA</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">SourceSystemId</td>
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;font-family:monospace;font-size:11px;">HDL_XXVA_E12345_EE_...</td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After the five MAP steps, the formula has all the values it needs. Now it generates the actual HDL output. Each vendor source row produces <strong>multiple</strong> HDL output rows — one ElementEntry header on pass 1, followed by one ElementEntryValue per input value on passes 2 through 7. LINEREPEATNO controls which one gets generated on each pass.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How LINEREPEAT Works</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The HDL engine calls the formula once per source row with <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEATNO = 1</code>. If the formula returns <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code>, the engine calls the formula <strong>again for the same row</strong> — this time with <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEATNO = 2</code>.</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* HDL engine processes one vendor source row: */</span>

<span style="color:#57A64A;font-style:italic;">/* Pass 1: LINEREPEATNO = 1 → ElementEntry header */</span>
<span style="color:#C8C8C8;">Formula outputs →</span>  <span style="color:#CE9178;">MERGE|ElementEntry|...|Dental EE Deduction|...</span>
<span style="color:#C8C8C8;">Formula returns →</span>  <span style="color:#fff;font-weight:700;">LINEREPEAT</span> = <span style="color:#CE9178;">'Y'</span>   <span style="color:#57A64A;font-style:italic;">← call me again</span>

<span style="color:#57A64A;font-style:italic;">/* Pass 2: LINEREPEATNO = 2 → EEV: Amount = 150.00 */</span>
<span style="color:#C8C8C8;">Formula outputs →</span>  <span style="color:#CE9178;">MERGE|ElementEntryValue|...|Amount|...|150.00</span>
<span style="color:#C8C8C8;">Formula returns →</span>  <span style="color:#fff;font-weight:700;">LINEREPEAT</span> = <span style="color:#CE9178;">'Y'</span>   <span style="color:#57A64A;font-style:italic;">← call me again (more input values)</span>

<span style="color:#57A64A;font-style:italic;">/* Pass 3: LINEREPEATNO = 3 → EEV: Period Type = Monthly */</span>
<span style="color:#C8C8C8;">Formula outputs →</span>  <span style="color:#CE9178;">MERGE|ElementEntryValue|...|Period Type|...|Monthly</span>
<span style="color:#C8C8C8;">Formula returns →</span>  <span style="color:#fff;font-weight:700;">LINEREPEAT</span> = <span style="color:#CE9178;">'Y'</span>   <span style="color:#57A64A;font-style:italic;">← call me again</span>

<span style="color:#57A64A;font-style:italic;">/* ... passes 4–6 for Loan Number, Total Owed, Percentage (if applicable) ... */</span>

<span style="color:#57A64A;font-style:italic;">/* Pass 7: LINEREPEATNO = 7 → EEV: Deduction Amount (last pass) */</span>
<span style="color:#C8C8C8;">Formula outputs →</span>  <span style="color:#CE9178;">MERGE|ElementEntryValue|...|Deduction Amount|...</span>
<span style="color:#C8C8C8;">Formula returns →</span>  <span style="color:#fff;font-weight:700;">LINEREPEAT</span> = <span style="color:#CE9178;">'N'</span>   <span style="color:#57A64A;font-style:italic;">← done, move to next source row</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">One source row → multiple output rows (1 ElementEntry + up to 6 ElementEntryValues). The HDL engine groups all ElementEntry rows together and all ElementEntryValue rows together in the final <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">.dat</code> file, separated by their METADATA header rows.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The .dat Output Structure</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The final .dat file has two blocks. Each block starts with a METADATA row that defines the columns, followed by the MERGE data rows:</p>

<!-- ELEMENT ENTRY VALUE BLOCK -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:10px 16px;font-weight:700;font-size:12px;">Block 1 — ElementEntryValue (generated by LINEREPEATNO = 2–7)</div>
<div style="overflow-x:auto;padding:8px 12px;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#8B8FA8;">A         B                C    D           E                  F               G               J                  K</span>
<span style="color:#D4622B;font-weight:700;">METADATA  ElementEntryVal  LDG  EffStart    ElementName        AssignmentNum   InputValueName  MultipleEntryCount ScreenEntryValue</span>
MERGE     ElementEntryVal  570  22-09-2019  Dental EE Deduct   123141402543    Amount          <span style="color:#D4622B;font-weight:700;">3</span>                  <strong>150.00</strong>
MERGE     ElementEntryVal  222  22-09-2019  Dental EE Deduct   123141402554    Amount          <span style="color:#D4622B;font-weight:700;">6</span>                  <strong>25.72</strong>
MERGE     ElementEntryVal  570  22-09-2019  Dental EE Deduct   123141402543    Amount          <span style="color:#D4622B;font-weight:700;">1</span>                  <strong>150.00</strong>
<span style="color:#8B8FA8;">...       more rows</span></pre>
</div>
</div>

<!-- ELEMENT ENTRY BLOCK -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:10px 16px;font-weight:700;font-size:12px;">Block 2 — ElementEntry (generated by LINEREPEATNO = 1)</div>
<div style="overflow-x:auto;padding:8px 12px;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#8B8FA8;">A         B             C    D           E                  F               G           I          J</span>
<span style="color:#D4622B;font-weight:700;">METADATA  ElementEntry  LDG  EffStart    ElementName        AssignmentNum   CreatorType EntryType  MultipleEntryCount</span>
MERGE     ElementEntry  570  22-09-2019  Dental EE Deduct   123141402543    H           E          <span style="color:#D4622B;font-weight:700;">3</span>
MERGE     ElementEntry  222  22-09-2019  Dental EE Deduct   123141402554    H           E          <span style="color:#D4622B;font-weight:700;">6</span>
<span style="color:#8B8FA8;">...       more rows</span></pre>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The key columns to notice: ElementEntry has <strong>CreatorType</strong> and <strong>EntryType</strong> but no dollar amount. ElementEntryValue has <strong>InputValueName</strong> (always "Amount") and <strong>ScreenEntryValue</strong> (the actual dollar amount like 150.00). Both carry <strong>MultipleEntryCount</strong> from Step 4.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">What LINEREPEATNO = 1 Generates</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">On the first pass, the formula checks POSITION11 (the STATUS column from the vendor file). This decides whether we're creating a new entry or end-dating an existing one:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:25%;">POSITION11</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">ElementEntry row generated</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:15%;">LINEREPEAT</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">Blank (Active)</td>
<td style="padding:8px 10px;">
<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">MERGE|ElementEntry|570|22-09-2019|Dental EE Deduction|123141402543|H||E|1</code><br>
<span style="font-size:13px;color:#8B8FA8;">EffectiveStartDate = POSITION2. No EndDate. CreatorType = H. EntryType = E.</span>
</td>
<td style="padding:8px 10px;font-weight:700;font-size:15px;">'Y'<br><span style="font-weight:400;font-size:13px;color:#8B8FA8;">→ needs pass 2</span></td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:8px 10px;font-weight:700;">C (Cancel)</td>
<td style="padding:8px 10px;">
<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">MERGE|ElementEntry|570|22-09-2019|Dental EE Deduction|123141402543|H|2019/09/22|E|1|...|Y</code><br>
<span style="font-size:13px;color:#8B8FA8;">Fetches original StartDate from cloud. Sets EndDate = cancellation date. Appends ReplaceLastEffectiveEndDate = Y.</span>
</td>
<td style="padding:8px 10px;font-weight:700;color:#C13B3B;font-size:15px;">'N'<br><span style="font-weight:400;font-size:13px;color:#8B8FA8;">→ no detail needed</span></td>
</tr>
</tbody></table>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How the Code Actually Writes the ElementEntry Row</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula does <strong>not</strong> use positional output variables like <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">HDL_LINE1_N</code>. Instead, it assigns values to <strong>named output variables</strong> that match the METADATA column names. Then an explicit <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">RETURN</code> statement tells the HDL engine which variables to pick up and in what order.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's the Active path (POSITION11 is blank):</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">IF</span> <span style="color:#C8C8C8;">LINEREPEATNO</span> = <span style="color:#B5CEA8;">1</span> <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* ======================================== */</span>
    <span style="color:#57A64A;font-style:italic;">/* ACTIVE entry — create new ElementEntry   */</span>
    <span style="color:#57A64A;font-style:italic;">/* ======================================== */</span>

    <span style="color:#B5CEA8;">FileName</span>                    = <span style="color:#CE9178;">'ElementEntry'</span>
    <span style="color:#B5CEA8;">BusinessOperation</span>           = <span style="color:#CE9178;">'MERGE'</span>
    <span style="color:#B5CEA8;">FileDiscriminator</span>           = <span style="color:#CE9178;">'ElementEntry'</span>
    <span style="color:#B5CEA8;">LegislativeDataGroupName</span>    = <span style="color:#B5CEA8;">l_LegislativeDataGroupName</span>
    <span style="color:#B5CEA8;">AssignmentNumber</span>            = <span style="color:#B5CEA8;">l_AssignmentNumber</span>
    <span style="color:#B5CEA8;">ElementName</span>                 = <span style="color:#B5CEA8;">l_ElementName</span>
    <span style="color:#B5CEA8;">EffectiveStartDate</span>          = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION2</span>),<span style="color:#CE9178;">'YYYY/MM/DD'</span>),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
    <span style="color:#B5CEA8;">EntryType</span>                   = <span style="color:#B5CEA8;">l_entry_type</span>
    <span style="color:#B5CEA8;">CreatorType</span>                 = <span style="color:#B5CEA8;">l_CreatorType</span>
    <span style="color:#B5CEA8;">SourceSystemOwner</span>           = <span style="color:#B5CEA8;">l_SourceSystemOwner</span>
    <span style="color:#B5CEA8;">SourceSystemId</span>              = <span style="color:#B5CEA8;">l_SourceSystemId</span>
    <span style="color:#B5CEA8;">LINEREPEAT</span>                  = <span style="color:#CE9178;">'Y'</span>             <span style="color:#57A64A;font-style:italic;">/* ← call me again for ElementEntryValue */</span>

    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">BusinessOperation</span>, <span style="color:#B5CEA8;">FileName</span>, <span style="color:#B5CEA8;">FileDiscriminator</span>,
           <span style="color:#B5CEA8;">CreatorType</span>, <span style="color:#B5CEA8;">EffectiveStartDate</span>, <span style="color:#B5CEA8;">ElementName</span>,
           <span style="color:#B5CEA8;">LegislativeDataGroupName</span>, <span style="color:#B5CEA8;">EntryType</span>, <span style="color:#B5CEA8;">AssignmentNumber</span>,
           <span style="color:#B5CEA8;">SourceSystemOwner</span>, <span style="color:#B5CEA8;">SourceSystemId</span>,
           <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#C8C8C8;">LINEREPEATNO</span>
)</pre>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-left:4px solid #D4622B;padding:14px 18px;margin:18px 0;border-radius:0 6px 6px 0;">
<p style="margin:0;font-size:14px;color:#3D3D5C;"><strong>How the RETURN works:</strong> The variable names in the RETURN statement must match the METADATA column names exactly. The HDL engine maps each returned variable to its corresponding METADATA position and writes the pipe-delimited row in that order. <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileName</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator</code> go to positions [1] and [2]. The rest map by name to the METADATA array you defined in Section 5.</p>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">For a <strong>Cancel</strong> row (POSITION11 = 'C'), the formula fetches the original start date from the cloud, sets an end date, and returns <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'N'</code> (no pass 2 needed — you don't need an ElementEntryValue for a cancellation):</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">IF</span> (<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION11</span>) = <span style="color:#CE9178;">'C'</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* Fetch the original start date from cloud */</span>
    <span style="color:#B5CEA8;">l_Effective_Start_Date</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_GET_EE_START_DATE'</span>, ...)

    <span style="color:#57A64A;font-style:italic;">/* Same named variables, but with end date + replace flag */</span>
    <span style="color:#B5CEA8;">FileName</span>                    = <span style="color:#CE9178;">'ElementEntry'</span>
    <span style="color:#B5CEA8;">BusinessOperation</span>           = <span style="color:#CE9178;">'MERGE'</span>
    <span style="color:#B5CEA8;">FileDiscriminator</span>           = <span style="color:#CE9178;">'ElementEntry'</span>
    <span style="color:#B5CEA8;">EffectiveStartDate</span>          = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#B5CEA8;">l_Effective_Start_Date</span>,...),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
    <span style="color:#B5CEA8;">EffectiveEndDate</span>            = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION2</span>),...),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
    <span style="color:#B5CEA8;">ReplaceLastEffectiveEndDate</span> = <span style="color:#CE9178;">'Y'</span>
    <span style="color:#B5CEA8;">LINEREPEAT</span>                  = <span style="color:#CE9178;">'N'</span>              <span style="color:#57A64A;font-style:italic;">/* ← no pass 2 for cancel */</span>
    <span style="color:#57A64A;font-style:italic;">/* ...same other variables as Active... */</span>

    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">BusinessOperation</span>, <span style="color:#B5CEA8;">FileName</span>, <span style="color:#B5CEA8;">FileDiscriminator</span>,
           <span style="color:#B5CEA8;">CreatorType</span>, <span style="color:#B5CEA8;">EffectiveStartDate</span>, <span style="color:#B5CEA8;">EffectiveEndDate</span>,
           <span style="color:#B5CEA8;">ElementName</span>, <span style="color:#B5CEA8;">LegislativeDataGroupName</span>, <span style="color:#B5CEA8;">EntryType</span>,
           <span style="color:#B5CEA8;">AssignmentNumber</span>, <span style="color:#B5CEA8;">SourceSystemOwner</span>, <span style="color:#B5CEA8;">SourceSystemId</span>,
           <span style="color:#B5CEA8;">ReplaceLastEffectiveEndDate</span>,
           <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#C8C8C8;">LINEREPEATNO</span>
)</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Notice the Cancel RETURN includes <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">EffectiveEndDate</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ReplaceLastEffectiveEndDate</code> — both absent from the Active RETURN.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Duplicate Header Prevention (WSA)</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">One person can have multiple vendor rows (Dental, Medical, Vision) that all map to different elements. Each element needs exactly one ElementEntry row. But if two vendor rows map to the <strong>same</strong> element, the formula must not generate a duplicate header. It checks WSA:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">WSA_EXISTS</span>(<span style="color:#CE9178;">'HDR_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* Header already generated for this combo — skip to pass 2 */</span>
    <span style="color:#C8C8C8;">LINEREPEAT</span> = <span style="color:#CE9178;">'Y'</span>
    <span style="color:#fff;font-weight:700;">RETURN</span>
)
<span style="color:#57A64A;font-style:italic;">/* First time for this combo — generate header, then mark in WSA */</span>
<span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#CE9178;">'HDR_'</span> || ..., <span style="color:#B5CEA8;">1</span>)</pre>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-left:4px solid #C13B3B;padding:14px 18px;margin:18px 0;border-radius:0 6px 6px 0;">
<p style="margin:0 0 8px;font-size:14px;color:#C13B3B;font-weight:700;">Watch out: ISNULL is inverted</p>
<p style="margin:0;font-size:14px;color:#3D3D5C;">The formula checks <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ISNULL(l_ElementName) = 'N'</code> before generating anything. In Fast Formula, <code>'N'</code> means the value IS null (not found). If the vendor code didn't map to any element, the formula skips the row silently.</p>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 8: LINEREPEATNO = 2 ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 8: LINEREPEATNO = 2–7 — ElementEntryValue Rows</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">LINEREPEATNO = 2–7 generates ElementEntryValue rows</div>
<div style="padding:14px 16px;">
<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin-bottom:8px;">Same Vendor Input Row → multiple ElementEntryValue outputs (one per input value):</div>

<div style="text-align:center;font-size:18px;color:#D4622B;font-weight:700;margin:10px 0;">↓ Each pass loads a different InputValueName ↓</div>

<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin:10px 0 8px;">Pass 2 — ElementEntryValue (Amount):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;width:35%;">InputValueName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">Amount</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">ScreenEntryValue</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">150.00</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">ElementEntryId(SSID)</td>
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;font-family:monospace;font-size:11px;">HDL_XXVA_E12345_EE_... (links to parent ElementEntry)</td>
</tr>
</table>

<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin:10px 0 8px;">Pass 3 — ElementEntryValue (Period Type):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;width:35%;">InputValueName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">Period Type</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">ScreenEntryValue</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">Monthly</td>
</tr>
</table>

<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin:10px 0 8px;">Pass 6 — ElementEntryValue (Percentage):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;width:35%;">InputValueName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">Percentage</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">ScreenEntryValue</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">5.5</td>
</tr>
</table>

<div style="background:#F5F3EF;border-radius:6px;padding:8px 10px;font-size:13px;color:#8B8FA8;">Passes 4, 5, 7 skipped — PRE type doesn't use Loan Number, Total Owed, or Deduction Amount. The formula returns <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code> with no output data on those passes.</div>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Passes 2 through 7 each generate one ElementEntryValue row. Each pass loads a different input value. The deduction type (POSITION4) controls which passes produce output and which ones skip.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">What LINEREPEATNO = 2 Generates</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Each ElementEntryValue pass sets <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">InputValueName</code> to a different value and loads the corresponding data into <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ScreenEntryValue</code>:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Column</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Value</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Source</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">LINEREPEATNO</td>
<td style="padding:8px 10px;font-family:monospace;">InputValueName</td>
<td style="padding:8px 10px;">ScreenEntryValue source</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">2</td>
<td style="padding:8px 10px;font-family:monospace;">Amount</td>
<td style="padding:8px 10px;font-size:13px;">l_Amount (POSITION5) = 150.00</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">3</td>
<td style="padding:8px 10px;font-family:monospace;">Period Type</td>
<td style="padding:8px 10px;font-size:13px;">l_PeriodType (POSITION6) = Monthly</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">4</td>
<td style="padding:8px 10px;font-family:monospace;">Loan Number</td>
<td style="padding:8px 10px;font-size:13px;">POSITION8 — LOAN type only</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">5</td>
<td style="padding:8px 10px;font-family:monospace;">Total Owed</td>
<td style="padding:8px 10px;font-size:13px;">l_TotalOwed — LOAN type only</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">6</td>
<td style="padding:8px 10px;font-family:monospace;">Percentage</td>
<td style="padding:8px 10px;font-size:13px;">l_Percentage (POSITION7) — PRE/POST type only</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-family:monospace;">7</td>
<td style="padding:8px 10px;font-family:monospace;">Deduction Amount</td>
<td style="padding:8px 10px;font-size:13px;">l_DeductionAmount — CU type only</td>
</tr>
</tbody></table>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How the Code Actually Writes the ElementEntryValue Row</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Each pass from 2 to 7 follows the same structure. The key difference is the skip logic: each pass checks POSITION4 (deduction type) to decide whether to generate output or just return <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code> with no data (effectively skipping to the next pass). Same pattern — named output variables + explicit RETURN. But now <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator = 'ElementEntryValue'</code> (not 'ElementEntry'), and the RETURN includes <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">InputValueName</code>, <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ScreenEntryValue</code>, and the parent link <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">"ElementEntryId(SourceSystemId)"</code>.</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">ELSE IF</span> (<span style="color:#C8C8C8;">LINEREPEATNO</span> = <span style="color:#B5CEA8;">2</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#B5CEA8;">l_InputValueName</span> = <span style="color:#CE9178;">'Amount'</span>

    <span style="color:#57A64A;font-style:italic;">/* Look up ElementEntryValue SourceSystemId from cloud (or construct new one) */</span>
    <span style="color:#B5CEA8;">l_EEV_SourceSystemId</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(
        <span style="color:#CE9178;">'XXVA_GET_EEV_SOURCE_SYSTEM_ID'</span>, ...)
    <span style="color:#B5CEA8;">l_EEV_SourceSystemOwner</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(
        <span style="color:#CE9178;">'XXVA_GET_EEV_SOURCE_SYSTEM_OWNER'</span>, ...)

    <span style="color:#57A64A;font-style:italic;">/* If no existing SSID found, construct a new one */</span>
    <span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">ISNULL</span>(<span style="color:#B5CEA8;">l_EEV_SourceSystemId</span>) = <span style="color:#CE9178;">'N'</span> <span style="color:#fff;font-weight:700;">THEN</span>
    (
        <span style="color:#B5CEA8;">l_EEV_SourceSystemId</span> = <span style="color:#CE9178;">'HDL_XXVA'</span> || <span style="color:#B5CEA8;">l_AssignmentNumber</span>
            || <span style="color:#CE9178;">'_EEV_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span>
            || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span>
            || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_InputValueName</span>
            || <span style="color:#CE9178;">'_'</span> || <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION2</span>),...),<span style="color:#CE9178;">'YYYYMMDD'</span>)
    )

    <span style="color:#57A64A;font-style:italic;">/* ============================================= */</span>
    <span style="color:#57A64A;font-style:italic;">/* Set the output variables for ElementEntryValue */</span>
    <span style="color:#57A64A;font-style:italic;">/* ============================================= */</span>

    <span style="color:#B5CEA8;">FileName</span>                          = <span style="color:#CE9178;">'ElementEntry'</span>        <span style="color:#57A64A;font-style:italic;">/* always ElementEntry */</span>
    <span style="color:#B5CEA8;">BusinessOperation</span>                 = <span style="color:#CE9178;">'MERGE'</span>
    <span style="color:#B5CEA8;">FileDiscriminator</span>                 = <span style="color:#CE9178;">'ElementEntryValue'</span>   <span style="color:#57A64A;font-style:italic;">/* ← THIS is the key difference */</span>
    <span style="color:#B5CEA8;">LegislativeDataGroupName</span>          = <span style="color:#B5CEA8;">l_LegislativeDataGroupName</span>
    <span style="color:#B5CEA8;">AssignmentNumber</span>                  = <span style="color:#B5CEA8;">l_AssignmentNumber</span>
    <span style="color:#B5CEA8;">ElementName</span>                       = <span style="color:#B5CEA8;">l_ElementName</span>
    <span style="color:#B5CEA8;">EntryType</span>                         = <span style="color:#B5CEA8;">l_entry_type</span>
    <span style="color:#B5CEA8;">EffectiveStartDate</span>                = <span style="color:#DCDCAA;">TO_CHAR</span>(...)
    <span style="color:#CE9178;">"ElementEntryId(SourceSystemId)"</span>  = <span style="color:#B5CEA8;">l_SourceSystemId</span>      <span style="color:#57A64A;font-style:italic;">/* ← links to parent ElementEntry */</span>
    <span style="color:#B5CEA8;">SourceSystemId</span>                    = <span style="color:#B5CEA8;">l_EEV_SourceSystemId</span>  <span style="color:#57A64A;font-style:italic;">/* ← EEV's own SSID */</span>
    <span style="color:#B5CEA8;">SourceSystemOwner</span>                 = <span style="color:#B5CEA8;">l_EEV_SourceSystemOwner</span>
    <span style="color:#B5CEA8;">InputValueName</span>                    = <span style="color:#B5CEA8;">l_InputValueName</span>      <span style="color:#57A64A;font-style:italic;">/* 'Amount' */</span>
    <span style="color:#B5CEA8;">ScreenEntryValue</span>                  = <span style="color:#DCDCAA;">To_Char</span>(<span style="color:#DCDCAA;">TO_NUM</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#B5CEA8;">l_Amount</span>)))
    <span style="color:#B5CEA8;">LINEREPEAT</span>                        = <span style="color:#CE9178;">'Y'</span>                  <span style="color:#57A64A;font-style:italic;">/* more passes to come (pass 7 returns 'N') */</span>

    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">BusinessOperation</span>, <span style="color:#B5CEA8;">FileName</span>, <span style="color:#B5CEA8;">FileDiscriminator</span>,
           <span style="color:#B5CEA8;">AssignmentNumber</span>, <span style="color:#B5CEA8;">EffectiveStartDate</span>, <span style="color:#B5CEA8;">ElementName</span>,
           <span style="color:#B5CEA8;">EntryType</span>, <span style="color:#B5CEA8;">LegislativeDataGroupName</span>,
           <span style="color:#CE9178;">"ElementEntryId(SourceSystemId)"</span>,
           <span style="color:#B5CEA8;">InputValueName</span>, <span style="color:#B5CEA8;">ScreenEntryValue</span>,
           <span style="color:#B5CEA8;">SourceSystemOwner</span>, <span style="color:#B5CEA8;">SourceSystemId</span>,
           <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#C8C8C8;">LINEREPEATNO</span>
)</pre>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-left:4px solid #D4622B;padding:14px 18px;margin:18px 0;border-radius:0 6px 6px 0;">
<p style="margin:0 0 8px;font-size:14px;color:#3D3D5C;"><strong>Three things to notice:</strong></p>
<p style="margin:0;font-size:14px;color:#3D3D5C;">
<strong>1.</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileName</code> is still <code>'ElementEntry'</code> — NOT <code>'ElementEntryValue'</code>. Only the <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator</code> changes to <code>'ElementEntryValue'</code>. This is how HDL knows the row goes into the ElementEntryValue block of the .dat file.<br><br>
<strong>2.</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">"ElementEntryId(SourceSystemId)"</code> is set to the <strong>ElementEntry's</strong> SourceSystemId (<code>l_SourceSystemId</code>). This is the parent-child link. The variable name contains parentheses, so it must be double-quoted in the formula code.<br><br>
<strong>3.</strong> The ElementEntryValue has its <strong>own</strong> SourceSystemId (<code>l_EEV_SourceSystemId</code>), different from the parent ElementEntry's. The formula first tries to find an existing one from the cloud via value set. If not found (<code>ISNULL = 'N'</code>), it constructs one with the pattern: <code>HDL_XXVA + AssignmentNumber + _EEV_ + PersonNumber + _ElementName + _InputValueName + _Date</code>.
</p>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The Parent-Child Link</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The ElementEntryValue row must reference its parent ElementEntry row. HDL uses SourceSystemId to link them:</p>

<div style="margin:18px 0;padding:20px;border:1px solid #DDD8D0;border-radius:10px;background:#fff;">
<div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
<div style="background:#fff;border:1px solid #DDD8D0;border-top:3px solid #D4622B;border-radius:8px;padding:14px 18px;text-align:center;min-width:250px;">
<div style="font-weight:700;font-size:14px;margin-bottom:6px;">ElementEntry (Pass 1)</div>
<div style="font-family:monospace;font-size:13px;color:#3D3D5C;">SourceSystemId = <span style="color:#D4622B;font-weight:700;">HDL_XXVA_E12345_EE_...</span></div>
</div>
<div style="font-size:24px;color:#D4622B;font-weight:700;">→</div>
<div style="background:#fff;border:1px solid #DDD8D0;border-top:3px solid #D4622B;border-radius:8px;padding:14px 18px;text-align:center;min-width:280px;">
<div style="font-weight:700;font-size:14px;margin-bottom:6px;">ElementEntryValue (Pass 2)</div>
<div style="font-family:monospace;font-size:13px;color:#3D3D5C;">ElementEntryId(SSID) = <span style="color:#D4622B;font-weight:700;">HDL_XXVA_E12345_EE_...</span></div>
<div style="font-family:monospace;font-size:13px;color:#8B8FA8;margin-top:4px;">SourceSystemId = HDL_XXVA_E12345_EEV_...</div>
</div>
</div>
<p style="margin:12px 0 0;font-size:13px;color:#8B8FA8;">The ElementEntryValue's <code>ElementEntryId(SourceSystemId)</code> matches the ElementEntry's <code>SourceSystemId</code>. This is how HDL knows which entry this value belongs to.</p>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The RTRIM Trick for Clean Numbers</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">the vendor sends amounts like <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">150.00</code>, but Oracle elements expect clean numbers. The formula strips trailing zeros:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#DCDCAA;">RTRIM</span>(<span style="color:#DCDCAA;">RTRIM</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#B5CEA8;">l_Amount</span>), <span style="color:#CE9178;">'0'</span>), <span style="color:#CE9178;">'.'</span>)

<span style="color:#57A64A;font-style:italic;">/* 150.00 → 150 | 75.50 → 75.5 | 12.30 → 12.3 | 150.00 → 150.00 */</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The inner RTRIM strips trailing zeros. The outer RTRIM strips the decimal point if nothing is left after it.</p>


<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== END-TO-END FLOW ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">End-to-End: One Vendor Row Through the Formula</div>

<div style="background:#fff;border:1px solid #DDD8D0;border-radius:10px;padding:20px;margin:18px 0;">

<p style="font-size:14px;margin:0 0 12px;"><strong>Vendor CSV Row:</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">123-45-6789,2024-01-15,DENTAL01,150.00,,,</code></p>

<div style="display:flex;gap:6px;margin:12px 0;flex-wrap:wrap;">
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 1: Type → ER, Amount → 150.00</div>
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 2: Key → DENTAL01 → Dental EE Deduction</div>
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 3: SSN → Person# 100045, Asg# E12345 (WSA)</div>
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 4: MultipleEntryCount = 1</div>
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 5: SourceSystemId constructed</div>
</div>

<p style="font-size:13px;margin:14px 0 6px;font-weight:700;color:#D4622B;">LINEREPEATNO=1 → ElementEntry:</p>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">MERGE|ElementEntry|570|2019/09/22|Dental EE Deduction|123141402543|H||E|1</pre>

<p style="font-size:13px;margin:0 0 6px;font-weight:700;color:#D4622B;">LINEREPEATNO=2 → ElementEntryValue (Amount):</p>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">MERGE|ElementEntryValue|570|2019/09/22|Dental EE Deduction|123141402543|Amount||E||1|150.00</pre>

</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SERIES CLOSING ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">What You Now Understand</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">If you've read this far, you can now explain — without looking at any code — how an HDL Transformation Formula works end-to-end. You know what each OPERATION does, why METADATA arrays define the .dat column headers, how the MAP block transforms source data in 5 steps, why WSA exists (performance + correctness), how LINEREPEATNO generates multiple output rows (1 ElementEntry + up to 6 ElementEntryValues) from one source row, and how named RETURN variables map to METADATA columns.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">That's the foundation. The concepts don't change whether you're building an vendor deduction interface, a benefits enrollment loader, or a payroll costing feed. Every HDL Transformation Formula follows this same structure.</p>

<!-- NEXT IN SERIES -->
<div style="margin:30px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:16px 20px;font-weight:700;font-size:16px;">Coming Next — Part 2: Code Walkthrough</div>
<div style="padding:20px;">

<p style="font-size:15px;margin:0 0 16px;color:#3D3D5C;">Part 2 takes every concept from this post and shows you the actual Fast Formula code that implements it. Line by line, with the Notepad++ syntax highlighting you've been seeing in the code snippets here.</p>

<p style="font-size:15px;margin:0 0 16px;color:#3D3D5C;">What Part 2 will cover:</p>

<table style="width:100%;border-collapse:collapse;font-size:12px;">
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;width:40%;">Full INPUTS ARE block</td>
<td style="padding:8px 10px;color:#8B8FA8;">Every POSITION mapped to its vendor column, every DEFAULT FOR explained</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">GET_VALUE_SET calls</td>
<td style="padding:8px 10px;color:#8B8FA8;">The exact parameter string construction with pipe delimiters, date conversions, and ISNULL checking</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">WSA implementation</td>
<td style="padding:8px 10px;color:#8B8FA8;">Real WSA_EXISTS / WSA_GET / WSA_SET code with key construction patterns</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">SourceSystemId logic</td>
<td style="padding:8px 10px;color:#8B8FA8;">The full lookup-or-construct pattern for both ElementEntry and ElementEntryValue SourceSystemIds</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">ESS_LOG_WRITE debugging</td>
<td style="padding:8px 10px;color:#8B8FA8;">Adding trace logs at each step so you can debug formula execution in real time</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:8px 10px;font-weight:700;">Cancel vs Active branching</td>
<td style="padding:8px 10px;color:#8B8FA8;">The complete IF POSITION11 = 'C' block with date fetching from cloud</td>
</tr>
</tbody>
</table>

</div>
</div>

<!-- PART 3 TEASER -->
<div style="margin:0 0 30px;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;color:#fff;padding:16px 20px;font-weight:700;font-size:16px;">Later — Part 3: Build Your Own</div>
<div style="padding:20px;">

<p style="font-size:15px;margin:0 0 16px;color:#3D3D5C;">Part 3 is the implementation guide. You'll build an HDL Transformation Formula from scratch — from creating the formula in Oracle Cloud, defining all 11 value sets, configuring the HDL integration, running test loads, reading ESS logs, and troubleshooting the errors you'll hit in production.</p>

<p style="font-size:15px;margin:0;color:#3D3D5C;">After Part 3, you'll have a working formula you can adapt for any inbound payroll interface — not just one vendor.</p>

</div>
</div>

<!-- SERIES ROADMAP REPEAT -->
<div style="margin:0 0 30px;padding:20px;background:#F5F3EF;border-radius:10px;">
<div style="font-weight:700;font-size:15px;color:#3D3D5C;margin-bottom:12px;">Series Roadmap</div>
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<div style="background:#D4622B;color:#fff;padding:8px 16px;border-radius:6px;font-weight:700;font-size:13px;">Part 1: Pure Concepts <span style="font-weight:400;opacity:0.8;">← This post</span></div>
<div style="color:#8B8FA8;font-size:18px;">→</div>
<div style="background:#fff;border:1px solid #DDD8D0;color:#3D3D5C;padding:8px 16px;border-radius:6px;font-weight:700;font-size:13px;">Part 2: Code Walkthrough <span style="font-weight:400;color:#8B8FA8;">Coming soon</span></div>
<div style="color:#8B8FA8;font-size:18px;">→</div>
<div style="background:#fff;border:1px solid #DDD8D0;color:#3D3D5C;padding:8px 16px;border-radius:6px;font-weight:700;font-size:13px;">Part 3: Build Your Own <span style="font-weight:400;color:#8B8FA8;">Coming soon</span></div>
</div>
</div>

<!-- ==================== AUTHOR FOOTER ==================== -->

<div style="display:flex;align-items:center;gap:14px;padding:20px 0;border-top:1px solid #DDD8D0;">
<div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#D4622B,#E8944F);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;flex-shrink:0;">AM</div>
<div>
<div style="font-weight:700;font-size:15px;">Abhishek Mohanty</div>
<div style="font-size:13px;color:#8B8FA8;line-height:1.5;">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.</div>
</div>
</div>

</div><div style="overflow-x:auto;padding:8px 12px;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#D4622B;font-weight:700;">ELEMENT_ENTRY_ID  PERSON_ID  ELEMENT_TYPE_ID         EFFECTIVE_START_DATE  MULTIPLE_ENTRY_COUNT  ENTRY_TYPE</span>
300000012345      100045     50001 (Dental EE Ded)   01-Oct-2024           <span style="color:#D4622B;font-weight:700;">1</span>                     E</pre>
</div>
</div>

@media (prefers-color-scheme: dark) {
.hdl-blog { background: #12131A !important; color: #C8C9D4 !important; }
.hdl-blog p, .hdl-blog li { color: #C8C9D4 !important; }
.hdl-blog strong { color: #EAEBF0 !important; }
.hdl-blog em { color: #C8C9D4 !important; }
.hdl-blog code { background: #1E1F2B !important; color: #D4D5DE !important; }
.hdl-blog hr { border-color: #2A2B38 !important; }

.hdl-blog [style*="background:linear-gradient(135deg,#1B4965"] { background: linear-gradient(135deg,#0D2B3E,#081C2B) !important; box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important; }
.hdl-blog [style*="font-size:17px"][style*="font-weight:700"] { color: #EAEBF0 !important; }
.hdl-blog [style*="font-size:15px"][style*="font-weight:700"][style*="border-left"] { color: #D4D5DE !important; }

.hdl-blog [style*="background:#fff"] { background: #1A1B26 !important; }
.hdl-blog [style*="background:#F5F3EF"] { background: #16171F !important; }
.hdl-blog [style*="background:#FDF5ED"] { background: #1C1812 !important; border-color: #3D3224 !important; }
.hdl-blog [style*="background:#FCF0F0"] { background: #1C1414 !important; }
.hdl-blog [style*="background:#EDE8E0"] { background: #1E1F2B !important; }

.hdl-blog [style*="#DDD8D0"] { border-color: #2A2B38 !important; }
.hdl-blog td, .hdl-blog th, .hdl-blog tr { border-color: #2A2B38 !important; }

.hdl-blog td { color: #C8C9D4 !important; }
.hdl-blog th { color: #fff !important; }
.hdl-blog td[style*="font-weight:700"] { color: #EAEBF0 !important; }
.hdl-blog td[style*="font-weight:600"] { color: #D4D5DE !important; }
.hdl-blog td[style*="font-weight:800"] { color: #EAEBF0 !important; }

.hdl-blog [style*="color:#D4622B"] { color: #E89060 !important; }
.hdl-blog td[style*="color:#D4622B"] { color: #E89060 !important; }
.hdl-blog [style*="background:#D4622B"], .hdl-blog [style*="background:linear-gradient(135deg,#D4622B"] { color: #fff !important; }

.hdl-blog [style*="color:#2D8B6F"] { color: #5CC4A0 !important; }
.hdl-blog [style*="background:#2D8B6F"] { background: #1A5C47 !important; }

.hdl-blog [style*="color:#C13B3B"] { color: #F08080 !important; }
.hdl-blog [style*="background:#C13B3B"] { background: #8B2020 !important; }
.hdl-blog [style*="border"][style*="#C13B3B"] { border-color: #5C1A1A !important; }

.hdl-blog [style*="color:#8B8FA8"] { color: #6B6F88 !important; }

.hdl-blog pre { background: #0D0E14 !important; border-color: #1E1F2B !important; }

.hdl-blog [style*="background:#1E1E1E"] { background: #0D0E14 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#8B8FA8"] { color: #6B6F88 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#B5CEA8"] { color: #B5CEA8 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#CE9178"] { color: #CE9178 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#2D8B6F"] { color: #5CC4A0 !important; }
.hdl-blog [style*="background:#1E1E1E"] td[style*="color:#C13B3B"] { color: #F08080 !important; }

.hdl-blog [style*="background:#1B4965"] { background: #0D2B3E !important; }

.hdl-blog [style*="font-size:28px"][style*="color:#C13B3B"] { color: #F08080 !important; }
.hdl-blog [style*="font-size:28px"][style*="color:#D4622B"] { color: #E89060 !important; }

.hdl-blog [style*="background:#eee"] { background: #2A2B38 !important; color: #8B8FA8 !important; }

.hdl-blog span[style*="border-radius:10px"] { color: #fff !important; }
.hdl-blog span[style*="border-radius:12px"] { color: #fff !important; }

.hdl-blog [style*="font-size:30px"][style*="font-weight:800"] { color: #F0F1F5 !important; }

.hdl-blog td[style*="font-family:monospace"] { color: #C8C9D4 !important; }

.hdl-blog [style*="color:#1A1A2E"] { color: #EAEBF0 !important; }
.hdl-blog [style*="color:#3D3D5C"] { color: #C8C9D4 !important; }
}

<style>
.hdl-blog table { min-width: 400px; }

.hdl-blog .block-table { font-size: 11px !important; }
.hdl-blog .block-table td, .hdl-blog .block-table th { padding: 5px 6px !important; font-size: 11px !important; white-space: nowrap !important; }
.hdl-blog .db-table { font-size: 11px !important; }
.hdl-blog .db-table td, .hdl-blog .db-table th { padding: 5px 6px !important; font-size: 11px !important; white-space: nowrap !important; }

.hdl-blog div[style*="overflow:hidden"] { overflow-x: auto !important; }
</style>
</style>
<div class="hdl-blog" style="font-family:'Open Sans',sans-serif;color:#3D3D5C;line-height:1.85;max-width:760px;margin:0 auto;background:#FCFBF9;">

<span style="display:inline-block;background:#D4622B;color:#fff;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:5px;margin-bottom:8px;margin-right:8px;box-shadow:0 2px 4px rgba(212,98,43,0.2);">Fast Formula</span>
<span style="display:inline-block;background:#D4622B;color:#fff;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:5px;margin-bottom:8px;margin-right:8px;box-shadow:0 2px 4px rgba(212,98,43,0.2);">HCM Data Loader</span>
<span style="display:inline-block;background:#D4622B;color:#fff;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:5px;margin-bottom:8px;margin-right:8px;box-shadow:0 2px 4px rgba(212,98,43,0.2);">Transformation Formula</span>
<span style="display:inline-block;background:#D4622B;color:#fff;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:5px;margin-bottom:8px;margin-right:8px;box-shadow:0 2px 4px rgba(212,98,43,0.2);">WSA</span>
<span style="display:inline-block;background:#1A1A2E;color:#fff;padding:5px 16px;font-size:11px;letter-spacing:1.5px;font-weight:700;letter-spacing:2px;text-transform:uppercase;border-radius:2px;margin-bottom:6px;margin-right:6px;">Series Part 1 of 3</span>

<div style="font-size:30px;font-weight:800;color:#1A1A2E;margin:24px 0 10px;line-height:1.25;letter-spacing:-0.8px;">HDL Transformation Formula Deep Dive — Part 1: Pure Concepts</div>

<div style="font-size:15px;color:#8B8FA8;margin-bottom:6px;letter-spacing:0.5px;">Vendor Deduction Interface | ElementEntry + ElementEntryValue</div>
<div style="font-size:13px;color:#8B8FA8;margin-bottom:25px;letter-spacing:0.5px;">March 2026 • 25 min read • Oracle HCM Cloud</div>

<div style="font-size:15px;color:#3D3D5C;line-height:1.7;margin-bottom:30px;font-style:italic;border-left:4px solid #D4622B;padding-left:18px;">
This is <strong>Part 1</strong> of a 3-part series on HDL Transformation Formulas. This post covers the concepts end-to-end — what each section of the formula does and why. No code to copy-paste here. Just the understanding you need before writing a single line.
</div>

<!-- SERIES ROADMAP -->
<div style="margin:0 0 35px;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;color:#fff;padding:14px 20px;font-weight:700;font-size:15px;">HDL Transformation Formula Series</div>
<div style="padding:0;">

<div style="display:flex;align-items:center;gap:16px;padding:16px 20px;border-bottom:1px solid #DDD8D0;background:#FDF5ED;">
<div style="background:#D4622B;color:#fff;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;box-shadow:0 2px 8px rgba(212,98,43,0.25);">1</div>
<div>
<div style="font-weight:700;font-size:15px;color:#D4622B;">Pure Concepts <span style="font-size:13px;font-weight:400;color:#8B8FA8;margin-left:6px;">← You are here</span></div>
<div style="font-size:13px;color:#8B8FA8;">What each section of the formula does. INPUTS, OPERATION, METADATA, MAP (5 steps), WSA, LINEREPEATNO, RETURN. Zero code to memorize — just understanding.</div>
</div>
</div>

<div style="display:flex;align-items:center;gap:16px;padding:16px 20px;border-bottom:1px solid #DDD8D0;">
<div style="background:#eee;color:#8B8FA8;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;">2</div>
<div>
<div style="font-weight:700;font-size:15px;color:#3D3D5C;">Code Walkthrough <span style="font-size:13px;font-weight:400;color:#8B8FA8;margin-left:6px;">Coming soon</span></div>
<div style="font-size:13px;color:#8B8FA8;">The actual formula code, explained line-by-line. Value set definitions, WSA implementation, date conversions, ISNULL patterns, ESS_LOG_WRITE debugging. Moderate complexity — you'll be able to read any HDL formula after this.</div>
</div>
</div>

<div style="display:flex;align-items:center;gap:16px;padding:16px 20px;">
<div style="background:#eee;color:#8B8FA8;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;">3</div>
<div>
<div style="font-weight:700;font-size:15px;color:#3D3D5C;">Build Your Own <span style="font-size:13px;font-weight:400;color:#8B8FA8;margin-left:6px;">Coming soon</span></div>
<div style="font-size:13px;color:#8B8FA8;">Full implementation guide. Setting up the formula in Oracle, creating the value sets, configuring the HDL integration, testing with real data, debugging production issues. Copy-paste ready.</div>
</div>
</div>

</div>
</div>

<div style="display:flex;align-items:center;gap:14px;padding:20px 0;border-top:1px solid #DDD8D0;border-bottom:2px solid #DDD8D0;margin-bottom:35px;">
<div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#D4622B,#E8944F);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;flex-shrink:0;">AM</div>
<div>
<div style="font-weight:700;font-size:15px;">Abhishek Mohanty</div>
<div style="font-size:13px;color:#8B8FA8;">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant</div>
</div>
</div>

<!-- ==================== BIG PICTURE FLOW ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">The Big Picture</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Before we go section by section, here's what this formula does end to end:</p>

<!-- VISUAL: END-TO-END PIPELINE -->
<div style="display:flex;align-items:center;gap:0;margin:20px 0;flex-wrap:wrap;">
<div style="background:#D4622B;color:#fff;padding:8px 10px;border-radius:8px 0 0 8px;font-weight:700;font-size:13px;text-align:center;min-width:100px;">
Vendor CSV File<br><span style="font-size:13px;font-weight:400;opacity:0.7;">SSN, Date, Code, Amounts</span>
</div>
<div style="width:0;height:0;border-top:24px solid transparent;border-bottom:24px solid transparent;border-left:14px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;min-width:120px;">
HDL Transformation<br><span style="font-size:13px;font-weight:400;opacity:0.7;">This Formula</span>
</div>
<div style="width:0;height:0;border-top:24px solid transparent;border-bottom:24px solid transparent;border-left:14px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;border-radius:0 8px 8px 0;font-weight:700;font-size:13px;text-align:center;min-width:120px;">
ElementEntry .dat<br><span style="font-size:13px;font-weight:400;opacity:0.7;">Header + Value rows</span>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">A third-party benefits administration vendor (BenAdmin) sends a CSV with deduction and employer contribution amounts. This formula transforms each row into Oracle HDL format — resolving SSNs to Assignment Numbers, mapping vendor codes to Oracle Element Names, managing MultipleEntryCount, and generating both ElementEntry (header) and ElementEntryValue (detail) rows.</p>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 1: VENDOR FILE ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 1: The Vendor Inbound File — What We Receive</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The vendor manages employee benefit enrollments — medical, dental, vision, life insurance, FSA, HSA, loans. Every pay period, they send a flat CSV file with deduction details to load into Oracle as Element Entries.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The Raw Input File Layout</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Each row in the vendor file maps to one set of delimited columns. The HDL engine reads these into POSITION variables:</p>

<div style="overflow-x:auto;margin:18px 0;border:1px solid #DDD8D0;border-radius:8px;">
<table style="width:100%;border-collapse:collapse;font-size:11px;min-width:700px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;">Column</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;">Position</th>
<th style="padding:6px 8px;text-align:left;font-size:10px;">Description</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;">Example</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">SSN</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION1</td>
<td style="padding:5px 8px;">Employee Social Security Number</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">123-45-6789</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">EFFECTIVE_DATE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION2</td>
<td style="padding:5px 8px;">Date the deduction applies (YYYY-MM-DD)</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">2024-01-15</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">BENEFIT_PLAN_CODE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION3</td>
<td style="padding:5px 8px;">Vendor’s internal code for the benefit plan</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">DENTAL01</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">DEDUCTION_TYPE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION4</td>
<td style="padding:5px 8px;">Controls LINEREPEATNO branches and how many input values are loaded</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">LOAN, PRE, POST, CU</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">AMOUNT</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION5</td>
<td style="padding:5px 8px;">Deduction amount (InputValueName = ‘Amount’)</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;">150.00</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">PERIOD_TYPE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION6</td>
<td style="padding:5px 8px;">Period type for the deduction</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(varies)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">PERCENTAGE</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION7</td>
<td style="padding:5px 8px;">Percentage for PRE/POST type deductions</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(blank or value)</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">LOAN_NUMBER</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION8</td>
<td style="padding:5px 8px;">Loan number (LOAN type only)</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(blank or value)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;color:#8B8FA8;">POSITION9–10</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION9–10</td>
<td style="padding:5px 8px;color:#8B8FA8;">Reserved / additional fields</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(varies)</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:5px 8px;font-weight:700;white-space:nowrap;">STATUS</td>
<td style="padding:5px 8px;font-family:monospace;font-size:10px;white-space:nowrap;color:#8B8FA8;">POSITION11</td>
<td style="padding:5px 8px;">C = Cancel/End-date, blank = Active/New</td>
<td style="padding:5px 8px;font-family:monospace;white-space:nowrap;color:#8B8FA8;">(blank)</td>
</tr>
</tbody></table>
</div>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-left:4px solid #D4622B;padding:14px 18px;margin:18px 0;border-radius:0 6px 6px 0;">
<p style="margin:0;font-size:14px;color:#3D3D5C;"><strong>Key point:</strong> POSITION4 (Deduction Type) is the most important field after SSN and Date. It controls the formula's branching logic — which LINEREPEATNO passes execute, which input values get loaded (Amount, Period Type, Percentage, Loan Number, Total Owed, Deduction Amount), and even whether the formula generates output on certain passes. A LOAN type deduction goes through 7 passes. A regular deduction goes through fewer.</p>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How One Vendor Row Becomes Multiple Input Values</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">A single vendor row carries multiple amounts for the same deduction. The formula uses LINEREPEATNO to load each input value in a separate pass. For a LOAN type deduction, one source row generates up to 7 output rows:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* One vendor row: */</span>
<span style="color:#CE9178;">123-45-6789,2024-01-15,DENTAL01,LOAN,150.00,Monthly,5.5,LN-001,,,,</span>

<span style="color:#57A64A;font-style:italic;">/* Formula generates (up to 7 passes): */</span>
<span style="color:#C8C8C8;">Pass 1 (LINEREPEATNO=1):</span> <span style="color:#CE9178;">ElementEntry header</span>
<span style="color:#C8C8C8;">Pass 2 (LINEREPEATNO=2):</span> <span style="color:#CE9178;">ElementEntryValue → Amount = 150.00</span>
<span style="color:#C8C8C8;">Pass 3 (LINEREPEATNO=3):</span> <span style="color:#CE9178;">ElementEntryValue → Period Type = Monthly</span>
<span style="color:#C8C8C8;">Pass 4 (LINEREPEATNO=4):</span> <span style="color:#CE9178;">ElementEntryValue → Loan Number = LN-001</span>
<span style="color:#C8C8C8;">Pass 5 (LINEREPEATNO=5):</span> <span style="color:#CE9178;">ElementEntryValue → Total Owed = ...</span>
<span style="color:#C8C8C8;">Pass 6 (LINEREPEATNO=6):</span> <span style="color:#CE9178;">ElementEntryValue → Percentage = 5.5</span>
<span style="color:#C8C8C8;">Pass 7 (LINEREPEATNO=7):</span> <span style="color:#CE9178;">ElementEntryValue → Deduction Amount = ...</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Not every deduction type needs all 7 passes. The formula checks POSITION4 on each pass — if the type doesn't apply (e.g. Percentage only runs for PRE/POST types), it returns <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code> with no output, effectively skipping that pass.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Understanding MultipleEntryCount</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Oracle HCM draws a fundamental distinction between <strong>recurring</strong> and <strong>non-recurring</strong> elements when it comes to MultipleEntryCount:</p>

<!-- VISUAL: Recurring vs Non-Recurring -->
<div style="display:flex;gap:20px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:300px;border-radius:10px;overflow:hidden;border:1px solid #DDD8D0;border-left:4px solid #D4622B;">
<div style="background:#fff;padding:12px 18px;border-bottom:1px solid #DDD8D0;">
<div style="font-weight:800;font-size:14px;color:#D4622B;">RECURRING ELEMENTS</div>
<div style="font-size:13px;color:#D4622B;">Monthly salary, standing allowance</div>
</div>
<div style="padding:14px 18px;background:#fff;">
<p style="margin:0 0 8px;font-size:14px;color:#3D3D5C;">MultipleEntryCount is <strong>not required</strong> as a key when using SourceSystemId.</p>
<div style="background:#fff;border-radius:6px;padding:6px 8px;font-size:13px;color:#D4622B;"><em>"You don't need to supply the MultipleEntryCount attribute as source keys to uniquely identify the records."</em> — Oracle Docs</div>
</div>
</div>
<div style="flex:1;min-width:300px;border-radius:10px;overflow:hidden;border:1px solid #DDD8D0;border-left:4px solid #D4622B;">
<div style="background:#fff;padding:12px 18px;border-bottom:1px solid #DDD8D0;">
<div style="font-weight:800;font-size:14px;color:#D4622B;">NON-RECURRING ELEMENTS</div>
<div style="font-size:13px;color:#D4622B;">Benefits deductions (our vendor elements)</div>
</div>
<div style="padding:14px 18px;background:#fff;">
<p style="margin:0 0 8px;font-size:14px;color:#3D3D5C;">MultipleEntryCount <strong>must be incremented</strong> for each entry of the same assignment + element within the same payroll period.</p>
<div style="background:#fff;border-radius:6px;padding:6px 8px;font-size:13px;color:#D4622B;"><em>"You must increment the value of MultipleEntryCount for each entry of the same assignment and element."</em> — Oracle Docs</div>
</div>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The vendor interface loads <strong>non-recurring elements that allow multiple entries</strong>. This means the formula must query the cloud for the current highest MultipleEntryCount before assigning the next one — and track assigned values across rows within the same batch using WSA.</p>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#D4622B;"><strong>Key Takeaway:</strong> Three benefit plan rows (Dental, Medical, Vision) for the same employee map to three <strong>different elements</strong>, so they each get independent entries with their own MultipleEntryCount. MultipleEntryCount is needed when the <strong>same non-recurring element</strong> requires <strong>multiple entries</strong> for the <strong>same assignment within the same payroll period</strong>.</p>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 2: VALUE SETS ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 2: Why Value Sets? Understanding Each GET_VALUE_SET Call</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The vendor file gives us an <strong>SSN</strong> and an <strong>Vendor Deduction Code</strong>. Oracle HCM needs an <strong>Assignment Number</strong> and an <strong>Oracle Element Name</strong>. These are completely different identifiers in completely different systems. Value Sets act as the bridge — SQL-backed lookup functions that run inside the Fast Formula engine.</p>

<!-- VISUAL: Translation bridge -->
<div style="display:flex;align-items:center;gap:0;margin:20px 0;flex-wrap:wrap;">
<div style="background:#fff;border:1px solid #DDD8D0;padding:14px 18px;border-radius:8px 0 0 8px;text-align:center;min-width:160px;">
<div style="font-size:13px;color:#D4622B;font-weight:700;letter-spacing:1px;">VENDOR ENVIRONMENT</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;margin-top:6px;">SSN: 123-45-6789</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">Code: DENTAL01</div>
</div>
<div style="background:#D4622B;color:#fff;padding:14px 18px;text-align:center;min-width:120px;">
<div style="font-size:13px;opacity:0.7;font-weight:700;letter-spacing:1px;">VALUE SETS</div>
<div style="font-size:20px;margin-top:4px;">→</div>
</div>
<div style="background:#fff;border:1px solid #DDD8D0;padding:14px 18px;border-radius:0 8px 8px 0;text-align:center;min-width:180px;">
<div style="font-size:13px;color:#D4622B;font-weight:700;letter-spacing:1px;">ORACLE WORLD</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;margin-top:6px;">Asg#: E12345</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">Element: Dental EE Deduction</div>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula uses 11 value sets. Here's what each one does:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:center;width:30px;">#</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Value Set</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">What It Does</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Returns</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">1</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">XXVA_DEDUCTION_CODES</td>
<td style="padding:6px 8px;">Maps vendor plan code (DENTAL01) to Oracle Element Name</td>
<td style="padding:6px 8px;">Element Name</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">2</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">XXVA_DEDUCTION_CODES_INPUT</td>
<td style="padding:6px 8px;">Gets Input Value Name for the element (e.g. Amount)</td>
<td style="padding:6px 8px;">Input Value Name</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">3</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">XXVA_GET_LATEST_ASSIGNMENT_NUMBER</td>
<td style="padding:6px 8px;">Resolves SSN + date → Assignment Number</td>
<td style="padding:6px 8px;">Assignment# (E12345)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">4</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">XXVA_GET_PERSON_NUMBER</td>
<td style="padding:6px 8px;">Resolves SSN → Person Number</td>
<td style="padding:6px 8px;">Person# (100045)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">5</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">MAX_MULTI_ENTRY_COUNT</td>
<td style="padding:6px 8px;">Gets highest existing MultipleEntryCount for Person+Element+Date</td>
<td style="padding:6px 8px;">Max count (or NULL)</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">6–7</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;">GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID / _OWNER</td>
<td style="padding:6px 8px;">Retrieves existing SourceSystemId/Owner for MERGE key reuse</td>
<td style="padding:6px 8px;">Existing SSID/SSO</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">8–9</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;">GET_ELEMENT_ENTRY_VALUE_SOURCE_SYSTEM_ID / _OWNER</td>
<td style="padding:6px 8px;">Same but at Element Entry Value level</td>
<td style="padding:6px 8px;">ElementEntryValue-level SSID/SSO</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">10</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">GET_ELEMENT_ENTRY_START_DATE</td>
<td style="padding:6px 8px;">For Cancel rows — gets original start date</td>
<td style="padding:6px 8px;">Original start date</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;text-align:center;font-weight:700;">11</td>
<td style="padding:6px 8px;font-family:monospace;font-size:13px;white-space:nowrap;">GET_ELEMENT_ENTRY_INPUT_START_DATE</td>
<td style="padding:6px 8px;">Same but at ElementEntryValue level (date-tracked scenarios)</td>
<td style="padding:6px 8px;">ElementEntryValue original start date</td>
</tr>
</tbody></table>

<!-- VISUAL: Code vs Person lookup split -->
<div style="display:flex;gap:16px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:250px;background:#fff;border:1px solid #DDD8D0;border-top:3px solid #D4622B;border-radius:8px;padding:16px;">
<div style="font-weight:800;font-size:13px;color:#D4622B;margin-bottom:8px;">CODE-BASED LOOKUPS (#1–2)</div>
<p style="margin:0;font-size:13px;color:#3D3D5C;">Translate vendor codes → Oracle element names. Called once per row regardless. No caching benefit.</p>
</div>
<div style="flex:1;min-width:250px;background:#fff;border:1px solid #DDD8D0;border-top:3px solid #D4622B;border-radius:8px;padding:16px;">
<div style="font-weight:800;font-size:13px;color:#D4622B;margin-bottom:8px;">PERSON-BASED LOOKUPS (#3–11)</div>
<p style="margin:0;font-size:13px;color:#3D3D5C;">Resolve SSN/Person data. Same SSN appears across multiple rows — <strong>WSA caching saves significant performance here.</strong></p>
</div>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 3: INPUTS ARE ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 3: INPUTS ARE — Declaring Formula Input Variables</div>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">INPUTS ARE</span> <span style="color:#C8C8C8;">OPERATION</span> (<span style="color:#CC7832;">TEXT</span>),
<span style="color:#C8C8C8;">LINEREPEATNO</span> (<span style="color:#CC7832;">NUMBER</span>),
<span style="color:#C8C8C8;">LINENO</span> (<span style="color:#CC7832;">NUMBER</span>),
<span style="color:#C8C8C8;">POSITION1</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION2</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION3</span> (<span style="color:#CC7832;">TEXT</span>),
<span style="color:#C8C8C8;">POSITION4</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION5</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION6</span> (<span style="color:#CC7832;">TEXT</span>),
<span style="color:#C8C8C8;">POSITION7</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION8</span> (<span style="color:#CC7832;">TEXT</span>),
<span style="color:#C8C8C8;">POSITION9</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION10</span> (<span style="color:#CC7832;">TEXT</span>), <span style="color:#C8C8C8;">POSITION11</span> (<span style="color:#CC7832;">TEXT</span>)

<span style="color:#fff;font-weight:700;">DEFAULT FOR</span> <span style="color:#C8C8C8;">LINENO</span> <span style="color:#fff;font-weight:700;">IS</span> <span style="color:#DCDCAA;">1</span>
<span style="color:#fff;font-weight:700;">DEFAULT FOR</span> <span style="color:#C8C8C8;">LINEREPEATNO</span> <span style="color:#fff;font-weight:700;">IS</span> <span style="color:#DCDCAA;">1</span>
<span style="color:#fff;font-weight:700;">DEFAULT FOR</span> <span style="color:#C8C8C8;">POSITION1</span> <span style="color:#fff;font-weight:700;">IS</span> <span style="color:#CE9178;">'NO DATA'</span>
<span style="color:#fff;font-weight:700;">DEFAULT FOR</span> <span style="color:#C8C8C8;">POSITION2</span> <span style="color:#fff;font-weight:700;">IS</span> <span style="color:#CE9178;">'NO DATA'</span>
<span style="color:#57A64A;font-style:italic;">/* ... same for POSITION3 through POSITION11 ... */</span></pre>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;width:130px;">Variable</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">What It Does</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;color:#000;width:130px;white-space:nowrap;">OPERATION</td>
<td style="padding:6px 8px;font-size:13px;">The HDL engine calls the formula multiple times with different values: FILETYPE, DELIMITER, READ, NUMBEROFBUSINESSOBJECTS, METADATALINEINFORMATION, then MAP per row. The formula is a router.</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;color:#000;width:130px;white-space:nowrap;">LINEREPEATNO</td>
<td style="padding:6px 8px;font-size:13px;">The repeat counter. When formula sets <code>LINEREPEAT = 'Y'</code>, HDL re-invokes for the same row with incremented LINEREPEATNO. One input row can generate up to 7 HDL output rows: 1 ElementEntry header (pass 1) + up to 6 ElementEntryValue rows (passes 2–7), one per input value (Amount, Period Type, Loan Number, Total Owed, Percentage, Deduction Amount). The deduction type (POSITION4) controls how many passes run.</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;color:#000;width:130px;white-space:nowrap;">LINENO</td>
<td style="padding:6px 8px;font-size:13px;">Line number from the source file (1-based). Useful for error tracing.</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;color:#000;width:130px;white-space:nowrap;">POSITION1–11</td>
<td style="padding:6px 8px;font-size:13px;">Map directly to CSV columns in order. HDL engine splits each line by delimiter and populates these.</td>
</tr>
</tbody></table>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#D4622B;"><strong>Why DEFAULT FOR is required:</strong> When HDL calls the formula for non-MAP operations (like FILETYPE), the POSITION variables aren't populated — no source row is being processed. Without defaults, the formula throws a null reference error at runtime.</p>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 4: OPERATIONS ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 4: OPERATION — The Setup Handshake</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">This section does NOT touch the vendor data — it configures the HDL engine</div>
<div style="padding:14px 16px;font-size:12px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;width:30%;">Input</td>
<td style="padding:6px 0;">HDL engine asks: "What file type? What delimiter? How many objects?"</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;">Formula returns</td>
<td style="padding:6px 0;font-family:monospace;">DELIMITED, comma, NONE, 2</td>
</tr>
<tr>
<td style="padding:6px 0;font-weight:700;">HDL output</td>
<td style="padding:6px 0;color:#8B8FA8;">Nothing written to .dat yet — engine is just being configured</td>
</tr>
</table>
</div>
</div>


<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'FILETYPE'</span> <span style="color:#fff;font-weight:700;">THEN</span>
    <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'DELIMITED'</span>
<span style="color:#fff;font-weight:700;">ELSE IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'DELIMITER'</span> <span style="color:#fff;font-weight:700;">THEN</span>
    <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">','</span>
<span style="color:#fff;font-weight:700;">ELSE IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'READ'</span> <span style="color:#fff;font-weight:700;">THEN</span>
    <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'NONE'</span>
<span style="color:#fff;font-weight:700;">ELSE IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'NUMBEROFBUSINESSOBJECTS'</span> <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'2'</span>
    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">OUTPUTVALUE</span>
)</pre>

<!-- VISUAL: Setup handshake flow -->
<div style="display:flex;align-items:center;gap:0;margin:20px 0;flex-wrap:wrap;">
<div style="background:#D4622B;color:#fff;padding:8px 10px;border-radius:6px 0 0 6px;font-weight:700;font-size:13px;text-align:center;">FILETYPE<br><span style="color:#fff;">DELIMITED</span></div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;">DELIMITER<br><span style="color:#fff;">,</span></div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;">READ<br><span style="color:#fff;">NONE</span></div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;">OBJECTS<br><span style="color:#fff;">2</span></div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;font-weight:700;font-size:13px;text-align:center;">METADATA</div>
<div style="width:0;height:0;border-top:20px solid transparent;border-bottom:20px solid transparent;border-left:10px solid #D4622B;"></div>
<div style="background:#D4622B;color:#fff;padding:8px 10px;border-radius:0 6px 6px 0;font-weight:700;font-size:13px;text-align:center;">MAP<br><span style="font-size:9px;font-weight:400;">(per row)</span></div>
</div>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Operation</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Engine Asks</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Our Answer</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Why</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;">FILETYPE</td>
<td style="padding:8px 10px;">"What kind of file?"</td>
<td style="padding:8px 10px;font-family:monospace;">DELIMITED</td>
<td style="padding:8px 10px;">Only valid option for HDL transformation</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;">DELIMITER</td>
<td style="padding:8px 10px;">"What separates values?"</td>
<td style="padding:8px 10px;font-family:monospace;">,</td>
<td style="padding:8px 10px;">the vendor sends CSV. Default is pipe (|), so we override.</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;">READ</td>
<td style="padding:8px 10px;">"Skip header rows?"</td>
<td style="padding:8px 10px;font-family:monospace;">NONE</td>
<td style="padding:8px 10px;">vendor file has no header row — process every line.</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-family:monospace;font-weight:700;">NUMBEROF...</td>
<td style="padding:8px 10px;">"How many HDL objects?"</td>
<td style="padding:8px 10px;font-family:monospace;">2</td>
<td style="padding:8px 10px;">ElementEntry (header) + ElementEntryValue (detail with amount)</td>
</tr>
</tbody></table>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 5: METADATA ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 5: METADATA — Generating the .dat File Headers</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">This section generates the .dat HEADER rows (not data rows)</div>
<div style="padding:14px 16px;font-size:12px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;width:30%;">Input</td>
<td style="padding:6px 0;">HDL engine asks: "What columns does each object have?"</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;">Formula returns</td>
<td style="padding:6px 0;font-family:monospace;">METADATA1[ ] array, METADATA2[ ] array</td>
</tr>
<tr>
<td style="padding:6px 0;font-weight:700;">HDL writes to .dat</td>
<td style="padding:6px 0;font-family:monospace;font-size:12px;"><span style="color:#D4622B;font-weight:700;">METADATA</span>|ElementEntry|LegislativeDataGroupName|EffectiveStartDate|...<br><span style="color:#D4622B;font-weight:700;">METADATA</span>|ElementEntryValue|LegislativeDataGroupName|EffectiveStartDate|...</td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After the setup handshake, the HDL engine calls the formula with <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">OPERATION = 'METADATALINEINFORMATION'</code>. This is where the formula defines the <strong>column headers</strong> for the .dat output file. These become the METADATA rows you see at the top of each block in the .dat file.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The .dat File Has Two METADATA Header Rows</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Since we told the engine <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">NUMBEROFBUSINESSOBJECTS = 2</code> (ElementEntry + ElementEntryValue), the formula must define two METADATA arrays — one per object. These become the two header rows in the .dat file:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* This header row in the .dat file: */</span>
<span style="color:#CE9178;">METADATA|ElementEntry|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|CreatorType|EffectiveEndDate|EntryType|MultipleEntryCount</span>

<span style="color:#57A64A;font-style:italic;">/* Is generated by this code: */</span></pre>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The Code — METADATA1 (ElementEntry Header)</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula uses an <strong>array variable</strong> called <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">METADATA1</code>. Each array position maps to a column in the .dat header. Positions [1] and [2] are reserved by the HDL engine for FileName and FileDiscriminator — the formula starts filling from position [3].</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">ELSE IF</span> <span style="color:#C8C8C8;">OPERATION</span> = <span style="color:#CE9178;">'METADATALINEINFORMATION'</span> <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* ================================================= */</span>
    <span style="color:#57A64A;font-style:italic;">/* METADATA1 — ElementEntry column definitions        */</span>
    <span style="color:#57A64A;font-style:italic;">/* [1] = FileName (auto-filled by HDL engine)         */</span>
    <span style="color:#57A64A;font-style:italic;">/* [2] = FileDiscriminator (auto-filled by HDL engine)*/</span>
    <span style="color:#57A64A;font-style:italic;">/* [3] onwards = we define                            */</span>
    <span style="color:#57A64A;font-style:italic;">/* ================================================= */</span>

    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">3</span>]  = <span style="color:#CE9178;">'LegislativeDataGroupName'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">4</span>]  = <span style="color:#CE9178;">'EffectiveStartDate'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">5</span>]  = <span style="color:#CE9178;">'ElementName'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">6</span>]  = <span style="color:#CE9178;">'AssignmentNumber'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">7</span>]  = <span style="color:#CE9178;">'CreatorType'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">8</span>]  = <span style="color:#CE9178;">'EffectiveEndDate'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">9</span>]  = <span style="color:#CE9178;">'EntryType'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">10</span>] = <span style="color:#CE9178;">'MultipleEntryCount'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">11</span>] = <span style="color:#CE9178;">'SourceSystemOwner'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">12</span>] = <span style="color:#CE9178;">'SourceSystemId'</span>
    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">13</span>] = <span style="color:#CE9178;">'ReplaceLastEffectiveEndDate'</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The HDL engine reads this array and writes the following row to the .dat file:</p>

<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Generated .dat header row (ElementEntry)</div>
<div style="background:#1E1E1E;border-radius:8px;padding:16px 20px;overflow-x:auto;margin:4px 0;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#D4622B;font-weight:700;">METADATA</span>|<span style="color:#D4622B;font-weight:700;">ElementEntry</span>|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|CreatorType|EffectiveEndDate|EntryType|MultipleEntryCount|SourceSystemOwner|SourceSystemId|ReplaceLastEffectiveEndDate</pre>
</div>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The Code — METADATA2 (ElementEntryValue Header)</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Same pattern. <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">METADATA2</code> array defines the columns for the ElementEntryValue block:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">    <span style="color:#57A64A;font-style:italic;">/* ================================================= */</span>
    <span style="color:#57A64A;font-style:italic;">/* METADATA2 — ElementEntryValue column definitions   */</span>
    <span style="color:#57A64A;font-style:italic;">/* ================================================= */</span>

    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">3</span>]  = <span style="color:#CE9178;">'LegislativeDataGroupName'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">4</span>]  = <span style="color:#CE9178;">'EffectiveStartDate'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">5</span>]  = <span style="color:#CE9178;">'ElementName'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">6</span>]  = <span style="color:#CE9178;">'AssignmentNumber'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">7</span>]  = <span style="color:#CE9178;">'InputValueName'</span>              <span style="color:#57A64A;font-style:italic;">/* ← changes per pass */</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">8</span>]  = <span style="color:#CE9178;">'EffectiveEndDate'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">9</span>]  = <span style="color:#CE9178;">'EntryType'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">10</span>] = <span style="color:#CE9178;">'MultipleEntryCount'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">11</span>] = <span style="color:#CE9178;">'ScreenEntryValue'</span>            <span style="color:#57A64A;font-style:italic;">/* ← the actual value */</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">12</span>] = <span style="color:#CE9178;">'"ElementEntryId(SourceSystemId)"'</span>  <span style="color:#57A64A;font-style:italic;">/* parent link */</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">13</span>] = <span style="color:#CE9178;">'SourceSystemOwner'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">14</span>] = <span style="color:#CE9178;">'SourceSystemId'</span>
    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">15</span>] = <span style="color:#CE9178;">'ReplaceLastEffectiveEndDate'</span>

    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">METADATA1</span>, <span style="color:#B5CEA8;">METADATA2</span>
)</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">This generates the second header row in the .dat file:</p>

<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Generated .dat header row (ElementEntryValue)</div>
<div style="background:#1E1E1E;border-radius:8px;padding:16px 20px;overflow-x:auto;margin:4px 0;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#D4622B;font-weight:700;">METADATA</span>|<span style="color:#D4622B;font-weight:700;">ElementEntryValue</span>|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|<span style="color:#D4622B;font-weight:700;">InputValueName</span>|EffectiveEndDate|EntryType|MultipleEntryCount|<span style="color:#D4622B;font-weight:700;">ScreenEntryValue</span>|ElementEntryId(SSID)|SourceSystemOwner|SourceSystemId|ReplaceLastEffectiveEndDate</pre>
</div>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How METADATA Links to RETURN in Sections 7 and 8</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The column names in the METADATA arrays directly map to the <strong>named output variables</strong> in the formula's RETURN statement. Here's the connection:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* METADATA defines the column header: */</span>
<span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">5</span>] = <span style="color:#CE9178;">'ElementName'</span>

<span style="color:#57A64A;font-style:italic;">/* In the MAP block, the formula assigns the named variable: */</span>
<span style="color:#B5CEA8;">ElementName</span>  = <span style="color:#B5CEA8;">l_ElementName</span>              <span style="color:#57A64A;font-style:italic;">/* = 'Dental EE Deduction' */</span>

<span style="color:#57A64A;font-style:italic;">/* And includes it in the RETURN: */</span>
<span style="color:#fff;font-weight:700;">RETURN</span> ..., <span style="color:#B5CEA8;">ElementName</span>, ...

<span style="color:#57A64A;font-style:italic;">/* Result in .dat file:                                                */</span>
<span style="color:#57A64A;font-style:italic;">/* METADATA |ElementEntry|...|ElementName                    |...      */</span>
<span style="color:#57A64A;font-style:italic;">/* MERGE    |ElementEntry|...|Dental EE Deduction   |...      */</span>
<span style="color:#57A64A;font-style:italic;">/*                             ↑ matched by variable name             */</span></pre>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0 0 8px;font-size:14px;color:#3D3D5C;"><strong>The mapping rule:</strong></p>
<p style="margin:0;font-size:14px;color:#3D3D5C;">
<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">METADATA1[N]</code> defines column N header name for object 1 (ElementEntry)<br>
In the MAP block, you assign a variable with <strong>that exact same name</strong> and include it in the RETURN statement<br><br>
The HDL engine matches the RETURN variable name to the METADATA column name and writes the value into the correct position in the .dat file. The <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator</code> value (<code>'ElementEntry'</code> vs <code>'ElementEntryValue'</code>) tells the engine which METADATA block to use.
</p>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 6: MAP ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 6: OPERATION: MAP — The Core Transformation</div>

<p style="font-size:15px;margin-bottom:6px;color:#3D3D5C;">The reference vendor row used in all examples below:</p>

<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;padding:10px 16px;font-weight:700;font-size:13px;color:#fff;">Vendor Input Row</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;width:25%;">POSITION1</td>
<td style="padding:8px 14px;font-weight:600;width:30%;">SSN</td>
<td style="padding:8px 14px;font-family:monospace;">123-45-6789</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION2</td>
<td style="padding:8px 14px;font-weight:600;">Effective Date</td>
<td style="padding:8px 14px;font-family:monospace;">2024-01-15</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION3</td>
<td style="padding:8px 14px;font-weight:600;">Benefit Plan</td>
<td style="padding:8px 14px;font-family:monospace;">DENTAL01</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION4</td>
<td style="padding:8px 14px;font-weight:600;">Deduction Type</td>
<td style="padding:8px 14px;font-family:monospace;">PRE</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION5</td>
<td style="padding:8px 14px;font-weight:600;">Amount</td>
<td style="padding:8px 14px;font-family:monospace;">150.00</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION6</td>
<td style="padding:8px 14px;font-weight:600;">Period Type</td>
<td style="padding:8px 14px;font-family:monospace;">Monthly</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION7</td>
<td style="padding:8px 14px;font-weight:600;">Percentage</td>
<td style="padding:8px 14px;font-family:monospace;">5.5</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION8</td>
<td style="padding:8px 14px;font-weight:600;">Loan Number</td>
<td style="padding:8px 14px;font-family:monospace;">LN-001</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:8px 14px;font-family:monospace;font-weight:700;color:#D4622B;">POSITION11</td>
<td style="padding:8px 14px;font-weight:600;">Status</td>
<td style="padding:8px 14px;font-family:monospace;color:#8B8FA8;">(blank = Active)</td>
</tr>
</table>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">This is the heart of the formula. When the HDL engine reaches a source row, it calls <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">OPERATION = 'MAP'</code>. The formula receives the raw CSV data in POSITION1–11 and must return Oracle HDL attributes. Five steps run in sequence.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's what the formula needs to figure out for each row:</p>

<!-- VISUAL: What the formula needs to answer -->
<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Question</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Vendor Gives Us</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Oracle Needs</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Step</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;">What type of deduction?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">POSITION4 (Deduction Type)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">PRE / POST / LOAN / CU</td>
<td style="padding:8px 10px;font-weight:700;">Step 1</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;">Which Oracle Element?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">DENTAL01</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">Dental EE Deduction</td>
<td style="padding:8px 10px;font-weight:700;">Step 2</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;">Which employee?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">123-45-6789 (SSN)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">E12345 (Assignment#)</td>
<td style="padding:8px 10px;font-weight:700;">Step 3</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;">How many entries already exist?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">(doesn't know)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">MultipleEntryCount = 2</td>
<td style="padding:8px 10px;font-weight:700;">Step 4</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;">New or existing entry?</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">(doesn't know)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">SourceSystemId for MERGE</td>
<td style="padding:8px 10px;font-weight:700;">Step 5</td>
</tr>
</tbody></table>

<!-- VISUAL: 5 Step pipeline -->
<div style="display:flex;gap:8px;margin:20px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 1<br><span style="font-weight:400;font-size:13px;">Element Type</span></div>
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 2<br><span style="font-weight:400;font-size:13px;">Element Lookup</span></div>
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 3<br><span style="font-weight:400;font-size:13px;">Person / Assignment</span></div>
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 4<br><span style="font-weight:400;font-size:13px;">MultipleEntryCount</span></div>
<div style="flex:1;min-width:120px;background:#D4622B;color:#fff;padding:10px;border-radius:6px;text-align:center;font-size:13px;font-weight:700;">STEP 5<br><span style="font-weight:400;font-size:13px;">SourceSystemId</span></div>
</div>

<!-- STEP 1 -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 1: Read Input Values from POSITION Fields</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 1 reads: POSITION4, POSITION5, POSITION6, POSITION7, POSITION8</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;width:50%;color:#8B8FA8;">POSITION4 = <span style="color:#3D3D5C;font-weight:700;">PRE</span></td>
<td style="padding:6px 0;">→ l_DeductionType = <span style="color:#D4622B;font-weight:700;">'PRE'</span></td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION5 = <span style="color:#3D3D5C;font-weight:700;">150.00</span></td>
<td style="padding:6px 0;">→ l_Amount = <span style="color:#D4622B;font-weight:700;">'150.00'</span></td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION6 = <span style="color:#3D3D5C;font-weight:700;">Monthly</span></td>
<td style="padding:6px 0;">→ l_PeriodType = <span style="color:#D4622B;font-weight:700;">'Monthly'</span></td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION7 = <span style="color:#3D3D5C;font-weight:700;">5.5</span></td>
<td style="padding:6px 0;">→ l_Percentage = <span style="color:#D4622B;font-weight:700;">'5.5'</span></td>
</tr>
<tr style="font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION8 = <span style="color:#3D3D5C;font-weight:700;">LN-001</span></td>
<td style="padding:6px 0;">→ l_LoanNumber = <span style="color:#D4622B;font-weight:700;">'LN-001'</span></td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula reads the deduction type from POSITION4 and the amount from POSITION5. It also captures other input values (Period Type, Percentage, Loan Number) from their respective positions for later LINEREPEATNO passes:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Read the key fields from the vendor row */</span>
<span style="color:#B5CEA8;">l_DeductionType</span>    = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION4</span>)     <span style="color:#57A64A;font-style:italic;">/* 'PRE', 'POST', 'LOAN', 'CU' */</span>
<span style="color:#B5CEA8;">l_Amount</span>           = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION5</span>)     <span style="color:#57A64A;font-style:italic;">/* '150.00' */</span>
<span style="color:#B5CEA8;">l_PeriodType</span>       = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION6</span>)     <span style="color:#57A64A;font-style:italic;">/* 'Monthly' */</span>
<span style="color:#B5CEA8;">l_Percentage</span>       = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION7</span>)     <span style="color:#57A64A;font-style:italic;">/* '5.5' (PRE/POST only) */</span>
<span style="color:#B5CEA8;">l_LoanNumber</span>       = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION8</span>)     <span style="color:#57A64A;font-style:italic;">/* 'LN-001' (LOAN only) */</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After this step: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_DeductionType = 'PRE'</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_Amount = '150.00'</code></p>

<!-- STEP 2 -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 2: Resolve Element Name from Benefit Plan Code</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 2 reads: POSITION3 (benefit plan code)</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 0;font-family:monospace;color:#8B8FA8;width:40%;">POSITION3 = <span style="color:#3D3D5C;font-weight:700;">DENTAL01</span></td>
<td style="padding:8px 0;font-family:monospace;">→ Value Set lookup</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 0;color:#8B8FA8;"></td>
<td style="padding:8px 0;font-family:monospace;">→ l_ElementName = <span style="color:#D4622B;font-weight:700;">'Dental EE Deduction'</span></td>
</tr>
<tr>
<td style="padding:8px 0;color:#8B8FA8;"></td>
<td style="padding:8px 0;font-family:monospace;">→ l_InputValueName = <span style="color:#D4622B;font-weight:700;">'Amount'</span></td>
</tr>
</table>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The vendor uses its own benefit plan codes (DENTAL01, MEDICAL01, VISION01). Oracle doesn't know these codes. The formula passes the vendor code to two value sets that translate it into Oracle terms:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Step 2: Translate vendor plan code → Oracle Element Name */</span>

<span style="color:#B5CEA8;">L_VendorPayCode</span> = <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION3</span>)
<span style="color:#57A64A;font-style:italic;">/* e.g. 'DENTAL01' */</span>

<span style="color:#57A64A;font-style:italic;">/* Value set 1: vendor code → Oracle Element Name */</span>
<span style="color:#B5CEA8;">l_ElementName</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_DEDUCTION_CODES'</span>,
    <span style="color:#CE9178;">'|=P_PAY_CODE='''</span> || <span style="color:#B5CEA8;">L_VendorPayCode</span> || <span style="color:#CE9178;">''''</span>)
<span style="color:#57A64A;font-style:italic;">/* 'DENTAL01' → 'Dental EE Deduction' */</span>

<span style="color:#57A64A;font-style:italic;">/* Value set 2: vendor code → Input Value Name */</span>
<span style="color:#B5CEA8;">l_InputValueName</span> = <span style="color:#DCDCAA;">INITCAP</span>(<span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_DEDUCTION_CODES_INPUT'</span>,
    <span style="color:#CE9178;">'|=P_PAY_CODE='''</span> || <span style="color:#B5CEA8;">L_VendorPayCode</span> || <span style="color:#CE9178;">''''</span>))
<span style="color:#57A64A;font-style:italic;">/* 'DENTAL01' → 'Amount' */</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">These are <strong>code-based</strong> lookups — the value set definition maps each vendor code to its Oracle element. No person data is involved, so no WSA caching is needed here.</p>

<!-- VISUAL: Translation flow -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;color:#fff;padding:10px 16px;font-weight:700;font-size:13px;">Value Set Translation</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<thead><tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-weight:700;color:#3D3D5C;">Vendor Code (POSITION3)</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-weight:700;color:#3D3D5C;">Oracle Element Name</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-weight:700;color:#3D3D5C;">Input Value Name</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-weight:700;">DENTAL01</td>
<td style="padding:6px 8px;color:#D4622B;font-weight:700;">Dental EE Deduction</td>
<td style="padding:6px 8px;">Amount</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-weight:700;">MEDICAL01</td>
<td style="padding:6px 8px;color:#D4622B;font-weight:700;">Medical EE Deduction</td>
<td style="padding:6px 8px;">Amount</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-family:monospace;font-weight:700;">VISION01</td>
<td style="padding:6px 8px;color:#D4622B;font-weight:700;">Vision EE Deduction</td>
<td style="padding:6px 8px;">Amount</td>
</tr>
</tbody></table>
<p style="margin:10px 0 0;font-size:13px;color:#8B8FA8;">This mapping is defined in the value set configuration — not in the formula code. Adding a new benefit plan just means adding a row to the value set.</p>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After Step 2: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_ElementName = 'Dental EE Deduction'</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_InputValueName = 'Amount'</code></p>

<!-- STEP 3 -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 3: Resolve Person & Assignment</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 3 reads: POSITION1 (SSN) + POSITION2 (Date)</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;width:50%;color:#8B8FA8;">POSITION1 = <span style="color:#3D3D5C;font-weight:700;">123-45-6789</span></td>
<td style="padding:6px 0;">→ GET_VALUE_SET → L_PersonNumber = <span style="color:#D4622B;font-weight:700;">'100045'</span></td>
</tr>
<tr style="font-family:monospace;">
<td style="padding:6px 0;color:#8B8FA8;">POSITION2 = <span style="color:#3D3D5C;font-weight:700;">2024-01-15</span></td>
<td style="padding:6px 0;">→ GET_VALUE_SET → l_AssignmentNumber = <span style="color:#D4622B;font-weight:700;">'E12345'</span></td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Oracle HDL doesn't understand SSN. It needs two things: <strong>Person Number</strong> and <strong>Assignment Number</strong>. Step 3 translates one into the other.</p>

<!-- VISUAL: Simple translation -->
<div style="margin:18px 0;padding:16px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;">
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:center;">
<div style="background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:10px 18px;text-align:center;">
<div style="font-size:13px;color:#D4622B;font-weight:700;letter-spacing:1px;">VENDOR FILE GIVES US</div>
<div style="font-family:monospace;font-size:14px;font-weight:700;color:#D4622B;margin-top:4px;">123-45-6789</div>
<div style="font-size:13px;color:#8B8FA8;">SSN (POSITION1)</div>
</div>
<div style="text-align:center;">
<div style="font-size:22px;color:#D4622B;">→</div>
<div style="font-size:13px;color:#8B8FA8;">Value Set<br>calls DB</div>
</div>
<div style="background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:10px 18px;text-align:center;">
<div style="font-size:13px;color:#D4622B;font-weight:700;letter-spacing:1px;">ORACLE HDL NEEDS</div>
<div style="font-family:monospace;font-size:14px;font-weight:700;color:#D4622B;margin-top:4px;">Person# 100045</div>
<div style="font-family:monospace;font-size:14px;font-weight:700;color:#D4622B;">Assignment# E12345</div>
</div>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Two value sets do this translation:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;font-weight:700;color:#D4622B;">XXVA_GET_PERSON_NUMBER</td>
<td style="padding:8px 10px;">Takes SSN + Date → returns Person Number (100045)</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;font-weight:700;color:#D4622B;">XXVA_GET_LATEST_ASSIGNMENT_NUMBER</td>
<td style="padding:8px 10px;">Takes SSN + Date → returns Assignment Number (E12345)</td>
</tr>
</tbody></table>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">That's the simple version. But there's a performance problem.</p>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Problem: Same SSN, Three Rows, Three Identical DB Calls</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">One employee can have multiple rows in the vendor file — one per benefit plan. If an employee has 3 benefit plans (Dental, Medical, Vision), the file has 3 rows with the <strong>same SSN</strong>. Without optimization, the formula calls the value set 3 times for the exact same SSN and gets the exact same answer 3 times.</p>

<!-- VISUAL: The waste -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#fff;padding:10px 16px;border-bottom:1px solid #DDD8D0;font-weight:700;font-size:13px;color:#D4622B;">Without caching — 3 rows, same SSN</div>
<div style="padding:14px 16px;background:#fff;font-size:13px;line-height:2;">
<strong>Row 1 (DENTAL01):</strong> SSN 123-45-6789 → <span style="color:#D4622B;">call DB</span> → Person# 100045 <span style="color:#2D8B6F;font-weight:700;">[OK]</span><br>
<strong>Row 2 (MEDICAL01):</strong> SSN 123-45-6789 → <span style="color:#D4622B;">call DB again</span> → Person# 100045 <span style="color:#D4622B;">← same SSN, wasted call</span><br>
<strong>Row 3 (VISION01):</strong> SSN 123-45-6789 → <span style="color:#D4622B;">call DB again</span> → Person# 100045 <span style="color:#D4622B;">← same SSN, wasted call</span>
</div>
</div>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Fix: Cache with WSA</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula uses WSA to remember the answer (explained in the WSA Deep Dive after Step 4). The logic is simple:</p>

<div style="display:flex;gap:12px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:220px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:14px;text-align:center;">
<div style="background:#D4622B;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;margin:0 auto 4px;box-shadow:0 2px 8px rgba(212,98,43,0.25);">1</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">Did I already look up this SSN?</div>
<div style="font-family:monospace;font-size:13px;color:#8B8FA8;margin-top:6px;">WSA_EXISTS('PER_123-45-6789_2024-01-15')</div>
</div>
<div style="flex:1;min-width:220px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:14px;text-align:center;">
<div style="background:#D4622B;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;margin:0 auto 4px;">2a</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">YES → Read from cache</div>
<div style="font-family:monospace;font-size:13px;color:#8B8FA8;margin-top:6px;">WSA_GET('PER_123-45-6789_2024-01-15', ' ')<br>→ 100045. Done. No DB call.</div>
</div>
<div style="flex:1;min-width:220px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;padding:14px;text-align:center;">
<div style="background:#D4622B;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;margin:0 auto 4px;">2b</div>
<div style="font-weight:700;font-size:13px;color:#D4622B;">NO → Call DB, then save to cache</div>
<div style="font-family:monospace;font-size:13px;color:#8B8FA8;margin-top:6px;">GET_VALUE_SET(...) → 100045<br>WSA_SET('PER_123-45-6789_2024-01-15', 100045)</div>
</div>
</div>

<!-- VISUAL: After caching — 3 rows -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#fff;padding:10px 16px;border-bottom:1px solid #DDD8D0;font-weight:700;font-size:13px;color:#D4622B;">With WSA caching — same 3 rows, same SSN</div>
<div style="padding:14px 16px;background:#fff;font-size:13px;line-height:2;">
<strong>Row 1 (DENTAL01):</strong> WSA_EXISTS? <strong>NO</strong> → <span style="color:#D4622B;">call DB</span> → 100045 → <span style="color:#D4622B;">WSA_SET (save it)</span> <span style="color:#2D8B6F;font-weight:700;">[OK]</span><br>
<strong>Row 2 (MEDICAL01):</strong> WSA_EXISTS? <strong>YES</strong> → <span style="color:#D4622B;">WSA_GET → 100045. Zero DB calls.</span> <span style="color:#2D8B6F;font-weight:700;">[OK]</span><br>
<strong>Row 3 (VISION01):</strong> WSA_EXISTS? <strong>YES</strong> → <span style="color:#D4622B;">WSA_GET → 100045. Zero DB calls.</span> <span style="color:#2D8B6F;font-weight:700;">[OK]</span>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's what the actual code looks like:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Build a unique WSA key from SSN + Date */</span>
<span style="color:#57A64A;font-style:italic;">/* e.g. 'PER_123-45-6789_2024-01-15' */</span>

<span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">WSA_EXISTS</span>(<span style="color:#CE9178;">'PER_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* Cache hit — read stored values */</span>
    <span style="color:#B5CEA8;">L_PersonNumber</span>     = <span style="color:#DCDCAA;">WSA_GET</span>(<span style="color:#CE9178;">'PER_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#CE9178;">' '</span>)
    <span style="color:#B5CEA8;">l_AssignmentNumber</span> = <span style="color:#DCDCAA;">WSA_GET</span>(<span style="color:#CE9178;">'ASG_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#CE9178;">' '</span>)
)
<span style="color:#fff;font-weight:700;">ELSE</span>
(
    <span style="color:#57A64A;font-style:italic;">/* Cache miss — call value sets (hits DB) */</span>
    <span style="color:#B5CEA8;">l_AssignmentNumber</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_GET_LATEST_ASSIGNMENT_NUMBER'</span>, ...)
    <span style="color:#B5CEA8;">L_PersonNumber</span>     = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_GET_PERSON_NUMBER'</span>, ...)

    <span style="color:#57A64A;font-style:italic;">/* Save to WSA — next row with same SSN skips DB */</span>
    <span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#CE9178;">'PER_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#B5CEA8;">L_PersonNumber</span>)
    <span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#CE9178;">'ASG_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#B5CEA8;">l_AssignmentNumber</span>)
)</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After Step 3: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">L_PersonNumber = '100045'</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_AssignmentNumber = 'E12345'</code></p>

<!-- STEP 4 -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 4: MultipleEntryCount</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 4 uses: L_PersonNumber + l_ElementName + POSITION2 (Date)</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;font-family:monospace;">
<td style="padding:6px 0;width:50%;color:#8B8FA8;">Person <span style="color:#3D3D5C;font-weight:700;">100045</span> + Element <span style="color:#3D3D5C;font-weight:700;">Dental EE Deduction</span> + Date <span style="color:#3D3D5C;font-weight:700;">2024-01-15</span></td>
<td style="padding:6px 0;">→ l_MultipleEntryCount = <span style="color:#D4622B;font-weight:700;">1</span> (or 2, 3... if entries already exist)</td>
</tr>
</table>
</div>
</div>


<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">What Is It?</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">When the same person has multiple entries of the <strong>same element</strong> in the <strong>same payroll period</strong>, Oracle needs a sequence number to tell them apart. That number is MultipleEntryCount.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">When does this happen in the vendor interface? Each pay period, the vendor sends a new deduction file. If person 100045 already has a Dental EE Deduction entry from a previous load, and this batch sends another one (maybe a mid-period adjustment), the new entry needs a higher count.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">If you know SQL, it's this:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#DCDCAA;">ROW_NUMBER</span>() <span style="color:#fff;font-weight:700;">OVER</span> (<span style="color:#fff;font-weight:700;">PARTITION BY</span> <span style="color:#C8C8C8;">person</span>, <span style="color:#C8C8C8;">element</span>, <span style="color:#C8C8C8;">payroll_period</span>)  =  MultipleEntryCount</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's what it looks like in <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PAY_ELEMENT_ENTRIES_F</code> after multiple loads:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:6px 8px;">Person#</th>
<th style="padding:6px 8px;">Element</th>
<th style="padding:6px 8px;">EffectiveStartDate</th>
<th style="padding:6px 8px;">Amount</th>
<th style="padding:6px 8px;">MultipleEntryCount</th>
<th style="padding:6px 8px;">Source</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;">100045</td>
<td style="padding:6px 8px;">Dental EE Deduction</td>
<td style="padding:6px 8px;font-family:monospace;">2024-01-15</td>
<td style="padding:6px 8px;font-family:monospace;">$150.00</td>
<td style="padding:6px 8px;text-align:center;font-weight:800;font-size:18px;color:#D4622B;">1</td>
<td style="padding:6px 8px;font-size:13px;color:#8B8FA8;">January batch</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;">100045</td>
<td style="padding:6px 8px;">Dental EE Deduction</td>
<td style="padding:6px 8px;font-family:monospace;">2024-01-20</td>
<td style="padding:6px 8px;font-family:monospace;">$25.00</td>
<td style="padding:6px 8px;text-align:center;font-weight:800;font-size:18px;color:#D4622B;">2</td>
<td style="padding:6px 8px;font-size:13px;color:#8B8FA8;">Mid-period adjustment</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;">100045</td>
<td style="padding:6px 8px;font-weight:700;color:#D4622B;">Medical EE Deduction</td>
<td style="padding:6px 8px;font-family:monospace;">2024-01-15</td>
<td style="padding:6px 8px;font-family:monospace;">$200.00</td>
<td style="padding:6px 8px;text-align:center;font-weight:800;font-size:18px;color:#D4622B;">1</td>
<td style="padding:6px 8px;font-size:13px;color:#8B8FA8;">← different element, count resets to 1</td>
</tr>
</tbody></table>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The partition key is <strong>Person + Element + Payroll Period</strong>. Same person + same element = same group, count increments. Different element = new group, count resets to 1. If two entries in the same group get the <strong>same</strong> count, Oracle overwrites the first one — data is lost.</p>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Problem: Fast Formula Has No Memory</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">In PL/SQL, you'd do this in a loop. The counter variable lives across iterations:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">-- PL/SQL: variable persists across loop iterations</span>
<span style="color:#B5CEA8;">l_counter</span> := <span style="color:#DCDCAA;">0</span>;
<span style="color:#fff;font-weight:700;">FOR</span> <span style="color:#B5CEA8;">rec</span> <span style="color:#fff;font-weight:700;">IN</span> <span style="color:#C8C8C8;">cursor</span> <span style="color:#fff;font-weight:700;">LOOP</span>
    <span style="color:#B5CEA8;">l_counter</span> := <span style="color:#B5CEA8;">l_counter</span> + <span style="color:#DCDCAA;">1</span>;
    <span style="color:#57A64A;font-style:italic;">-- Row 1: l_counter = 1</span>
    <span style="color:#57A64A;font-style:italic;">-- Row 2: l_counter = 2  ← remembers what happened in Row 1</span>
<span style="color:#fff;font-weight:700;">END LOOP</span>;</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Fast Formula is <strong>not</strong> a loop. The HDL engine calls the formula once per row as a <strong>separate, independent invocation</strong>. All local variables are destroyed after each call. It's like calling a standalone function 10,000 times — each call starts from zero with no memory of the previous call.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">So the formula has to ask the database: <em>"What's the highest count that already exists?"</em> The value set runs something like this behind the scenes against <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PAY_ELEMENT_ENTRIES_F</code>:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">SELECT</span> <span style="color:#DCDCAA;">MAX</span>(<span style="color:#C8C8C8;">pee.MULTIPLE_ENTRY_COUNT</span>) 
<span style="color:#fff;font-weight:700;">FROM</span>   <span style="color:#C8C8C8;">PAY_ELEMENT_ENTRIES_F</span>  <span style="color:#B5CEA8;">pee</span>
      ,<span style="color:#C8C8C8;">PAY_ELEMENT_TYPES_F</span>    <span style="color:#B5CEA8;">pet</span>
      ,<span style="color:#C8C8C8;">PER_ALL_ASSIGNMENTS_M</span>  <span style="color:#B5CEA8;">paam</span>
<span style="color:#fff;font-weight:700;">WHERE</span>  <span style="color:#B5CEA8;">pee</span>.<span style="color:#C8C8C8;">ELEMENT_TYPE_ID</span>  = <span style="color:#B5CEA8;">pet</span>.<span style="color:#C8C8C8;">ELEMENT_TYPE_ID</span>
<span style="color:#fff;font-weight:700;">AND</span>    <span style="color:#B5CEA8;">pee</span>.<span style="color:#C8C8C8;">PERSON_ID</span>         = <span style="color:#B5CEA8;">paam</span>.<span style="color:#C8C8C8;">PERSON_ID</span>
<span style="color:#fff;font-weight:700;">AND</span>    <span style="color:#B5CEA8;">pet</span>.<span style="color:#C8C8C8;">ELEMENT_NAME</span>      = <span style="color:#CE9178;">'Dental EE Deduction'</span>
<span style="color:#fff;font-weight:700;">AND</span>    <span style="color:#B5CEA8;">paam</span>.<span style="color:#C8C8C8;">PERSON_NUMBER</span>    = <span style="color:#CE9178;">'100045'</span>
<span style="color:#fff;font-weight:700;">AND</span>    <span style="color:#CE9178;">'2024-10-15'</span> <span style="color:#fff;font-weight:700;">BETWEEN</span> <span style="color:#B5CEA8;">pee</span>.<span style="color:#C8C8C8;">EFFECTIVE_START_DATE</span> <span style="color:#fff;font-weight:700;">AND</span> <span style="color:#B5CEA8;">pee</span>.<span style="color:#C8C8C8;">EFFECTIVE_END_DATE</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">This works fine when each batch has only one row per person+element. But what if the batch has two?</p>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Bug: Two Rows Read the Same Stale MAX</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's what's already in <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PAY_ELEMENT_ENTRIES_F</code> from last month's load:</p>

<!-- EXISTING DATA IN TABLE -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">PAY_ELEMENT_ENTRIES_F — existing data in cloud</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<thead><tr style="background:#F5F3EF;">
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;font-weight:700;color:#D4622B;">ELEMENT_ENTRY_ID</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">PERSON_ID</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">ELEMENT_TYPE_ID</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">EFFECTIVE_START_DATE</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">MULTIPLE_ENTRY_COUNT</th>
<th style="padding:6px 8px;text-align:left;white-space:nowrap;font-size:10px;color:#D4622B;">ENTRY_TYPE</th>
</tr></thead>
<tbody>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-family:monospace;">300000012345</td>
<td style="padding:8px 10px;font-family:monospace;">100045</td>
<td style="padding:8px 10px;font-family:monospace;">50001 <span style="color:#8B8FA8;font-size:13px;">(Dental EE Deduction)</span></td>
<td style="padding:8px 10px;font-family:monospace;">01-Oct-2024</td>
<td style="padding:8px 10px;font-weight:800;font-size:15px;color:#D4622B;text-align:center;">1</td>
<td style="padding:8px 10px;font-family:monospace;">E</td>
</tr>
</tbody></table>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Now our vendor batch has two new Dental EE Deduction rows for the same person. The formula runs <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">SELECT MAX(MULTIPLE_ENTRY_COUNT)</code> for each — but the problem is Row 5's INSERT hasn't reached the table yet when Row 8 queries it:</p>

<!-- RED: Without WSA -->
<div style="margin:18px 0;border-radius:10px;overflow:hidden;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);">
<div style="background:#C13B3B;padding:12px 20px;color:#fff;font-weight:800;font-size:15px;"><span style="background:#fff;color:#C13B3B;padding:2px 8px;border-radius:4px;font-size:13px;margin-right:6px;">FAIL</span> WITHOUT WSA</div>
<div style="padding:20px;background:#fff;">

<div style="font-weight:700;font-size:14px;color:#3D3D5C;margin-bottom:10px;">Row 5 processes — formula queries the table:</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">SELECT</span> <span style="color:#DCDCAA;">MAX</span>(<span style="color:#C8C8C8;">MULTIPLE_ENTRY_COUNT</span>) <span style="color:#fff;font-weight:700;">FROM</span> <span style="color:#C8C8C8;">PAY_ELEMENT_ENTRIES_F</span>
<span style="color:#fff;font-weight:700;">WHERE</span> PERSON_ID = <span style="color:#DCDCAA;">100045</span> <span style="color:#fff;font-weight:700;">AND</span> ELEMENT_TYPE_ID = <span style="color:#DCDCAA;">50001</span>  <span style="color:#57A64A;font-style:italic;">→ Returns 1</span></pre>
<p style="font-size:14px;margin:0 0 16px;">Formula assigns: 1 + 1 = <span style="background:#C13B3B;color:#fff;padding:3px 12px;border-radius:12px;font-weight:800;font-size:15px;">2</span>   <span style="color:#8B8FA8;font-size:13px;">← this row is still in the HDL batch, NOT yet inserted into PAY_ELEMENT_ENTRIES_F</span></p>

<div style="font-weight:700;font-size:14px;color:#3D3D5C;margin-bottom:10px;">Row 8 processes — formula queries the SAME table:</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">SELECT</span> <span style="color:#DCDCAA;">MAX</span>(<span style="color:#C8C8C8;">MULTIPLE_ENTRY_COUNT</span>) <span style="color:#fff;font-weight:700;">FROM</span> <span style="color:#C8C8C8;">PAY_ELEMENT_ENTRIES_F</span>
<span style="color:#fff;font-weight:700;">WHERE</span> PERSON_ID = <span style="color:#DCDCAA;">100045</span> <span style="color:#fff;font-weight:700;">AND</span> ELEMENT_TYPE_ID = <span style="color:#DCDCAA;">50001</span>  <span style="color:#57A64A;font-style:italic;">→ STILL returns 1!</span></pre>
<p style="font-size:14px;margin:0 0 16px;">Formula assigns: 1 + 1 = <span style="background:#C13B3B;color:#fff;padding:3px 12px;border-radius:12px;font-weight:800;font-size:15px;">2</span>   <span style="color:#C13B3B;font-size:13px;font-weight:700;">← SAME count as Row 5!</span></p>

<p style="font-size:14px;margin:0 0 12px;">What the generated .dat file looks like — both rows got the same count:</p>

<div style="border:1px solid #DDD8D0;border-radius:6px;overflow:hidden;">
<div style="background:#1B4965;color:#fff;padding:8px 14px;font-weight:700;font-size:12px;">ElementEntry.dat — FAIL output</div>
<div style="background:#1E1E1E;padding:8px 10px;">
<div style="font-size:12px;color:#8E8680;margin-bottom:8px;">Existing entry (already in Oracle):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:5px 10px;color:#8E8680;width:35%;">ElementName</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:5px 10px;color:#8B8FA8;">MultipleEntryCount</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">1</td>
</tr>
</table>

<div style="font-size:12px;color:#C13B3B;margin-bottom:8px;font-weight:700;">Row 5 output ($175.00):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:5px 10px;color:#8E8680;width:35%;">ElementName</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:5px 10px;color:#8B8FA8;">MultipleEntryCount</td><td style="padding:5px 10px;color:#C13B3B;font-family:monospace;font-weight:700;font-size:16px;">2</td>
</tr>
</table>

<div style="font-size:12px;color:#C13B3B;margin-bottom:8px;font-weight:700;">Row 8 output ($200.00) — SAME count!</div>
__DARK_0__
</div>
</div>

<div style="background:#FCF0F0;border:1px solid #DDD8D0;border-radius:8px;padding:12px 18px;text-align:center;margin-top:12px;">
<span style="font-size:15px;font-weight:800;color:#C13B3B;"><strong>BUG:</strong> Two rows in the .dat file with MultipleEntryCount = 2. When Oracle loads this file, Row 8 overwrites Row 5. $175.00 entry is lost.</span>
</div>

</div>
</div>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Fix: WSA Tracks What the Table Can't See Yet</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">WSA acts as an in-memory counter that survives between formula calls. Row 5 saves its assigned count to WSA. When Row 8 runs, it reads from WSA instead of querying the table:</p>

<!-- GREEN: With WSA -->
<div style="margin:18px 0;border-radius:10px;overflow:hidden;border:1px solid #D4622B;box-shadow:0 2px 8px rgba(212,98,43,0.1);">
<div style="background:#D4622B;padding:12px 20px;color:#fff;font-weight:800;font-size:15px;"><span style="background:#fff;color:#2D8B6F;padding:2px 8px;border-radius:4px;font-size:13px;margin-right:6px;">PASS</span> WITH WSA</div>
<div style="padding:20px;background:#fff;">

<table style="width:100%;border-collapse:collapse;font-size:12px;">
<thead><tr style="background:#F5F3EF;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;font-weight:700;">Row</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;font-weight:700;">WSA has data?</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Source of MAX</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Assigns</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Saves to WSA</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">Row 5</td>
<td style="padding:8px 10px;">NO</td>
<td style="padding:8px 10px;font-size:13px;">PAY_ELEMENT_ENTRIES_F → MAX = 1</td>
<td style="padding:8px 10px;"><span style="background:#D4622B;color:#fff;padding:3px 12px;border-radius:12px;font-weight:800;">2</span></td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;color:#D4622B;">WSA_SET(2)</td>
</tr>
<tr>
<td style="padding:8px 10px;font-weight:700;">Row 8</td>
<td style="padding:8px 10px;font-weight:700;color:#D4622B;">YES → 2</td>
<td style="padding:8px 10px;font-size:13px;color:#D4622B;">WSA memory (skips table)</td>
<td style="padding:8px 10px;"><span style="background:#D4622B;color:#fff;padding:3px 12px;border-radius:12px;font-weight:800;">3</span></td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;color:#D4622B;">WSA_SET(3)</td>
</tr>
</tbody></table>

<p style="font-size:14px;margin:12px 0 0;">What the .dat file looks like — each row gets a unique count:</p>

<div style="border:1px solid #DDD8D0;border-radius:6px;overflow:hidden;margin-top:8px;">
<div style="background:#1B4965;color:#fff;padding:8px 14px;font-weight:700;font-size:12px;">ElementEntry.dat — PASS output</div>
<div style="background:#1E1E1E;padding:8px 10px;">
<div style="font-size:12px;color:#8E8680;margin-bottom:8px;">Existing entry (already in Oracle):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:5px 10px;color:#8E8680;width:35%;">ElementName</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:5px 10px;color:#8B8FA8;">MultipleEntryCount</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">1</td>
</tr>
</table>

<div style="font-size:12px;color:#2D8B6F;margin-bottom:8px;font-weight:700;">Row 5 output ($175.00):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:5px 10px;color:#8E8680;width:35%;">ElementName</td><td style="padding:5px 10px;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:5px 10px;color:#8B8FA8;">MultipleEntryCount</td><td style="padding:5px 10px;color:#2D8B6F;font-family:monospace;font-weight:700;font-size:16px;">2 <span style="font-size:12px;font-weight:400;color:#2D8B6F;">[OK]</span></td>
</tr>
</table>

<div style="font-size:12px;color:#2D8B6F;margin-bottom:8px;font-weight:700;">Row 8 output ($200.00):</div>
__DARK_1__
</div>
</div>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-radius:8px;padding:12px 18px;text-align:center;margin-top:12px;">
<span style="font-size:15px;font-weight:800;color:#D4622B;"><span style="background:#2D8B6F;color:#fff;padding:2px 8px;border-radius:4px;font-size:12px;margin-right:4px;">PASS</span> Three unique MultipleEntryCount values (1, 2, 3) in the .dat file. Oracle loads all three entries successfully.</span>
</div>

</div>
</div>

<div style="font-size:15px;font-weight:700;color:#3D3D5C;margin:24px 0 12px;padding-left:14px;border-left:3px solid #DDD8D0;">The Fast Formula Code</div>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Check: did a previous row already assign a count for this combo? */</span>
<span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">WSA_EXISTS</span>(<span style="color:#CE9178;">'MEC_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* YES — read last assigned count and add 1 */</span>
    <span style="color:#B5CEA8;">l_MultipleEntryCount</span> = <span style="color:#DCDCAA;">WSA_GET</span>(<span style="color:#CE9178;">'MEC_'</span> || ..., <span style="color:#DCDCAA;">0</span>) + <span style="color:#DCDCAA;">1</span>
)
<span style="color:#fff;font-weight:700;">ELSE</span>
(
    <span style="color:#57A64A;font-style:italic;">/* NO — first row for this combo. Ask the database. */</span>
    <span style="color:#B5CEA8;">l_db_max</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'MAX_MULTI_ENTRY_COUNT'</span>, ...)

    <span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">ISNULL</span>(<span style="color:#B5CEA8;">l_db_max</span>) = <span style="color:#CE9178;">'N'</span> <span style="color:#fff;font-weight:700;">THEN</span>
        <span style="color:#B5CEA8;">l_MultipleEntryCount</span> = <span style="color:#DCDCAA;">1</span>              <span style="color:#57A64A;font-style:italic;">/* Nothing in cloud → start at 1 */</span>
    <span style="color:#fff;font-weight:700;">ELSE</span>
        <span style="color:#B5CEA8;">l_MultipleEntryCount</span> = <span style="color:#B5CEA8;">l_db_max</span> + <span style="color:#DCDCAA;">1</span>  <span style="color:#57A64A;font-style:italic;">/* Cloud has 1 → assign 2 */</span>
)

<span style="color:#57A64A;font-style:italic;">/* Save what we assigned — next row reads this instead of hitting DB */</span>
<span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#CE9178;">'MEC_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>, <span style="color:#B5CEA8;">l_MultipleEntryCount</span>)</pre>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#D4622B;"><strong>Summary in one line:</strong> WSA is a working storage area that persists across formula invocations — like a PL/SQL package variable. The formula writes the assigned count to WSA, so the next row with the same combo reads from memory instead of hitting a stale database. The formula writes the assigned count to WSA, so the next row with the same combo reads from memory instead of hitting a stale database.</p>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After Step 4: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_MultipleEntryCount = 2</code> (cloud had 1, so we assigned 1 + 1)</p>

<!-- ==================== WSA BRIDGE ==================== -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">WSA in This Formula — Connecting Step 3 and Step 4</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">You've now seen WSA used twice in the MAP block, but for <strong>two completely different reasons</strong>. Let's connect them before moving to Step 5.</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:15%;">Step</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:25%;">WSA Key</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:25%;">What It Stores</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:15%;">Why</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:20%;">What Breaks Without It</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">Step 3</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">PER_<SSN>_<Date><br>ASG_<SSN>_<Date></td>
<td style="padding:8px 10px;">Person Number<br>Assignment Number</td>
<td style="padding:8px 10px;font-weight:700;color:#D4622B;">Performance</td>
<td style="padding:8px 10px;font-size:13px;">Same SSN queried 3x instead of 1x. Slow but correct.</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-weight:700;">Step 4</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">MEC_<Person>_<Element>_<Date></td>
<td style="padding:8px 10px;">Last assigned MultipleEntryCount</td>
<td style="padding:8px 10px;font-weight:700;color:#C13B3B;">Correctness</td>
<td style="padding:8px 10px;font-size:13px;color:#C13B3B;font-weight:600;">Duplicate MULTIPLE_ENTRY_COUNT in PAY_ELEMENT_ENTRIES_F. Data lost.</td>
</tr>
</tbody></table>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">This is the key distinction:</p>

<div style="display:flex;gap:16px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:280px;border:1px solid #DDD8D0;border-left:4px solid #D4622B;border-radius:0 8px 8px 0;padding:16px;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#D4622B;margin-bottom:8px;">Step 3 WSA = Cache</div>
<p style="margin:0 0 6px;font-size:12px;">Removes WSA from Step 3 → formula still <strong>works correctly</strong></p>
<p style="margin:0;font-size:12px;">It just runs <strong>slower</strong> (3 DB calls instead of 1 per SSN group)</p>
</div>
<div style="flex:1;min-width:280px;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);border-radius:8px;padding:16px;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#C13B3B;margin-bottom:8px;">Step 4 WSA = Required for Correct Data</div>
<p style="margin:0 0 6px;font-size:12px;">Remove WSA from Step 4 → formula <strong>produces wrong output</strong></p>
<p style="margin:0;font-size:12px;">Duplicate counts → rows overwrite each other in PAY_ELEMENT_ENTRIES_F</p>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Both use the same WSA methods (<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">WSA_EXISTS</code>, <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">WSA_GET</code>, <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">WSA_SET</code>), same pattern (check → hit or miss → store), but different purposes. Step 3 is optional optimization. Step 4 is mandatory for data integrity.</p>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== WSA DEEP DIVE ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">WSA Deep Dive — Working Storage Area</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">You've now seen WSA used in Step 3 and Step 4. Let's go deeper into how it works, what this formula caches, and one critical deployment rule you can't skip.</p>

<!-- WHAT IS WSA -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">What Is WSA?</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">WSA (Working Storage Area) is, per Oracle documentation, <strong>a mechanism for storing global values across formulas</strong>. Local variables die after each formula invocation, but WSA values persist across calls within the same session. You write a value on Row 1, and you can read it back on Row 500. WSA names are <strong>case-independent</strong> — <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'PER_123'</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'per_123'</code> refer to the same item.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">In PL/SQL terms: WSA is a package-level associative array (<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">TABLE OF VARCHAR2 INDEX BY VARCHAR2</code>). It persists across function calls within the same session.</p>

<!-- THE API -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The API — Four Methods</div>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Method</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">PL/SQL Equivalent</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">What It Does</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;font-family:monospace;font-weight:700;color:#D4622B;white-space:nowrap;font-size:10px;">WSA_EXISTS(item [, type])</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">g_cache.EXISTS(key)</td>
<td style="padding:8px 10px;">Tests whether item exists in the storage area. Optional <code>type</code> parameter restricts to a specific data type (TEXT, NUMBER, DATE, TEXT_TEXT, TEXT_NUMBER, etc.)</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;font-family:monospace;font-weight:700;color:#D4622B;white-space:nowrap;font-size:10px;">WSA_GET(item, default-value)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">l_val := g_cache(key)</td>
<td style="padding:8px 10px;">Retrieves the stored value. If item doesn't exist, returns the <strong>default-value</strong> instead. The data type of default-value determines the expected data type.</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;font-family:monospace;font-weight:700;color:#D4622B;white-space:nowrap;font-size:10px;">WSA_SET(item, value)</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">g_cache(key) := val</td>
<td style="padding:8px 10px;">Sets the value for item. Any existing item of the same name is <strong>overwritten</strong>.</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:4px 5px;font-family:monospace;font-weight:700;color:#D4622B;white-space:nowrap;font-size:10px;">WSA_DELETE([item])</td>
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">g_cache.DELETE(key)</td>
<td style="padding:8px 10px;">Deletes item from storage. If no name specified, <strong>all storage area data is deleted</strong>. Not used in this vendor formula, but important for cleanup scenarios.</td>
</tr>
</tbody></table>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#3D3D5C;"><strong>Key detail from Oracle docs:</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">WSA_GET</code> always requires a <strong>default-value</strong> parameter. The formula always calls <code>WSA_EXISTS</code> first and only calls <code>WSA_GET</code> when the item is known to exist — so the default is never actually used, but it must still be provided. The data type of the default tells the engine what data type to expect.</p>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Every WSA usage in this formula follows the same pattern. You already saw it twice:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* THE PATTERN — same in Step 3, Step 4, and everywhere else */</span>

<span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">WSA_EXISTS</span>(<span style="color:#B5CEA8;">l_key</span>) <span style="color:#fff;font-weight:700;">THEN</span>            <span style="color:#57A64A;font-style:italic;">/* 1. Check memory */</span>
    <span style="color:#B5CEA8;">l_value</span> = <span style="color:#DCDCAA;">WSA_GET</span>(<span style="color:#B5CEA8;">l_key</span>, <span style="color:#CE9178;">' '</span>)    <span style="color:#57A64A;font-style:italic;">/* 2a. HIT  — read from memory (default never used) */</span>
<span style="color:#fff;font-weight:700;">ELSE</span>
    <span style="color:#B5CEA8;">l_value</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(...)      <span style="color:#57A64A;font-style:italic;">/* 2b. MISS — call the database */</span>
    <span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#B5CEA8;">l_key</span>, <span style="color:#B5CEA8;">l_value</span>)          <span style="color:#57A64A;font-style:italic;">/* 3.  SAVE — store for next row */</span></pre>

<!-- WHERE YOU ALREADY SAW THIS -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Where You Already Saw This Pattern</div>

<div style="display:flex;gap:16px;margin:18px 0;flex-wrap:wrap;">
<!-- STEP 3 RECAP -->
<div style="flex:1;min-width:300px;border:1px solid #DDD8D0;border-left:4px solid #D4622B;border-radius:0 8px 8px 0;padding:16px;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#D4622B;margin-bottom:10px;">Step 3 — Person & Assignment Lookup</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:8px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Key:</td>
<td style="padding:4px 0;font-family:monospace;">'PER_123-45-6789_2024-01-15'</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Stores:</td>
<td style="padding:4px 0;">Person Number (100045)</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">DB call saved:</td>
<td style="padding:4px 0;">GET_VALUE_SET('XXVA_GET_PERSON_NUMBER')</td>
</tr>
<tr>
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Purpose:</td>
<td style="padding:4px 0;font-weight:700;color:#D4622B;">Performance — same SSN in 3 rows, only 1 DB call</td>
</tr>
</table>
</div>
<!-- STEP 4 RECAP -->
<div style="flex:1;min-width:300px;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);border-radius:8px;padding:16px;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#C13B3B;margin-bottom:10px;">Step 4 — MultipleEntryCount</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:8px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Key:</td>
<td style="padding:4px 0;font-family:monospace;">'MEC_100045_Dental EE Deduction_2024-01-15'</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Stores:</td>
<td style="padding:4px 0;">Last assigned count (2, then 3, then 4...)</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">DB call saved:</td>
<td style="padding:4px 0;">GET_VALUE_SET('MAX_MULTI_ENTRY_COUNT')</td>
</tr>
<tr>
<td style="padding:4px 0;color:#8B8FA8;font-weight:600;">Purpose:</td>
<td style="padding:4px 0;font-weight:700;color:#C13B3B;">Correctness — prevents duplicate MULTIPLE_ENTRY_COUNT</td>
</tr>
</table>
</div>
</div>

<!-- ALL WSA KEYS -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">All WSA Keys This Formula Uses</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Steps 3 and 4 are the two main ones, but the formula caches more. Here's the complete list:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">WSA Key</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Stores</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Used In</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Type</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">PER_<SSN>_<Date></td>
<td style="padding:8px 10px;">Person Number</td>
<td style="padding:8px 10px;font-weight:700;">Step 3</td>
<td style="padding:8px 10px;color:#D4622B;font-weight:600;">Performance</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">ASG_<SSN>_<Date></td>
<td style="padding:8px 10px;">Assignment Number</td>
<td style="padding:8px 10px;font-weight:700;">Step 3</td>
<td style="padding:8px 10px;color:#D4622B;font-weight:600;">Performance</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">MEC_<Person>_<Element>_<Date></td>
<td style="padding:8px 10px;">Last assigned MultipleEntryCount</td>
<td style="padding:8px 10px;font-weight:700;">Step 4</td>
<td style="padding:8px 10px;color:#C13B3B;font-weight:700;">Correctness</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">SSID_, SSO_, EEVID_, EEVO_</td>
<td style="padding:8px 10px;">SourceSystemId/Owner lookups</td>
<td style="padding:8px 10px;font-weight:700;">Step 5</td>
<td style="padding:8px 10px;color:#D4622B;font-weight:600;">Performance</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-family:monospace;font-size:11px;">HDR_<Person>_<Element>_<Date></td>
<td style="padding:8px 10px;">Flag: ElementEntry header already generated</td>
<td style="padding:8px 10px;font-weight:700;">Section 7</td>
<td style="padding:8px 10px;color:#C13B3B;font-weight:700;">Correctness</td>
</tr>
</tbody></table>

<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0;font-size:14px;color:#D4622B;"><strong>Pattern:</strong> Performance keys (PER_, ASG_, SSID_) can be removed and the formula still works — just slower. Correctness keys (MEC_, HDR_) cannot be removed — the formula produces wrong data without them.</p>
</div>

<!-- TRACED EXAMPLE -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Traced Example: 3 Benefit Plan Rows, Same Employee</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Watch Step 3 and Step 4 WSA caching in action across three rows for SSN 123-45-6789:</p>

<!-- SOURCE ROWS REFERENCE -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;color:#fff;padding:12px 18px;font-weight:700;font-size:13px;">Vendor Input File — 3 rows for the same employee (SSN 123-45-6789)</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<thead><tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#3D3D5C;width:15%;">Row</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS1 (SSN)</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS2 (Date)</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS3 (Plan)</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS4 (Type)</th>
<th style="padding:8px 14px;text-align:left;white-space:nowrap;font-weight:700;color:#D4622B;">POS5 (Amt)</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-weight:800;color:#D4622B;">Row 1</td>
<td style="padding:8px 14px;font-family:monospace;">123-45-6789</td>
<td style="padding:8px 14px;font-family:monospace;">2024-01-15</td>
<td style="padding:8px 14px;font-family:monospace;font-weight:700;">DENTAL01</td>
<td style="padding:8px 14px;font-family:monospace;">PRE</td>
<td style="padding:8px 14px;font-family:monospace;">150.00</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 14px;font-weight:800;color:#D4622B;">Row 2</td>
<td style="padding:8px 14px;font-family:monospace;">123-45-6789</td>
<td style="padding:8px 14px;font-family:monospace;">2024-01-15</td>
<td style="padding:8px 14px;font-family:monospace;font-weight:700;">MEDICAL01</td>
<td style="padding:8px 14px;font-family:monospace;">PRE</td>
<td style="padding:8px 14px;font-family:monospace;">75.50</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 14px;font-weight:800;color:#D4622B;">Row 3</td>
<td style="padding:8px 14px;font-family:monospace;">123-45-6789</td>
<td style="padding:8px 14px;font-family:monospace;">2024-01-15</td>
<td style="padding:8px 14px;font-family:monospace;font-weight:700;">VISION01</td>
<td style="padding:8px 14px;font-family:monospace;">PRE</td>
<td style="padding:8px 14px;font-family:monospace;">12.30</td>
</tr>
</tbody></table>
<div style="padding:10px 18px;background:#FDF5ED;font-size:13px;color:#8B8FA8;">
Same SSN, same date — but <strong style="color:#3D3D5C;">different benefit plans</strong>. This is typical: one employee enrolled in Dental + Medical + Vision.
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Now let's trace what happens when the formula processes each row:</p>

<!-- ==================== ROW 1 ==================== -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:12px 18px;font-weight:800;font-size:12px;">ROW 1 — DENTAL01, PRE, $150.00</div>
<div style="padding:0;">

<!-- Step 3 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 3</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">Person & Assignment Lookup</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('PER_123-45-6789_2024-01-15')</td>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;width:15%;text-align:center;">MISS</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;" colspan="2">Call DB → Person# = <strong>100045</strong>, Asg# = <strong>E12345</strong></td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">WSA Save</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;color:#D4622B;" colspan="2">WSA_SET('PER_...', 100045)   WSA_SET('ASG_...', E12345)</td>
</tr>
</table>
</div>

<!-- Step 4 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 4</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">MultipleEntryCount</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('MEC_100045_Dental EE Deduction_2024')</td>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;width:15%;text-align:center;">MISS</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;" colspan="2">Call DB → MAX = NULL (no existing entry)</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Result</td>
<td style="padding:6px 8px;" colspan="2">MultipleEntryCount = <span style="background:#D4622B;color:#fff;padding:2px 10px;border-radius:10px;font-weight:800;">1</span>   → WSA_SET('MEC_...Dental...', 1)</td>
</tr>
</table>
</div>

<!-- Summary -->
<div style="padding:10px 18px;background:#FDF5ED;font-size:13px;color:#8B8FA8;">
DB calls: <strong style="color:#3D3D5C;">11</strong> — all cache misses (first time seeing this SSN)
</div>

</div>
</div>

<!-- ==================== ROW 2 ==================== -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:12px 18px;font-weight:800;font-size:12px;">ROW 2 — MEDICAL01, PRE, $75.50</div>
<div style="padding:0;">

<!-- Step 3 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 3</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">Person & Assignment Lookup</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('PER_123-45-6789_2024-01-15')</td>
<td style="padding:6px 8px;font-weight:700;color:#2D8B6F;width:15%;text-align:center;">HIT!</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;color:#2D8B6F;font-weight:600;" colspan="2">WSA_GET → Person# 100045, Asg# E12345 — zero DB calls</td>
</tr>
</table>
</div>

<!-- Step 4 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 4</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">MultipleEntryCount</span>
<span style="font-size:12px;color:#8B8FA8;font-style:italic;">— different element name = new WSA key</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('MEC_100045_<strong>Medical</strong> EE Deduction_2024')</td>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;width:15%;text-align:center;">MISS</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;" colspan="2">Call DB → MAX = NULL</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Result</td>
<td style="padding:6px 8px;" colspan="2">MultipleEntryCount = <span style="background:#D4622B;color:#fff;padding:2px 10px;border-radius:10px;font-weight:800;">1</span>   → WSA_SET('MEC_...Medical...', 1)</td>
</tr>
</table>
</div>

<!-- Summary -->
<div style="padding:10px 18px;background:#FDF5ED;font-size:13px;color:#8B8FA8;">
DB calls: <strong style="color:#3D3D5C;">4</strong> — Step 3 saved 2 calls (cache hit), Step 4 missed (different element)
</div>

</div>
</div>

<!-- ==================== ROW 3 ==================== -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:12px 18px;font-weight:800;font-size:12px;">ROW 3 — VISION01, PRE, $12.30</div>
<div style="padding:0;">

<!-- Step 3 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 3</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">Person & Assignment Lookup</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('PER_123-45-6789_2024-01-15')</td>
<td style="padding:6px 8px;font-weight:700;color:#2D8B6F;width:15%;text-align:center;">HIT!</td>
</tr>
<tr style="background:#fff;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;color:#2D8B6F;font-weight:600;" colspan="2">WSA_GET → Person# 100045, Asg# E12345 — zero DB calls</td>
</tr>
</table>
</div>

<!-- Step 4 -->
<div style="padding:14px 18px;border-bottom:1px solid #DDD8D0;">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
<span style="background:#D4622B;color:#fff;padding:4px 10px;border-radius:4px;font-weight:800;font-size:12px;">STEP 4</span>
<span style="font-weight:700;font-size:14px;color:#3D3D5C;">MultipleEntryCount</span>
<span style="font-size:12px;color:#8B8FA8;font-style:italic;">— yet another element = yet another WSA key</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;width:30%;">WSA Check</td>
<td style="padding:6px 8px;font-family:monospace;font-size:12px;">WSA_EXISTS('MEC_100045_<strong>Vision</strong> EE Deduction_2024')</td>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;width:15%;text-align:center;">MISS</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Action</td>
<td style="padding:6px 8px;" colspan="2">Call DB → MAX = NULL</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:6px 8px;font-weight:700;color:#3D3D5C;">Result</td>
<td style="padding:6px 8px;" colspan="2">MultipleEntryCount = <span style="background:#D4622B;color:#fff;padding:2px 10px;border-radius:10px;font-weight:800;">1</span></td>
</tr>
</table>
</div>

<!-- Summary -->
<div style="padding:10px 18px;background:#FDF5ED;font-size:13px;color:#8B8FA8;">
DB calls: <strong style="color:#3D3D5C;">4</strong> — same pattern as Row 2
</div>

</div>
</div>

<!-- KEY INSIGHT -->
<div style="background:#FDF5ED;border-left:4px solid #D4622B;padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
<p style="margin:0 0 10px;font-size:14px;color:#3D3D5C;font-weight:700;">The Pattern:</p>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;width:20%;"></td>
<td style="padding:6px 0;font-weight:700;width:40%;">Step 3 (Person lookup)</td>
<td style="padding:6px 0;font-weight:700;">Step 4 (MEC)</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;">Row 1</td>
<td style="padding:6px 0;color:#C13B3B;">MISS — call DB</td>
<td style="padding:6px 0;color:#C13B3B;">MISS — call DB</td>
</tr>
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 0;font-weight:700;">Row 2</td>
<td style="padding:6px 0;color:#2D8B6F;font-weight:700;">HIT — zero DB calls</td>
<td style="padding:6px 0;color:#C13B3B;">MISS — different element</td>
</tr>
<tr>
<td style="padding:6px 0;font-weight:700;">Row 3</td>
<td style="padding:6px 0;color:#2D8B6F;font-weight:700;">HIT — zero DB calls</td>
<td style="padding:6px 0;color:#C13B3B;">MISS — different element</td>
</tr>
</table>
<p style="margin:10px 0 0;font-size:13px;color:#8B8FA8;">Step 3 always hits after Row 1 (same SSN = same key). Step 4 always misses here because each row maps to a different element. Step 4 WSA becomes critical when the batch has multiple rows for the <strong>same person + same element</strong>.</p>
</div>

<!-- PERFORMANCE -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Performance at Scale</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">For 10,000 vendor rows where employees average 3 benefit plans each:</p>

<div style="display:flex;gap:16px;margin:18px 0;flex-wrap:wrap;">
<div style="flex:1;min-width:250px;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);border-radius:8px;padding:16px;text-align:center;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#C13B3B;margin-bottom:8px;">WITHOUT WSA</div>
<div style="font-size:28px;font-weight:800;color:#C13B3B;letter-spacing:-0.5px;">~110,000</div>
<div style="font-size:13px;color:#8B8FA8;">value set calls (10K × 11 per row)</div>
</div>
<div style="flex:1;min-width:250px;border:1px solid #D4622B;box-shadow:0 2px 8px rgba(212,98,43,0.1);border-radius:8px;padding:16px;text-align:center;background:#fff;">
<div style="font-weight:800;font-size:14px;color:#D4622B;margin-bottom:8px;">WITH WSA</div>
<div style="font-size:28px;font-weight:800;color:#D4622B;letter-spacing:-0.5px;">~40,000</div>
<div style="font-size:13px;color:#8B8FA8;">63% reduction — Step 3 caching saves ~7 calls per duplicate SSN</div>
</div>
</div>

<!-- SINGLE THREAD -->
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Critical Rule: Set Threads = 1</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">There's one deployment rule for WSA that you absolutely cannot skip:</p>

<div style="margin:18px 0;border-radius:10px;overflow:hidden;border:1px solid #C13B3B;box-shadow:0 2px 8px rgba(220,38,38,0.1);">
<div style="background:#C13B3B;padding:12px 20px;color:#fff;font-weight:800;font-size:15px;"><span style="background:#fff;color:#C13B3B;padding:2px 8px;border-radius:4px;font-size:13px;margin-right:6px;">WARNING</span> WSA memory is per-thread. Multi-thread = broken.</div>
<div style="padding:20px;background:#fff;">

<p style="font-size:14px;margin:0 0 12px;color:#3D3D5C;">If "Load Data from File" runs with 4 threads, each thread gets its <strong>own independent WSA</strong>:</p>

<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
<tr style="border-bottom:1px solid #DDD8D0;">
<td style="padding:6px 8px;font-weight:700;width:25%;">Step 3 breaks:</td>
<td style="padding:6px 8px;">Thread 1 caches Person# for SSN 123. Thread 2 gets a different row for the same SSN — but Thread 2's WSA is empty. It calls the value set again. <span style="color:#8B8FA8;">(Wastes performance, but data is still correct.)</span></td>
</tr>
<tr>
<td style="padding:6px 8px;font-weight:700;color:#C13B3B;">Step 4 breaks:</td>
<td style="padding:6px 8px;color:#C13B3B;">Thread 1 assigns MultipleEntryCount = 2 and saves to its WSA. Thread 2 gets another row for the same person+element — but Thread 2's WSA is empty. It queries the DB, gets MAX = 1, assigns count = 2. <strong>Duplicate. Data lost.</strong></td>
</tr>
</table>

</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;"><strong>The fix:</strong></p>

<div style="margin:18px 0;padding:16px;background:#fff;border:1px solid #DDD8D0;border-radius:8px;">
<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px;font-weight:600;">
<span style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;">My Client Groups</span>
<span style="color:#8B8FA8;">→</span>
<span style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;">Payroll</span>
<span style="color:#8B8FA8;">→</span>
<span style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;">Payroll Process Configuration</span>
<span style="color:#8B8FA8;">→</span>
<span style="background:#C13B3B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-weight:800;">Threads = 1</span>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Set thread count to 1 before running "Load Data from File." All rows process sequentially in one thread. WSA works as a true shared cache across every row.</p>

<hr style="border:none;border-top:1px dashed #DDD8D0;margin:30px 0;">
<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Step 5: SourceSystemId Resolution</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">Step 5 uses: l_AssignmentNumber + L_PersonNumber + l_ElementName + POSITION2</div>
<div style="padding:14px 16px;">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="font-family:monospace;">
<td style="padding:6px 0;width:50%;color:#8B8FA8;">All resolved values from Steps 1–4</td>
<td style="padding:6px 0;">→ l_SourceSystemId = <span style="color:#D4622B;font-weight:700;">'HDL_XXVA_E12345_EE_100045_Dental EE Deduction_20240115'</span></td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Oracle HDL uses SourceSystemId as the MERGE key. If an entry already exists in cloud, the formula reuses its SourceSystemId (so HDL updates it). If not, it constructs one:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* For active employees — construct using PersonNumber */</span>
<span style="color:#CE9178;">'HDL_XXVA'</span> || <span style="color:#B5CEA8;">l_AssignmentNumber</span> || <span style="color:#CE9178;">'_EE_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>

<span style="color:#57A64A;font-style:italic;">/* For terminated employees (PersonNumber unavailable) — use SSN */</span>
<span style="color:#CE9178;">'HDL_XXVA'</span> || <span style="color:#B5CEA8;">l_AssignmentNumber</span> || <span style="color:#CE9178;">'_EE_'</span> || <span style="color:#C8C8C8;">POSITION1</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After all five steps, the formula has everything it needs: Element Name, Assignment Number, Person Number, MultipleEntryCount, SourceSystemId, and the dollar amount. Now it generates the HDL output rows (Sections 7 and 8).</p>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 7: LINEREPEATNO = 1 ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 7: LINEREPEATNO Passes — How Output Rows Are Generated</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">LINEREPEATNO = 1 generates the ElementEntry row</div>
<div style="padding:14px 16px;">
<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin-bottom:8px;">Vendor Input (what the formula receives):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;width:30%;">POSITION1</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;width:25%;">SSN</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">123-45-6789</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION2</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Date</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">2024-01-15</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION3</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Plan Code</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">DENTAL01</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION4</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Ded Type</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">PRE</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION5</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Amount</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;">150.00</td>
</tr>
<tr style="background:#fff;">
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;font-weight:700;color:#D4622B;">POSITION11</td>
<td style="padding:4px 5px;white-space:nowrap;font-weight:600;">Status</td>
<td style="padding:4px 5px;white-space:nowrap;font-family:monospace;color:#8B8FA8;">(blank = Active)</td>
</tr>
</table>

<div style="text-align:center;font-size:18px;color:#D4622B;font-weight:700;margin:10px 0;">↓ Formula transforms (Steps 1–5 + LINEREPEATNO=1) ↓</div>

<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin:10px 0 8px;">HDL .dat Output (ElementEntry):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;width:35%;">BusinessOperation</td>
<td style="padding:4px 5px;white-space:nowrap;color:#fff;font-weight:700;font-family:monospace;">MERGE</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">FileDiscriminator</td>
<td style="padding:4px 5px;white-space:nowrap;color:#CE9178;font-family:monospace;">ElementEntry</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">LegislativeDataGroupName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">570</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">EffectiveStartDate</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">2024/01/15</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">ElementName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">Dental EE Deduction</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">AssignmentNumber</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">E12345</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">CreatorType</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">H</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">EntryType</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">E</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">MultipleEntryCount</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;">1</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">SourceSystemOwner</td>
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;font-family:monospace;">HDL_XXVA</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;">SourceSystemId</td>
<td style="padding:4px 5px;white-space:nowrap;color:#8E8680;font-family:monospace;font-size:11px;">HDL_XXVA_E12345_EE_...</td>
</tr>
</table>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">After the five MAP steps, the formula has all the values it needs. Now it generates the actual HDL output. Each vendor source row produces <strong>multiple</strong> HDL output rows — one ElementEntry header on pass 1, followed by one ElementEntryValue per input value on passes 2 through 7. LINEREPEATNO controls which one gets generated on each pass.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How LINEREPEAT Works</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The HDL engine calls the formula once per source row with <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEATNO = 1</code>. If the formula returns <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code>, the engine calls the formula <strong>again for the same row</strong> — this time with <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEATNO = 2</code>.</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* HDL engine processes one vendor source row: */</span>

<span style="color:#57A64A;font-style:italic;">/* Pass 1: LINEREPEATNO = 1 → ElementEntry header */</span>
<span style="color:#C8C8C8;">Formula outputs →</span>  <span style="color:#CE9178;">MERGE|ElementEntry|...|Dental EE Deduction|...</span>
<span style="color:#C8C8C8;">Formula returns →</span>  <span style="color:#fff;font-weight:700;">LINEREPEAT</span> = <span style="color:#CE9178;">'Y'</span>   <span style="color:#57A64A;font-style:italic;">← call me again</span>

<span style="color:#57A64A;font-style:italic;">/* Pass 2: LINEREPEATNO = 2 → EEV: Amount = 150.00 */</span>
<span style="color:#C8C8C8;">Formula outputs →</span>  <span style="color:#CE9178;">MERGE|ElementEntryValue|...|Amount|...|150.00</span>
<span style="color:#C8C8C8;">Formula returns →</span>  <span style="color:#fff;font-weight:700;">LINEREPEAT</span> = <span style="color:#CE9178;">'Y'</span>   <span style="color:#57A64A;font-style:italic;">← call me again (more input values)</span>

<span style="color:#57A64A;font-style:italic;">/* Pass 3: LINEREPEATNO = 3 → EEV: Period Type = Monthly */</span>
<span style="color:#C8C8C8;">Formula outputs →</span>  <span style="color:#CE9178;">MERGE|ElementEntryValue|...|Period Type|...|Monthly</span>
<span style="color:#C8C8C8;">Formula returns →</span>  <span style="color:#fff;font-weight:700;">LINEREPEAT</span> = <span style="color:#CE9178;">'Y'</span>   <span style="color:#57A64A;font-style:italic;">← call me again</span>

<span style="color:#57A64A;font-style:italic;">/* ... passes 4–6 for Loan Number, Total Owed, Percentage (if applicable) ... */</span>

<span style="color:#57A64A;font-style:italic;">/* Pass 7: LINEREPEATNO = 7 → EEV: Deduction Amount (last pass) */</span>
<span style="color:#C8C8C8;">Formula outputs →</span>  <span style="color:#CE9178;">MERGE|ElementEntryValue|...|Deduction Amount|...</span>
<span style="color:#C8C8C8;">Formula returns →</span>  <span style="color:#fff;font-weight:700;">LINEREPEAT</span> = <span style="color:#CE9178;">'N'</span>   <span style="color:#57A64A;font-style:italic;">← done, move to next source row</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">One source row → multiple output rows (1 ElementEntry + up to 6 ElementEntryValues). The HDL engine groups all ElementEntry rows together and all ElementEntryValue rows together in the final <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">.dat</code> file, separated by their METADATA header rows.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The .dat Output Structure</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The final .dat file has two blocks. Each block starts with a METADATA row that defines the columns, followed by the MERGE data rows:</p>

<!-- ELEMENT ENTRY VALUE BLOCK -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:10px 16px;font-weight:700;font-size:12px;">Block 1 — ElementEntryValue (generated by LINEREPEATNO = 2–7)</div>
<div style="overflow-x:auto;padding:8px 12px;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#8B8FA8;">A         B                C    D           E                  F               G               J                  K</span>
<span style="color:#D4622B;font-weight:700;">METADATA  ElementEntryVal  LDG  EffStart    ElementName        AssignmentNum   InputValueName  MultipleEntryCount ScreenEntryValue</span>
MERGE     ElementEntryVal  570  22-09-2019  Dental EE Deduct   123141402543    Amount          <span style="color:#D4622B;font-weight:700;">3</span>                  <strong>150.00</strong>
MERGE     ElementEntryVal  222  22-09-2019  Dental EE Deduct   123141402554    Amount          <span style="color:#D4622B;font-weight:700;">6</span>                  <strong>25.72</strong>
MERGE     ElementEntryVal  570  22-09-2019  Dental EE Deduct   123141402543    Amount          <span style="color:#D4622B;font-weight:700;">1</span>                  <strong>150.00</strong>
<span style="color:#8B8FA8;">...       more rows</span></pre>
</div>
</div>

<!-- ELEMENT ENTRY BLOCK -->
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:10px 16px;font-weight:700;font-size:12px;">Block 2 — ElementEntry (generated by LINEREPEATNO = 1)</div>
<div style="overflow-x:auto;padding:8px 12px;">
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#8B8FA8;">A         B             C    D           E                  F               G           I          J</span>
<span style="color:#D4622B;font-weight:700;">METADATA  ElementEntry  LDG  EffStart    ElementName        AssignmentNum   CreatorType EntryType  MultipleEntryCount</span>
MERGE     ElementEntry  570  22-09-2019  Dental EE Deduct   123141402543    H           E          <span style="color:#D4622B;font-weight:700;">3</span>
MERGE     ElementEntry  222  22-09-2019  Dental EE Deduct   123141402554    H           E          <span style="color:#D4622B;font-weight:700;">6</span>
<span style="color:#8B8FA8;">...       more rows</span></pre>
</div>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The key columns to notice: ElementEntry has <strong>CreatorType</strong> and <strong>EntryType</strong> but no dollar amount. ElementEntryValue has <strong>InputValueName</strong> (always "Amount") and <strong>ScreenEntryValue</strong> (the actual dollar amount like 150.00). Both carry <strong>MultipleEntryCount</strong> from Step 4.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">What LINEREPEATNO = 1 Generates</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">On the first pass, the formula checks POSITION11 (the STATUS column from the vendor file). This decides whether we're creating a new entry or end-dating an existing one:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:25%;">POSITION11</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">ElementEntry row generated</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;width:15%;">LINEREPEAT</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">Blank (Active)</td>
<td style="padding:8px 10px;">
<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">MERGE|ElementEntry|570|22-09-2019|Dental EE Deduction|123141402543|H||E|1</code><br>
<span style="font-size:13px;color:#8B8FA8;">EffectiveStartDate = POSITION2. No EndDate. CreatorType = H. EntryType = E.</span>
</td>
<td style="padding:8px 10px;font-weight:700;font-size:15px;">'Y'<br><span style="font-weight:400;font-size:13px;color:#8B8FA8;">→ needs pass 2</span></td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:8px 10px;font-weight:700;">C (Cancel)</td>
<td style="padding:8px 10px;">
<code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">MERGE|ElementEntry|570|22-09-2019|Dental EE Deduction|123141402543|H|2019/09/22|E|1|...|Y</code><br>
<span style="font-size:13px;color:#8B8FA8;">Fetches original StartDate from cloud. Sets EndDate = cancellation date. Appends ReplaceLastEffectiveEndDate = Y.</span>
</td>
<td style="padding:8px 10px;font-weight:700;color:#C13B3B;font-size:15px;">'N'<br><span style="font-weight:400;font-size:13px;color:#8B8FA8;">→ no detail needed</span></td>
</tr>
</tbody></table>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How the Code Actually Writes the ElementEntry Row</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The formula does <strong>not</strong> use positional output variables like <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">HDL_LINE1_N</code>. Instead, it assigns values to <strong>named output variables</strong> that match the METADATA column names. Then an explicit <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">RETURN</code> statement tells the HDL engine which variables to pick up and in what order.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Here's the Active path (POSITION11 is blank):</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">IF</span> <span style="color:#C8C8C8;">LINEREPEATNO</span> = <span style="color:#B5CEA8;">1</span> <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* ======================================== */</span>
    <span style="color:#57A64A;font-style:italic;">/* ACTIVE entry — create new ElementEntry   */</span>
    <span style="color:#57A64A;font-style:italic;">/* ======================================== */</span>

    <span style="color:#B5CEA8;">FileName</span>                    = <span style="color:#CE9178;">'ElementEntry'</span>
    <span style="color:#B5CEA8;">BusinessOperation</span>           = <span style="color:#CE9178;">'MERGE'</span>
    <span style="color:#B5CEA8;">FileDiscriminator</span>           = <span style="color:#CE9178;">'ElementEntry'</span>
    <span style="color:#B5CEA8;">LegislativeDataGroupName</span>    = <span style="color:#B5CEA8;">l_LegislativeDataGroupName</span>
    <span style="color:#B5CEA8;">AssignmentNumber</span>            = <span style="color:#B5CEA8;">l_AssignmentNumber</span>
    <span style="color:#B5CEA8;">ElementName</span>                 = <span style="color:#B5CEA8;">l_ElementName</span>
    <span style="color:#B5CEA8;">EffectiveStartDate</span>          = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION2</span>),<span style="color:#CE9178;">'YYYY/MM/DD'</span>),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
    <span style="color:#B5CEA8;">EntryType</span>                   = <span style="color:#B5CEA8;">l_entry_type</span>
    <span style="color:#B5CEA8;">CreatorType</span>                 = <span style="color:#B5CEA8;">l_CreatorType</span>
    <span style="color:#B5CEA8;">SourceSystemOwner</span>           = <span style="color:#B5CEA8;">l_SourceSystemOwner</span>
    <span style="color:#B5CEA8;">SourceSystemId</span>              = <span style="color:#B5CEA8;">l_SourceSystemId</span>
    <span style="color:#B5CEA8;">LINEREPEAT</span>                  = <span style="color:#CE9178;">'Y'</span>             <span style="color:#57A64A;font-style:italic;">/* ← call me again for ElementEntryValue */</span>

    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">BusinessOperation</span>, <span style="color:#B5CEA8;">FileName</span>, <span style="color:#B5CEA8;">FileDiscriminator</span>,
           <span style="color:#B5CEA8;">CreatorType</span>, <span style="color:#B5CEA8;">EffectiveStartDate</span>, <span style="color:#B5CEA8;">ElementName</span>,
           <span style="color:#B5CEA8;">LegislativeDataGroupName</span>, <span style="color:#B5CEA8;">EntryType</span>, <span style="color:#B5CEA8;">AssignmentNumber</span>,
           <span style="color:#B5CEA8;">SourceSystemOwner</span>, <span style="color:#B5CEA8;">SourceSystemId</span>,
           <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#C8C8C8;">LINEREPEATNO</span>
)</pre>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-left:4px solid #D4622B;padding:14px 18px;margin:18px 0;border-radius:0 6px 6px 0;">
<p style="margin:0;font-size:14px;color:#3D3D5C;"><strong>How the RETURN works:</strong> The variable names in the RETURN statement must match the METADATA column names exactly. The HDL engine maps each returned variable to its corresponding METADATA position and writes the pipe-delimited row in that order. <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileName</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator</code> go to positions [1] and [2]. The rest map by name to the METADATA array you defined in Section 5.</p>
</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">For a <strong>Cancel</strong> row (POSITION11 = 'C'), the formula fetches the original start date from the cloud, sets an end date, and returns <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'N'</code> (no pass 2 needed — you don't need an ElementEntryValue for a cancellation):</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">IF</span> (<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION11</span>) = <span style="color:#CE9178;">'C'</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* Fetch the original start date from cloud */</span>
    <span style="color:#B5CEA8;">l_Effective_Start_Date</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(<span style="color:#CE9178;">'XXVA_GET_EE_START_DATE'</span>, ...)

    <span style="color:#57A64A;font-style:italic;">/* Same named variables, but with end date + replace flag */</span>
    <span style="color:#B5CEA8;">FileName</span>                    = <span style="color:#CE9178;">'ElementEntry'</span>
    <span style="color:#B5CEA8;">BusinessOperation</span>           = <span style="color:#CE9178;">'MERGE'</span>
    <span style="color:#B5CEA8;">FileDiscriminator</span>           = <span style="color:#CE9178;">'ElementEntry'</span>
    <span style="color:#B5CEA8;">EffectiveStartDate</span>          = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#B5CEA8;">l_Effective_Start_Date</span>,...),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
    <span style="color:#B5CEA8;">EffectiveEndDate</span>            = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION2</span>),...),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
    <span style="color:#B5CEA8;">ReplaceLastEffectiveEndDate</span> = <span style="color:#CE9178;">'Y'</span>
    <span style="color:#B5CEA8;">LINEREPEAT</span>                  = <span style="color:#CE9178;">'N'</span>              <span style="color:#57A64A;font-style:italic;">/* ← no pass 2 for cancel */</span>
    <span style="color:#57A64A;font-style:italic;">/* ...same other variables as Active... */</span>

    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">BusinessOperation</span>, <span style="color:#B5CEA8;">FileName</span>, <span style="color:#B5CEA8;">FileDiscriminator</span>,
           <span style="color:#B5CEA8;">CreatorType</span>, <span style="color:#B5CEA8;">EffectiveStartDate</span>, <span style="color:#B5CEA8;">EffectiveEndDate</span>,
           <span style="color:#B5CEA8;">ElementName</span>, <span style="color:#B5CEA8;">LegislativeDataGroupName</span>, <span style="color:#B5CEA8;">EntryType</span>,
           <span style="color:#B5CEA8;">AssignmentNumber</span>, <span style="color:#B5CEA8;">SourceSystemOwner</span>, <span style="color:#B5CEA8;">SourceSystemId</span>,
           <span style="color:#B5CEA8;">ReplaceLastEffectiveEndDate</span>,
           <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#C8C8C8;">LINEREPEATNO</span>
)</pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Notice the Cancel RETURN includes <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">EffectiveEndDate</code> and <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ReplaceLastEffectiveEndDate</code> — both absent from the Active RETURN.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">Duplicate Header Prevention (WSA)</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">One person can have multiple vendor rows (Dental, Medical, Vision) that all map to different elements. Each element needs exactly one ElementEntry row. But if two vendor rows map to the <strong>same</strong> element, the formula must not generate a duplicate header. It checks WSA:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">WSA_EXISTS</span>(<span style="color:#CE9178;">'HDR_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">'_'</span> || <span style="color:#C8C8C8;">POSITION2</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#57A64A;font-style:italic;">/* Header already generated for this combo — skip to pass 2 */</span>
    <span style="color:#C8C8C8;">LINEREPEAT</span> = <span style="color:#CE9178;">'Y'</span>
    <span style="color:#fff;font-weight:700;">RETURN</span>
)
<span style="color:#57A64A;font-style:italic;">/* First time for this combo — generate header, then mark in WSA */</span>
<span style="color:#DCDCAA;">WSA_SET</span>(<span style="color:#CE9178;">'HDR_'</span> || ..., <span style="color:#B5CEA8;">1</span>)</pre>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-left:4px solid #C13B3B;padding:14px 18px;margin:18px 0;border-radius:0 6px 6px 0;">
<p style="margin:0 0 8px;font-size:14px;color:#C13B3B;font-weight:700;">Watch out: ISNULL is inverted</p>
<p style="margin:0;font-size:14px;color:#3D3D5C;">The formula checks <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ISNULL(l_ElementName) = 'N'</code> before generating anything. In Fast Formula, <code>'N'</code> means the value IS null (not found). If the vendor code didn't map to any element, the formula skips the row silently.</p>
</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SECTION 8: LINEREPEATNO = 2 ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">Section 8: LINEREPEATNO = 2–7 — ElementEntryValue Rows</div>
<div style="margin:18px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:linear-gradient(135deg,#1B4965,#0D2B3E);color:#fff;padding:12px 18px;font-weight:700;font-size:13px;letter-spacing:0.3px;">LINEREPEATNO = 2–7 generates ElementEntryValue rows</div>
<div style="padding:14px 16px;">
<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin-bottom:8px;">Same Vendor Input Row → multiple ElementEntryValue outputs (one per input value):</div>

<div style="text-align:center;font-size:18px;color:#D4622B;font-weight:700;margin:10px 0;">↓ Each pass loads a different InputValueName ↓</div>

<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin:10px 0 8px;">Pass 2 — ElementEntryValue (Amount):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;width:35%;">InputValueName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">Amount</td>
</tr>
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">ScreenEntryValue</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">150.00</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">ElementEntryId(SSID)</td>
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;font-family:monospace;font-size:11px;">HDL_XXVA_E12345_EE_... (links to parent ElementEntry)</td>
</tr>
</table>

<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin:10px 0 8px;">Pass 3 — ElementEntryValue (Period Type):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;width:35%;">InputValueName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">Period Type</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">ScreenEntryValue</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">Monthly</td>
</tr>
</table>

<div style="font-size:13px;font-weight:700;color:#3D3D5C;margin:10px 0 8px;">Pass 6 — ElementEntryValue (Percentage):</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:14px;">
<tr style="background:#1E1E1E;border-bottom:1px solid #333;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;width:35%;">InputValueName</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">Percentage</td>
</tr>
<tr style="background:#1E1E1E;">
<td style="padding:4px 5px;white-space:nowrap;color:#8B8FA8;">ScreenEntryValue</td>
<td style="padding:4px 5px;white-space:nowrap;color:#B5CEA8;font-family:monospace;font-weight:700;">5.5</td>
</tr>
</table>

<div style="background:#F5F3EF;border-radius:6px;padding:8px 10px;font-size:13px;color:#8B8FA8;">Passes 4, 5, 7 skipped — PRE type doesn't use Loan Number, Total Owed, or Deduction Amount. The formula returns <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code> with no output data on those passes.</div>
</div>
</div>


<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Passes 2 through 7 each generate one ElementEntryValue row. Each pass loads a different input value. The deduction type (POSITION4) controls which passes produce output and which ones skip.</p>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">What LINEREPEATNO = 2 Generates</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Each ElementEntryValue pass sets <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">InputValueName</code> to a different value and loads the corresponding data into <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ScreenEntryValue</code>:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:12px;">
<thead><tr style="background:linear-gradient(135deg,#D4622B,#B8531F);color:#fff;">
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Column</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Value</th>
<th style="padding:8px 10px;text-align:left;white-space:nowrap;">Source</th>
</tr></thead>
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">LINEREPEATNO</td>
<td style="padding:8px 10px;font-family:monospace;">InputValueName</td>
<td style="padding:8px 10px;">ScreenEntryValue source</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">2</td>
<td style="padding:8px 10px;font-family:monospace;">Amount</td>
<td style="padding:8px 10px;font-size:13px;">l_Amount (POSITION5) = 150.00</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">3</td>
<td style="padding:8px 10px;font-family:monospace;">Period Type</td>
<td style="padding:8px 10px;font-size:13px;">l_PeriodType (POSITION6) = Monthly</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">4</td>
<td style="padding:8px 10px;font-family:monospace;">Loan Number</td>
<td style="padding:8px 10px;font-size:13px;">POSITION8 — LOAN type only</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">5</td>
<td style="padding:8px 10px;font-family:monospace;">Total Owed</td>
<td style="padding:8px 10px;font-size:13px;">l_TotalOwed — LOAN type only</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-family:monospace;">6</td>
<td style="padding:8px 10px;font-family:monospace;">Percentage</td>
<td style="padding:8px 10px;font-size:13px;">l_Percentage (POSITION7) — PRE/POST type only</td>
</tr>
<tr style="background:#fff;">
<td style="padding:8px 10px;font-family:monospace;">7</td>
<td style="padding:8px 10px;font-family:monospace;">Deduction Amount</td>
<td style="padding:8px 10px;font-size:13px;">l_DeductionAmount — CU type only</td>
</tr>
</tbody></table>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">How the Code Actually Writes the ElementEntryValue Row</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">Each pass from 2 to 7 follows the same structure. The key difference is the skip logic: each pass checks POSITION4 (deduction type) to decide whether to generate output or just return <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code> with no data (effectively skipping to the next pass). Same pattern — named output variables + explicit RETURN. But now <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator = 'ElementEntryValue'</code> (not 'ElementEntry'), and the RETURN includes <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">InputValueName</code>, <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ScreenEntryValue</code>, and the parent link <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">"ElementEntryId(SourceSystemId)"</code>.</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#fff;font-weight:700;">ELSE IF</span> (<span style="color:#C8C8C8;">LINEREPEATNO</span> = <span style="color:#B5CEA8;">2</span>) <span style="color:#fff;font-weight:700;">THEN</span>
(
    <span style="color:#B5CEA8;">l_InputValueName</span> = <span style="color:#CE9178;">'Amount'</span>

    <span style="color:#57A64A;font-style:italic;">/* Look up ElementEntryValue SourceSystemId from cloud (or construct new one) */</span>
    <span style="color:#B5CEA8;">l_EEV_SourceSystemId</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(
        <span style="color:#CE9178;">'XXVA_GET_EEV_SOURCE_SYSTEM_ID'</span>, ...)
    <span style="color:#B5CEA8;">l_EEV_SourceSystemOwner</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(
        <span style="color:#CE9178;">'XXVA_GET_EEV_SOURCE_SYSTEM_OWNER'</span>, ...)

    <span style="color:#57A64A;font-style:italic;">/* If no existing SSID found, construct a new one */</span>
    <span style="color:#fff;font-weight:700;">IF</span> <span style="color:#DCDCAA;">ISNULL</span>(<span style="color:#B5CEA8;">l_EEV_SourceSystemId</span>) = <span style="color:#CE9178;">'N'</span> <span style="color:#fff;font-weight:700;">THEN</span>
    (
        <span style="color:#B5CEA8;">l_EEV_SourceSystemId</span> = <span style="color:#CE9178;">'HDL_XXVA'</span> || <span style="color:#B5CEA8;">l_AssignmentNumber</span>
            || <span style="color:#CE9178;">'_EEV_'</span> || <span style="color:#B5CEA8;">L_PersonNumber</span>
            || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_ElementName</span>
            || <span style="color:#CE9178;">'_'</span> || <span style="color:#B5CEA8;">l_InputValueName</span>
            || <span style="color:#CE9178;">'_'</span> || <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#C8C8C8;">POSITION2</span>),...),<span style="color:#CE9178;">'YYYYMMDD'</span>)
    )

    <span style="color:#57A64A;font-style:italic;">/* ============================================= */</span>
    <span style="color:#57A64A;font-style:italic;">/* Set the output variables for ElementEntryValue */</span>
    <span style="color:#57A64A;font-style:italic;">/* ============================================= */</span>

    <span style="color:#B5CEA8;">FileName</span>                          = <span style="color:#CE9178;">'ElementEntry'</span>        <span style="color:#57A64A;font-style:italic;">/* always ElementEntry */</span>
    <span style="color:#B5CEA8;">BusinessOperation</span>                 = <span style="color:#CE9178;">'MERGE'</span>
    <span style="color:#B5CEA8;">FileDiscriminator</span>                 = <span style="color:#CE9178;">'ElementEntryValue'</span>   <span style="color:#57A64A;font-style:italic;">/* ← THIS is the key difference */</span>
    <span style="color:#B5CEA8;">LegislativeDataGroupName</span>          = <span style="color:#B5CEA8;">l_LegislativeDataGroupName</span>
    <span style="color:#B5CEA8;">AssignmentNumber</span>                  = <span style="color:#B5CEA8;">l_AssignmentNumber</span>
    <span style="color:#B5CEA8;">ElementName</span>                       = <span style="color:#B5CEA8;">l_ElementName</span>
    <span style="color:#B5CEA8;">EntryType</span>                         = <span style="color:#B5CEA8;">l_entry_type</span>
    <span style="color:#B5CEA8;">EffectiveStartDate</span>                = <span style="color:#DCDCAA;">TO_CHAR</span>(...)
    <span style="color:#CE9178;">"ElementEntryId(SourceSystemId)"</span>  = <span style="color:#B5CEA8;">l_SourceSystemId</span>      <span style="color:#57A64A;font-style:italic;">/* ← links to parent ElementEntry */</span>
    <span style="color:#B5CEA8;">SourceSystemId</span>                    = <span style="color:#B5CEA8;">l_EEV_SourceSystemId</span>  <span style="color:#57A64A;font-style:italic;">/* ← EEV's own SSID */</span>
    <span style="color:#B5CEA8;">SourceSystemOwner</span>                 = <span style="color:#B5CEA8;">l_EEV_SourceSystemOwner</span>
    <span style="color:#B5CEA8;">InputValueName</span>                    = <span style="color:#B5CEA8;">l_InputValueName</span>      <span style="color:#57A64A;font-style:italic;">/* 'Amount' */</span>
    <span style="color:#B5CEA8;">ScreenEntryValue</span>                  = <span style="color:#DCDCAA;">To_Char</span>(<span style="color:#DCDCAA;">TO_NUM</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#B5CEA8;">l_Amount</span>)))
    <span style="color:#B5CEA8;">LINEREPEAT</span>                        = <span style="color:#CE9178;">'Y'</span>                  <span style="color:#57A64A;font-style:italic;">/* more passes to come (pass 7 returns 'N') */</span>

    <span style="color:#fff;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">BusinessOperation</span>, <span style="color:#B5CEA8;">FileName</span>, <span style="color:#B5CEA8;">FileDiscriminator</span>,
           <span style="color:#B5CEA8;">AssignmentNumber</span>, <span style="color:#B5CEA8;">EffectiveStartDate</span>, <span style="color:#B5CEA8;">ElementName</span>,
           <span style="color:#B5CEA8;">EntryType</span>, <span style="color:#B5CEA8;">LegislativeDataGroupName</span>,
           <span style="color:#CE9178;">"ElementEntryId(SourceSystemId)"</span>,
           <span style="color:#B5CEA8;">InputValueName</span>, <span style="color:#B5CEA8;">ScreenEntryValue</span>,
           <span style="color:#B5CEA8;">SourceSystemOwner</span>, <span style="color:#B5CEA8;">SourceSystemId</span>,
           <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#C8C8C8;">LINEREPEATNO</span>
)</pre>

<div style="background:#FDF5ED;border:1px solid #DDD8D0;border-left:4px solid #D4622B;padding:14px 18px;margin:18px 0;border-radius:0 6px 6px 0;">
<p style="margin:0 0 8px;font-size:14px;color:#3D3D5C;"><strong>Three things to notice:</strong></p>
<p style="margin:0;font-size:14px;color:#3D3D5C;">
<strong>1.</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileName</code> is still <code>'ElementEntry'</code> — NOT <code>'ElementEntryValue'</code>. Only the <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator</code> changes to <code>'ElementEntryValue'</code>. This is how HDL knows the row goes into the ElementEntryValue block of the .dat file.<br><br>
<strong>2.</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">"ElementEntryId(SourceSystemId)"</code> is set to the <strong>ElementEntry's</strong> SourceSystemId (<code>l_SourceSystemId</code>). This is the parent-child link. The variable name contains parentheses, so it must be double-quoted in the formula code.<br><br>
<strong>3.</strong> The ElementEntryValue has its <strong>own</strong> SourceSystemId (<code>l_EEV_SourceSystemId</code>), different from the parent ElementEntry's. The formula first tries to find an existing one from the cloud via value set. If not found (<code>ISNULL = 'N'</code>), it constructs one with the pattern: <code>HDL_XXVA + AssignmentNumber + _EEV_ + PersonNumber + _ElementName + _InputValueName + _Date</code>.
</p>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The Parent-Child Link</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The ElementEntryValue row must reference its parent ElementEntry row. HDL uses SourceSystemId to link them:</p>

<div style="margin:18px 0;padding:20px;border:1px solid #DDD8D0;border-radius:10px;background:#fff;">
<div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
<div style="background:#fff;border:1px solid #DDD8D0;border-top:3px solid #D4622B;border-radius:8px;padding:14px 18px;text-align:center;min-width:250px;">
<div style="font-weight:700;font-size:14px;margin-bottom:6px;">ElementEntry (Pass 1)</div>
<div style="font-family:monospace;font-size:13px;color:#3D3D5C;">SourceSystemId = <span style="color:#D4622B;font-weight:700;">HDL_XXVA_E12345_EE_...</span></div>
</div>
<div style="font-size:24px;color:#D4622B;font-weight:700;">→</div>
<div style="background:#fff;border:1px solid #DDD8D0;border-top:3px solid #D4622B;border-radius:8px;padding:14px 18px;text-align:center;min-width:280px;">
<div style="font-weight:700;font-size:14px;margin-bottom:6px;">ElementEntryValue (Pass 2)</div>
<div style="font-family:monospace;font-size:13px;color:#3D3D5C;">ElementEntryId(SSID) = <span style="color:#D4622B;font-weight:700;">HDL_XXVA_E12345_EE_...</span></div>
<div style="font-family:monospace;font-size:13px;color:#8B8FA8;margin-top:4px;">SourceSystemId = HDL_XXVA_E12345_EEV_...</div>
</div>
</div>
<p style="margin:12px 0 0;font-size:13px;color:#8B8FA8;">The ElementEntryValue's <code>ElementEntryId(SourceSystemId)</code> matches the ElementEntry's <code>SourceSystemId</code>. This is how HDL knows which entry this value belongs to.</p>
</div>

<div style="font-size:17px;font-weight:700;color:#1A1A2E;margin:32px 0 16px;padding-left:16px;border-left:3px solid #D4622B;">The RTRIM Trick for Clean Numbers</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">the vendor sends amounts like <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">150.00</code>, but Oracle elements expect clean numbers. The formula strips trailing zeros:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#DCDCAA;">RTRIM</span>(<span style="color:#DCDCAA;">RTRIM</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#B5CEA8;">l_Amount</span>), <span style="color:#CE9178;">'0'</span>), <span style="color:#CE9178;">'.'</span>)

<span style="color:#57A64A;font-style:italic;">/* 150.00 → 150 | 75.50 → 75.5 | 12.30 → 12.3 | 150.00 → 150.00 */</span></pre>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">The inner RTRIM strips trailing zeros. The outer RTRIM strips the decimal point if nothing is left after it.</p>


<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== END-TO-END FLOW ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">End-to-End: One Vendor Row Through the Formula</div>

<div style="background:#fff;border:1px solid #DDD8D0;border-radius:10px;padding:20px;margin:18px 0;">

<p style="font-size:14px;margin:0 0 12px;"><strong>Vendor CSV Row:</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">123-45-6789,2024-01-15,DENTAL01,150.00,,,</code></p>

<div style="display:flex;gap:6px;margin:12px 0;flex-wrap:wrap;">
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 1: Type → ER, Amount → 150.00</div>
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 2: Key → DENTAL01 → Dental EE Deduction</div>
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 3: SSN → Person# 100045, Asg# E12345 (WSA)</div>
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 4: MultipleEntryCount = 1</div>
<div style="background:#D4622B;color:#fff;padding:4px 5px;white-space:nowrap;border-radius:4px;font-size:13px;font-weight:600;">STEP 5: SourceSystemId constructed</div>
</div>

<p style="font-size:13px;margin:14px 0 6px;font-weight:700;color:#D4622B;">LINEREPEATNO=1 → ElementEntry:</p>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">MERGE|ElementEntry|570|2019/09/22|Dental EE Deduction|123141402543|H||E|1</pre>

<p style="font-size:13px;margin:0 0 6px;font-weight:700;color:#D4622B;">LINEREPEATNO=2 → ElementEntryValue (Amount):</p>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">MERGE|ElementEntryValue|570|2019/09/22|Dental EE Deduction|123141402543|Amount||E||1|150.00</pre>

</div>

<hr style="border:none;border-top:1px solid #DDD8D0;margin:45px 0;">

<!-- ==================== SERIES CLOSING ==================== -->

<div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:0.5px;background:linear-gradient(135deg,#1B4965,#0D2B3E);padding:18px 24px;border-radius:8px;border-left:5px solid #D4622B;margin:50px 0 24px;box-shadow:0 4px 16px rgba(27,73,101,0.2);">What You Now Understand</div>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">If you've read this far, you can now explain — without looking at any code — how an HDL Transformation Formula works end-to-end. You know what each OPERATION does, why METADATA arrays define the .dat column headers, how the MAP block transforms source data in 5 steps, why WSA exists (performance + correctness), how LINEREPEATNO generates multiple output rows (1 ElementEntry + up to 6 ElementEntryValues) from one source row, and how named RETURN variables map to METADATA columns.</p>

<p style="font-size:15px;margin-bottom:16px;color:#3D3D5C;line-height:1.75;">That's the foundation. The concepts don't change whether you're building an vendor deduction interface, a benefits enrollment loader, or a payroll costing feed. Every HDL Transformation Formula follows this same structure.</p>

<!-- NEXT IN SERIES -->
<div style="margin:30px 0;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#D4622B;color:#fff;padding:16px 20px;font-weight:700;font-size:16px;">Coming Next — Part 2: Code Walkthrough</div>
<div style="padding:20px;">

<p style="font-size:15px;margin:0 0 16px;color:#3D3D5C;">Part 2 takes every concept from this post and shows you the actual Fast Formula code that implements it. Line by line, with the Notepad++ syntax highlighting you've been seeing in the code snippets here.</p>

<p style="font-size:15px;margin:0 0 16px;color:#3D3D5C;">What Part 2 will cover:</p>

<table style="width:100%;border-collapse:collapse;font-size:12px;">
<tbody>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;width:40%;">Full INPUTS ARE block</td>
<td style="padding:8px 10px;color:#8B8FA8;">Every POSITION mapped to its vendor column, every DEFAULT FOR explained</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">GET_VALUE_SET calls</td>
<td style="padding:8px 10px;color:#8B8FA8;">The exact parameter string construction with pipe delimiters, date conversions, and ISNULL checking</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">WSA implementation</td>
<td style="padding:8px 10px;color:#8B8FA8;">Real WSA_EXISTS / WSA_GET / WSA_SET code with key construction patterns</td>
</tr>
<tr style="background:#F5F3EF;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">SourceSystemId logic</td>
<td style="padding:8px 10px;color:#8B8FA8;">The full lookup-or-construct pattern for both ElementEntry and ElementEntryValue SourceSystemIds</td>
</tr>
<tr style="background:#fff;border-bottom:1px solid #DDD8D0;">
<td style="padding:8px 10px;font-weight:700;">ESS_LOG_WRITE debugging</td>
<td style="padding:8px 10px;color:#8B8FA8;">Adding trace logs at each step so you can debug formula execution in real time</td>
</tr>
<tr style="background:#F5F3EF;">
<td style="padding:8px 10px;font-weight:700;">Cancel vs Active branching</td>
<td style="padding:8px 10px;color:#8B8FA8;">The complete IF POSITION11 = 'C' block with date fetching from cloud</td>
</tr>
</tbody>
</table>

</div>
</div>

<!-- PART 3 TEASER -->
<div style="margin:0 0 30px;border:1px solid #DDD8D0;border-radius:10px;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="background:#1B4965;color:#fff;padding:16px 20px;font-weight:700;font-size:16px;">Later — Part 3: Build Your Own</div>
<div style="padding:20px;">

<p style="font-size:15px;margin:0 0 16px;color:#3D3D5C;">Part 3 is the implementation guide. You'll build an HDL Transformation Formula from scratch — from creating the formula in Oracle Cloud, defining all 11 value sets, configuring the HDL integration, running test loads, reading ESS logs, and troubleshooting the errors you'll hit in production.</p>

<p style="font-size:15px;margin:0;color:#3D3D5C;">After Part 3, you'll have a working formula you can adapt for any inbound payroll interface — not just one vendor.</p>

</div>
</div>

<!-- SERIES ROADMAP REPEAT -->
<div style="margin:0 0 30px;padding:20px;background:#F5F3EF;border-radius:10px;">
<div style="font-weight:700;font-size:15px;color:#3D3D5C;margin-bottom:12px;">Series Roadmap</div>
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<div style="background:#D4622B;color:#fff;padding:8px 16px;border-radius:6px;font-weight:700;font-size:13px;">Part 1: Pure Concepts <span style="font-weight:400;opacity:0.8;">← This post</span></div>
<div style="color:#8B8FA8;font-size:18px;">→</div>
<div style="background:#fff;border:1px solid #DDD8D0;color:#3D3D5C;padding:8px 16px;border-radius:6px;font-weight:700;font-size:13px;">Part 2: Code Walkthrough <span style="font-weight:400;color:#8B8FA8;">Coming soon</span></div>
<div style="color:#8B8FA8;font-size:18px;">→</div>
<div style="background:#fff;border:1px solid #DDD8D0;color:#3D3D5C;padding:8px 16px;border-radius:6px;font-weight:700;font-size:13px;">Part 3: Build Your Own <span style="font-weight:400;color:#8B8FA8;">Coming soon</span></div>
</div>
</div>

<!-- ==================== AUTHOR FOOTER ==================== -->

<div style="display:flex;align-items:center;gap:14px;padding:20px 0;border-top:1px solid #DDD8D0;">
<div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#D4622B,#E8944F);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;flex-shrink:0;">AM</div>
<div>
<div style="font-weight:700;font-size:15px;">Abhishek Mohanty</div>
<div style="font-size:13px;color:#8B8FA8;line-height:1.5;">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.</div>
</div>
</div>

</div>