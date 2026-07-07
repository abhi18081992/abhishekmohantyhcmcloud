---
title: "Oracle Fast Formula: Time Entry Rule (Part 4)"
pubDate: 2026-05-29
description: "Oracle Fast Formula: Time Entry Rule (Part 4)"
tags: ["Fast Formula", "Oracle HCM Cloud", "Time & Labor"]
author: "Abhishek Mohanty"
draft: false
---

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
--ink: #2d2926;
--paper: #faf7f2;
--rule: #1a1a1a;
--accent: #c0392b;
--accent-soft: #f4ddd9;
--muted: #7a7570;
--code-bg: #2d2926;
--code-text: #e6e1d8;
--code-keyword: #c678dd;
--code-string: #98c379;
--code-number: #d19a66;
--code-comment: #b8b0a0;
--code-fn: #61afef;
--green: #27704a;
--amber: #b97417;
}
* { box-sizing: border-box; }
body {
font-family: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;
color: var(--ink);
background: var(--paper);
margin: 0;
padding: 0;
line-height: 1.7;
font-size: 17px;
}
.container {
max-width: 100%;
margin: 0;
padding: 0;
box-sizing: border-box;
}
/* Hero */
.meta-tag {
display: inline-block;
font-size: 11px;
font-weight: 700;
letter-spacing: 1.6px;
text-transform: uppercase;
color: var(--accent);
margin-bottom: 18px;
}
h1 {
font-family: 'Manrope', -apple-system, sans-serif;
font-weight: 900;
font-size: 40px;
line-height: 1.15;
margin: 0 0 18px;
color: var(--ink);
letter-spacing: -0.5px;
}
.subtitle {
font-family: 'Manrope', -apple-system, sans-serif;
font-style: italic;
font-weight: 400;
font-size: 20px;
line-height: 1.45;
color: #4a443e;
margin: 0 0 30px;
}
.byline {
display: flex;
align-items: center;
gap: 14px;
padding: 18px 0;
border-top: 2px solid var(--rule);
border-bottom: 1px solid #d8d2c8;
margin-bottom: 40px;
}
.avatar {
width: 44px;
height: 44px;
border-radius: 50%;
background: var(--accent);
color: #fff;
display: flex;
align-items: center;
justify-content: center;
font-weight: 700;
font-size: 14px;
letter-spacing: 0.5px;
}
.author-block { line-height: 1.3; }
.author-name { font-weight: 700; font-size: 14px; }
.author-creds { font-size: 12px; color: var(--muted); }
.pub-meta {
margin-left: auto;
font-size: 11px;
letter-spacing: 1.4px;
text-transform: uppercase;
color: var(--muted);
text-align: right;
}
/* Drop quote opener */
.opening {
font-family: 'Manrope', -apple-system, sans-serif;
font-style: italic;
font-size: 22px;
line-height: 1.5;
color: #3a342e;
border-left: 3px solid var(--accent);
padding: 4px 0 4px 22px;
margin: 0 0 30px;
}
/* Body */
p { margin: 0 0 18px; }
h2 {
font-family: 'Manrope', -apple-system, sans-serif;
font-weight: 700;
font-size: 30px;
line-height: 1.2;
margin: 56px 0 18px;
color: var(--ink);
border-bottom: 2px solid var(--rule);
padding-bottom: 10px;
}
h3 {
font-family: 'Manrope', -apple-system, sans-serif;
font-weight: 700;
font-size: 22px;
margin: 38px 0 12px;
color: var(--ink);
}
h4 {
font-family: 'Manrope', sans-serif;
font-weight: 700;
font-size: 16px;
text-transform: uppercase;
letter-spacing: 1px;
color: var(--accent);
margin: 28px 0 10px;
}
strong { font-weight: 700; color: var(--ink); }
em { color: #2d2926; font-weight: 600; }
/* Inline code chip */
code.chip {
font-family: 'JetBrains Mono', monospace;
font-size: 13.5px;
background: #ede5d6;
color: #5a3225;
padding: 2px 7px;
border-radius: 3px;
border: 1px solid #d4c8b0;
}
/* Code block */
.code-wrap {
background: var(--code-bg);
border-radius: 4px;
margin: 22px 0;
overflow: hidden;
box-shadow: 0 2px 12px rgba(0,0,0,0.18);
}
.code-header {
background: #1f1c19;
color: #b8b0a4;
padding: 8px 16px;
font-family: 'Manrope', sans-serif;
font-size: 10.5px;
letter-spacing: 1.5px;
text-transform: uppercase;
font-weight: 600;
display: flex;
justify-content: space-between;
align-items: center;
}
.code-header .label-right { color: var(--accent); }
pre {
margin: 0;
padding: 18px 18px;
overflow-x: auto;
font-family: 'JetBrains Mono', monospace;
font-size: 12.5px;
line-height: 1.65;
color: var(--code-text);
}
pre code .k { color: var(--code-keyword); font-weight: 600; }
pre code .s { color: var(--code-string); }
pre code .n { color: var(--code-number); }
pre code .c { color: var(--code-comment); font-style: italic; }
pre code .f { color: var(--code-fn); }
pre code .v { color: #e6e1d8; }
pre code .op { color: #abb2bf; }
/* Tags row */
.tag-row {
display: flex;
flex-wrap: wrap;
gap: 6px;
margin: 14px 0 28px;
}
.tag {
display: inline-block;
font-size: 10px;
font-weight: 700;
letter-spacing: 1.3px;
text-transform: uppercase;
background: #1a1a1a;
color: #f0e9dc;
padding: 5px 9px;
border-radius: 0;
}
.tag-accent {
background: var(--accent);
color: #fff;
}
/* Tables */
table {
border-collapse: collapse;
width: 100%;
margin: 22px 0;
font-size: 14.5px;
}
th, td {
text-align: left;
padding: 11px 14px;
border-bottom: 1px solid #d8d2c8;
vertical-align: top;
}
th {
background: #ede5d6;
font-weight: 700;
font-size: 11px;
text-transform: uppercase;
letter-spacing: 1px;
color: #4a443e;
border-bottom: 2px solid var(--rule);
}
td code {
font-family: 'JetBrains Mono', monospace;
font-size: 12.5px;
color: var(--accent);
}
/* Cards */
.rule-grid {
display: grid;
grid-template-columns: repeat(5, 1fr);
gap: 8px;
margin: 26px 0;
}
.rule-card {
border: 1.5px solid var(--rule);
padding: 14px 10px;
text-align: center;
background: #fff;
}
.rule-card .num {
font-size: 9.5px;
letter-spacing: 1.3px;
color: var(--accent);
font-weight: 700;
text-transform: uppercase;
display: block;
margin-bottom: 6px;
}
.rule-card .title-rc {
font-weight: 700;
font-size: 12px;
line-height: 1.25;
color: var(--ink);
text-transform: uppercase;
letter-spacing: 0.4px;
margin-bottom: 4px;
}
.rule-card .desc {
font-size: 11px;
color: var(--muted);
line-height: 1.4;
}
@media (max-width: 720px) {
.rule-grid { grid-template-columns: repeat(2, 1fr); }
h1 { font-size: 30px; }
.container { padding: 12px 20px 60px; }
}
/* Numbered story steps */
.story-list { list-style: none; padding: 0; margin: 24px 0; counter-reset: stepc; }
.story-list li {
position: relative;
padding: 0 0 22px 56px;
counter-increment: stepc;
border-left: 1px solid #d8d2c8;
margin-left: 16px;
}
.story-list li::before {
content: counter(stepc);
position: absolute;
left: -16px;
top: 0;
width: 32px;
height: 32px;
background: var(--accent);
color: #fff;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
font-weight: 700;
font-size: 14px;
}
.story-time {
font-size: 11px;
letter-spacing: 1.2px;
text-transform: uppercase;
font-weight: 700;
color: var(--accent);
margin-bottom: 4px;
}
.story-head {
font-weight: 700;
font-size: 15.5px;
color: var(--ink);
margin-bottom: 4px;
}
.story-body { font-size: 14.5px; color: #3a342e; }
/* Callout / aside */
.aside {
background: var(--accent-soft);
border-left: 4px solid var(--accent);
padding: 18px 22px;
margin: 26px 0;
font-size: 14.5px;
line-height: 1.65;
}
.aside .head {
font-weight: 700;
color: var(--accent);
font-style: italic;
font-family: 'Manrope', -apple-system, sans-serif;
font-size: 17px;
margin-bottom: 6px;
}
/* Figure caption */
.figure {
border: 1px solid #d8d2c8;
background: #fbf8f2;
margin: 30px 0;
padding: 22px;
}
.fig-meta {
font-size: 10px;
letter-spacing: 1.5px;
color: var(--accent);
font-weight: 700;
text-transform: uppercase;
margin-bottom: 8px;
}
.fig-title {
font-family: 'Manrope', -apple-system, sans-serif;
font-size: 22px;
font-weight: 700;
line-height: 1.25;
margin-bottom: 6px;
}
.fig-sub {
font-style: italic;
color: #4a443e;
margin-bottom: 18px;
font-size: 14px;
}
.fig-howto {
background: #fff;
border-left: 3px solid var(--accent);
padding: 14px 18px;
margin-top: 14px;
font-size: 13.5px;
}
.fig-howto .head {
font-size: 10px;
letter-spacing: 1.4px;
color: var(--accent);
font-weight: 700;
text-transform: uppercase;
margin-bottom: 6px;
}
/* Numbered pitfalls */
.pitfall {
display: flex;
gap: 18px;
margin: 26px 0;
padding-bottom: 18px;
border-bottom: 1px dashed #d8d2c8;
}
.pitfall .num-big {
font-family: 'Manrope', -apple-system, sans-serif;
font-size: 44px;
font-weight: 900;
color: var(--accent);
line-height: 1;
flex-shrink: 0;
width: 50px;
}
.pitfall .body { flex: 1; }
.pitfall h4 { margin-top: 0; color: var(--ink); }
/* Wrong / Right code */
.code-wrong .code-header { background: #4a1f1f; }
.code-wrong .code-header .label-right { color: #ff8b78; }
.code-right .code-header { background: #1f3a2a; }
.code-right .code-header .label-right { color: #7fc99a; }
/* Layer cards */
.layer-grid {
display: grid;
grid-template-columns: 1fr 1fr;
gap: 14px;
margin: 26px 0;
}
.layer-card {
border: 1.5px solid var(--rule);
padding: 22px 18px;
text-align: center;
background: #fff;
}
.layer-card.center {
border-color: var(--accent);
background: var(--accent-soft);
grid-column: span 2;
}
.layer-card .layer-num {
font-size: 10px;
letter-spacing: 1.4px;
color: var(--accent);
font-weight: 700;
text-transform: uppercase;
margin-bottom: 8px;
}
.layer-card .layer-title {
font-family: 'Manrope', -apple-system, sans-serif;
font-size: 20px;
font-weight: 700;
margin-bottom: 8px;
letter-spacing: 0.5px;
}
.layer-card .layer-body {
font-size: 13.5px;
color: #4a443e;
line-height: 1.5;
}
/* Footer bio */
.footer-bio {
margin-top: 70px;
padding: 26px 0 0;
border-top: 2px solid var(--rule);
display: flex;
align-items: flex-start;
gap: 18px;
}
.footer-bio .avatar { width: 56px; height: 56px; font-size: 18px; }
.footer-bio .author-name { font-size: 16px; }
.footer-bio .bio-text {
font-size: 13.5px;
color: var(--muted);
line-height: 1.55;
margin-top: 4px;
}
.copy {
margin-top: 30px;
font-size: 11px;
color: var(--muted);
text-align: center;
letter-spacing: 1.2px;
text-transform: uppercase;
}
/* Boolean trace mini */
.bool-row {
display: grid;
grid-template-columns: 1.5fr 1fr 60px;
align-items: center;
padding: 8px 12px;
border-bottom: 1px solid #ebe4d6;
font-size: 13.5px;
}
.bool-row:nth-child(even) { background: #fbf8f2; }
.bool-row .label { font-family: 'JetBrains Mono', monospace; font-size: 12.5px; }
.bool-row .truth { font-weight: 700; }
.truth-T { color: var(--green); }
.truth-F { color: var(--accent); }
.bool-block {
background: #fff;
border: 1px solid #d8d2c8;
margin: 14px 0;
}
.bool-block .case-head {
background: #1a1a1a;
color: #fbf8f2;
padding: 10px 14px;
font-size: 11px;
letter-spacing: 1.5px;
font-weight: 700;
text-transform: uppercase;
}
.bool-result {
padding: 10px 14px;
background: #ede5d6;
font-size: 12.5px;
font-weight: 700;
letter-spacing: 1px;
text-transform: uppercase;
}
.bool-result.fire { color: var(--accent); }
.bool-result.skip { color: var(--green); }
/* Excel-style timecard snippet */
.excel-wrap {
margin: 24px 0;
border: 1px solid #b0b0b0;
background: #fff;
overflow-x: auto;
}
.excel-titlebar {
background: #217346;
color: #fff;
padding: 6px 12px;
font-family: 'Segoe UI', Calibri, Arial, sans-serif;
font-size: 12px;
font-weight: 600;
letter-spacing: 0.5px;
display: flex;
justify-content: space-between;
align-items: center;
}
.excel-titlebar .filename { font-weight: 600; }
.excel-titlebar .app { opacity: 0.85; font-size: 11px; }
.excel-sheet {
font-family: Calibri, 'Segoe UI', Arial, sans-serif;
border-collapse: collapse;
width: 100%;
background: #fff;
font-size: 13.5px;
}
.excel-sheet th, .excel-sheet td {
border: 1px solid #d4d4d4;
padding: 5px 9px;
text-align: left;
vertical-align: middle;
}
.excel-sheet thead th {
background: #4472c4;
color: #fff;
font-weight: 700;
font-size: 13px;
border: 1px solid #2f5597;
}
.excel-sheet td.row-num {
background: #e8e8e8;
color: #555;
text-align: center;
font-size: 11px;
min-width: 36px;
width: auto;
white-space: nowrap;
font-weight: 600;
padding: 5px 6px;
}
.excel-sheet thead th:first-child {
min-width: 36px;
white-space: nowrap;
}
.excel-sheet td.num {
text-align: right;
font-variant-numeric: tabular-nums;
}
.excel-sheet td.time-cell {
font-variant-numeric: tabular-nums;
letter-spacing: 0.3px;
}
.excel-sheet tr.row-clean td.status-cell {
color: #217346;
font-weight: 600;
}
.excel-sheet tr.row-flagged td {
background: #fce8e8;
}
.excel-sheet tr.row-flagged td.status-cell {
color: #c0392b;
font-weight: 600;
}
.excel-sheet tr.row-clean td.row-num { background: #d8e9d4; }
.excel-sheet tr.row-flagged td.row-num { background: #f5cccc; }
.excel-caption {
font-size: 12px;
color: #6a655e;
font-style: italic;
margin: 8px 0 24px;
text-align: center;
}
/* Architecture diagram - flow card */
.arch-flow {
background: #fafaf7;
border: 1px solid #e8e3d8;
border-radius: 6px;
padding: 32px 28px;
margin: 28px 0 36px;
}
.arch-flow .arch-eyebrow {
font-size: 10px;
letter-spacing: 2.5px;
font-weight: 700;
color: var(--accent);
text-transform: uppercase;
margin-bottom: 4px;
}
.arch-flow .arch-title {
font-family: 'Manrope', -apple-system, sans-serif;
font-size: 19px;
color: #2d2926;
margin-bottom: 22px;
letter-spacing: -0.2px;
}
.arch-stages {
display: grid;
grid-template-columns: 1fr;
gap: 0;
}
.arch-stage {
display: grid;
grid-template-columns: 100px 28px 1fr;
gap: 0;
align-items: stretch;
position: relative;
}
.arch-stage .stage-label {
text-align: right;
padding: 16px 14px 16px 0;
}
.arch-stage .stage-num {
font-size: 9px;
letter-spacing: 1.8px;
font-weight: 700;
color: #c8b88a;
text-transform: uppercase;
}
.arch-stage .stage-name {
font-family: 'JetBrains Mono', monospace;
font-size: 11px;
color: #2d2926;
margin-top: 3px;
font-weight: 600;
}
.arch-stage .stage-rail {
position: relative;
background: linear-gradient(to bottom,#e8e3d8 0,#e8e3d8 100%);
background-size: 2px 100%;
background-position: center;
background-repeat: no-repeat;
}
.arch-stage .stage-dot {
position: absolute;
top: 22px;
left: 50%;
transform: translateX(-50%);
width: 11px;
height: 11px;
border-radius: 50%;
background: #fff;
border: 2px solid var(--accent);
z-index: 2;
}
.arch-stage.active .stage-dot { background: var(--accent); }
.arch-stage:first-child .stage-rail { background-image: linear-gradient(to bottom, transparent 0, transparent 22px, #e8e3d8 22px, #e8e3d8 100%); }
.arch-stage:last-child .stage-rail { background-image: linear-gradient(to bottom, #e8e3d8 0, #e8e3d8 22px, transparent 22px, transparent 100%); }
.arch-stage .stage-body {
padding: 14px 0 22px 18px;
}
.arch-stage .stage-headline {
font-size: 14.5px;
color: #2d2926;
font-weight: 600;
line-height: 1.4;
margin-bottom: 4px;
}
.arch-stage .stage-meta {
font-size: 12px;
color: #6a655e;
margin-bottom: 8px;
}
.arch-stage .stage-meta code {
font-size: 11px;
background: #fff;
padding: 1px 6px;
border: 1px solid #e8e3d8;
border-radius: 2px;
color: var(--accent);
}
.arch-stage .stage-pill {
display: inline-block;
font-size: 9px;
letter-spacing: 1.5px;
font-weight: 700;
text-transform: uppercase;
padding: 2px 8px;
border-radius: 2px;
background: #fff;
border: 1px solid #e8e3d8;
color: #6a655e;
margin-right: 6px;
}
.arch-stage .stage-pill.scope-init { color: #4472c4; border-color: #c5d4ed; background: #f6f9fd; }
.arch-stage .stage-pill.scope-loop { color: var(--accent); border-color: #f0c8c0; background: #fdf3ec; }
.arch-stage .stage-pill.scope-exit { color: var(--green); border-color: #c5dfd1; background: #f0f7f3; }
/* Annotated code block */
.annot-wrap {
margin: 24px 0 28px;
border-radius: 4px;
overflow: hidden;
box-shadow: 0 2px 12px rgba(0,0,0,0.18);
}
.annot-head {
background: #1f1c19;
color: #b8b0a4;
padding: 10px 18px;
font-family: 'Manrope', sans-serif;
font-size: 10.5px;
letter-spacing: 1.5px;
text-transform: uppercase;
font-weight: 600;
display: flex;
justify-content: space-between;
}
.annot-head .label-right { color: var(--accent); }
.annot-body {
background: var(--code-bg);
padding: 0;
}
.annot-line {
display: grid;
grid-template-columns: 1fr;
gap: 0;
border-top: 1px solid #2d2926;
}
.annot-line:first-child { border-top: none; }
.annot-line .annot-code {
padding: 12px 16px;
font-family: 'JetBrains Mono', monospace;
font-size: 12px;
line-height: 1.55;
color: var(--code-text);
overflow-x: auto;
}
.annot-line .annot-note {
background: #161310;
border-left: 3px solid var(--accent);
border-top: none;
padding: 14px 18px;
font-size: 13px;
color: #e8e2d6;
line-height: 1.6;
}
.annot-line .annot-note .nt {
display: block;
font-size: 10px;
letter-spacing: 1.6px;
font-weight: 700;
color: var(--accent);
text-transform: uppercase;
margin-bottom: 6px;
}
/* Mini Excel inside annotation note panel */
.annot-note .ann-excel {
margin: 8px 0 10px;
background: #fff;
border: 1px solid #d4d4d4;
overflow: hidden;
border-radius: 2px;
}
.annot-note .ann-excel .ax-bar {
background: #217346;
color: #fff;
font-family: 'Segoe UI', Calibri, Arial, sans-serif;
font-size: 9.5px;
font-weight: 600;
padding: 3px 8px;
letter-spacing: 0.3px;
display: flex;
justify-content: space-between;
align-items: center;
}
.annot-note .ann-excel .ax-bar .app { opacity: 0.85; font-size: 9px; }
.annot-note .ann-excel table {
font-family: Calibri, 'Segoe UI', Arial, sans-serif;
font-size: 11px;
border-collapse: collapse;
width: 100%;
color: #2d2926;
}
.annot-note .ann-excel th, .annot-note .ann-excel td {
border: 1px solid #d4d4d4;
padding: 3px 6px;
text-align: left;
color: #2d2926;
}
.annot-note .ann-excel thead th {
background: #4472c4;
color: #fff;
font-weight: 700;
font-size: 10.5px;
border-color: #2f5597;
}
.annot-note .ann-excel td.idx {
background: #e8e8e8;
color: #555;
text-align: center;
font-size: 10px;
font-weight: 600;
min-width: 32px;
width: auto;
white-space: nowrap;
padding: 3px 4px;
}
.annot-note .ann-excel td.tc { font-variant-numeric: tabular-nums; }
.annot-note .ann-excel td.empty { color: #b0b0b0; font-style: italic; font-size: 10.5px; }
.annot-note .ann-excel tr.row-pass { background: #e8f4ea; }
.annot-note .ann-excel tr.row-pass td.tag { color: #1d5e34; font-weight: 700; }
.annot-note .ann-excel tr.row-fail { background: #fce8e8; }
.annot-note .ann-excel tr.row-fail td.tag { color: #c0392b; font-weight: 700; }
.annot-note .ann-excel tr.row-warn { background: #fff7e0; }
.annot-note .ann-excel tr.row-warn td.tag { color: #b97417; font-weight: 700; }
.annot-note .ann-excel-cap {
font-size: 10px;
color: #c8b88a;
font-style: italic;
margin: -4px 0 8px;
}
.annot-note .ann-text {
color: #d8d2c8;
line-height: 1.55;
}
.annot-note .ann-text strong { color: #f5e8c8; }
.annot-note .ann-text code {
background: #2d2926;
color: #e6e1d8;
padding: 1px 5px;
border-radius: 2px;
font-size: 10.5px;
}
/* Structured annotation parts — replaces wall-of-prose */
.annot-note .ann-parts { margin-top: 8px; }
.annot-note .ann-part {
margin: 0 0 14px;
padding-bottom: 12px;
border-bottom: 1px dashed #3a342e;
}
.annot-note .ann-part:last-child {
border-bottom: none;
padding-bottom: 0;
margin-bottom: 0;
}
.annot-note .ann-part-head {
font-size: 10px;
letter-spacing: 1.5px;
font-weight: 700;
color: var(--accent);
text-transform: uppercase;
margin-bottom: 8px;
}
.annot-note .ann-part-head .num {
display: inline-block;
background: var(--accent);
color: #fff;
width: 18px;
height: 18px;
border-radius: 50%;
text-align: center;
line-height: 18px;
font-size: 10px;
margin-right: 6px;
vertical-align: 1px;
}
.annot-note ul.ann-bullets {
list-style: none;
padding: 0;
margin: 0;
}
.annot-note ul.ann-bullets li {
position: relative;
padding: 0 0 6px 16px;
color: #d8d2c8;
font-size: 12px;
line-height: 1.55;
}
.annot-note ul.ann-bullets li:last-child { padding-bottom: 0; }
.annot-note ul.ann-bullets li::before {
content: '';
position: absolute;
left: 0;
top: 8px;
width: 5px;
height: 5px;
background: var(--accent);
border-radius: 50%;
}
.annot-note ul.ann-bullets li strong { color: #f5e8c8; }
.annot-note ul.ann-bullets li code {
background: #2d2926;
color: #e6e1d8;
padding: 1px 5px;
border-radius: 2px;
font-size: 10.5px;
}
/* Mini snippet inside annotation note (dark theme) */
.annot-note .ann-snippet {
background: #0d0c0a;
border-left: 2px solid var(--accent);
padding: 8px 10px;
margin: 8px 0;
font-family: 'JetBrains Mono', monospace;
font-size: 10.5px;
line-height: 1.5;
color: var(--code-text);
overflow-x: auto;
border-radius: 2px;
}
.annot-note .ann-snippet .lbl {
display: block;
font-family: 'Manrope', sans-serif;
font-size: 9px;
letter-spacing: 1.4px;
color: #c8b88a;
text-transform: uppercase;
font-weight: 700;
margin-bottom: 4px;
}
.annot-note .ann-takeaway {
margin-top: 10px;
background: #2a1a16;
border-left: 3px solid var(--accent);
padding: 8px 12px;
font-size: 11.5px;
color: #f5e8c8;
line-height: 1.5;
}
.annot-note .ann-takeaway::before {
content: 'Takeaway';
display: block;
font-size: 8.5px;
letter-spacing: 1.5px;
color: var(--accent);
text-transform: uppercase;
font-weight: 700;
margin-bottom: 3px;
}
/* Mobile: stack code over note instead of side-by-side */
@media (max-width: 720px) {
.annot-line {
grid-template-columns: 1fr;
}
.annot-line .annot-note {
border-left: none;
border-top: 2px solid var(--accent);
}
.annot-line .annot-code {
font-size: 11.5px;
}
}
/* Section opener / lead */
.section-lead {
font-size: 16px;
line-height: 1.6;
color: #4a443e;
margin: 14px 0 26px;
border-left: 3px solid var(--accent);
padding: 4px 0 4px 16px;
}
/* Input card — mobile-friendly stacked layout */
.input-card {
border: 1px solid #e8e3d8;
border-radius: 4px;
margin: 14px 0;
background: #fff;
overflow: hidden;
}
.input-card .ic-head {
background: #f6f9fd;
border-left: 3px solid #4472c4;
padding: 12px 16px;
}
.input-card .ic-eyebrow {
font-size: 9.5px;
letter-spacing: 1.8px;
font-weight: 700;
color: #4472c4;
text-transform: uppercase;
margin-bottom: 4px;
}
.input-card .ic-name {
font-family: 'JetBrains Mono', monospace;
font-size: 13.5px;
font-weight: 700;
color: #2d2926;
word-break: break-all;
}
.input-card .ic-question {
padding: 14px 16px 8px;
font-size: 14.5px;
color: #2d2926;
font-weight: 600;
line-height: 1.4;
}
.input-card .ic-value-row {
display: flex;
gap: 10px;
align-items: center;
padding: 0 16px 12px;
flex-wrap: wrap;
}
.input-card .ic-value-row .vlabel {
font-size: 10px;
letter-spacing: 1.3px;
font-weight: 700;
color: #7a7570;
text-transform: uppercase;
}
.input-card .ic-value-row .vbox {
font-family: 'JetBrains Mono', monospace;
font-size: 12.5px;
font-weight: 700;
color: #2d2926;
background: #f5f1e8;
border: 1px solid #d8d2c8;
padding: 4px 10px;
border-radius: 3px;
}
.input-card .ic-value-row .vbox.empty {
color: #999;
font-style: italic;
font-weight: 400;
}
.input-card .ic-snippet {
background: var(--code-bg);
color: var(--code-text);
font-family: 'JetBrains Mono', monospace;
font-size: 11.5px;
line-height: 1.55;
padding: 12px 16px;
overflow-x: auto;
border-top: 1px solid #2d2926;
}
.input-card .ic-snippet .lbl {
display: block;
font-family: 'Manrope', sans-serif;
font-size: 9px;
letter-spacing: 1.5px;
font-weight: 700;
color: var(--accent);
text-transform: uppercase;
margin-bottom: 6px;
}
.input-card .ic-explain {
padding: 12px 16px;
font-size: 13px;
color: #4a443e;
line-height: 1.55;
border-top: 1px solid #e8e3d8;
background: #fafaf7;
}
.input-card.reserved .ic-head {
background: #f5f5f5;
border-left-color: #b0b0b0;
}
.input-card.reserved .ic-eyebrow { color: #7a7570; }
.input-card.reserved { opacity: 0.75; }
.input-card.output .ic-head {
background: #fce8e8;
border-left-color: var(--accent);
}
.input-card.output .ic-eyebrow { color: var(--accent); }
.input-card.output .ic-question { color: var(--accent); }
/* Mini Excel snippet inside input cards */
.ic-mini-excel {
margin: 0 16px 8px;
border: 1px solid #d4d4d4;
background: #fff;
overflow: hidden;
}
.ic-mini-excel .me-bar {
background: #217346;
color: #fff;
font-family: 'Segoe UI', Calibri, Arial, sans-serif;
font-size: 10.5px;
font-weight: 600;
padding: 4px 10px;
display: flex;
justify-content: space-between;
align-items: center;
letter-spacing: 0.3px;
}
.ic-mini-excel .me-bar .app { opacity: 0.85; font-size: 10px; }
.ic-mini-excel table {
font-family: Calibri, 'Segoe UI', Arial, sans-serif;
font-size: 12.5px;
border-collapse: collapse;
width: 100%;
}
.ic-mini-excel th, .ic-mini-excel td {
border: 1px solid #d4d4d4;
padding: 4px 8px;
text-align: left;
}
.ic-mini-excel thead th {
background: #4472c4;
color: #fff;
font-weight: 700;
font-size: 11.5px;
border-color: #2f5597;
}
.ic-mini-excel td.idx {
background: #e8e8e8;
color: #555;
text-align: center;
font-size: 10.5px;
font-weight: 600;
width: 32px;
}
.ic-mini-excel td.tc { font-variant-numeric: tabular-nums; }
.ic-mini-excel td.empty { color: #b0b0b0; font-style: italic; font-size: 11.5px; }
.ic-mini-excel tr.marker td.idx { background: #fff3e0; }
.ic-mini-excel tr.boundary td.idx { background: #fce8e8; }
.ic-mini-excel tr.flagged-row { background: #fce8e8; }
.ic-mini-excel tr.flagged-row td.msg { color: #c0392b; font-weight: 600; }
.ic-mini-excel tr.clean-row td.tag { color: #27704a; font-weight: 600; }
.ic-mini-excel-cap {
margin: -2px 16px 12px;
font-size: 11px;
color: #6a655e;
font-style: italic;
}
/* Phase divider */
.phase-divider {
text-align: center;
color: var(--accent);
font-size: 13px;
font-weight: 700;
letter-spacing: 2px;
margin: 18px 0;
}
/* Anchor banner above the cards */
.anchor-banner {
background: #fff;
border: 2px solid var(--accent);
border-radius: 6px;
padding: 18px 20px;
margin: 24px 0 18px;
text-align: center;
}
.anchor-banner .ab-eyebrow {
font-size: 10px;
letter-spacing: 2.5px;
font-weight: 700;
color: var(--accent);
text-transform: uppercase;
margin-bottom: 6px;
}
.anchor-banner .ab-line {
font-size: 14.5px;
font-weight: 600;
color: #2d2926;
line-height: 1.5;
}
.anchor-banner .ab-sub {
font-size: 11.5px;
color: #7a7570;
font-style: italic;
margin-top: 4px;
}

/* ============================================================
* Blogger / mobile SVG sizing safeguards
* Make every inline SVG scale to its container width without
* horizontal overflow. Works around Blogger themes that
* impose narrow post columns.
* ============================================================ */
svg {
max-width: 100% !important;
height: auto !important;
display: block;
}
/* SVG-containing wrappers: enable horizontal scroll as a last resort */
div[style*="overflow-x:auto"],
div[style*="overflow-x: auto"] {
-webkit-overflow-scrolling: touch;
position: relative;
}
/* Mobile-specific: shrink padding on SVG wrappers so they get more breathing room */
@media (max-width: 600px) {
div[style*="background:#fafaf7"][style*="border:1px solid #e8e3d8"] {
padding: 12px !important;
}
/* Reduce default body font-size lever for diagram captions on small screens */
svg text {
font-size: inherit;
}
}
/* Print / Blogger AMP fallback — ensure SVGs respect container even when CSS doesn't fully load */
img, svg, table { max-width: 100%; }

/* ============================================================
* Protect SVG text from inheriting italic/color from parent
* annotation containers. Without this, when SVG layout breaks
* on mobile the text content falls back to inheriting the
* .ann-text italic-cream styling — which looks like a wall
* of unreadable italic prose.
* ============================================================ */
svg text, svg tspan {
font-family: 'Manrope', -apple-system, sans-serif !important;
font-style: normal !important;
text-rendering: geometricPrecision !important;
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
}
/* Crisp shape rendering for all SVG vector elements */
svg {
shape-rendering: geometricPrecision;
text-rendering: geometricPrecision;
image-rendering: -webkit-optimize-contrast;
image-rendering: crisp-edges;
}
/* Ensure SVGs inside annotation blocks keep their own bg/colors */
.annot-note svg {
background: #ffffff;
display: block;
border-radius: 4px;
}
/* ============================================================
* <em> color override for dark backgrounds.
* The global rule `em { color: #3a342e }` is correct on the
* light cream body background but invisible inside dark
* annotation blocks. Force readable warm cream wherever em
* appears on a dark surface.
* ============================================================ */
.annot-note em,
.annot-note .ann-text em,
.annot-note .ann-bullets li em,
.annot-note .ann-bullets em,
.annot-note .ann-snippet em,
.annot-note .ann-takeaway em,
.annot-code em,
.annot-line em,
pre em,
pre code em {
color: #f0d68a !important;
font-style: italic;
}
</style>
</head><body>
<div class="container">

<!-- HEADER (Philippine-leave-post style) -->
<div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Fast Formula</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Time Entry Rule</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">OTL</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Hands-On</span>
</div>

<div style="font-size:13px; color:#7a7570; margin-bottom:18px;">May 21, 2026 • 15 min read • Oracle HCM Cloud</div>

<!-- SERIES BREADCRUMB -->
<div style="background:#f5f1e8; border-left:3px solid #b97417; padding:10px 14px; margin-bottom:24px; border-radius:0 3px 3px 0; font-size:12px;">
<span style="font-weight:700; color:#b97417; letter-spacing:0.5px; text-transform:uppercase; font-size:10px;">The TER Series</span>
<span style="color:#5a544e; margin-left:8px;">Part 4 of 4</span>
<div style="margin-top:6px; color:#7a7570; font-size:11.5px; line-height:1.5;">
1. OTL Foundations ·
2. The Input Contract ·
3. Algorithm: Routing & Overlap ·
4. The State Machine
</div>
</div>

<h1>The State Machine: Continuous-Hours Tracking, End to End<br><span style="color:#7a7570; font-size:0.7em; font-weight:400; font-style:italic;">Part 4 of 4 — The TER Series</span></h1>

<div class="byline">
<div class="avatar">AM</div>
<div class="author-block">
<div class="author-name">Abhishek Mohanty</div>
<div class="author-creds">Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead</div>
</div>
</div>

<div class="opening">The first three posts covered what TER does, the input contract, and the first half of the algorithm. Now the final piece: the continuous-hours state machine that makes the whole formula stateful, plus the OTL configuration that has to exist for any of this to fire, plus a full end-to-end trace of Sarah's broken Tuesday timecard.</div>

<h3>Continuous-Hours State Machine</h3>

<p>This is the heart of the formula. The rule says <em>"no worker shall log more than 6 hours of continuous Regular Hours without a meal break."</em> Simple to state, easy to get wrong. You can't write it as a stateless <code>IF</code> inside the loop — the formula has to <em>remember</em> what came before.</p>

<h4>The state diagram</h4>

<p>Two states. Four transitions. Every line of Block 8's code maps to one of them.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-4/diagram-1.png" alt="Diagram 1: Oracle Fast Formula: Time Entry Rule (Part 4)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p><strong>Idle</strong> is the starting state. <strong>Active</strong> is where the formula spends most of its time when work is happening. The four transitions cover every case: a stretch begins, continues without a break, resumes after a gap, or ends because the worker took a meal break.</p>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Why this is the formula's hardest concept</div>
Most production bugs in continuous-hours validation come down to one of two mistakes. First: writing EXTEND as <em>"start > prev stop"</em> instead of <em>"start = prev stop"</em>, which makes any tiny gap incorrectly extend the stretch. Second: forgetting that meal breaks force a RESET, which makes the formula keep counting after the worker has already eaten. Both pass UAT and fail audits months later. <strong>Remember the four transitions and you remember the rule.</strong>
</div>

<h4>The annotated code</h4>

<p>With the state model in mind, the code reads like a direct translation of the diagram. Block 8a is the gate (which entries qualify). Block 8b is the EXTEND/RESTART decision. Block 8c computes hours. Block 8d compares against thresholds.</p>

<div class="annot-wrap">
<div class="annot-head">
<span>Block 8 · Continuous-hours tracker</span>
<span class="label-right">Annotated</span>
</div>
<div class="annot-body">

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="c">/* gate — only count Reg Hours, real punches, no meal yet */</span>
<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span>
    <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span>
    <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>
    <span class="k">AND</span> <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'N'</span>
    <span class="k">AND</span> <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>) <span class="k">THEN</span>
(</code></pre></div>
<div class="annot-note">
<span class="nt">Block 8a · Five-condition gate</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The legal rule — cap measures continuous work, not total daily hours</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">12 HOURS · WITH MEAL — OK</div>
<div style="padding:10px 12px;">
<div style="display:flex; gap:0; height:18px; margin-bottom:8px;">
<div style="flex:3; background:#3d7a52; opacity:0.85; color:#fff; font-size:9px; font-weight:700; display:flex; align-items:center; justify-content:center;">3h work</div>
<div style="flex:1; background:#b97417; opacity:0.85; color:#fff; font-size:8px; font-weight:700; display:flex; align-items:center; justify-content:center;">meal</div>
<div style="flex:9; background:#3d7a52; opacity:0.85; color:#fff; font-size:9px; font-weight:700; display:flex; align-items:center; justify-content:center;">9h work (post-meal)</div>
</div>
<div style="font-size:10px; color:#3d7a52;">Total: 12h. <strong>Continuous: 3h pre-meal.</strong></div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">Meal interrupted the count → legal cap not breached.</div>
</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">7 HOURS · NO MEAL — VIOLATION</div>
<div style="padding:10px 12px;">
<div style="display:flex; height:18px; margin-bottom:8px;">
<div style="flex:1; background:#c0392b; opacity:0.85; color:#fff; font-size:9px; font-weight:700; display:flex; align-items:center; justify-content:center;">7h continuous, no break</div>
</div>
<div style="font-size:10px; color:#c0392b;">Total: 7h. <strong>Continuous: 7h.</strong></div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">Cap is 6h. Worker should have taken meal at 5h.</div>
</div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:10px;"><strong style="color:#2d2926;">The cap measures uninterrupted work.</strong> A meal break is the legal reset trigger. Block 8a is where this rule meets the data.</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · The gate — five conditions, all must hold</div>

<div style="font-size:10.5px; color:#5a544e; margin-bottom:8px;">Each condition rules out one specific case that shouldn't count:</div>

<div style="display:flex; align-items:stretch; margin-bottom:6px;">
<div style="flex:0 0 40px; background:#dbe5f4; border:1px solid #1f5fa8; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:#1f5fa8;">1</div>
<div style="flex:1; background:#fff; border:1px solid #1f5fa8; padding:8px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#2d2926;">aiTimeType = p_reg_type</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">filter to Reg Hours only — leave/holiday don't count toward the cap</div>
</div>
</div>
<div style="display:flex; align-items:stretch; margin-bottom:6px;">
<div style="flex:0 0 40px; background:#dbe5f4; border:1px solid #1f5fa8; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:#1f5fa8;">2</div>
<div style="flex:1; background:#fff; border:1px solid #1f5fa8; padding:8px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#2d2926;">aiStartTime <> NullDate</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">need a real start — can't measure stretch from a missing punch</div>
</div>
</div>
<div style="display:flex; align-items:stretch; margin-bottom:6px;">
<div style="flex:0 0 40px; background:#dbe5f4; border:1px solid #1f5fa8; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:#1f5fa8;">3</div>
<div style="flex:1; background:#fff; border:1px solid #1f5fa8; padding:8px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#2d2926;">aiStopTime <> NullDate</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">need a real stop — same reason</div>
</div>
</div>
<div style="display:flex; align-items:stretch; margin-bottom:6px;">
<div style="flex:0 0 40px; background:#dbe5f4; border:1px solid #1f5fa8; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:#1f5fa8;">4</div>
<div style="flex:1; background:#fff; border:1px solid #1f5fa8; padding:8px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#2d2926;">l_qty_only = 'N'</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">qty-only placeholders fail even though they have fake punches (00:00, 23:59)</div>
</div>
</div>
<div style="display:flex; align-items:stretch; margin-bottom:10px;">
<div style="flex:0 0 40px; background:#fff5f0; border:1.5px solid #c0392b; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:#c0392b;">5</div>
<div style="flex:1; background:#fff5f0; border:1.5px solid #c0392b; padding:8px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#c0392b; font-weight:700;">l_meal_taken = 'N'</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">most consequential: meal already taken → gate locks for rest of day</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; font-style:italic;">If any one of the five fails → entry is silently skipped — no error, no warning, just continues to next iteration.</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · Why condition 5 locks the gate for the rest of the day</div>

<div style="font-size:10.5px; color:#5a544e; margin-bottom:8px;"><strong style="color:#2d2926;">Gate state through Sarah's day:</strong></div>
<div style="overflow-x:auto;">
<div style="display:flex; min-width:480px;">
<div style="flex:1; background:#e8f4ea; border:1px solid #3d7a52; padding:8px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#3d7a52;">Reg 09—12</div>
<div style="font-size:9px; color:#3d7a52; margin-top:2px;">GATE OPEN</div>
</div>
<div style="flex:1; background:#fff3e0; border:1px solid #b97417; padding:8px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#b97417;">Meal 12—13</div>
<div style="font-size:9px; color:#b97417; margin-top:2px;">flag flips 'Y'</div>
</div>
<div style="flex:1; background:#fff5f0; border:1.5px solid #c0392b; padding:8px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#c0392b;">Reg 13—15</div>
<div style="font-size:9px; color:#c0392b; margin-top:2px;">GATE CLOSED</div>
</div>
<div style="flex:1; background:#fff5f0; border:1.5px solid #c0392b; padding:8px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#c0392b;">Reg 15—18</div>
<div style="font-size:9px; color:#c0392b; margin-top:2px;">GATE CLOSED</div>
</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; line-height:1.6; margin-top:10px;">
Once <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_meal_taken</code> flips to 'Y' (when the meal entry is processed in Block 6e), every subsequent Reg Hours entry on the same day fails condition 5. The stretch tracker stops accumulating. New work after the meal is treated as a fresh shift — which it legally is.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The legal rule this block enforces</div>
<ul class="ann-bullets">
<li>Across most labour jurisdictions, regulations cap <strong>uninterrupted work at 5 or 6 hours</strong>. After that point, a meal break is legally required — the worker must stop, eat, and rest before continuing.</li>
<li>The cap measures <em>continuous</em> work, not total daily hours. A worker can log 12 hours total in a day without violating the cap, as long as those hours are split by an actual meal break in the middle. The break is what resets the count.</li>
<li>This block is the formula's enforcement of that rule. Its job is to track the running length of the current uninterrupted stretch and fire warnings or errors when that stretch crosses the threshold.</li>
<li>The challenge is figuring out which timecard entries actually count toward "continuous work" and which don't. Marker rows clearly don't. Meal breaks clearly don't. But what about qty-only placeholders? What about Reg Hours entries with missing punches? What about Reg Hours entries that come <em>after</em> the worker already took their meal?</li>
<li>The five-condition gate is the formula's answer to all those questions. Each condition rules out one specific case that shouldn't count, and the AND combines them all into a single <em>"this entry qualifies"</em> check.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>The five conditions, each one earning its place</div>
<div class="ann-snippet">IF (aiTimeType  = p_reg_type
AND aiStartTime <> NullDate
AND aiStopTime  <> NullDate
AND l_qty_only  = 'N'
AND l_meal_taken = 'N') THEN ...</div>
<ul class="ann-bullets">
<li><strong>Condition 1:</strong> <code>aiTimeType = p_reg_type</code>. Only Regular Hours counts toward the cap. Annual Leave, Sick Leave, Public Holiday entries don't represent active work, so they shouldn't extend the stretch. This first check filters them out.</li>
<li><strong>Condition 2 & 3:</strong> Real start and stop times must be present. Without both endpoints, the formula can't measure duration — you can't compute a stretch from missing punches. These checks would normally be redundant after Block 6c (which flags missing punches as errors), but the defensive check here ensures Block 8 doesn't crash on data that Block 6c already flagged.</li>
<li><strong>Condition 4:</strong> <code>l_qty_only = 'N'</code>. Qty-only placeholders fail the gate even though they technically have punch times (00:00 and 23:59). They're not real work intervals, so they shouldn't accumulate against the legal cap. Block 6b detected the placeholder pattern and set this flag earlier in the same iteration.</li>
<li><strong>Condition 5:</strong> <code>l_meal_taken = 'N'</code>. Once a meal break has been logged anywhere on this day, the gate stays closed for every subsequent Reg Hours entry. This is the most consequential of the five conditions and deserves its own discussion below.</li>
<li>All five conditions must be TRUE simultaneously for the entry to enter the stretch tracker. If any one fails, the entry is silently skipped — no error, no warning, just continues to the next iteration.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>Why l_meal_taken locks the gate for the rest of the day</div>
<ul class="ann-bullets">
<li>The reasoning is rooted in the legal definition. The continuous-work cap measures <em>uninterrupted work before a meal break</em>. Once the worker eats, they've satisfied the meal-break requirement — the legal counter resets in their favour. The pre-meal stretch is the only one that needed validating.</li>
<li>What about the post-meal stretch? Could it also exceed 6 hours and need flagging? In theory yes, but in practice it doesn't happen in office environments — workers stop work at the end of the schedule, not 6+ hours after lunch. Manufacturing with double-shifts is different, but those LEs would configure their rules differently or implement custom logic.</li>
<li>By locking the gate at <code>l_meal_taken = 'Y'</code>, the formula trusts that the meal break did its legal job. Subsequent Reg Hours entries are tracked elsewhere (they still go into the day buffer for overlap testing in Block 7) but they're excluded from continuous-hours validation.</li>
<li>The flag was set by Block 6e when the loop encountered a meal-break entry. It stays <code>'Y'</code> through every subsequent iteration of the same day. Block 7c resets it to <code>'N'</code> at the day boundary, giving tomorrow a clean slate.</li>
<li>If your business case really does need post-meal stretches tracked separately (24-hour manufacturing with rotating breaks, perhaps), removing condition 5 from the gate is the architectural change. Don't carve out a special case in the middle of the algorithm; rethink the gate.</li>
</ul>
</div>
<div class="ann-takeaway">The gate is a bouncer at the door of the stretch tracker. Five conditions, all must hold, every one earning its place. Block 6's earlier work (qty-only detection, meal-break recognition) flows into this gate through shared flags — the formula coordinates across blocks through these shared signals, keeping each block's own logic focused.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code>  <span class="c">/* state transition: idle -> active, or continue */</span>
  <span class="k">IF</span> (<span class="v">inStretch</span> <span class="op">=</span> <span class="s">'N'</span>) <span class="k">THEN</span>
  ( <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">aiStartTime</span>
    <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">aiStopTime</span>
    <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'Y'</span>
  )
  <span class="k">ELSE</span>
  ( <span class="k">IF</span> (<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">stretchEnd</span>) <span class="k">THEN</span>
    ( <span class="v">stretchEnd</span> <span class="op">=</span> <span class="v">aiStopTime</span>           <span class="c">// EXTEND</span>
    )
    <span class="k">ELSE</span>
    ( <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">aiStartTime</span>         <span class="c">// RESTART</span>
      <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">aiStopTime</span>
    )
  )</code></pre></div>
<div class="annot-note">
<span class="nt">Block 8b · State transitions</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Four concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The state machine — idle vs active, and when each path fires</div>

<div style="background:#1f1c19; color:#fff; padding:8px 14px; border-radius:4px; text-align:center; margin-bottom:10px; font-size:10.5px; font-weight:700;">Entry passes gate (Block 8a OK)</div>
<div style="text-align:center; color:#7a7570; font-size:14px;">↓</div>

<div style="background:#fff; border:1.5px solid #7a7570; border-radius:4px; padding:10px 14px; text-align:center; margin-bottom:10px;">
<div style="font-size:11px; font-weight:700; color:#2d2926;">inStretch = 'N' ?</div>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; padding:10px 12px;">
<div style="font-size:10px; color:#3d7a52; font-style:italic; margin-bottom:4px;">YES (idle) →</div>
<div style="font-size:11px; font-weight:700; color:#3d7a52;">START</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">stretchStart = ai · flag='Y'</div>
</div>
<div style="background:#fff; border:1.5px solid #7a7570; border-radius:4px; padding:10px 12px; text-align:center;">
<div style="font-size:10px; color:#7a7570; font-style:italic; margin-bottom:4px;">NO (active) →</div>
<div style="font-size:11px; font-weight:700; color:#2d2926;">aiStartTime = stretchEnd ?</div>
</div>
</div>

<div style="text-align:center; color:#7a7570; font-size:14px; padding:6px 0;">(when 'no')</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#f0f4fa; border:1.5px solid #1f5fa8; border-radius:4px; padding:10px 12px;">
<div style="font-size:10px; color:#1f5fa8; font-style:italic; margin-bottom:4px;">YES (touches) →</div>
<div style="font-size:11px; font-weight:700; color:#1f5fa8;">EXTEND</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">stretchEnd = ai (start unchanged)</div>
</div>
<div style="background:#fff3e0; border:1.5px solid #b97417; border-radius:4px; padding:10px 12px;">
<div style="font-size:10px; color:#b97417; font-style:italic; margin-bottom:4px;">NO (gap) →</div>
<div style="font-size:11px; font-weight:700; color:#b97417;">RESTART</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:2px;">stretchStart = ai · stretchEnd = ai</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:10px;">Two states (idle/active), three transitions inside Block 8b. Resets back to idle happen in Block 6e (meal) or Block 7c (END_DAY).</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · EXTEND — when the worker's punches touch (no gap)</div>

<div style="background:#f0f4fa; border:1.5px solid #1f5fa8; border-radius:4px; overflow:hidden;">
<div style="background:#1f5fa8; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">EXAMPLE · EXTEND</div>
<div style="padding:12px;">
<div style="display:flex; gap:0; height:18px; margin-bottom:6px;">
<div style="flex:1; background:#3d7a52; opacity:0.85; color:#fff; font-size:9px; font-weight:700; display:flex; align-items:center; justify-content:center;">Entry 1: 09—11</div>
<div style="flex:1; background:#1f5fa8; opacity:0.85; color:#fff; font-size:9px; font-weight:700; display:flex; align-items:center; justify-content:center;">Entry 2: 11—13 (touches!)</div>
</div>
<div style="display:flex; justify-content:space-between; font-size:9px; color:#5a544e;">
<span>09</span><span>10</span><span>11</span><span>12</span><span>13</span>
</div>
<div style="font-size:10.5px; color:#1f5fa8; font-weight:700; margin-top:10px;">EXTEND fires</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; color:#2d2926; margin-top:2px;">stretch: 09→13 (4h)</div>
</div>
</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · RESTART — when a gap appears (any size)</div>

<div style="background:#fff3e0; border:1.5px solid #b97417; border-radius:4px; overflow:hidden;">
<div style="background:#b97417; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">EXAMPLE · RESTART</div>
<div style="padding:12px;">
<div style="display:flex; gap:0; height:18px; margin-bottom:6px;">
<div style="flex:2; background:#3d7a52; opacity:0.85; color:#fff; font-size:9px; font-weight:700; display:flex; align-items:center; justify-content:center;">Entry 1: 09—11</div>
<div style="flex:0.5; border:1px dashed #c0392b; color:#c0392b; font-size:8px; font-weight:700; display:flex; align-items:center; justify-content:center;">gap</div>
<div style="flex:2.5; background:#b97417; opacity:0.85; color:#fff; font-size:9px; font-weight:700; display:flex; align-items:center; justify-content:center;">Entry 2: 11:30—14</div>
</div>
<div style="display:flex; justify-content:space-between; font-size:9px; color:#5a544e;">
<span>09</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span>
</div>
<div style="font-size:10.5px; color:#b97417; font-weight:700; margin-top:10px;">RESTART fires</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; color:#2d2926; margin-top:2px;">stretch: 11:30→14 (2.5h)</div>
</div>
</div>

<!-- PART 4 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 4 · Why even a tiny gap forces restart — not a bug, a feature</div>

<div style="background:#fff8e8; border-left:3px solid #b97417; padding:10px 14px; border-radius:0 3px 3px 0; font-size:10.5px; color:#2d2926; line-height:1.6;">
The condition <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">aiStartTime = stretchEnd</code> is <em>strict equality</em>. A 1-minute gap (11:00 stop, 11:01 start) fails the equality check — treated as RESTART, not EXTEND. That's intentional: any deliberate gap signals the worker stopped working, even briefly. The state machine doesn't try to be lenient about "almost touching" because tolerance would let cumulative drift build up across many entries.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The state machine, simplified</div>
<ul class="ann-bullets">
<li>The continuous-hours tracker is a small state machine with two states: <strong>idle</strong> (<code>inStretch = 'N'</code>, no active stretch being measured) and <strong>active</strong> (<code>inStretch = 'Y'</code>, currently tracking a stretch with known start and end).</li>
<li>Once an entry passes the gate from Block 8a, the formula must decide what to do with it. The decision depends entirely on which state the tracker is currently in.</li>
<li>From idle: any qualifying entry transitions to active. The new stretch begins at this entry's start time and currently ends at this entry's stop time. The flag flips to <code>'Y'</code>.</li>
<li>From active: there are two sub-decisions. If this entry continues the stretch seamlessly (its start matches the previous stop), extend. If there's a gap, restart from this new entry. Either way the tracker stays active.</li>
<li>A meal break in Block 6e or an END_DAY in Block 7c forces the tracker back to idle by clearing the state variables. From there the cycle begins again.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>The EXTEND path: when work continues seamlessly</div>
<div class="ann-snippet">IF (aiStartTime = stretchEnd) THEN
stretchEnd = aiStopTime    <span style="color:#d4c896;">// extend</span></div>
<ul class="ann-bullets">
<li>The EXTEND path fires when the new entry's start time exactly matches the previous stretch's end time. The worker stopped one Reg Hours entry and immediately started another, with no gap in between.</li>
<li>The action is minimal: just move <code>stretchEnd</code> forward to this entry's stop time. The start stays where it was; the stretch grows by the duration of the new entry.</li>
<li>Example: a worker logged Reg Hours 09:00–11:00, then logged 11:00–13:00 (perhaps they switched task codes at 11:00 but kept working). The stretch was 09:00–11:00 (2 hours). After EXTEND, it becomes 09:00–13:00 (4 hours). One unbroken run of 4 hours of work.</li>
<li>This is the case where the formula correctly recognises that splitting a continuous work session into multiple Reg Hours rows (for cost-centre tracking, say) doesn't break continuity. The worker hasn't actually stopped working; they've just paused to change which project they're billing.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The RESTART path: when there's a gap</div>
<div class="ann-snippet">ELSE
stretchStart = aiStartTime  <span style="color:#d4c896;">// restart from here</span>
stretchEnd   = aiStopTime</div>
<ul class="ann-bullets">
<li>The RESTART path fires when the new entry's start doesn't match the previous stop — there's a gap in time between them. The worker did something between the two entries that wasn't logged as Reg Hours.</li>
<li>The action: discard the previous stretch entirely and begin a fresh one from this entry. Both <code>stretchStart</code> and <code>stretchEnd</code> get rewritten.</li>
<li>Example: a worker logged Reg Hours 09:00–11:00, then logged 11:30–14:00. The 30-minute gap from 11:00 to 11:30 isn't accounted for — maybe a coffee break, maybe a chat with a colleague, maybe a personal phone call. The formula doesn't know and doesn't need to. The gap itself is enough proof that continuous work was interrupted.</li>
<li>After RESTART, the stretch is 11:30–14:00 (2.5 hours), not 09:00–14:00 (5 hours). The earlier work isn't lost — it might have already triggered a warning when it completed at 11:00 — but it no longer accumulates against the new stretch.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">4</span>Why even a tiny gap forces a restart</div>
<ul class="ann-bullets">
<li>The legal cap measures <strong>continuous work</strong>, not total daily hours. The two are different. A worker can legitimately log 12 hours of total work in a day without violating any cap, as long as that work isn't continuous.</li>
<li>What does "continuous" mean? The formula's interpretation: <em>punches that don't touch each other are not part of the same stretch</em>. If there's any visible gap between the previous stop and the next start, continuity is considered broken.</li>
<li>This is a deliberately strict interpretation. A worker who logged 09:00–11:00, then 11:01–14:00 has only a 1-minute gap, but the formula still treats them as separate stretches. If you wanted to allow such tiny gaps to be ignored, you'd need to add a tolerance test (e.g. <code>(aiStartTime - stretchEnd) < (5/1440)</code> still extends, allowing 5-minute gaps to count as continuous).</li>
<li>For most office work, the strict interpretation is correct — even small gaps imply some kind of break, and breaks are exactly what the legal cap is designed to encourage. If your business has different requirements (pure manufacturing, perhaps), the tolerance can be added with one additional check.</li>
<li>Adding the two stretches together as if they were one would misrepresent reality. A worker who took a 30-minute break in the middle of their morning isn't doing the same thing as a worker who powered through 5 straight hours. The formula needs to distinguish those cases, and the strict gap-based reset is how it does.</li>
</ul>
</div>
<div class="ann-takeaway">Adjacent entries extend the stretch; gaps reset it. The strict interpretation of "continuous" reflects the legal definition, not just the arithmetic. If your jurisdiction allows small gaps to count as continuous (rare), add a tolerance test — but the default should be strict.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code>  <span class="c">/* compute span via Julian-day arithmetic */</span>
  <span class="v">endMins</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>, <span class="s">'J'</span>))<span class="op">*</span><span class="n">1440</span>
            <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>, <span class="s">'HH24'</span>))<span class="op">*</span><span class="n">60</span>
            <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>, <span class="s">'MI'</span>))
  <span class="v">stMins</span>  <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'J'</span>))<span class="op">*</span><span class="n">1440</span>
            <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'HH24'</span>))<span class="op">*</span><span class="n">60</span>
            <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'MI'</span>))
  <span class="v">contHrs</span> <span class="op">=</span> (<span class="v">endMins</span> <span class="op">-</span> <span class="v">stMins</span>) <span class="op">/</span> <span class="n">60</span></code></pre></div>
<div class="annot-note">
<span class="nt">Block 8c · Cross-midnight safe</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Four concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · Why naive same-day math breaks for graveyard shifts</div>

<div style="background:#1f1c19; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:10.5px; line-height:1.6; margin-bottom:10px; overflow-x:auto;">
<span style="color:#f0d68a;">// the naive approach</span><br>
<span style="color:#e6e1d8;">contMins = (stop_hour×60 + stop_min) - (start_hour×60 + start_min)</span>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">CASE A · SAME-DAY — works fine</div>
<div style="padding:10px 12px; font-family:'JetBrains Mono', monospace; font-size:10px; line-height:1.6;">
<div style="color:#3d7a52;">08:30 → 14:45</div>
<div style="color:#5a544e;">(14×60 + 45) - (8×60 + 30)</div>
<div style="color:#5a544e;">= 885 - 510 = 375 mins</div>
<div style="color:#3d7a52; font-weight:700; margin-top:6px;">✓ 6.25 hours — correct</div>
</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">CASE B · CROSS-MIDNIGHT — breaks</div>
<div style="padding:10px 12px; font-family:'JetBrains Mono', monospace; font-size:10px; line-height:1.6;">
<div style="color:#c0392b;">23:00 → 03:00 (next day)</div>
<div style="color:#5a544e;">(3×60 + 0) - (23×60 + 0)</div>
<div style="color:#5a544e;">= 180 - 1380 = <span style="color:#c0392b; font-weight:700;">-1200 mins</span></div>
<div style="color:#c0392b; font-weight:700; margin-top:6px;">✗ Negative 20 hours — nonsense</div>
</div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:10px;">The bug survives UAT (test data is typically office hours) and surfaces in production with the first night-shift submission.</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · The fix — Julian Day Numbers turn dates into a continuous integer count</div>

<div style="background:#1f1c19; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:10.5px; line-height:1.6; overflow-x:auto;">
<span style="color:#f0d68a;">// the cross-midnight-safe approach</span><br>
<span style="color:#7fc8a0;">contMins = TO_NUMBER(TO_CHAR(stretchEnd,   'J'))×1440 + (h×60+m)</span><br>
<span style="color:#7fc8a0;">         - TO_NUMBER(TO_CHAR(stretchStart, 'J'))×1440 - (h×60+m)</span><br>
<br>
<span style="color:#f0d68a;">'J' format mask — gives Julian Day Number (continuous count since 4713 BCE)</span>
</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · The graveyard-shift example, worked through</div>

<div style="background:#fff; border:1.5px solid #7a7570; border-radius:4px; padding:12px 14px;">
<div style="font-size:10.5px; font-weight:700; color:#5a544e; margin-bottom:8px;">Stretch: 23:00 on day 100 — 03:00 on day 101 (next morning)</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; line-height:1.8;">
<div><span style="color:#3d7a52;">end_mins:</span>     101 × 1440 + 3×60 + 0 = <strong style="color:#3d7a52;">145,620</strong></div>
<div><span style="color:#1f5fa8;">stretch_mins:</span> 100 × 1440 + 23×60 + 0 = <strong style="color:#1f5fa8;">145,380</strong></div>
<hr style="border:none; border-top:1px solid #7a7570; margin:6px 0;">
<div><span style="color:#c0392b;">diff:</span>        <strong>145,620 − 145,380 = 240 minutes</strong></div>
<div><span style="color:#3d7a52;">contHrs:</span>    <strong style="color:#3d7a52;">240 / 60 = 4 hours ✓ CORRECT</strong></div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; line-height:1.6; margin-top:10px;">
Notice the Julian Day numbers (100, 101) are arbitrary — the formula doesn't care about the absolute magnitude. The arithmetic just needs them to <strong style="color:#2d2926;">always increase</strong> as time moves forward, which they do, by definition.
</div>

<!-- PART 4 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 4 · The defensive-engineering value</div>

<div style="background:#fff8e8; border-left:3px solid #b97417; padding:10px 14px; border-radius:0 3px 3px 0; font-size:10.5px; color:#2d2926; line-height:1.6;">
One extra character per <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">TO_CHAR</code> call (the <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">'J'</code> format mask). No measurable performance difference. Catches an entire class of opaque production bugs — the negative-minutes nonsense that surfaces with night-shift workers. Risk-reward is dramatically asymmetric in favour of always including it.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The problem this block exists to solve</div>
<ul class="ann-bullets">
<li>The continuous-hours calculation needs to compute a single number: how many hours has the current stretch been running? In office-hours timecards (09:00–17:00), this is trivial — subtract the start time from the end time, you're done.</li>
<li>But timecards aren't all office hours. A graveyard-shift worker might punch in at 23:00 (11 PM) and punch out at 03:00 (3 AM) the next day. That's 4 hours of work. Any formula that gets that wrong is going to fire false errors at exactly the workers least equipped to argue back.</li>
<li>The naive approach — <code>(stop_hour × 60 + stop_min) − (start_hour × 60 + start_min)</code> — gives a wildly wrong answer for cross-midnight stretches. The arithmetic <code>(3 × 60) − (23 × 60) = −1200</code> minutes — negative twenty hours, obviously broken.</li>
<li>The naive approach works for any stretch contained within a single calendar day. It silently fails the moment the stretch crosses midnight. And the bug is exactly the kind that survives UAT (where test data is typically office-hours) and surfaces only in production once a night-shift worker submits their first timecard.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>Julian Day Numbers, explained</div>
<ul class="ann-bullets">
<li>The Julian Day Number is a continuous count of days since a fixed reference date in 4713 BCE. Every calendar day on Earth has its own Julian Day Number, and these numbers increase monotonically — today is one more than yesterday, no matter what month, year, or calendar system you're using.</li>
<li>Oracle's <code>TO_CHAR(date, 'J')</code> format mask returns the Julian Day Number as a string. <code>TO_NUMBER</code> converts it to a numeric value the formula can do arithmetic on.</li>
<li>The trick: combine the Julian Day with the time-of-day to produce a single <em>absolute</em> minute count. Multiply the day number by 1440 (the number of minutes in a day) and add the hours-and-minutes within that day. The result is a single number that uniquely identifies a moment in time and always increases as time moves forward.</li>
<li>Two such numbers can be subtracted directly to get the elapsed minutes between them — regardless of whether they're on the same day, adjacent days, or even weeks apart. The maths just works.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The graveyard-shift example, worked through</div>
<div class="ann-snippet">23:00 day 100  →  100×1440 + 23×60 = 145,380 mins
03:00 day 101  →  101×1440 + 3×60  = 145,620 mins
—————
diff: 145,620 − 145,380 = 240 mins = <span style="color:#7fc8a0;">4 hours ✓</span></div>
<ul class="ann-bullets">
<li>23:00 on Julian day 100 becomes <code>100 × 1440 + 23 × 60 + 0</code> = 145,380 minutes since the Julian epoch.</li>
<li>03:00 on Julian day 101 (the next day) becomes <code>101 × 1440 + 3 × 60 + 0</code> = 145,620 minutes since the same epoch.</li>
<li>The difference is 240 minutes — exactly 4 hours. Correct.</li>
<li>Notice the Julian day numbers (100, 101) are arbitrary — they happen to be small here for readability, but in real Oracle they'd be 7-digit numbers. The maths still works the same way; only the absolute magnitude changes.</li>
<li>Try the same calculation for any other cross-midnight pair and you'll get the right answer every time. The formula doesn't need a special case for "is this stretch cross-midnight?" — the Julian arithmetic handles it uniformly.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">4</span>Why this safeguard is so often skipped</div>
<ul class="ann-bullets">
<li>The naive same-day calculation is easier to write and easier to read. It works for the vast majority of timecards your formula will ever see, because most workers don't have shifts that cross midnight.</li>
<li>The Julian Day approach looks more complex on the page, even though it's only one extra character per <code>TO_CHAR</code> call (the <code>'J'</code> format mask). Developers under deadline pressure often skip the safeguard because they can't immediately see when it would matter.</li>
<li>Then a manufacturing client goes live with a night shift, or a 24/7 healthcare client adds graveyard rotations to their rollout. The formula breaks on day one of production for those workers, and the bug is opaque (negative minutes? what?) until someone with prior context recognises the pattern.</li>
<li>The cost of including Julian arithmetic from day one is negligible — one extra character per call, no measurable performance difference. The cost of <em>not</em> including it is a production incident with a hard-to-diagnose bug. The risk-reward is dramatically asymmetric in favour of always including it.</li>
<li>This is a small example of <strong>defensive engineering</strong>: pay tiny costs upfront to remove entire classes of bugs that would otherwise surface at the worst possible time. The pattern generalises beyond TER — any time math operation that might cross a boundary (midnight, year-end, daylight-saving) deserves the same treatment.</li>
</ul>
</div>
<div class="ann-takeaway">Cross-midnight safety costs one extra character per <code>TO_CHAR</code> call: the <code>'J'</code> format mask. The performance impact is unmeasurable. The bug it prevents is opaque, hard to reproduce, and surfaces in production with night-shift workers — exactly when you can least afford it. Pay the cost upfront, every time.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code>  <span class="c">/* threshold check — error wins over warning */</span>
  <span class="k">IF</span> (<span class="v">contHrs</span> <span class="op">></span> <span class="v">p_max_cont_err</span>
      <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span>
      <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span>
      <span class="k">AND</span> <span class="f">length</span>(<span class="v">hol</span>) <span class="op">=</span> <span class="n">0</span>) <span class="k">THEN</span>
  ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> ... <span class="v">p_msg_cont_err</span> )
  <span class="k">ELSE</span>
  ( <span class="k">IF</span> (<span class="v">contHrs</span> <span class="op">></span> <span class="v">p_max_cont_warn</span>
        <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span>
        <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span>
        <span class="k">AND</span> <span class="f">length</span>(<span class="v">hol</span>) <span class="op">=</span> <span class="n">0</span>) <span class="k">THEN</span>
    ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> ... <span class="v">p_msg_cont_warn</span> )
  )
)</code></pre></div>
<div class="annot-note">
<span class="nt">Block 8d · Error wins</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Four concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · Two thresholds, two audiences — warning for worker, error for legal</div>

<div style="background:#fff; border:1.5px solid #7a7570; border-radius:4px; padding:14px;">
<div style="position:relative; height:36px; background:linear-gradient(to right, #e8f4ea 0%, #e8f4ea 71%, #fff8e7 71%, #fff8e7 85%, #fff5f0 85%, #fff5f0 100%); border-radius:3px; overflow:hidden;">
<div style="position:absolute; left:71%; top:0; bottom:0; width:2px; background:#b97417;"></div>
<div style="position:absolute; left:85%; top:0; bottom:0; width:2px; background:#c0392b;"></div>
<div style="position:absolute; left:25%; top:8px; font-size:10px; color:#3d7a52; font-weight:700;">clean</div>
<div style="position:absolute; left:74%; top:8px; font-size:9px; color:#b97417; font-weight:700;">warn</div>
<div style="position:absolute; left:90%; top:8px; font-size:9px; color:#c0392b; font-weight:700;">error</div>
</div>
<div style="display:flex; justify-content:space-between; font-size:9px; color:#5a544e; margin-top:6px;">
<span>0h</span><span>2h</span><span>4h</span><span style="color:#b97417; font-weight:700;">5h (warn)</span><span style="color:#c0392b; font-weight:700;">6h (error)</span><span>7h</span>
</div>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:10px;">
<div style="background:#fff3e0; border:1.5px solid #b97417; border-radius:4px; overflow:hidden;">
<div style="background:#b97417; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">WARNING · soft</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#2d2926;">Audience: the worker</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:4px; line-height:1.5;">"You've been working 5 hours straight — take a break soon." Doesn't block submission. Worker can ignore but is informed.</div>
</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">ERROR · hard</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#2d2926;">Audience: legal/compliance</div>
<div style="font-size:9.5px; color:#5a544e; margin-top:4px; line-height:1.5;">"You've exceeded the 6-hour cap." Blocks submission. Worker must split the entry or add a meal break.</div>
</div>
</div>
</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · Why error wins — IF/ELSE structure ensures only one fires</div>

<div style="background:#1f1c19; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:10.5px; line-height:1.6; overflow-x:auto;">
<span style="color:#f0d68a;">// the structure</span><br>
<span style="color:#7fc8a0;">IF (contHrs > p_max_cont_err) THEN</span><br>
<span style="color:#e6e1d8;">  OUT_MSG[nidx] = <em style="color:#e07060;">error message</em></span><br>
<span style="color:#7fc8a0;">ELSE</span><br>
<span style="color:#e6e1d8;">  IF (contHrs > p_max_cont_warn) THEN</span><br>
<span style="color:#e6e1d8;">    OUT_MSG[nidx] = <em style="color:#7fc8a0;">warning message</em></span>
</div>
<div style="font-size:10.5px; color:#5a544e; line-height:1.6; margin-top:10px;">
The nested <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">IF/ELSE</code> guarantees mutual exclusion: if the error condition fires, the warning branch isn't even checked. The worker sees the more severe message; the less severe one is suppressed.
</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · What goes wrong with naive IF / IF instead</div>

<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">THE BUG — two independent IFs</div>
<div style="padding:10px 12px;">
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10px; line-height:1.6;">
IF (contHrs > p_max_cont_err)  THEN OUT_MSG[nidx] = error<br>
IF (contHrs > p_max_cont_warn) THEN OUT_MSG[nidx] = warning
</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:8px; line-height:1.6;">
At 7 hours continuous: <strong>both</strong> conditions fire. First the error writes. Then the warning <em>overwrites</em> it. Worker sees only the warning — less severe message wins. Legal cap silently violated.
</div>
<div style="font-size:10.5px; color:#c0392b; font-weight:700; margin-top:6px;">✗ The more dangerous error gets hidden by the milder warning.</div>
</div>
</div>

<!-- PART 4 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 4 · The weekend & holiday short-circuits</div>

<div style="background:#fff; border:1.5px solid #7a7570; border-radius:4px; padding:12px 14px;">
<div style="font-size:10.5px; color:#2d2926; line-height:1.6;">
Both threshold checks include three guard conditions:
<ul style="margin:6px 0 0 16px; padding:0; color:#5a544e;">
<li><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_day <> 'SAT'</code></li>
<li><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_day <> 'SUN'</code></li>
<li><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">length(hol) = 0</code> (no public holiday)</li>
</ul>
</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:8px;">Weekend and holiday work is governed by different rules — usually paid at premium and not subject to the same continuous-hours cap. These guards prevent false flags on those days.</div>
</div>

<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:3px; margin-top:14px; font-size:10.5px; line-height:1.6;">
<span style="font-family:'JetBrains Mono', monospace; font-weight:700; color:#f0d68a;">TAKEAWAY:</span> Use IF/ELSE structure when thresholds overlap. The order matters — check the more severe condition first. Add the weekend/holiday guards uniformly to every threshold check.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>Two thresholds, two purposes</div>
<ul class="ann-bullets">
<li>The continuous-hours validation has two distinct thresholds rather than one. The <strong>soft warning</strong> (default 5 hours, parameter <code>p_max_cont_warn</code>) gives the worker advance notice that they're approaching the legal cap. The <strong>hard error</strong> (default 6 hours, parameter <code>p_max_cont_err</code>) blocks submission entirely once the cap is exceeded.</li>
<li>The two-tier design serves different audiences. The warning is for the worker — a heads-up that says <em>"you're getting close to needing a meal break"</em>. It doesn't block submission; it just informs.</li>
<li>The error is for legal compliance. Once the worker actually crosses the cap, the formula refuses to let the timecard through — not because the formula is being mean, but because the labor regulation forbids it.</li>
<li>The gap between the two thresholds (warning at 5h, error at 6h) is deliberate. It gives the worker an hour of grace to wrap up what they're doing and take a break. A single threshold at the cap would be too abrupt; a single threshold at warning would be ineffective. Two thresholds with an hour of separation is the design that serves both audiences.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>The 6.25-hour scenario, in detail</div>
<ul class="ann-bullets">
<li>Picture a stretch that has grown to 6.25 hours. The worker started at 08:30 and hasn't taken a meal break; it's now 14:45 and they're still going.</li>
<li>The stretch crosses the warning threshold (5 hours, at 13:30) and then crosses the error threshold (6 hours, at 14:30). At 6.25 hours, both conditions in the threshold check evaluate TRUE.</li>
<li>Technically, both messages would apply. The worker has earned the warning ("approaching cap") and earned the error ("exceeded cap"). The formula now has a choice: surface both messages, or just one?</li>
<li>Surfacing both creates noise. The worker sees two red markers on the same row and has to figure out which one to address. The error message ("exceeded") is more actionable than the warning ("approaching"), so the warning becomes redundant.</li>
<li>The right behaviour is to surface only the more serious message — the error. The warning is implicitly subsumed (if you've exceeded the cap, you've also approached it). This is the principle the IF/ELSE structure enforces.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>Two parallel IFs vs one IF/ELSE</div>
<div class="ann-snippet"><span style="color:#e07060;">// WRONG — two parallel IFs</span>
IF contHrs > 6 THEN OUT_MSG[nidx] = "ERROR"
IF contHrs > 5 THEN OUT_MSG[nidx] = "WARN"
<span style="color:#d4c896;">// at 6.25h: error written, then overwritten by warn</span>

<span style="color:#7fc8a0;">// RIGHT — IF/ELSE</span>
IF contHrs > 6 THEN OUT_MSG[nidx] = "ERROR"
ELSE IF contHrs > 5 THEN OUT_MSG[nidx] = "WARN"
<span style="color:#d4c896;">// at 6.25h: error written; warning branch skipped</span></div>
<ul class="ann-bullets">
<li>The wrong shape uses two independent IF statements. At 6.25 hours, the first IF fires and writes the error message into <code>OUT_MSG[nidx]</code>. Then the second IF fires (because 6.25 also exceeds 5) and <em>overwrites</em> the same slot with the warning message. The worker sees the warning, misses the error.</li>
<li>This is exactly backwards. The worker is over the legal cap, but the message they see says they're <em>approaching</em> it. The misinformation is worse than no message at all.</li>
<li>The right shape uses IF/ELSE. The first branch checks the more severe condition. If it matches, the error fires and the second branch is <em>skipped entirely</em>. The warning never gets a chance to overwrite the error.</li>
<li>This single structural choice is the difference between a formula that almost-works and one that does what the legal team actually intended. The two versions look superficially similar — same conditions, same messages, same data — but their behaviour at the boundary case is opposite.</li>
<li>The general principle: <strong>when multiple conditions can fire on the same row, ensure mutual exclusivity through IF/ELSE structure</strong>. Don't trust write-order to produce the right outcome — encode the priority directly in the control flow.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">4</span>Why both thresholds are suspended on weekends and holidays</div>
<ul class="ann-bullets">
<li>Both threshold checks include the same suppression conditions: <code>l_day <> 'SAT' AND l_day <> 'SUN' AND length(hol) = 0</code>. If the day is a weekend or a public holiday, neither error nor warning fires.</li>
<li>The reasoning is legal. Most labor regulations explicitly exempt non-working days from continuous-work caps. The cap is designed to enforce rest during normal working hours; on a Saturday or a public holiday, normal working hours don't apply, and the cap doesn't either.</li>
<li>The holiday check uses <code>length(hol) = 0</code>, where <code>hol</code> is a string containing the holiday name fetched from the holiday value set. If the day is a public holiday, <code>hol</code> contains the holiday name and has nonzero length; the condition fails and the threshold check is suppressed. If it's a regular workday, <code>hol</code> is empty, the condition passes, and the threshold check proceeds.</li>
<li>The weekend check uses simple string comparison against the day name. If you're rolling out to a region where the weekend isn't Saturday-Sunday (some jurisdictions use Friday-Saturday or other configurations), this is one of the places to adjust — ideally by parameterising the weekend days so the formula stays portable.</li>
</ul>
</div>
<div class="ann-takeaway">Two thresholds, both suspended on non-working days, with IF/ELSE ensuring the more severe message wins when both conditions match. The structural choice between IF/ELSE and two parallel IFs is invisible in the code shape but decisive in worker experience — encode priority through control flow, not through write-order.</div>
</div></div>
</div>
</div>

</div>
</div>

<p>That's the algorithm in full. Setup runs once. The loop runs N times — classifying each row, buffering Reg Hours into the day buffer, advancing the stretch tracker, and at every <code>END_DAY</code> running pairwise overlap then resetting. Block 8 fires last on each row, comparing the running stretch against the soft and hard caps. Whatever flags accumulated across the run land in <code>OUT_MSG</code>, which the framework reads on return.</p>

<h2>Setup Dependencies</h2>

<p>The formula itself is one piece of a much larger picture. There's a layer of <strong>prerequisites</strong> that must exist before the formula will compile cleanly or fire correctly, and there's a <strong>six-step rule pipeline</strong> from the raw formula to a worker actually running it. Both layers matter: miss something in prerequisites and the formula compiles successfully but throws at runtime; miss something in the pipeline and the formula never reaches the worker.</p>

<h3>Prerequisites — what must exist first</h3>

<p>Before you even compile the formula, six artefacts must exist in the target environment. None of them are part of the formula source — they're separate setup items that the formula <em>references</em>.</p>

<table>
<thead><tr><th>Prerequisite</th><th>Where</th><th>Why the formula needs it</th></tr></thead>
<tbody>
<tr><td>Custom messages registered</td><td>Setup and Maintenance → Manage Messages (Application = <code>HXT</code>)</td><td>Every <code>get_output_msg('HXT', p_msg_xxx)</code> call resolves a message name into translated text. The five <code>XX_*</code> messages must exist before runtime — the formula compiles fine without them but throws when a code path fires.</td></tr>
<tr><td>Payroll Time Type values</td><td>Setup and Maintenance → Manage Common Lookups → Lookup Type for payroll time types</td><td>The literal strings <code>'Regular Hours'</code> and <code>'Meal Break'</code> in <code>p_reg_type</code> and <code>p_break_type</code> must match actual configured payroll time types. If a worker's time card uses <code>'Reg Hrs'</code> instead, the gate <code>aiTimeType = p_reg_type</code> never matches and every rule silently skips.</td></tr>
<tr><td>Public Holidays value set</td><td>Setup and Maintenance → Manage Value Sets</td><td><code>GET_VALUE_SET('XX_HOLIDAY_CALENDAR_VS', ...)</code> looks up the holiday calendar at runtime. Value set must exist with the WHERE clause that scopes by date and legal entity. Test it with the <code>pay_ff_functions.gvs()</code> BIP query before attaching to the formula.</td></tr>
<tr><td>Profile option for rule logging</td><td>Setup and Maintenance → Manage Administrator Profile Values → <code>ORA_HWM_RULES_LOG_LEVEL</code></td><td>Every <code>add_rlog</code> call in the formula writes to a buffer that's only persisted if logging is enabled. Set Site-level value to <code>Fine</code> or <code>Finer</code> in non-production. Without this, your debug logs vanish and the Analyze Rule Processing Details UI shows nothing.</td></tr>
<tr><td>Time Consumer Sets</td><td>Setup and Maintenance → Manage Time Consumer Sets</td><td>Tells the framework where validated time goes after rules run — Payroll, Project Costing, both, or neither. Without a consumer set linked to the worker's profile, time cards have nowhere to land even after the formula approves them.</td></tr>
<tr><td>Repeating Time Periods</td><td>Setup and Maintenance → Manage Repeating Time Periods</td><td>Defines the time card period (weekly, biweekly, monthly). Drives the <code>END_PERIOD</code> boundary marker in the input array. Use delivered periods or create custom ones — either way, one must be linked to the worker's processing profile.</td></tr>
</tbody>
</table>

<div class="aside">
<div class="head">The "compiles but throws" trap</div>
Fast Formula's compile-time validation does <em>not</em> verify that referenced messages, lookup values, or value sets actually exist. Your formula will compile cleanly even if every <code>XX_*</code> message is missing — the failure surfaces only at runtime when that specific code path fires for a specific worker on a specific timecard. To verify before the formula lands in production, run: <code>SELECT MESSAGE_NAME FROM FND_NEW_MESSAGES WHERE MESSAGE_NAME LIKE 'XX_%' AND APPLICATION_ID = (SELECT APPLICATION_ID FROM FND_APPLICATION WHERE APPLICATION_SHORT_NAME = 'HXT')</code>. Should return all five names. Same approach for lookup values and value set existence.
</div>

<h3>The Rule Pipeline — six steps from formula to worker</h3>

<p>Once prerequisites are in place, the formula travels through a six-step pipeline before a worker's time card actually runs through it. The most commonly missed step is <strong>Step 2: Rule Templates</strong> — you cannot create a Time Rule directly from a formula in OTL. The Rule Template is the bridge that exposes the formula's parameters and outputs to the rule-creation UI.</p>

<table>
<thead><tr><th>Step</th><th>Task</th><th>What to Set</th></tr></thead>
<tbody>
<tr><td>1</td><td>My Client Groups → Time Management → <strong>Fast Formulas</strong></td><td>Create the formula. Type = <strong>Time Entry Rules</strong>. Compile and verify no errors. The Manage Fast Formulas UI is plain-text — no syntax highlighting, no folding. Author your formula in a real editor and paste it in.</td></tr>
<tr><td>2</td><td>My Client Groups → Time Management → <strong>Rule Templates</strong></td><td>Create a Time Entry Rule Template. Select the formula. Configure: <em>Rule Classification</em> (e.g., Business message), <em>Reporting Level</em>, <em>Process Empty Time Card</em>, <em>Time Card Events That Trigger</em>, <em>Suppress Duplicate Messages Display</em>. Configure each formula <strong>parameter</strong> (display name, value type, default value) and each <strong>output</strong> (display name, message severity for OUT_MSG — Information, Warning, or Error).</td></tr>
<tr><td>3</td><td>My Client Groups → Time Management → <strong>Rules</strong></td><td>Create a Time Entry Rule from the template. <em>This is where the actual parameter values live</em> — <code>SCHEDULE_START_HOUR=9</code>, <code>SCHEDULE_END_HOUR=18</code>, <code>MAX_CONTINUOUS_HRS_ERR=6</code>, <code>MAX_CONTINUOUS_HRS_WARN=5</code>. These are what <code>get_rvalue_number</code> reads at runtime via <code>rule_id</code>. Different LEs use the same template with different rule values.</td></tr>
<tr><td>4</td><td>My Client Groups → Time Management → <strong>Rule Sets</strong></td><td>Add the rule to a Time Entry Rule Set. The rule set bundles together all the validations that apply to a given worker population. Different LEs may share rules but bundle them into different sets.</td></tr>
<tr><td>5</td><td>My Client Groups → Time Management → <strong>Worker Time Processing Profiles</strong></td><td>Attach the Rule Set to a Time Processing Profile, along with: Time Consumer Set, Repeating Time Period, default Payroll Time Type. The profile is what gets assigned to workers — it bundles every piece of OTL config they touch.</td></tr>
<tr><td>6</td><td>HCM Groups + Profile assignment (batch-driven via Evaluate HCM Group Membership)</td><td>Link workers to the Time Processing Profile via HCM Group membership. Run <em>Evaluate HCM Group Membership</em> for the date range. From this point, every timecard submission for matching workers runs through your formula.</td></tr>
</tbody>
</table>

<div class="figure">
<div class="fig-meta">Figure 07 · Setup Topology</div>
<div class="fig-title">How the prerequisites and pipeline connect</div>
<div class="fig-sub">The formula sits in the middle. Prerequisites feed in from the left. The pipeline carries it out to the worker on the right.</div>

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-4/diagram-2.png" alt="Diagram 2: Oracle Fast Formula: Time Entry Rule (Part 4)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<h4>Why Step 2 (Rule Template) is the most commonly missed</h4>

<p>It's tempting to think "I have a Fast Formula, now I need to attach it to a worker." That skips the Rule Template, which is genuinely required. The template is what tells OTL: <em>here is a formula, here are the parameters that need values when an admin creates a rule, here is what each output means, here is what severity OUT_MSG carries</em>. Without it, the rule-creation UI has no way to render parameter fields or know how to interpret outputs.</p>

<p>Practically: the template defines <em>what kind of rule</em> this formula creates (the Rule Classification), and the rule defines <em>the actual values</em>. One template + many rules + many rule sets is the typical pattern for multi-LE rollouts. The template is reusable; the rule is entity-specific.</p>

<h4>Why Step 6 (HCM Group + assignment) is the silent failure point</h4>

<p>If the worker isn't linked to the Time Processing Profile through HCM Group membership, the formula never fires for them — <em>silently</em>. UAT testers usually have the profile manually assigned during testing, so this passes UAT cleanly. In production, the assignment is typically batch-driven by the <em>Evaluate HCM Group Membership</em> process. If the batch hasn't run, or the eligibility criteria excluded a population, those workers' timecards bypass the formula entirely. Submissions sail through with no validation, and the gap is invisible from the OTL side because there's no error — the formula simply never runs.</p>

<p>Validate Step 6 as part of go-live readiness, not just the formula compile. The query <code>SELECT * FROM HWM_USER_TIME_PROCESSING_PROFILES WHERE PROFILE_ID = :your_profile_id</code> should return rows for every worker who's supposed to be running this formula. If it doesn't, the HCM Group evaluation hasn't completed for them.</p>

<h2>The Worked Example, End-to-End</h2>

<p>Now that every block has been explained, here's how all of them work together on a real submission. We'll trace Sarah's timecard from the moment she clicks Submit through to the three error markers she sees on her screen.</p>

<p><strong>The submission.</strong> Sarah's timecard for 14-Apr-2026 has four worker entries plus three system markers (HEADER, END_DAY, END_PERIOD). The framework hands the formula seven array slots in total, indexed [1] through [7].</p>

<div class="figure" style="background:#1a1815; border-color:#2d2926; padding:26px;">
<div class="fig-meta" style="color:#e07060;">Figure 06 · End-to-End · Gantt View</div>
<div class="fig-title" style="color:#f5f1e8;">Sarah's Tuesday on a single 24-hour axis</div>
<div class="fig-sub" style="color:#d4c896;">All four worker entries laid out by index. Red shaded zones mark where the OVERLAP rule fires; coral pulse markers show which entry takes the flag.</div>

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-4/diagram-3.png" alt="Diagram 3: Oracle Fast Formula: Time Entry Rule (Part 4)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

<div style="margin-top:18px; padding:14px 18px; background:#0d0c0a; border-left:3px solid #c0392b;">
<div style="font-size:10px; letter-spacing:1.5px; color:#c0392b; font-weight:700; margin-bottom:8px;">FINAL OUT_MSG</div>
  <pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code>OUT_MSG[3] = "Continuous work exceeds 6 hours ..."
OUT_MSG[4] = "Break outside working hours ..."
OUT_MSG[5] = "Overlapping entries ..."</code></pre>
</div>
</div>

<h3>What happens inside the loop, iteration by iteration</h3>

<p>The formula runs through seven iterations of its WHILE loop, one per array index. Here's exactly what changes in each iteration:</p>

<div class="excel-wrap">
<div class="excel-titlebar">
<span class="filename">Loop_Trace.xlsx</span>
<span class="app">Excel</span>
</div>
<table class="excel-sheet">
<thead>
<tr>
<th>Iter</th>
<th>Row</th>
<th>What the formula does</th>
<th>State after iteration</th>
</tr>
</thead>
<tbody>
<tr>
<td class="num">1</td>
<td><strong>HEADER</strong> at [1]</td>
<td>Reads <code>RECORD_POSITIONS[1] = 'HEADER'</code>. The other arrays at [1] are empty — the <code>.exists()</code> guards skip those reads. No validation runs; no state changes.</td>
<td>Day buffer empty. Stretch tracker idle.</td>
</tr>
<tr class="row-clean">
<td class="num">2</td>
<td>Reg Hours [2]<br>08:30–10:00</td>
<td>Block 6 reads the row. Block 6c confirms both punches present. Block 6d adds the entry to the day buffer. Block 8 starts a new stretch (1.5h, well under cap).</td>
<td>Day buffer = [(08:30, 10:00, idx 2)]<br>Stretch = 08:30–10:00 (1.5h)</td>
</tr>
<tr class="row-flagged">
<td class="num">3</td>
<td>Reg Hours [3]<br>10:00–14:45</td>
<td>Block 6 reads the row. Block 6d adds it to the day buffer. Block 8 sees this entry's start (10:00) matches the previous stretch's end (10:00) — so it <strong>extends</strong> the stretch to 08:30–14:45 (6.25h). 6.25 > 6 → <strong>error fires on row [3]</strong>: <em>"Continuous work exceeds 6 hours"</em>.</td>
<td>Day buffer has 2 entries.<br>Stretch = 08:30–14:45 (6.25h, flagged)<br><code>OUT_MSG[3]</code> populated.</td>
</tr>
<tr class="row-flagged">
<td class="num">4</td>
<td>Meal Break [4]<br>19:00–20:00</td>
<td>Block 6 reads the row. Block 6e checks the meal break's window: 19:00–20:00 falls outside the 09:00–18:00 schedule. <strong>Error fires on row [4]</strong>: <em>"Break outside working hours"</em>. Block 6e also flips <code>l_meal_taken = 'Y'</code>.</td>
<td><code>OUT_MSG[4]</code> populated.<br>Meal flag now 'Y'.</td>
</tr>
<tr class="row-flagged">
<td class="num">5</td>
<td>Reg Hours [5]<br>08:00–20:00</td>
<td>Block 6 reads the row. Block 6c confirms both punches present. Block 6d adds it to the day buffer. Block 8's gate is now closed (because <code>l_meal_taken = 'Y'</code>) so the stretch tracker doesn't grow further.</td>
<td>Day buffer has 3 entries: [2], [3], [5].</td>
</tr>
<tr style="background:#f5e9d8;">
<td class="num">6</td>
<td><strong>END_DAY</strong> at [6]</td>
<td>Block 7 fires. The pairwise overlap test runs on the day buffer's three entries. Pair (2, 3) — touching at 10:00, no overlap. Pair (2, 5) — entry 5's range 08:00–20:00 contains entry 2's 08:30–10:00 → overlap. Pair (3, 5) — entry 5's range contains entry 3's 10:00–14:45 → overlap. <strong>Error fires on row [5]</strong> (the later entry in each conflicting pair): <em>"Overlapping entries"</em>. Then Block 7c clears the day buffer, the stretch tracker, and the meal flag.</td>
<td><code>OUT_MSG[5]</code> populated.<br>All day-level state reset to empty.</td>
</tr>
<tr>
<td class="num">7</td>
<td><strong>END_PERIOD</strong> at [7]</td>
<td>The formula's WHILE loop reaches the end. <code>RETURN out_msg_ary</code> hands the populated array back to the framework.</td>
<td>Loop terminates.</td>
</tr>
</tbody>
</table>
</div>
<div class="excel-caption">Seven iterations, three errors, one return. Notice how each block's output (day buffer growth, stretch extension, meal flag) feeds into other blocks' decisions on later iterations.</div>

<p>The framework receives the array and renders three red error markers on Sarah's timecard, one beside each flagged row. <strong>The submission is blocked until she fixes all three.</strong></p>

<p>Sarah sees three red error markers when the formula returns. She edits the times, removes the consolidated entry [5], moves the meal break to a real lunch slot, and resubmits. The formula re-runs from scratch on the corrected array. Clean OUT_MSG → submission accepted → timecard moves to approval.</p>

<div style="background:#fff; padding:48px 36px 56px 36px; margin:48px 0 24px 0; border-radius:8px; border:1px solid #e8e3d8;">

<!-- Header: title + tagline -->
<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:36px; flex-wrap:wrap; gap:16px;">
<div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#1f5fa8; letter-spacing:-0.5px;">Three layers.</div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#2d2926; letter-spacing:-0.5px; margin-top:4px;">Choose deliberately.</div>
</div>
<div style="text-align:right;">
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:14px; font-weight:700; color:#2d2926; letter-spacing:0.5px;">RECAP</div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:11px; color:#7a7570; margin-top:2px; letter-spacing:0.5px;">Where this formula sits</div>
</div>
</div>

<!-- Tile grid: 3 layer tiles with Layer 02 (TER) highlighted -->
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-4/diagram-4.png" alt="Diagram 4: Oracle Fast Formula: Time Entry Rule (Part 4)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

<!-- Caption beneath -->
<p style="margin:32px 0 0 0; font-size:14px; color:#5a544e; line-height:1.65; text-align:center; font-style:italic;">
"Validate first, calculate second." <span style="font-style:normal;">A clean separation between Layer 02 and Layer 03 keeps each formula focused and testable.</span>
</p>

<!-- CTA -->
<div style="text-align:center; margin-top:28px;">
<span style="display:inline-block; padding:12px 28px; border:1.5px solid #1f5fa8; color:#1f5fa8; font-family:'Manrope', -apple-system, sans-serif; font-size:13px; font-weight:700; letter-spacing:0.3px; border-radius:2px;">
The TER formula is your last gate before bad data lands in the repository.
</span>
</div>

</div>

<p>Build it once with care, parameterize the entity-specific values, and the same formula serves your whole rollout — one source of truth, configured per legal entity through rule parameters.</p>

<h2>References</h2>

<table>
<thead><tr><th>#</th><th>Source</th><th>What I used</th></tr></thead>
<tbody>
<tr><td>1</td><td>Administering Fast Formulas — Time Entry Rule</td><td>Formula type contract, OUT_MSG output structure, framework arrays</td></tr>
<tr><td>2</td><td>Implementing Time and Labor — Validation Rules</td><td>Validation rule attachment, rule sets, processing profiles</td></tr>
<tr><td>3</td><td>Local labor regulation references (jurisdiction-specific)</td><td>Continuous-work caps, mandatory break requirements per locale</td></tr>
<tr><td>4</td><td>OTL Database Items Reference (REL11)</td><td><code>HWM_CTXARY_*</code> prefix, <code>.exists()</code> patterns, sparse arrays</td></tr>
</tbody>
</table>




<!-- SERIES COMPLETE -->
<div style="background:#fff8e8; border:1px solid #b97417; border-radius:6px; padding:20px 24px; margin:40px 0 32px 0;">
<div style="font-size:10px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">The TER Series · Complete</div>
<div style="font-size:15px; color:#2d2926; line-height:1.65;">You now have the complete picture of how a production Oracle HCM Cloud TER formula works — from the OTL submission flow, through the input contract, through the algorithm and state machine, end to end. Bookmark this series as a reference for your next TER implementation.</div>
</div>

<!-- FOOTER (Philippine-leave-post style) -->
<hr style="margin:48px 0 32px 0; border:none; border-top:1px solid #e8e3d8;">

<div class="byline">
<div class="avatar">AM</div>
<div class="author-block">
<div class="author-name">Abhishek Mohanty</div>
<div class="author-creds">Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Time and Labor, Absence Management, Core HR, Redwood, HDL, OTBI.</div>
</div>
</div>

<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:24px;">
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/Fast%20Formula" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">Fast Formula</a>
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20Entry%20Rule" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">Time Entry Rule</a>
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/OTL" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">OTL</a>
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20and%20Labor" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">Time and Labor</a>
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/Oracle%20HCM%20Cloud" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">Oracle HCM Cloud</a>
</div>

</div>
</body>
</html>