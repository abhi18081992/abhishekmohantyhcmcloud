---
title: "Step-by-step code walkthrough of Oracle HCM Cloud HDL Transformation Fast Formula — INPUTS ARE declaration, GET_VALUE_SET parameter construction, ISNULL checking, SourceSystemId resolution, ESS_LOG_WRITE tracing, LINEREPEATNO pass logic for ElementEntry and ElementEntryValue, and Cancel end-dating with ReplaceLastEffectiveEndDate. Part 2 of 3."
pubDate: 2026-03-26
description: "Step-by-step code walkthrough of Oracle HCM Cloud HDL Transformation Fast Formula — INPUTS ARE declaration, GET_VALUE_SET parameter construction,..."
tags: ["Fast Formula", "HDL", "Null Handling", "Oracle HCM Cloud"]
author: "Abhishek Mohanty"
draft: false
---

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Line-by-line code walkthrough of Oracle HCM Cloud HDL Transformation Fast Formula. Covers INPUTS ARE, GET_VALUE_SET parameter string syntax, ISNULL checks, SourceSystemId lookup-or-construct, ESS_LOG_WRITE debugging, Cancel vs Active branching with LINEREPEATNO, EffectiveEndDate, and ReplaceLastEffectiveEndDate. Part 2 of 3.">
<meta name="keywords" content="Oracle HCM Cloud, Fast Formula, HDL, HCM Data Loader, Transformation Formula, GET_VALUE_SET, ISNULL, SourceSystemId, ESS_LOG_WRITE, LINEREPEATNO, ElementEntry, ElementEntryValue, METADATA, OPERATION MAP, Cancel Branching, ReplaceLastEffectiveEndDate, MultipleEntryCount, POSITION variables, Oracle Payroll Integration">
<meta property="og:title" content="Oracle HCM Cloud HDL Transformation Fast Formula — Line-by-Line Code Walkthrough (Part 2 of 3)">
<meta property="og:description" content="Complete code walkthrough: INPUTS ARE, GET_VALUE_SET pipe-delimiter syntax, ISNULL patterns, SourceSystemId MERGE logic, ESS_LOG_WRITE debug tracing, Cancel vs Active branching with LINEREPEATNO.">
<meta property="og:type" content="article">
<meta name="author" content="Abhishek Mohanty">
<title>Oracle HCM Cloud HDL Transformation Fast Formula — Line-by-Line Code Walkthrough (Part 2 of 3)</title>
<style>
:root { --accent: #D4622B; --dark: #1A1A2E; --text: #3D3D5C; --muted: #8B8FA8; --bg-subtle: #F8F7F4; --border: #E8E4DE; --green: #2D8B6F; --red: #B8423A; --blue: #4A6FA5; --code-bg: #1B1D2E; }

/* ── Diagram system ── */
.diag { background: var(--bg-subtle); border-radius: 14px; padding: 28px 24px; margin: 24px 0; position: relative; }
.diag-title { font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: var(--muted); margin-bottom: 18px; }

/* Timeline / vertical flow */
.timeline { position: relative; padding-left: 36px; }
.timeline::before { content: ''; position: absolute; left: 13px; top: 8px; bottom: 8px; width: 2px; background: linear-gradient(to bottom, var(--accent), var(--border)); border-radius: 1px; }
.tl-step { position: relative; margin-bottom: 18px; }
.tl-step:last-child { margin-bottom: 0; }
.tl-dot { position: absolute; left: -29px; top: 4px; width: 12px; height: 12px; border-radius: 50%; border: 2px solid var(--accent); background: var(--bg-subtle); }
.tl-dot.active { background: var(--accent); }
.tl-label { font-size: 13px; font-weight: 700; color: var(--dark); margin-bottom: 2px; }
.tl-desc { font-size: 12px; color: var(--muted); line-height: 1.5; }
.tl-result { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 500; background: rgba(212,98,43,0.08); color: var(--accent); padding: 2px 8px; border-radius: 4px; margin-top: 4px; }

/* Horizontal pipeline */
.pipeline { display: flex; align-items: center; gap: 0; flex-wrap: wrap; justify-content: center; }
.pipe-node { background: #fff; border-radius: 10px; padding: 12px 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04); text-align: center; min-width: 100px; position: relative; }
.pipe-node.accent { box-shadow: 0 1px 4px rgba(212,98,43,0.12), 0 4px 16px rgba(212,98,43,0.08); }
.pipe-connector { width: 32px; height: 2px; background: linear-gradient(to right, var(--border), var(--accent)); position: relative; flex-shrink: 0; }
.pipe-connector::after { content: ''; position: absolute; right: -3px; top: -3px; border: solid var(--accent); border-width: 0 2px 2px 0; padding: 3px; transform: rotate(-45deg); }
.pipe-label { font-size: 10px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
.pipe-value { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; color: var(--dark); }
.pipe-sub { font-size: 10px; color: var(--muted); margin-top: 2px; }

/* Code annotation strips */
.code-annot { display: flex; gap: 0; margin: 4px 0; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 6px rgba(0,0,0,0.06); }
.code-annot-line { background: var(--code-bg); padding: 10px 16px; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #C8C9D4; flex: 1; min-width: 0; overflow-x: auto; white-space: nowrap; border-right: 1px solid rgba(255,255,255,0.05); }
.code-annot-note { background: #fff; padding: 10px 16px; font-size: 12px; color: var(--text); min-width: 180px; max-width: 220px; display: flex; align-items: center; line-height: 1.4; }
.code-annot-note::before { content: '←'; color: var(--accent); font-weight: 700; margin-right: 8px; flex-shrink: 0; }

/* Professional code block with header */
.code-pro { border-radius: 10px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin: 20px 0; }
.code-pro-header { background: #151726; padding: 10px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); }
.code-pro-header .dots { display: flex; gap: 6px; }
.code-pro-header .dots span { width: 10px; height: 10px; border-radius: 50%; }
.code-pro-header .label { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #6B6F88; letter-spacing: 0.3px; }
.code-pro pre { background: var(--code-bg); color: #C8C9D4; padding: 20px 24px; font-family: 'JetBrains Mono', monospace; font-weight: 500; font-size: 13.5px; line-height: 1.85; overflow-x: auto; margin: 0; white-space: pre-wrap; counter-reset: codeline; }
.code-pro .ln { color: #3D4058; font-size: 12px; display: inline-block; width: 28px; text-align: right; margin-right: 16px; user-select: none; }

/* Decision cards */
.decision-pair { display: flex; gap: 16px; flex-wrap: wrap; }
.decision-card { flex: 1; min-width: 220px; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.decision-card-head { padding: 10px 16px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px; }
.decision-card-body { background: #fff; padding: 16px; font-size: 13px; line-height: 1.7; }

/* Segment bar (for SSID assembly) */
.seg-bar { display: flex; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin: 16px 0; }
.seg-bar > div { padding: 10px 12px; font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 600; text-align: center; }
.seg-bar .seg-label { font-size: 9px; font-weight: 400; opacity: 0.7; display: block; margin-top: 2px; }

/* Plain english */
.ipe { background: #fff; border-left: 3px solid var(--green); border-radius: 0 10px 10px 0; padding: 16px 20px; margin: 18px 0 28px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.ipe p { margin: 0 0 6px; font-size: 14px; color: var(--text); line-height: 1.65; }
.ipe p:last-child { margin-bottom: 0; }
.ipe strong { color: var(--dark); }

@media (prefers-color-scheme: dark) {
.hdl-blog { background: #12131A !important; color: #C8C9D4 !important; }
.hdl-blog p, .hdl-blog li { color: #C8C9D4 !important; }
.hdl-blog strong { color: #EAEBF0 !important; }
.hdl-blog code { background: #1E1F2B !important; color: #D4D5DE !important; }
.hdl-blog hr { border-color: #2A2B38 !important; }
.hdl-blog pre { background: #0D0E14 !important; }
.hdl-blog .diag { background: #16171F !important; }
.hdl-blog .pipe-node, .hdl-blog .ipe, .hdl-blog .code-annot-note, .hdl-blog .decision-card-body { background: #1A1B26 !important; }
.hdl-blog .pipe-node { box-shadow: 0 1px 4px rgba(0,0,0,0.3) !important; }
.hdl-blog td, .hdl-blog th { border-color: #2A2B38 !important; }
.hdl-blog td { color: #C8C9D4 !important; }
.hdl-blog th { color: #fff !important; }
.hdl-blog .tl-dot { background: #16171F !important; }
.hdl-blog .tl-dot.active { background: var(--accent) !important; }
.hdl-blog .timeline::before { background: linear-gradient(to bottom, var(--accent), #2A2B38) !important; }
}
</style>
</head>
<body>
<div class="hdl-blog" style="font-family:'Plus Jakarta Sans',sans-serif;max-width:820px;margin:0 auto;padding:32px 24px;line-height:1.75;color:var(--dark);">

<!-- ══════ TAGS ══════ -->
<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;">
<span style="background:var(--accent);color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:10px;letter-spacing:0.8px;">Fast Formula</span>
<span style="background:var(--accent);color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:10px;letter-spacing:0.8px;">HCM Data Loader</span>
<span style="background:var(--accent);color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:10px;letter-spacing:0.8px;">Transformation Formula</span>
<span style="background:var(--accent);color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:10px;letter-spacing:0.8px;">ESS_LOG_WRITE</span>
<span style="background:var(--dark);color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:10px;letter-spacing:0.8px;">Series Part 2 of 3</span>
</div>

<!-- ══════ TITLE ══════ -->
<h1 style="font-size:30px;font-weight:800;color:var(--dark);line-height:1.25;margin:0 0 6px;font-family:inherit;">Oracle HCM Cloud HDL Transformation Fast Formula — Line-by-Line Code Walkthrough</h1>
<div style="font-size:16px;color:var(--text);margin-bottom:4px;">Vendor Deduction Interface | ElementEntry + ElementEntryValue</div>
<div style="font-size:13px;color:var(--muted);margin-bottom:24px;">March 2026 · 30 min read · Oracle HCM Cloud</div>

<!-- ══════ INTRO ══════ -->
<div style="background:#FDF5ED;border:1px solid #E8DDD0;border-radius:8px;padding:18px 22px;margin-bottom:28px;">
<p style="margin:0;font-size:15px;color:var(--text);">This is <strong>Part 2</strong> of a 3-part series on HDL Transformation Formulas. Part 1 covered the concepts — what each section does and why. This post opens the actual code. Every line is explained in simple English with visuals showing what the Fast Formula engine does at each step.</p>
</div>

<!-- ══════ SERIES ROADMAP ══════ -->
<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 16px;font-family:inherit;">HDL Transformation Formula Series</h3>
<div style="display:flex;gap:16px;margin-bottom:32px;flex-wrap:wrap;">
<div style="flex:1;min-width:200px;background:var(--bg-subtle);border-radius:8px;padding:16px 18px;border-left:4px solid var(--muted);">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
<span style="background:var(--muted);color:#fff;font-size:13px;font-weight:800;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;">1</span>
<span style="font-size:14px;font-weight:700;color:var(--muted);">Pure Concepts</span></div>
<p style="margin:0;font-size:12px;color:var(--muted);">INPUTS, OPERATION, METADATA, MAP, WSA, LINEREPEATNO, RETURN. Zero code.</p></div>
<div style="flex:1;min-width:200px;background:#FDF5ED;border-radius:8px;padding:16px 18px;border-left:4px solid var(--accent);">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
<span style="background:var(--accent);color:#fff;font-size:13px;font-weight:800;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;">2</span>
<span style="font-size:14px;font-weight:700;color:var(--accent);">Code Walkthrough ← You are here</span></div>
<p style="margin:0;font-size:12px;color:var(--text);">Actual code, line-by-line. Value set calls, ISNULL, SourceSystemId, ESS_LOG_WRITE, Cancel branching.</p></div>
<div style="flex:1;min-width:200px;background:var(--bg-subtle);border-radius:8px;padding:16px 18px;border-left:4px solid var(--border);">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
<span style="background:var(--border);color:#fff;font-size:13px;font-weight:800;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;">3</span>
<span style="font-size:14px;font-weight:700;color:#bbb;">Build Your Own <span style="font-size:11px;background:#eee;padding:2px 8px;border-radius:8px;color:#999;">Soon</span></span></div>
<p style="margin:0;font-size:12px;color:#bbb;">WSA code, HDL config, test loads, production debugging.</p></div>
</div>

<!-- ══════ AUTHOR ══════ -->
<div style="display:flex;align-items:center;gap:14px;margin-bottom:32px;padding:14px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
<div style="background:linear-gradient(135deg,var(--accent),#B8501F);color:#fff;font-size:15px;font-weight:800;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;">AM</div>
<div><div style="font-weight:700;font-size:15px;">Abhishek Mohanty</div><div style="font-size:13px;color:#888;line-height:1.5;">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant</div></div>
</div>

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- BEFORE WE START: ENGINE FLOW                               -->
<!-- ═══════════════════════════════════════════════════════════ -->
<h2 style="font-size:22px;font-weight:700;color:var(--dark);margin:30px 0 16px;font-family:inherit;">OPERATION Routing in HDL Transformation Formula — FILETYPE, DELIMITER, METADATA</h2>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">The HDL engine calls your formula many times. The OPERATION variable tells the formula <em>why</em> it's being called. Here's the routing code that handles each call:</p>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">OPERATION Routing — Setup Handshake</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln"> 1</span><span style="color:#569CD6;font-weight:700;">IF</span> <span style="color:#B5CEA8;">OPERATION</span> = <span style="color:#CE9178;">'FILETYPE'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln"> 2</span>   <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'DELIMITED'</span>
<span class="ln"> 3</span><span style="color:#569CD6;font-weight:700;">ELSE IF</span> <span style="color:#B5CEA8;">OPERATION</span> = <span style="color:#CE9178;">'DELIMITER'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln"> 4</span>   <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">','</span>
<span class="ln"> 5</span><span style="color:#569CD6;font-weight:700;">ELSE IF</span> <span style="color:#B5CEA8;">OPERATION</span> = <span style="color:#CE9178;">'READ'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln"> 6</span>   <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'NONE'</span>
<span class="ln"> 7</span><span style="color:#569CD6;font-weight:700;">ELSE IF</span> <span style="color:#B5CEA8;">OPERATION</span> = <span style="color:#CE9178;">'NUMBEROFBUSINESSOBJECTS'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln"> 8</span>(
<span class="ln"> 9</span>   <span style="color:#B5CEA8;">OUTPUTVALUE</span> = <span style="color:#CE9178;">'2'</span>                              <span style="color:#57A64A;font-style:italic;">/* ElementEntry + ElementEntryValue */</span>
<span class="ln">10</span>   <span style="color:#569CD6;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">OUTPUTVALUE</span>
<span class="ln">11</span>)</pre>
</div>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">OPERATION Routing — METADATA Header Definitions</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln">12</span><span style="color:#569CD6;font-weight:700;">ELSE IF</span> <span style="color:#B5CEA8;">OPERATION</span> = <span style="color:#CE9178;">'METADATALINEINFORMATION'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln">13</span>(
<span class="ln">14</span>    <span style="color:#57A64A;font-style:italic;">/* Object 1: ElementEntry columns */</span>
<span class="ln">15</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">1</span>] = <span style="color:#CE9178;">'ElementEntry'</span>               <span style="color:#57A64A;font-style:italic;">/* FileName (reserved)        */</span>
<span class="ln">16</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">2</span>] = <span style="color:#CE9178;">'ElementEntry'</span>               <span style="color:#57A64A;font-style:italic;">/* FileDiscriminator (reserved)*/</span>
<span class="ln">17</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">3</span>] = <span style="color:#CE9178;">'LegislativeDataGroupName'</span>
<span class="ln">18</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">4</span>] = <span style="color:#CE9178;">'EffectiveStartDate'</span>
<span class="ln">19</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">5</span>] = <span style="color:#CE9178;">'ElementName'</span>
<span class="ln">20</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">6</span>] = <span style="color:#CE9178;">'AssignmentNumber'</span>
<span class="ln">21</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">7</span>] = <span style="color:#CE9178;">'CreatorType'</span>
<span class="ln">22</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">8</span>] = <span style="color:#CE9178;">'EntryType'</span>
<span class="ln">23</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">9</span>] = <span style="color:#CE9178;">'MultipleEntryCount'</span>
<span class="ln">24</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">10</span>] = <span style="color:#CE9178;">'SourceSystemOwner'</span>
<span class="ln">25</span>    <span style="color:#B5CEA8;">METADATA1</span>[<span style="color:#DCDCAA;">11</span>] = <span style="color:#CE9178;">'SourceSystemId'</span>
<span class="ln">26</span>
<span class="ln">27</span>    <span style="color:#57A64A;font-style:italic;">/* Object 2: ElementEntryValue columns */</span>
<span class="ln">28</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">1</span>] = <span style="color:#CE9178;">'ElementEntry'</span>               <span style="color:#57A64A;font-style:italic;">/* FileName (reserved)        */</span>
<span class="ln">29</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">2</span>] = <span style="color:#CE9178;">'ElementEntryValue'</span>          <span style="color:#57A64A;font-style:italic;">/* FileDiscriminator (reserved)*/</span>
<span class="ln">30</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">3</span>] = <span style="color:#CE9178;">'LegislativeDataGroupName'</span>
<span class="ln">31</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">4</span>] = <span style="color:#CE9178;">'EffectiveStartDate'</span>
<span class="ln">32</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">5</span>] = <span style="color:#CE9178;">'ElementName'</span>
<span class="ln">33</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">6</span>] = <span style="color:#CE9178;">'AssignmentNumber'</span>
<span class="ln">34</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">7</span>] = <span style="color:#CE9178;">'InputValueName'</span>
<span class="ln">35</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">8</span>] = <span style="color:#CE9178;">'EntryType'</span>
<span class="ln">36</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">9</span>] = <span style="color:#CE9178;">'MultipleEntryCount'</span>
<span class="ln">37</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">10</span>] = <span style="color:#CE9178;">'ScreenEntryValue'</span>           <span style="color:#57A64A;font-style:italic;">/* the actual dollar amount    */</span>
<span class="ln">38</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">11</span>] = <span style="color:#CE9178;">'ElementEntryId(SourceSystemId)'</span>  <span style="color:#57A64A;font-style:italic;">/* parent link */</span>
<span class="ln">39</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">12</span>] = <span style="color:#CE9178;">'SourceSystemOwner'</span>
<span class="ln">40</span>    <span style="color:#B5CEA8;">METADATA2</span>[<span style="color:#DCDCAA;">13</span>] = <span style="color:#CE9178;">'SourceSystemId'</span>
<span class="ln">41</span>
<span class="ln">42</span>    <span style="color:#569CD6;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">METADATA1</span>, <span style="color:#B5CEA8;">METADATA2</span>
<span class="ln">43</span>)</pre>
</div>

<div class="ipe">
<p><strong>Lines 1–11:</strong> Setup handshake. The engine asks config questions, the formula answers. Same in every HDL formula.</p>
<p><strong>Lines 14–25:</strong> METADATA1 defines the .dat columns for ElementEntry. Lines 28–40: METADATA2 defines columns for ElementEntryValue. The column names here must exactly match the variable names in the RETURN statement later.</p>
</div>

<!-- ══════ WHAT THIS POST COVERS ══════ -->
<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">What This Post Covers</h3>
<div style="background:var(--bg-subtle);border-radius:8px;padding:18px 22px;margin-bottom:28px;">
<table style="width:100%;border-collapse:collapse;font-size:14px;">
<tr style="border-bottom:1px solid var(--border);"><td style="padding:8px 12px;font-weight:700;color:var(--accent);width:30px;">1</td><td style="padding:8px 12px;font-weight:700;">Full INPUTS ARE Block</td><td style="padding:8px 12px;color:#888;">Every POSITION mapped to its vendor column.</td></tr>
<tr style="border-bottom:1px solid var(--border);"><td style="padding:8px 12px;font-weight:700;color:var(--accent);">2</td><td style="padding:8px 12px;font-weight:700;">GET_VALUE_SET Calls</td><td style="padding:8px 12px;color:#888;">How the formula talks to the database.</td></tr>
<tr style="border-bottom:1px solid var(--border);"><td style="padding:8px 12px;font-weight:700;color:var(--accent);">3</td><td style="padding:8px 12px;font-weight:700;">SourceSystemId Logic</td><td style="padding:8px 12px;color:#888;">"Am I updating old or creating new?"</td></tr>
<tr style="border-bottom:1px solid var(--border);"><td style="padding:8px 12px;font-weight:700;color:var(--accent);">4</td><td style="padding:8px 12px;font-weight:700;">ESS_LOG_WRITE Debugging</td><td style="padding:8px 12px;color:#888;">Printing debug messages to the log.</td></tr>
<tr><td style="padding:8px 12px;font-weight:700;color:var(--accent);">5</td><td style="padding:8px 12px;font-weight:700;">LINEREPEATNO Output Logic</td><td style="padding:8px 12px;color:#888;">Pass 1 (ElementEntry), Pass 2 (ElementEntryValue), and Cancel End-Dating</td></tr>
</table>
</div>
<p style="font-size:15px;color:var(--text);margin-bottom:14px;"><strong>Not in this post:</strong> WSA caching code. Part 1 explained the concept. Part 3 will show the full WSA_EXISTS / WSA_GET / WSA_SET implementation.</p>

<hr style="border:none;border-top:1px solid var(--border);margin:36px 0;">

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- SECTION 1: INPUTS ARE                                      -->
<!-- ═══════════════════════════════════════════════════════════ -->
<h2 style="font-size:22px;font-weight:700;color:var(--dark);margin:30px 0 16px;font-family:inherit;">INPUTS ARE and DEFAULT FOR — Declaring POSITION Variables in Fast Formula</h2>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">Every formula starts by declaring what data it expects. The HDL engine reads your CSV file and puts each column into a POSITION variable — column 1 → POSITION1, column 2 → POSITION2, and so on.</p>

<!-- ── CSV → POSITION pipeline ── -->
<div class="diag">
<div class="diag-title">How the Engine Maps CSV Columns to POSITION Variables</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:12px;background:var(--code-bg);color:#C8C9D4;padding:12px 16px;border-radius:8px;margin-bottom:16px;overflow-x:auto;">
<span style="color:#57A64A;">/* Your CSV row: */</span>  <span style="color:#DCDCAA;">1</span><span style="color:#666;">,</span><span style="color:#CE9178;">DENTAL01</span><span style="color:#666;">,</span><span style="color:#CE9178;">2024-01-15</span><span style="color:#666;">,</span><span style="color:#CE9178;">100045</span><span style="color:#666;">,</span><span style="color:#CE9178;">E12345</span><span style="color:#666;">,</span><span style="color:#DCDCAA;">150.00</span><span style="color:#666;">,</span><span style="color:#888;">...</span>
</div>
<div class="pipeline" style="gap:4px;">
<div class="pipe-node"><div class="pipe-label">COL 1</div><div class="pipe-value" style="color:var(--muted);">1</div><div class="pipe-sub">POSITION1</div></div>
<div class="pipe-connector"></div>
<div class="pipe-node accent"><div class="pipe-label" style="color:var(--accent);">COL 2 ★</div><div class="pipe-value" style="color:var(--accent);">DENTAL01</div><div class="pipe-sub">POSITION2</div></div>
<div class="pipe-connector"></div>
<div class="pipe-node accent"><div class="pipe-label" style="color:var(--accent);">COL 3 ★</div><div class="pipe-value" style="color:var(--accent);">2024-01-15</div><div class="pipe-sub">POSITION3</div></div>
<div class="pipe-connector"></div>
<div class="pipe-node accent"><div class="pipe-label" style="color:var(--accent);">COL 4 ★</div><div class="pipe-value" style="color:var(--accent);">100045</div><div class="pipe-sub">POSITION4</div></div>
<div class="pipe-connector"></div>
<div class="pipe-node"><div class="pipe-label">COL 5</div><div class="pipe-value" style="color:var(--muted);">E12345</div><div class="pipe-sub">POSITION5</div></div>
<div class="pipe-connector"></div>
<div class="pipe-node accent"><div class="pipe-label" style="color:var(--accent);">COL 6 ★</div><div class="pipe-value" style="color:var(--accent);">150.00</div><div class="pipe-sub">POSITION6</div></div>
</div>
<div style="text-align:center;font-size:11px;color:var(--muted);margin-top:10px;">★ Columns actively used in the MAP logic. Others are declared but not referenced.</div>
</div>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">Here's the actual declaration code:</p>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">XXTAV_HDL_ACCRUAL_INBOUND — Input Declaration</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln"> 1</span><span style="color:#569CD6;font-weight:700;">INPUTS ARE</span> <span style="color:#B5CEA8;">OPERATION</span> (<span style="color:#4EC9B0;">TEXT</span>),          <span style="color:#57A64A;font-style:italic;">/* Engine control signal                          */</span>
<span class="ln"> 2</span><span style="color:#B5CEA8;">LINEREPEATNO</span> (<span style="color:#4EC9B0;">NUMBER</span>),                   <span style="color:#57A64A;font-style:italic;">/* Which pass: 1 = header, 2 = value row          */</span>
<span class="ln"> 3</span><span style="color:#B5CEA8;">LINENO</span> (<span style="color:#4EC9B0;">NUMBER</span>),                         <span style="color:#57A64A;font-style:italic;">/* Source file line number                         */</span>
<span class="ln"> 4</span><span style="color:#B5CEA8;">POSITION1</span> (<span style="color:#4EC9B0;">TEXT</span>),                         <span style="color:#57A64A;font-style:italic;">/* LINE_SEQUENCE                                   */</span>
<span class="ln"> 5</span><span style="color:#B5CEA8;">POSITION2</span> (<span style="color:#4EC9B0;">TEXT</span>),                         <span style="color:#57A64A;font-style:italic;">/* XXTAV_CODE — vendor pay code              ★    */</span>
<span class="ln"> 6</span><span style="color:#B5CEA8;">POSITION3</span> (<span style="color:#4EC9B0;">TEXT</span>),                         <span style="color:#57A64A;font-style:italic;">/* EFFECTIVE_START_DATE — YYYY-MM-DD          ★    */</span>
<span class="ln"> 7</span><span style="color:#B5CEA8;">POSITION4</span> (<span style="color:#4EC9B0;">TEXT</span>),                         <span style="color:#57A64A;font-style:italic;">/* PERSON_NUMBER                              ★    */</span>
<span class="ln"> 8</span><span style="color:#B5CEA8;">POSITION5</span> (<span style="color:#4EC9B0;">TEXT</span>),                         <span style="color:#57A64A;font-style:italic;">/* ASSIGNMENT_NUMBER                               */</span>
<span class="ln"> 9</span><span style="color:#B5CEA8;">POSITION6</span> (<span style="color:#4EC9B0;">TEXT</span>),                         <span style="color:#57A64A;font-style:italic;">/* XXTAV_PTO_BALANCE — the dollar amount         ★    */</span>
<span class="ln">10</span><span style="color:#B5CEA8;">POSITION7</span> (<span style="color:#4EC9B0;">TEXT</span>),  <span style="color:#B5CEA8;">POSITION8</span> (<span style="color:#4EC9B0;">TEXT</span>),    <span style="color:#57A64A;font-style:italic;">/* AMOUNT, EARNED_DATE                             */</span>
<span class="ln">11</span><span style="color:#B5CEA8;">POSITION9</span> (<span style="color:#4EC9B0;">TEXT</span>),  <span style="color:#B5CEA8;">POSITION10</span> (<span style="color:#4EC9B0;">TEXT</span>),  <span style="color:#57A64A;font-style:italic;">/* LOC, LOB                                        */</span>
<span class="ln">12</span><span style="color:#B5CEA8;">POSITION11</span> (<span style="color:#4EC9B0;">TEXT</span>)                         <span style="color:#57A64A;font-style:italic;">/* DEPARTMENT                                      */</span></pre>
</div>

<div class="ipe">
<p><strong>In plain English:</strong> This block says: "Engine, when you call me, give me three system variables (OPERATION, LINEREPEATNO, LINENO) and eleven data variables (POSITION1–11) — one for each column in my CSV." The ★ marks show which four columns the formula actually uses. The rest are declared because the engine fills them regardless.</p>
</div>

<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">DEFAULT FOR — Why Every POSITION Variable Needs a Default</h3>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#569CD6;font-weight:700;">DEFAULT FOR</span> <span style="color:#B5CEA8;">LINENO</span> <span style="color:#569CD6;">IS</span> <span style="color:#DCDCAA;">1</span>
<span style="color:#569CD6;font-weight:700;">DEFAULT FOR</span> <span style="color:#B5CEA8;">LINEREPEATNO</span> <span style="color:#569CD6;">IS</span> <span style="color:#DCDCAA;">1</span>
<span style="color:#569CD6;font-weight:700;">DEFAULT FOR</span> <span style="color:#B5CEA8;">POSITION1</span> <span style="color:#569CD6;">IS</span> <span style="color:#CE9178;">'NO DATA'</span>
<span style="color:#57A64A;font-style:italic;">/* ... same for POSITION2 through POSITION11 ... */</span>
<span style="color:#569CD6;font-weight:700;">DEFAULT FOR</span> <span style="color:#B5CEA8;">POSITION11</span> <span style="color:#569CD6;">IS</span> <span style="color:#CE9178;">'NO DATA'</span></pre>

<div class="ipe">
<p><strong>Why?</strong> Look at the engine timeline above. The first five calls (FILETYPE, DELIMITER, etc.) happen <em>before</em> any CSV row is read. POSITION variables are empty during those calls. Without defaults, the formula crashes with a null error before it even reaches the MAP block.</p>
</div>

<hr style="border:none;border-top:1px solid var(--border);margin:36px 0;">

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- SECTION 2: GET_VALUE_SET                                   -->
<!-- ═══════════════════════════════════════════════════════════ -->
<h2 style="font-size:22px;font-weight:700;color:var(--dark);margin:30px 0 16px;font-family:inherit;">GET_VALUE_SET in Fast Formula — Parameter String Syntax, Pipe Delimiters, ISNULL Checks</h2>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">The vendor gives us a code like <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">DENTAL01</code>. Oracle doesn't know it. We need to ask the database: "What Element Name does DENTAL01 map to?" GET_VALUE_SET runs a SQL query and brings the answer back.</p>

<!-- ── GET_VALUE_SET pipeline ── -->
<div class="diag">
<div class="diag-title">How GET_VALUE_SET Works</div>
<div class="pipeline">
<div class="pipe-node accent" style="min-width:150px;">
<div class="pipe-label" style="color:var(--accent);">Your Formula</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--dark);">GET_VALUE_SET(<br>'XXTAV_ACCRUAL_ELEMENTS',<br>'DENTAL01')</div>
</div>
<div class="pipe-connector" style="width:40px;"></div>
<div class="pipe-node" style="min-width:150px;">
<div class="pipe-label">Value Set</div>
<div style="font-size:12px;color:var(--muted);line-height:1.5;">Looks up vendor code<br>in the mapping table<br>and returns the Oracle<br>element name</div>
</div>
<div class="pipe-connector" style="width:40px;"></div>
<div class="pipe-node" style="min-width:120px;border-left:3px solid var(--green);">
<div class="pipe-label" style="color:var(--green);">Result</div>
<div class="pipe-value" style="color:var(--green);">Dental EE Deduction</div>
</div>
</div>
</div>

<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">GET_VALUE_SET Call 1 — Resolving Person Number to Assignment Number</h3>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#B5CEA8;">l_AssignmentNumber</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(
    <span style="color:#CE9178;">'XXTAV_GET_LATEST_ASSIGNMENT_NUMBER'</span>,
    <span style="color:#CE9178;">'|=P_PERSON_NUMBER='''</span> || <span style="color:#B5CEA8;">POSITION4</span> || <span style="color:#CE9178;">''''</span>
 || <span style="color:#CE9178;">'|P_EFFECTIVE_START_DATE='''</span>
 || <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#B5CEA8;">POSITION3</span>,<span style="color:#CE9178;">'YYYY-MM-DD'</span>),<span style="color:#CE9178;">'YYYY-MM-DD'</span>)
 || <span style="color:#CE9178;">''''</span>)</pre>

<!-- ── Code annotation strips ── -->
<div style="margin:20px 0;">
<div class="code-annot"><div class="code-annot-line"><span style="color:#B5CEA8;">l_AssignmentNumber</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(</div><div class="code-annot-note">Store the answer here</div></div>
<div class="code-annot"><div class="code-annot-line">  <span style="color:#CE9178;">'XXTAV_GET_LATEST_ASSIGNMENT_NUMBER'</span>,</div><div class="code-annot-note">Which value set to call</div></div>
<div class="code-annot"><div class="code-annot-line">  <span style="color:#CE9178;">'|=P_PERSON_NUMBER='''</span> || <span style="color:#B5CEA8;text-decoration:underline;">POSITION4</span> || <span style="color:#CE9178;">''''</span></div><div class="code-annot-note">Param 1: Person# (100045)</div></div>
<div class="code-annot"><div class="code-annot-line"> || <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#B5CEA8;text-decoration:underline;">POSITION3</span>,...),<span style="color:#CE9178;">'YYYY-MM-DD'</span>)</div><div class="code-annot-note">Param 2: Date (normalized)</div></div>
</div>

<!-- ── Date normalization pipeline ── -->
<div class="diag" style="padding:20px;">
<div class="diag-title">TO_DATE → TO_CHAR: Date Normalization Pipeline</div>
<div class="pipeline">
<div class="pipe-node" style="border-left:3px solid var(--red);"><div class="pipe-label" style="color:var(--red);">Raw Input</div><div class="pipe-value">POSITION3</div><div class="pipe-sub">'2024-01-15' or '2024/01/15'</div></div>
<div class="pipe-connector" style="width:28px;"></div>
<div class="pipe-node"><div class="pipe-label">TO_DATE( )</div><div class="pipe-sub">Parse string → date object</div><div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent);margin-top:4px;">15-JAN-2024</div></div>
<div class="pipe-connector" style="width:28px;"></div>
<div class="pipe-node"><div class="pipe-label">TO_CHAR( )</div><div class="pipe-sub">Date object → clean string</div><div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--green);margin-top:4px;">2024-01-15</div></div>
<div class="pipe-connector" style="width:28px;"></div>
<div class="pipe-node" style="border-left:3px solid var(--green);"><div class="pipe-label" style="color:var(--green);">Clean Output</div><div class="pipe-sub">Ready to pass into<br>the value set</div></div>
</div>
</div>

<div class="ipe">
<p><strong>Why convert twice?</strong> The vendor might change date formats. TO_DATE reads whatever arrives. TO_CHAR writes it in the exact format the value set expects. Your formula works either way without code changes.</p>
</div>

<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">GET_VALUE_SET Call 2 — Mapping Vendor Code to Oracle Element Name</h3>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#B5CEA8;">l_ElementName</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(
    <span style="color:#CE9178;">'XXTAV_ACCRUAL_ELEMENTS TEST'</span>,
    <span style="color:#CE9178;">'|=P_PAY_CODE='''</span> || <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#B5CEA8;">POSITION2</span>) || <span style="color:#CE9178;">''''</span>)</pre>

<div class="ipe">
<p><strong>Simplest call — one parameter.</strong> Takes the vendor code from POSITION2, strips whitespace with TRIM(), and asks: "What Oracle Element Name does this map to?" If the vendor sends <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">' DENTAL01 '</code> with spaces, TRIM cleans it first.</p>
</div>

<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">ISNULL in Fast Formula — Why 'N' Means Null (Not What You Expect)</h3>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#569CD6;font-weight:700;">IF</span> <span style="color:#DCDCAA;">ISNULL</span>(<span style="color:#B5CEA8;">l_MultipleEntryCount</span>) = <span style="color:#CE9178;">'N'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
(
    <span style="color:#B5CEA8;">l_MultipleEntryCount</span> = <span style="color:#CE9178;">'1'</span>     <span style="color:#57A64A;font-style:italic;">/* default to 1 */</span>
)</pre>

<!-- ── ISNULL decision cards ── -->
<div class="decision-pair" style="margin:18px 0;">
<div class="decision-card">
<div class="decision-card-head" style="background:var(--green);color:#fff;">ISNULL(x) = 'Y' → value exists ✓</div>
<div class="decision-card-body">
<div style="font-family:'JetBrains Mono',monospace;font-size:12px;line-height:2;">
l_MEC = <strong>'3'</strong><br>
ISNULL('3') → <span style="color:var(--green);font-weight:700;">'Y'</span><br>
Is 'Y' = 'N'? → <strong>No</strong><br>
<span style="color:var(--green);">→ Skip IF. Keep '3'.</span>
</div>
</div>
</div>
<div class="decision-card">
<div class="decision-card-head" style="background:var(--red);color:#fff;">ISNULL(x) = 'N' → value is null ✗</div>
<div class="decision-card-body">
<div style="font-family:'JetBrains Mono',monospace;font-size:12px;line-height:2;">
l_MEC = <strong>(null)</strong><br>
ISNULL(null) → <span style="color:var(--red);font-weight:700;">'N'</span><br>
Is 'N' = 'N'? → <strong>Yes</strong><br>
<span style="color:var(--red);">→ Enter IF. Set to '1'.</span>
</div>
</div>
</div>
</div>

<div class="ipe">
<p><strong>Memory trick:</strong> Think of ISNULL as asking "Does this have data? Yes/No." — <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'Y'</code> = Yes, it has data. <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'N'</code> = No data. So <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">= 'N'</code> means "nothing found."</p>
</div>

<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">Value Set Dependency Chain — Why Call Order Matters in the MAP Block</h3>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">These GET_VALUE_SET calls are not independent. Each one depends on the result of a previous one. The formula resolves values in a specific order because later calls need the output of earlier ones as input:</p>

<!-- Value set dependency chain -->
<div class="diag">
<div class="diag-title">Value Set Resolution Chain — Each Step Feeds the Next</div>
<div class="timeline">

<div class="tl-step">
<div class="tl-dot active"></div>
<div class="tl-label">Call 1 — Element Name</div>
<div class="tl-desc">Uses: <strong>POSITION2</strong> (vendor code)<br>Produces: <strong style="color:var(--accent);">l_ElementName</strong></div>
<div class="tl-result">DENTAL01 → 'Dental EE Deduction'</div>
<div style="font-size:11px;color:var(--muted);margin-top:4px;">No dependencies — this call only needs the raw vendor code from the CSV.</div>
</div>

<div class="tl-step">
<div class="tl-dot active"></div>
<div class="tl-label">Call 2 — Assignment Number</div>
<div class="tl-desc">Uses: <strong>POSITION4</strong> (person#) + <strong>POSITION3</strong> (date)<br>Produces: <strong style="color:var(--accent);">l_AssignmentNumber</strong></div>
<div class="tl-result">100045 + 2024-01-15 → 'E12345'</div>
<div style="font-size:11px;color:var(--muted);margin-top:4px;">No dependencies — uses raw CSV values directly.</div>
</div>

<div class="tl-step">
<div class="tl-dot active"></div>
<div class="tl-label">Call 3 — MultipleEntryCount</div>
<div class="tl-desc">Uses: <strong>POSITION4</strong> + <strong>POSITION3</strong> + <strong style="color:var(--accent);">l_ElementName</strong> ← <em>from Call 1</em><br>Produces: <strong style="color:var(--accent);">l_MultipleEntryCount</strong></div>
<div class="tl-result">100045 + 2024-01-15 + 'Dental EE Deduction' → '1'</div>
<div style="font-size:11px;color:var(--red);margin-top:4px;">Depends on Call 1. If you swap the order, l_ElementName is empty and this call returns wrong results.</div>
</div>

<div class="tl-step">
<div class="tl-dot active"></div>
<div class="tl-label">Call 4 — SourceSystemId</div>
<div class="tl-desc">Uses: <strong>POSITION4</strong> + <strong>POSITION3</strong> + <strong style="color:var(--accent);">l_ElementName</strong> ← <em>from Call 1</em><br>Produces: <strong style="color:var(--accent);">l_SourceSystemId</strong></div>
<div class="tl-result">Lookup existing SSID or construct new one</div>
<div style="font-size:11px;color:var(--red);margin-top:4px;">Depends on Call 1. Also uses l_AssignmentNumber from Call 2 when constructing a new ID.</div>
</div>

</div>
</div>

<div class="ipe">
<p><strong>The key insight:</strong> Call 1 (Element Name) and Call 2 (Assignment Number) can run in any order — they only use raw POSITION values from the CSV. But Calls 3 and 4 <strong>must</strong> come after Call 1 because they pass <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_ElementName</code> as a parameter. If you rearrange the formula and move Call 3 above Call 1, the element name variable will be empty and the value set will return the wrong result — or nothing at all.</p>
<p>This is a common mistake when modifying someone else's formula. The calls look independent, but they chain.</p>
</div>

<hr style="border:none;border-top:1px solid var(--border);margin:36px 0;">

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- SECTION 3: SOURCESYSTEMID                                  -->
<!-- ═══════════════════════════════════════════════════════════ -->
<h2 style="font-size:22px;font-weight:700;color:var(--dark);margin:30px 0 16px;font-family:inherit;">SourceSystemId in HDL — Lookup-or-Construct Pattern for MERGE</h2>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">Every element entry has a SourceSystemId — a unique name tag. During MERGE, Oracle checks: "Do I already have an entry with this tag?" If yes → update. If no → create. The formula follows a two-step pattern:</p>

<!-- ── Decision flow ── -->
<div class="diag">
<div class="diag-title">SourceSystemId Resolution Flow</div>
<div class="timeline">
<div class="tl-step">
<div class="tl-dot active"></div>
<div class="tl-label">Step 1 — Ask the cloud</div>
<div class="tl-desc">"Does a SourceSystemId already exist for this person + element + date?"</div>
<div class="tl-result">GET_VALUE_SET('XXTAV_GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID', ...)</div>
</div>
<div class="tl-step">
<div class="tl-dot"></div>
<div class="tl-label">Step 2 — Check what came back</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px;">
<div style="flex:1;min-width:180px;background:#fff;border-radius:8px;padding:12px;box-shadow:0 1px 4px rgba(0,0,0,0.05);border-left:3px solid var(--green);">
<div style="font-size:12px;font-weight:700;color:var(--green);">Found → Reuse it</div>
<div style="font-size:11px;color:var(--muted);margin-top:4px;">Oracle will UPDATE the existing entry</div>
</div>
<div style="flex:1;min-width:180px;background:#fff;border-radius:8px;padding:12px;box-shadow:0 1px 4px rgba(0,0,0,0.05);border-left:3px solid var(--red);">
<div style="font-size:12px;font-weight:700;color:var(--red);">Not found → Build a new one</div>
<div style="font-size:11px;color:var(--muted);margin-top:4px;">Oracle will INSERT a new entry</div>
</div>
</div>
</div>
</div>
</div>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#57A64A;font-style:italic;">/* Step 1: Try cloud lookup */</span>
<span style="color:#B5CEA8;">l_SourceSystemId</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(
    <span style="color:#CE9178;">'XXTAV_GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID'</span>,
    <span style="color:#CE9178;">'|=P_PERSON_NUMBER='''</span> || <span style="color:#B5CEA8;">POSITION4</span> || <span style="color:#CE9178;">''''</span>
 || <span style="color:#CE9178;">'|P_EFFECTIVE_START_DATE='''</span> || <span style="color:#B5CEA8;">...</span> || <span style="color:#CE9178;">''''</span>
 || <span style="color:#CE9178;">'|P_ELEMENT_NAME='''</span> || <span style="color:#B5CEA8;">l_ElementName</span> || <span style="color:#CE9178;">''''</span>)

<span style="color:#57A64A;font-style:italic;">/* Step 2: If null → build new */</span>
<span style="color:#569CD6;font-weight:700;">IF</span> <span style="color:#DCDCAA;">ISNULL</span>(<span style="color:#B5CEA8;">l_SourceSystemId</span>) = <span style="color:#CE9178;">'N'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
(
    <span style="color:#B5CEA8;">l_SourceSystemId</span> = <span style="color:#CE9178;">'XXTAV_HDL'</span> || <span style="color:#B5CEA8;">l_AssignmentNumber</span>
        || <span style="color:#CE9178;">'_EE_'</span> || <span style="color:#B5CEA8;">POSITION4</span>
        || <span style="color:#CE9178;">'_'</span>    || <span style="color:#B5CEA8;">POSITION2</span>
        || <span style="color:#CE9178;">'_'</span>    || <span style="color:#B5CEA8;">POSITION3</span>
)</pre>

<!-- ── Segment bar: SSID assembly ── -->
<div class="diag" style="padding:20px;">
<div class="diag-title">SourceSystemId — Assembled from parts</div>
<div class="seg-bar">
<div style="background:var(--accent);color:#fff;">XXTAV_HDL<span class="seg-label">prefix</span></div>
<div style="background:var(--blue);color:#fff;">E12345<span class="seg-label">Assignment#</span></div>
<div style="background:#666;color:#fff;">_EE_<span class="seg-label">marker</span></div>
<div style="background:var(--green);color:#fff;">100045<span class="seg-label">Person#</span></div>
<div style="background:#7B5EA7;color:#fff;">DENTAL01<span class="seg-label">Code</span></div>
<div style="background:var(--red);color:#fff;">2024-01-15<span class="seg-label">Date</span></div>
</div>
<div style="display:flex;gap:12px;justify-content:center;margin-top:12px;">
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;padding:8px 14px;background:var(--code-bg);color:#C8C9D4;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
<span style="color:#888;">ElementEntry:</span> XXTAV_HDL...<strong style="color:var(--green);">_EE_</strong>...
</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;padding:8px 14px;background:var(--code-bg);color:#C8C9D4;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
<span style="color:#888;">EntryValue:</span> XXTAV_HDL...<strong style="color:var(--accent);">_EEV_</strong>...
</div>
</div>
<div style="text-align:center;font-size:11px;color:var(--muted);margin-top:8px;">Only difference between header and value ID: <strong>_EE_</strong> vs <strong>_EEV_</strong></div>
</div>

<hr style="border:none;border-top:1px solid var(--border);margin:36px 0;">

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- SECTION 4: ESS_LOG_WRITE                                   -->
<!-- ═══════════════════════════════════════════════════════════ -->
<h2 style="font-size:22px;font-weight:700;color:var(--dark);margin:30px 0 16px;font-family:inherit;">ESS_LOG_WRITE in HDL Fast Formula — Adding Debug Trace Logs to the MAP Block</h2>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">You can't step through a Fast Formula with a debugger. The only way to see what's happening inside is to write trace messages to the ESS job log. <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ESS_LOG_WRITE</code> prints a message each time the formula passes through it — so you know exactly which step ran, what value it produced, and where it stopped if something fails.</p>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">Place one after every major step in the MAP block. Here's how that looks:</p>

<!-- Professional code block -->
<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">XXTAV_HDL_ACCRUAL_INBOUND — Debug Trace Logs</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln"> 1</span><span style="color:#57A64A;font-style:italic;">/* ─────────────────────────────────────────────── */</span>
<span class="ln"> 2</span><span style="color:#57A64A;font-style:italic;">/*  STEP 1: Log the raw input from the CSV row    */</span>
<span class="ln"> 3</span><span style="color:#57A64A;font-style:italic;">/* ─────────────────────────────────────────────── */</span>
<span class="ln"> 4</span><span style="color:#DCDCAA;">ESS_LOG_WRITE</span>(<span style="color:#CE9178;">'XXTAV > START'</span>
<span class="ln"> 5</span>    || <span style="color:#CE9178;">' | Line='</span>   || <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#B5CEA8;">LINENO</span>)
<span class="ln"> 6</span>    || <span style="color:#CE9178;">' | Code='</span>   || <span style="color:#B5CEA8;">POSITION2</span>
<span class="ln"> 7</span>    || <span style="color:#CE9178;">' | Person='</span> || <span style="color:#B5CEA8;">POSITION4</span>)
<span class="ln"> 8</span>
<span class="ln"> 9</span><span style="color:#57A64A;font-style:italic;">/*  STEP 2: After the element name lookup         */</span>
<span class="ln">10</span><span style="color:#DCDCAA;">ESS_LOG_WRITE</span>(<span style="color:#CE9178;">'XXTAV > ELEMENT = '</span> || <span style="color:#B5CEA8;">l_ElementName</span>)
<span class="ln">11</span>
<span class="ln">12</span><span style="color:#57A64A;font-style:italic;">/*  STEP 3: After the assignment number lookup    */</span>
<span class="ln">13</span><span style="color:#DCDCAA;">ESS_LOG_WRITE</span>(<span style="color:#CE9178;">'XXTAV > ASSIGNMENT = '</span> || <span style="color:#B5CEA8;">l_AssignmentNumber</span>)
<span class="ln">14</span>
<span class="ln">15</span><span style="color:#57A64A;font-style:italic;">/*  STEP 4: Final resolved values before output   */</span>
<span class="ln">16</span><span style="color:#DCDCAA;">ESS_LOG_WRITE</span>(<span style="color:#CE9178;">'XXTAV > MEC='</span> || <span style="color:#B5CEA8;">l_MultipleEntryCount</span>
<span class="ln">17</span>    || <span style="color:#CE9178;">' | SSID='</span> || <span style="color:#B5CEA8;">l_SourceSystemId</span>)</pre>
</div>

<p style="font-size:15px;color:var(--text);margin-bottom:8px;margin-top:22px;">After running <strong>Load Data from File</strong>, open the ESS job log: <strong>Scheduled Processes → your job → Log tab</strong>. You will see output like this:</p>

<!-- ESS Log output block -->
<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">ESS Job Log — Output for Row 1</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln">›</span> XXTAV > START | Line=1 | Code=DENTAL01 | Person=100045
<span class="ln">›</span> XXTAV > ELEMENT = Dental EE Deduction
<span class="ln">›</span> XXTAV > ASSIGNMENT = E12345
<span class="ln">›</span> XXTAV > MEC=1 | SSID=XXTAV_HDLE12345_EE_100045_DENTAL01_2024-01-15</pre>
</div>

<div class="ipe">
<p><strong>How to read it:</strong> Each line is one trace log from a step in your formula. If the formula fails at the assignment lookup, you'll see Steps 1 and 2 in the log but not Step 3 — so you know exactly where it broke. The <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">XXTAV ></code> prefix makes it easy to search for your formula's output in a log that might contain messages from other formulas running in the same batch.</p>
<p><strong>Before production:</strong> Remove or comment out all ESS_LOG_WRITE calls. With 10,000 rows and 4 log calls per row, that's 40,000 extra write operations slowing down your load.</p>
</div>

<hr style="border:none;border-top:1px solid var(--border);margin:36px 0;">

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- SECTION 5: CANCEL vs ACTIVE                                -->
<!-- ═══════════════════════════════════════════════════════════ -->
<h2 style="font-size:22px;font-weight:700;color:var(--dark);margin:30px 0 16px;font-family:inherit;">LINEREPEATNO — How the Formula Generates ElementEntry and ElementEntryValue Output Rows</h2>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">The vendor uses a status field: blank = Active (create/update), <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'C'</code> = Cancel (end-date). The formula handles these two paths completely differently.</p>

<!-- ── Decision cards ── -->
<div class="decision-pair" style="margin:20px 0;">
<div class="decision-card">
<div class="decision-card-head" style="background:var(--green);color:#fff;">Active (POSITION11 = blank)</div>
<div class="decision-card-body">
<div style="font-size:13px;line-height:1.8;color:var(--text);">
<strong>EffectiveStartDate</strong> = vendor date (POSITION3)<br>
<strong>EffectiveEndDate</strong> = <span style="color:var(--muted);">not set</span><br>
<strong>LINEREPEAT</strong> = <span style="color:var(--green);font-weight:700;">'Y'</span> → Pass 2 follows<br>
<span style="color:var(--green);font-weight:600;">Oracle creates or updates the entry</span>
</div>
</div>
</div>
<div class="decision-card">
<div class="decision-card-head" style="background:var(--red);color:#fff;">Cancel (POSITION11 = 'C')</div>
<div class="decision-card-body">
<div style="font-size:13px;line-height:1.8;color:var(--text);">
<strong>EffectiveStartDate</strong> = <span style="color:var(--red);font-weight:600;">fetched from cloud</span><br>
<strong>EffectiveEndDate</strong> = <span style="color:var(--red);font-weight:600;">vendor's cancel date</span><br>
<strong>LINEREPEAT</strong> = <span style="color:var(--red);font-weight:700;">'N'</span> → Done, no Pass 2<br>
<span style="color:var(--red);font-weight:600;">Oracle end-dates the entry</span>
</div>
</div>
</div>
</div>

<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">LINEREPEATNO = 1 — Active Path: Creating the ElementEntry Row</h3>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">On the first pass, the formula sets all output variables for the ElementEntry header. Each variable name must match a METADATA1 column name exactly — that's how the engine knows which .dat column to write it into.</p>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">Active Path — LINEREPEATNO = 1 — Create ElementEntry</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln"> 1</span><span style="color:#569CD6;font-weight:700;">IF</span> <span style="color:#B5CEA8;">LINEREPEATNO</span> = <span style="color:#DCDCAA;">1</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln"> 2</span>(
<span class="ln"> 3</span>    <span style="color:#B5CEA8;">FileName</span>                 = <span style="color:#CE9178;">'ElementEntry'</span>
<span class="ln"> 4</span>    <span style="color:#B5CEA8;">BusinessOperation</span>        = <span style="color:#CE9178;">'MERGE'</span>
<span class="ln"> 5</span>    <span style="color:#B5CEA8;">FileDiscriminator</span>        = <span style="color:#CE9178;">'ElementEntry'</span>        <span style="color:#57A64A;font-style:italic;">/* ← tells engine: use METADATA1 */</span>
<span class="ln"> 6</span>    <span style="color:#B5CEA8;">LegislativeDataGroupName</span> = <span style="color:#B5CEA8;">l_LegislativeDataGroupName</span>
<span class="ln"> 7</span>    <span style="color:#B5CEA8;">AssignmentNumber</span>         = <span style="color:#B5CEA8;">l_AssignmentNumber</span>     <span style="color:#57A64A;font-style:italic;">/* from GET_VALUE_SET Call 1      */</span>
<span class="ln"> 8</span>    <span style="color:#B5CEA8;">ElementName</span>              = <span style="color:#B5CEA8;">l_ElementName</span>          <span style="color:#57A64A;font-style:italic;">/* from GET_VALUE_SET Call 2      */</span>
<span class="ln"> 9</span>    <span style="color:#B5CEA8;">EffectiveStartDate</span>       = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(<span style="color:#B5CEA8;">POSITION3</span>,<span style="color:#CE9178;">'YYYY-MM-DD'</span>),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
<span class="ln">10</span>                                                    <span style="color:#57A64A;font-style:italic;">/* ↑ input YYYY-MM-DD → output YYYY/MM/DD */</span>
<span class="ln">11</span>    <span style="color:#B5CEA8;">MultipleEntryCount</span>       = <span style="color:#B5CEA8;">l_MultipleEntryCount</span>   <span style="color:#57A64A;font-style:italic;">/* from GET_VALUE_SET Call 3      */</span>
<span class="ln">12</span>    <span style="color:#B5CEA8;">EntryType</span>                = <span style="color:#B5CEA8;">l_entry_type</span>           <span style="color:#57A64A;font-style:italic;">/* 'E' = normal entry             */</span>
<span class="ln">13</span>    <span style="color:#B5CEA8;">CreatorType</span>              = <span style="color:#B5CEA8;">l_CreatorType</span>          <span style="color:#57A64A;font-style:italic;">/* 'H' = HDL created              */</span>
<span class="ln">14</span>    <span style="color:#B5CEA8;">SourceSystemOwner</span>        = <span style="color:#B5CEA8;">l_SourceSystemOwner</span>    <span style="color:#57A64A;font-style:italic;">/* from Section 3 lookup          */</span>
<span class="ln">15</span>    <span style="color:#B5CEA8;">SourceSystemId</span>           = <span style="color:#B5CEA8;">l_SourceSystemId</span>       <span style="color:#57A64A;font-style:italic;">/* from Section 3 lookup-or-build */</span>
<span class="ln">16</span>    <span style="color:#B5CEA8;">LINEREPEAT</span>               = <span style="color:#CE9178;">'Y'</span>                    <span style="color:#57A64A;font-style:italic;">/* ← KEY: tells engine to call    */</span>
<span class="ln">17</span>                                                    <span style="color:#57A64A;font-style:italic;">/*   formula again with            */</span>
<span class="ln">18</span>                                                    <span style="color:#57A64A;font-style:italic;">/*   LINEREPEATNO = 2              */</span></pre>
</div>

<div class="ipe">
<p><strong>Line 5:</strong> <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">FileDiscriminator = 'ElementEntry'</code> tells the engine to use the METADATA1 column layout for this row. In Pass 2, this switches to <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'ElementEntryValue'</code> — which uses METADATA2 instead.</p>
<p><strong>Lines 16–18:</strong> This is the entire LINEREPEAT mechanism. Setting <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT = 'Y'</code> tells the engine: "I have more output rows for this same CSV row. Call me again." The engine re-invokes the formula with LINEREPEATNO incremented to 2.</p>
</div>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">After setting the variables, the formula decides what to RETURN. This is the guard logic — if the element lookup failed, skip the row:</p>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">The ISNULL Guard — Two Different RETURN Paths</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln">19</span>    <span style="color:#57A64A;font-style:italic;">/* ─── GUARD: Did the element lookup return a valid name? ─── */</span>
<span class="ln">20</span>
<span class="ln">21</span>    <span style="color:#569CD6;font-weight:700;">IF</span> <span style="color:#DCDCAA;">ISNULL</span>(<span style="color:#B5CEA8;">l_ElementName</span>) = <span style="color:#CE9178;">'N'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln">22</span>    (
<span class="ln">23</span>        <span style="color:#57A64A;font-style:italic;">/* Element IS null → vendor code not in value set mapping.      */</span>
<span class="ln">24</span>        <span style="color:#57A64A;font-style:italic;">/* Return only LINEREPEAT + LINEREPEATNO — no data variables.   */</span>
<span class="ln">25</span>        <span style="color:#57A64A;font-style:italic;">/* Engine writes nothing to .dat for this row. Silent skip.     */</span>
<span class="ln">26</span>        <span style="color:#569CD6;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#B5CEA8;">LINEREPEATNO</span>
<span class="ln">27</span>    )
<span class="ln">28</span>    <span style="color:#569CD6;font-weight:700;">ELSE</span>
<span class="ln">29</span>    (
<span class="ln">30</span>        <span style="color:#57A64A;font-style:italic;">/* Element found → return all output variables.                 */</span>
<span class="ln">31</span>        <span style="color:#57A64A;font-style:italic;">/* Engine writes one MERGE|ElementEntry|... row to the .dat     */</span>
<span class="ln">32</span>        <span style="color:#569CD6;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">BusinessOperation</span>, <span style="color:#B5CEA8;">FileName</span>, <span style="color:#B5CEA8;">FileDiscriminator</span>,
<span class="ln">33</span>               <span style="color:#B5CEA8;">MultipleEntryCount</span>, <span style="color:#B5CEA8;">CreatorType</span>, <span style="color:#B5CEA8;">EffectiveStartDate</span>,
<span class="ln">34</span>               <span style="color:#B5CEA8;">ElementName</span>, <span style="color:#B5CEA8;">LegislativeDataGroupName</span>, <span style="color:#B5CEA8;">EntryType</span>,
<span class="ln">35</span>               <span style="color:#B5CEA8;">AssignmentNumber</span>, <span style="color:#B5CEA8;">SourceSystemOwner</span>, <span style="color:#B5CEA8;">SourceSystemId</span>,
<span class="ln">36</span>               <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#B5CEA8;">LINEREPEATNO</span>
<span class="ln">37</span>    )
<span class="ln">38</span>)</pre>
</div>

<div class="ipe">
<p><strong>Line 26 vs Lines 32–36 — the key difference:</strong> When the element is null (line 26), the formula returns <em>only</em> LINEREPEAT and LINEREPEATNO — no data variables at all. The engine writes nothing to the .dat file and moves on. When the element exists (lines 32–36), the formula returns all the output variables. The engine matches each variable name to the METADATA1 column name and writes a full <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">MERGE|ElementEntry|...</code> row.</p>
</div>

<!-- ── Full journey: one row through both passes ── -->
<div class="diag">
<div class="diag-title">One Vendor Row → Two .dat Rows (Full Journey)</div>
<div class="timeline">
<div class="tl-step">
<div class="tl-dot active"></div>
<div class="tl-label">Vendor CSV Row</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--muted);margin-top:4px;">1, DENTAL01, 2024-01-15, 100045, E12345, <strong style="color:var(--accent);">150.00</strong>, ...</div>
</div>
<div class="tl-step">
<div class="tl-dot active"></div>
<div class="tl-label" style="color:var(--green);">Pass 1 (LINEREPEATNO = 1) → ElementEntry</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--muted);background:#fff;padding:8px 12px;border-radius:6px;margin-top:6px;box-shadow:0 1px 3px rgba(0,0,0,0.04);overflow-x:auto;">MERGE|ElementEntry|US LDG|2024/01/15|Dental EE Deduction|E12345|H|E|1|XXTAV_HDL|XXTAV_HDL...</div>
<div class="tl-result">LINEREPEAT = 'Y' → engine increments LINEREPEATNO to 2, calls formula again</div>
</div>
<div class="tl-step">
<div class="tl-dot active"></div>
<div class="tl-label" style="color:var(--accent);">Pass 2 (LINEREPEATNO = 2) → ElementEntryValue</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--muted);background:#fff;padding:8px 12px;border-radius:6px;margin-top:6px;box-shadow:0 1px 3px rgba(0,0,0,0.04);overflow-x:auto;">MERGE|ElementEntryValue|US LDG|2024/01/15|Dental EE Deduction|E12345|XXTAV_PTO BALANCE|E|1|<strong style="color:var(--accent);">150</strong>|...</div>
<div class="tl-result">LINEREPEAT = 'N' → engine moves to next CSV row</div>
</div>
</div>
</div>

<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">LINEREPEATNO = 1 — Cancel Path: End-Dating with GET_VALUE_SET for Original Start Date</h3>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">The vendor only sends the <em>cancellation date</em>. Oracle also needs the <em>original start date</em>. So the formula fetches it from the cloud:</p>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">Cancel Path — POSITION11 = 'C' — End-Date Entry</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln"> 1</span><span style="color:#569CD6;font-weight:700;">IF</span> (<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#B5CEA8;">POSITION11</span>) = <span style="color:#CE9178;">'C'</span>) <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln"> 2</span>(
<span class="ln"> 3</span>    <span style="color:#57A64A;font-style:italic;">/* Fetch original start date from cloud */</span>
<span class="ln"> 4</span>    <span style="color:#B5CEA8;">l_Effective_Start_Date</span> = <span style="color:#DCDCAA;">GET_VALUE_SET</span>(
<span class="ln"> 5</span>        <span style="color:#CE9178;">'XXTAV_GET_ELEMENT_ENTRY_START_DATE'</span>, ...)
<span class="ln"> 6</span>
<span class="ln"> 7</span>    <span style="color:#B5CEA8;">EffectiveStartDate</span> = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(
<span class="ln"> 8</span>        <span style="color:#B5CEA8;">l_Effective_Start_Date</span>,<span style="color:#CE9178;">'YYYY-MM-DD'</span>),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
<span class="ln"> 9</span>                                          <span style="color:#57A64A;font-style:italic;">/* ↑ from cloud */</span>
<span class="ln">10</span>    <span style="color:#B5CEA8;">EffectiveEndDate</span> = <span style="color:#DCDCAA;">TO_CHAR</span>(<span style="color:#DCDCAA;">TO_DATE</span>(
<span class="ln">11</span>        <span style="color:#DCDCAA;">TRIM</span>(<span style="color:#B5CEA8;">POSITION3</span>),<span style="color:#CE9178;">'YYYY-MM-DD'</span>),<span style="color:#CE9178;">'YYYY/MM/DD'</span>)
<span class="ln">12</span>                                          <span style="color:#57A64A;font-style:italic;">/* ↑ from vendor */</span>
<span class="ln">13</span>    <span style="color:#B5CEA8;">ReplaceLastEffectiveEndDate</span> = <span style="color:#CE9178;">'Y'</span>       <span style="color:#57A64A;font-style:italic;">/* override existing */</span>
<span class="ln">14</span>    <span style="color:#57A64A;font-style:italic;">/* ... same other vars ... */</span>
<span class="ln">15</span>    <span style="color:#B5CEA8;">LINEREPEAT</span> = <span style="color:#CE9178;">'N'</span>                        <span style="color:#57A64A;font-style:italic;">/* done. no pass 2. */</span>
<span class="ln">16</span>
<span class="ln">17</span>    <span style="color:#569CD6;font-weight:700;">RETURN</span> ..., <span style="color:#B5CEA8;">EffectiveStartDate</span>, <span style="color:#B5CEA8;">EffectiveEndDate</span>,
<span class="ln">18</span>           <span style="color:#B5CEA8;">ReplaceLastEffectiveEndDate</span>, <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#B5CEA8;">LINEREPEATNO</span>
<span class="ln">19</span>)</pre>
</div>

<!-- ── Cancel date sources ── -->
<div class="diag">
<div class="diag-title">Cancel Path — Where Each Date Comes From</div>
<div style="display:flex;gap:16px;flex-wrap:wrap;">
<div style="flex:1;min-width:200px;">
<div style="padding:12px 16px;background:var(--blue);color:#fff;border-radius:10px 10px 0 0;font-size:12px;font-weight:700;">EffectiveStartDate</div>
<div style="background:#fff;border:1px solid var(--border);border-top:none;border-radius:0 0 10px 10px;padding:16px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
<div style="font-size:11px;color:var(--muted);margin-bottom:8px;">Source: <strong style="color:var(--blue);">Oracle Cloud</strong></div>
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--blue);background:rgba(74,111,165,0.06);padding:6px 10px;border-radius:4px;">GET_VALUE_SET('XXTAV_GET_EE_START_DATE')</div>
<div style="font-size:12px;color:var(--text);margin-top:8px;">When the entry <strong>originally started</strong></div>
<div style="font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--blue);font-weight:600;margin-top:4px;">2024/01/01</div>
</div>
</div>
<div style="flex:1;min-width:200px;">
<div style="padding:12px 16px;background:var(--red);color:#fff;border-radius:10px 10px 0 0;font-size:12px;font-weight:700;">EffectiveEndDate</div>
<div style="background:#fff;border:1px solid var(--border);border-top:none;border-radius:0 0 10px 10px;padding:16px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
<div style="font-size:11px;color:var(--muted);margin-bottom:8px;">Source: <strong style="color:var(--red);">Vendor File</strong></div>
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--red);background:rgba(184,66,58,0.06);padding:6px 10px;border-radius:4px;">POSITION3 (cancellation date)</div>
<div style="font-size:12px;color:var(--text);margin-top:8px;">When the entry <strong>should end</strong></div>
<div style="font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--red);font-weight:600;margin-top:4px;">2024/03/15</div>
</div>
</div>
</div>
</div>

<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">Pass 2: Loading the Dollar Amount (LINEREPEATNO = 2)</h3>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">The engine calls the formula again. Same CSV row. But LINEREPEATNO is now 2.</p>

<p style="font-size:15px;color:var(--text);margin-bottom:10px;"><strong>First — clean the amount:</strong></p>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">Pass 2 — Clean the Dollar Amount</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln">1</span><span style="color:#569CD6;font-weight:700;">ELSE IF</span> (<span style="color:#B5CEA8;">LINEREPEATNO</span> = <span style="color:#DCDCAA;">2</span>) <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln">2</span>(
<span class="ln">3</span>    <span style="color:#B5CEA8;">l_ScreenEntryValue</span> = <span style="color:#DCDCAA;">RTRIM</span>(<span style="color:#DCDCAA;">RTRIM</span>(<span style="color:#DCDCAA;">TRIM</span>(<span style="color:#B5CEA8;">POSITION6</span>),<span style="color:#CE9178;">'0'</span>),<span style="color:#CE9178;">'.'</span>)
<span class="ln">4</span>
<span class="ln">5</span>    <span style="color:#569CD6;font-weight:700;">IF</span> <span style="color:#DCDCAA;">ISNULL</span>(<span style="color:#B5CEA8;">l_ScreenEntryValue</span>) = <span style="color:#CE9178;">'N'</span> <span style="color:#569CD6;font-weight:700;">THEN</span>
<span class="ln">6</span>    (   <span style="color:#B5CEA8;">l_ScreenEntryValue</span> = <span style="color:#CE9178;">'0'</span>   )</pre>
</div>

<p style="font-size:14px;color:var(--text);margin:8px 0;">Line 3 strips trailing zeros and dots. If the result is empty, line 5 defaults to '0'.</p>

<div class="diag" style="padding:14px 20px;">
<div class="diag-title">What line 3 does to different amounts</div>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="border-bottom:1px solid var(--border);"><td style="padding:6px 12px;font-family:'JetBrains Mono',monospace;color:var(--muted);">150.00</td><td style="padding:6px 12px;font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);">→ 150</td></tr>
<tr style="border-bottom:1px solid var(--border);"><td style="padding:6px 12px;font-family:'JetBrains Mono',monospace;color:var(--muted);">75.50</td><td style="padding:6px 12px;font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);">→ 75.5</td></tr>
<tr><td style="padding:6px 12px;font-family:'JetBrains Mono',monospace;color:var(--muted);">200.00</td><td style="padding:6px 12px;font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);">→ 200</td></tr>
</table>
</div>

<p style="font-size:15px;color:var(--text);margin:18px 0 10px;"><strong>Then — set output variables.</strong> Most are the same as Pass 1. Only three things change:</p>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">Pass 2 — The Three Things That Change</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln"> 7</span>    <span style="color:#57A64A;font-style:italic;">/* Change 1: Switch to ElementEntryValue layout */</span>
<span class="ln"> 8</span>    <span style="color:#B5CEA8;">FileDiscriminator</span>     = <span style="color:#CE9178;">'ElementEntryValue'</span>
<span class="ln"> 9</span>
<span class="ln">10</span>    <span style="color:#57A64A;font-style:italic;">/* Change 2: Two new variables — the value data */</span>
<span class="ln">11</span>    <span style="color:#B5CEA8;">InputValueName</span>        = <span style="color:#B5CEA8;">l_InputValueName</span>         <span style="color:#57A64A;font-style:italic;">/* 'XXTAV_PTO BALANCE' */</span>
<span class="ln">12</span>    <span style="color:#B5CEA8;">ScreenEntryValue</span>      = <span style="color:#B5CEA8;">l_ScreenEntryValue</span>       <span style="color:#57A64A;font-style:italic;">/* '150' (cleaned)    */</span>
<span class="ln">13</span>
<span class="ln">14</span>    <span style="color:#57A64A;font-style:italic;">/* Change 3: Done with this row */</span>
<span class="ln">15</span>    <span style="color:#B5CEA8;">LINEREPEAT</span>            = <span style="color:#CE9178;">'N'</span>
<span class="ln">16</span>
<span class="ln">17</span>    <span style="color:#57A64A;font-style:italic;">/* Everything else — same as Pass 1 */</span>
<span class="ln">18</span>    <span style="color:#B5CEA8;">SourceSystemId</span>        = <span style="color:#B5CEA8;">l_EEV_SourceSystemId</span>
<span class="ln">19</span>    <span style="color:#B5CEA8;">SourceSystemOwner</span>     = <span style="color:#B5CEA8;">l_EEV_SourceSystemOwner</span>
<span class="ln">20</span>    <span style="color:#57A64A;font-style:italic;">/* ... AssignmentNumber, ElementName, etc. — same ... */</span></pre>
</div>

<p style="font-size:15px;color:var(--text);margin:18px 0 10px;"><strong>Finally — RETURN:</strong></p>

<div class="code-pro">
<div class="code-pro-header">
<div class="dots"><span style="background:#FF5F56;"></span><span style="background:#FFBD2E;"></span><span style="background:#27C93F;"></span></div>
<div class="label">Pass 2 — RETURN</div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">
<span class="ln">21</span>    <span style="color:#569CD6;font-weight:700;">RETURN</span> <span style="color:#B5CEA8;">BusinessOperation</span>, <span style="color:#B5CEA8;">FileName</span>, <span style="color:#B5CEA8;">FileDiscriminator</span>,
<span class="ln">22</span>           <span style="color:#B5CEA8;">AssignmentNumber</span>, <span style="color:#B5CEA8;">EffectiveStartDate</span>,
<span class="ln">23</span>           <span style="color:#B5CEA8;">ElementName</span>, <span style="color:#B5CEA8;">EntryType</span>,
<span class="ln">24</span>           <span style="color:#B5CEA8;">LegislativeDataGroupName</span>, <span style="color:#B5CEA8;">MultipleEntryCount</span>,
<span class="ln">25</span>           <span style="color:#B5CEA8;">InputValueName</span>, <span style="color:#B5CEA8;">ScreenEntryValue</span>,
<span class="ln">26</span>           <span style="color:#B5CEA8;">SourceSystemOwner</span>, <span style="color:#B5CEA8;">SourceSystemId</span>,
<span class="ln">27</span>           <span style="color:#B5CEA8;">LINEREPEAT</span>, <span style="color:#B5CEA8;">LINEREPEATNO</span>
<span class="ln">28</span>)</pre>
</div>

<p style="font-size:15px;color:var(--text);margin-bottom:6px;">The engine writes this to the .dat file:</p>
<div style="font-family:'JetBrains Mono',monospace;font-size:12px;background:var(--code-bg);color:var(--accent);padding:12px 16px;border-radius:8px;margin:8px 0 20px;overflow-x:auto;">
MERGE|ElementEntryValue|United States LDG|2024/01/15|Dental EE Deduction|E12345|XXTAV_PTO BALANCE|E|1|<strong>150</strong>
</div>

<div class="ipe">
<p><strong>That's it for one row.</strong> Pass 1 creates the header. Pass 2 creates the value. Now the engine moves to the next CSV row and the whole cycle repeats.</p>
</div>

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- ENGINE CALL SEQUENCE — FULL PICTURE                        -->
<!-- ═══════════════════════════════════════════════════════════ -->
<h3 style="font-size:17px;font-weight:700;color:var(--dark);margin:28px 0 14px;font-family:inherit;">Putting It All Together — How the Engine Processes a 3-Row File</h3>

<p style="font-size:15px;color:var(--text);margin-bottom:20px;">Here's a vendor file with 3 rows. Two active deductions and one cancellation. Watch how the engine and formula talk to each other for each row:</p>

<!-- ═══ THE SOURCE FILE ═══ -->
<div style="border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.06);margin:0 0 24px;">
<div style="background:var(--code-bg);padding:10px 16px;display:flex;align-items:center;justify-content:space-between;">
<span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#6B6F88;">vendor_accrual_file.csv</span>
<div style="display:flex;gap:5px;"><span style="width:9px;height:9px;border-radius:50%;background:#FF5F56;"></span><span style="width:9px;height:9px;border-radius:50%;background:#FFBD2E;"></span><span style="width:9px;height:9px;border-radius:50%;background:#27C93F;"></span></div>
</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#6B6F88;">Row 1:</span>  1,<span style="color:var(--green);">DENTAL01</span>,2024-01-15,100045,E12345,<span style="color:var(--green);font-weight:600;">150.00</span>,...
<span style="color:#6B6F88;">Row 2:</span>  2,<span style="color:var(--accent);">MEDICAL01</span>,2024-01-15,100045,E12345,<span style="color:var(--accent);font-weight:600;">200.00</span>,...
<span style="color:#6B6F88;">Row 3:</span>  3,<span style="color:var(--red);">VISION01</span>,2024-03-15,100045,E12345,,<span style="color:var(--red);font-weight:600;">C</span></pre>
</div>

<!-- ═══ ROW 1: DENTAL — ACTIVE ═══ -->
<div style="border-radius:12px;border:1px solid var(--border);overflow:hidden;margin-bottom:16px;box-shadow:0 1px 6px rgba(0,0,0,0.04);">

<!-- Row header -->
<div style="background:var(--bg-subtle);padding:12px 20px;display:flex;align-items:center;justify-content:space-between;">
<div style="display:flex;align-items:center;gap:10px;">
<span style="background:var(--green);color:#fff;font-size:11px;font-weight:700;padding:3px 10px;border-radius:4px;">ROW 1</span>
<span style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;color:var(--dark);">DENTAL01  ·  100045  ·  $150.00</span>
</div>
<span style="font-size:11px;font-weight:600;color:var(--green);letter-spacing:0.5px;">ACTIVE</span>
</div>

<!-- Pass 1 -->
<div style="padding:16px 20px;border-bottom:1px solid var(--border);display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;">
<div style="min-width:60px;">
<div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:0.5px;margin-bottom:4px;">PASS 1</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:800;color:var(--green);">1</div>
</div>
<div style="flex:1;min-width:200px;">
<div style="font-size:13px;color:var(--text);line-height:1.7;">
<span style="color:var(--muted);font-size:11px;">Engine sends LINEREPEATNO =</span> <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);">1</span><br>
<span style="color:var(--muted);font-size:11px;">Formula creates →</span> <strong>ElementEntry</strong> header for <span style="color:var(--green);font-weight:600;">Dental EE Deduction</span>
</div>
</div>
<div style="text-align:right;min-width:120px;">
<div style="font-size:10px;color:var(--muted);margin-bottom:4px;">FORMULA RETURNS</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:var(--green);background:rgba(45,139,111,0.08);padding:4px 10px;border-radius:5px;display:inline-block;">LINEREPEAT = 'Y'</div>
<div style="font-size:11px;color:var(--muted);margin-top:4px;">↓ engine calls again</div>
</div>
</div>

<!-- Pass 2 -->
<div style="padding:16px 20px;display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;background:rgba(212,98,43,0.02);">
<div style="min-width:60px;">
<div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:0.5px;margin-bottom:4px;">PASS 2</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:800;color:var(--accent);">2</div>
</div>
<div style="flex:1;min-width:200px;">
<div style="font-size:13px;color:var(--text);line-height:1.7;">
<span style="color:var(--muted);font-size:11px;">Engine sends LINEREPEATNO =</span> <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--accent);">2</span><br>
<span style="color:var(--muted);font-size:11px;">Formula creates →</span> <strong>ElementEntryValue</strong> with amount <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--accent);">$150</span>
</div>
</div>
<div style="text-align:right;min-width:120px;">
<div style="font-size:10px;color:var(--muted);margin-bottom:4px;">FORMULA RETURNS</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:var(--accent);background:rgba(212,98,43,0.08);padding:4px 10px;border-radius:5px;display:inline-block;">LINEREPEAT = 'N'</div>
<div style="font-size:11px;color:var(--accent);font-weight:600;margin-top:4px;">→ next row</div>
</div>
</div>

</div>

<!-- ═══ ROW 2: MEDICAL — ACTIVE ═══ -->
<div style="border-radius:12px;border:1px solid var(--border);overflow:hidden;margin-bottom:16px;box-shadow:0 1px 6px rgba(0,0,0,0.04);">

<div style="background:var(--bg-subtle);padding:12px 20px;display:flex;align-items:center;justify-content:space-between;">
<div style="display:flex;align-items:center;gap:10px;">
<span style="background:var(--green);color:#fff;font-size:11px;font-weight:700;padding:3px 10px;border-radius:4px;">ROW 2</span>
<span style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;color:var(--dark);">MEDICAL01  ·  100045  ·  $200.00</span>
</div>
<span style="font-size:11px;font-weight:600;color:var(--green);letter-spacing:0.5px;">ACTIVE</span>
</div>

<div style="padding:16px 20px;border-bottom:1px solid var(--border);display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;">
<div style="min-width:60px;">
<div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:0.5px;margin-bottom:4px;">PASS 1</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:800;color:var(--green);">1</div>
</div>
<div style="flex:1;min-width:200px;">
<div style="font-size:13px;color:var(--text);line-height:1.7;">
<span style="color:var(--muted);font-size:11px;">Engine sends LINEREPEATNO =</span> <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);">1</span><br>
<span style="color:var(--muted);font-size:11px;">Formula creates →</span> <strong>ElementEntry</strong> header for <span style="color:var(--green);font-weight:600;">Medical EE Deduction</span>
</div>
</div>
<div style="text-align:right;min-width:120px;">
<div style="font-size:10px;color:var(--muted);margin-bottom:4px;">FORMULA RETURNS</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:var(--green);background:rgba(45,139,111,0.08);padding:4px 10px;border-radius:5px;display:inline-block;">LINEREPEAT = 'Y'</div>
<div style="font-size:11px;color:var(--muted);margin-top:4px;">↓ engine calls again</div>
</div>
</div>

<div style="padding:16px 20px;display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;background:rgba(212,98,43,0.02);">
<div style="min-width:60px;">
<div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:0.5px;margin-bottom:4px;">PASS 2</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:800;color:var(--accent);">2</div>
</div>
<div style="flex:1;min-width:200px;">
<div style="font-size:13px;color:var(--text);line-height:1.7;">
<span style="color:var(--muted);font-size:11px;">Engine sends LINEREPEATNO =</span> <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--accent);">2</span><br>
<span style="color:var(--muted);font-size:11px;">Formula creates →</span> <strong>ElementEntryValue</strong> with amount <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--accent);">$200</span>
</div>
</div>
<div style="text-align:right;min-width:120px;">
<div style="font-size:10px;color:var(--muted);margin-bottom:4px;">FORMULA RETURNS</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:var(--accent);background:rgba(212,98,43,0.08);padding:4px 10px;border-radius:5px;display:inline-block;">LINEREPEAT = 'N'</div>
<div style="font-size:11px;color:var(--accent);font-weight:600;margin-top:4px;">→ next row</div>
</div>
</div>

</div>

<!-- ═══ ROW 3: VISION — CANCEL ═══ -->
<div style="border-radius:12px;border:1px solid rgba(184,66,58,0.25);overflow:hidden;margin-bottom:16px;box-shadow:0 1px 6px rgba(184,66,58,0.06);">

<div style="background:rgba(184,66,58,0.04);padding:12px 20px;display:flex;align-items:center;justify-content:space-between;">
<div style="display:flex;align-items:center;gap:10px;">
<span style="background:var(--red);color:#fff;font-size:11px;font-weight:700;padding:3px 10px;border-radius:4px;">ROW 3</span>
<span style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;color:var(--dark);">VISION01  ·  100045  ·  Status = C</span>
</div>
<span style="font-size:11px;font-weight:600;color:var(--red);letter-spacing:0.5px;">CANCEL</span>
</div>

<!-- Only Pass 1 -->
<div style="padding:16px 20px;display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;">
<div style="min-width:60px;">
<div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:0.5px;margin-bottom:4px;">PASS 1</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:800;color:var(--red);">1</div>
</div>
<div style="flex:1;min-width:200px;">
<div style="font-size:13px;color:var(--text);line-height:1.7;">
<span style="color:var(--muted);font-size:11px;">Engine sends LINEREPEATNO =</span> <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--red);">1</span><br>
<span style="color:var(--muted);font-size:11px;">Formula creates →</span> <strong>ElementEntry</strong> with <span style="color:var(--red);font-weight:600;">end-date</span> for Vision EE Deduction<br>
<span style="color:var(--muted);font-size:11px;">No Pass 2 — cancellation has no dollar amount to load</span>
</div>
</div>
<div style="text-align:right;min-width:120px;">
<div style="font-size:10px;color:var(--muted);margin-bottom:4px;">FORMULA RETURNS</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:var(--red);background:rgba(184,66,58,0.08);padding:4px 10px;border-radius:5px;display:inline-block;">LINEREPEAT = 'N'</div>
<div style="font-size:11px;color:var(--red);font-weight:600;margin-top:4px;">→ done</div>
</div>
</div>

</div>

<!-- Summary -->
<div class="ipe">
<p><strong>3 CSV rows → 5 engine calls.</strong> Active rows get 2 calls (header + value). Cancel rows get 1 call (header only). The formula controls this entirely through <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LINEREPEAT</code>: return <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'Y'</code> to say "call me again", return <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'N'</code> to say "move on."</p>
</div>

<!-- ═══ FINAL .DAT OUTPUT ═══ -->
<h4 style="font-size:15px;font-weight:700;color:var(--dark);margin:24px 0 10px;font-family:inherit;">The Final .dat Output</h4>
<p style="font-size:14px;color:var(--text);margin-bottom:10px;">After all 5 calls, the engine writes this file:</p>

<div style="border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.07);margin:14px 0 24px;">
<div style="background:var(--code-bg);padding:10px 16px;font-family:'JetBrains Mono',monospace;font-size:10px;color:#6B6F88;letter-spacing:0.3px;">ElementEntry.dat — Generated Output</div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#6B6F88;">/* ElementEntry block */</span>
<span style="color:#888;">METADATA|</span>ElementEntry|LDG|EffStart|ElementName|Asg#|Creator|Entry|MEC
<span style="color:var(--green);">MERGE</span>|ElementEntry|US LDG|2024/01/15|<span style="color:var(--green);">Dental EE Deduction</span>|E12345|H|E|1
<span style="color:var(--green);">MERGE</span>|ElementEntry|US LDG|2024/01/15|<span style="color:var(--green);">Medical EE Deduction</span>|E12345|H|E|1
<span style="color:var(--red);">MERGE</span>|ElementEntry|US LDG|<span style="color:var(--red);">2024/01/01</span>|<span style="color:var(--red);">Vision EE Deduction</span>|E12345|H|<span style="color:var(--red);">2024/03/15</span>|E|1

<span style="color:#6B6F88;">/* ElementEntryValue block */</span>
<span style="color:#888;">METADATA|</span>ElementEntryValue|LDG|EffStart|ElementName|Asg#|InputValue|Entry|MEC|ScreenValue
<span style="color:var(--accent);">MERGE</span>|ElementEntryValue|US LDG|2024/01/15|Dental EE|E12345|XXTAV_PTO BALANCE|E|1|<span style="color:var(--accent);font-weight:700;">150</span>
<span style="color:var(--accent);">MERGE</span>|ElementEntryValue|US LDG|2024/01/15|Medical EE|E12345|XXTAV_PTO BALANCE|E|1|<span style="color:var(--accent);font-weight:700;">200</span>
<span style="color:#6B6F88;">/* ↑ No row for Vision — cancel has no dollar amount */</span></pre>
</div>

<hr style="border:none;border-top:1px solid var(--border);margin:36px 0;">

<!-- ══════ WHAT YOU NOW UNDERSTAND ══════ -->
<h2 style="font-size:22px;font-weight:700;color:var(--dark);margin:30px 0 16px;font-family:inherit;">What You Can Now Do After Part 1 and Part 2</h2>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;">After Part 1 and Part 2, you can open any HDL Transformation Formula and read it. You know the engine calls the formula many times — first for setup, then per row, then per pass. You can decode the triple-quote syntax in GET_VALUE_SET calls. You know <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ISNULL(x) = 'N'</code> means the value IS null. You understand lookup-or-construct for SourceSystemId. You know where to put ESS_LOG_WRITE. And you can follow the Cancel vs Active branching.</p>

<p style="font-size:15px;color:var(--text);margin-bottom:14px;"><strong>Left for Part 3:</strong> WSA implementation (WSA_EXISTS / WSA_GET / WSA_SET code), the complete formula assembled end-to-end, and the step-by-step build-your-own guide.</p>

<hr style="border:none;border-top:1px solid var(--border);margin:36px 0;">

<!-- ══════ COMING NEXT ══════ -->
<div style="background:linear-gradient(135deg,var(--accent),#B8501F);border-radius:10px;padding:22px 26px;margin:28px 0;box-shadow:0 4px 16px rgba(212,98,43,0.15);">
<div style="font-size:20px;font-weight:800;color:#fff;margin-bottom:12px;">Coming Next — Part 3: Build Your Own</div>
<p style="font-size:14px;color:rgba(255,255,255,0.9);margin-bottom:16px;">Everything copy-paste ready.</p>
<table style="width:100%;border-collapse:collapse;">
<tr style="border-bottom:1px solid rgba(255,255,255,0.15);"><td style="padding:8px 0;font-size:14px;color:#fff;font-weight:700;">WSA Implementation</td><td style="padding:8px 0;font-size:13px;color:rgba(255,255,255,0.8);">Full WSA_EXISTS / WSA_GET / WSA_SET code</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.15);"><td style="padding:8px 0;font-size:14px;color:#fff;font-weight:700;">Complete Formula</td><td style="padding:8px 0;font-size:13px;color:rgba(255,255,255,0.8);">Assembled end-to-end</td></tr>
<tr><td style="padding:8px 0;font-size:14px;color:#fff;font-weight:700;">Test & Debug</td><td style="padding:8px 0;font-size:13px;color:rgba(255,255,255,0.8);">Load, verify, fix common errors</td></tr>
</table>
</div>

<!-- ══════ ROADMAP BOTTOM ══════ -->
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:32px 0;">
<div style="background:var(--bg-subtle);border-radius:20px;padding:6px 16px;font-size:13px;color:var(--muted);font-weight:600;">Part 1: Pure Concepts</div>
<span style="color:var(--border);">→</span>
<div style="background:var(--accent);border-radius:20px;padding:6px 16px;font-size:13px;color:#fff;font-weight:600;">Part 2: Code Walkthrough ← This post</div>
<span style="color:var(--border);">→</span>
<div style="background:var(--bg-subtle);border-radius:20px;padding:6px 16px;font-size:13px;color:#bbb;font-weight:600;">Part 3: Build Your Own <span style="font-size:10px;background:#eee;padding:1px 6px;border-radius:6px;color:#999;">Soon</span></div>
</div>

<!-- ══════ AUTHOR BOTTOM ══════ -->
<div style="display:flex;align-items:center;gap:14px;padding:18px 0;border-top:1px solid var(--border);">
<div style="background:linear-gradient(135deg,var(--accent),#B8501F);color:#fff;font-size:15px;font-weight:800;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;">AM</div>
<div><div style="font-weight:700;font-size:15px;">Abhishek Mohanty</div><div style="font-size:13px;color:#888;line-height:1.5;">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.</div></div>
</div>

</div>
</body>
</html>