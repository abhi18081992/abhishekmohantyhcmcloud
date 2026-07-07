---
title: "Oracle Fast Formula: Time Entry Rule (Part 1)"
pubDate: 2026-05-21
description: "Oracle Fast Formula: Time Entry Rule (Part 1)"
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
--code-comment: #7c7670;
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
em { color: #3a342e; }
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
color: #a8a39c;
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
grid-template-columns: 1fr 280px;
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
border-left: 2px solid var(--accent);
padding: 12px 14px;
font-size: 11.5px;
color: #d8d2c8;
line-height: 1.5;
}
.annot-line .annot-note .nt {
display: block;
font-size: 9px;
letter-spacing: 1.5px;
font-weight: 700;
color: var(--accent);
text-transform: uppercase;
margin-bottom: 3px;
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
color: #a8a39c;
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
color: #a8a39c;
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
</style>
</head><body>
</head><body>
<div class="container">

<!-- HEADER (Philippine-leave-post style) -->
<div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Fast Formula</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Time Entry Rule</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">OTL</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Hands-On</span>
</div>

<div style="font-size:13px; color:#7a7570; margin-bottom:18px;">May 21, 2026 • 14 min read • Oracle HCM Cloud</div>

<!-- SERIES BREADCRUMB -->
<div style="background:#f5f1e8; border-left:3px solid #b97417; padding:10px 14px; margin-bottom:24px; border-radius:0 3px 3px 0; font-size:12px;">
<span style="font-weight:700; color:#b97417; letter-spacing:0.5px; text-transform:uppercase; font-size:10px;">The TER Series</span>
<span style="color:#5a544e; margin-left:8px;">Part 1 of 4</span>
<div style="margin-top:6px; color:#7a7570; font-size:11.5px; line-height:1.5;">
1. OTL Foundations ·
2. The Input Contract ·
3. Algorithm: Routing & Overlap ·
4. The State Machine
</div>
</div>

<h1>Oracle OTL and Where Time Entry Rules Fit<br><span style="color:#7a7570; font-size:0.7em; font-weight:400; font-style:italic;">Part 1 of 4 — The TER Series</span></h1>

<div class="byline">
<div class="avatar">AM</div>
<div class="author-block">
<div class="author-name">Abhishek Mohanty</div>
<div class="author-creds">Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead</div>
</div>
</div>


<div class="opening">
Time Entry Rule (TER) formulas live inside Oracle's Time and Labor module — the part of HCM Cloud that workers use to log their hours. This first post in the series introduces what OTL is, where TER sits in its submission flow, and why this is the validation layer where the real business logic lives.
</div>

<h2>What OTL Is</h2>

<p>Oracle Time and Labor (OTL) is the time-tracking module inside Oracle HCM Cloud. Workers log their hours into it through a timecard layout. Managers approve those timecards. The approved data flows downstream to payroll, project costing, or wherever the hours need to land. That's the loop at its simplest.</p>

<p>What makes OTL interesting from a developer's point of view is the extensibility model. Between the worker hitting Submit and the data landing in payroll, OTL runs the timecard through a series of <strong>rule formulas</strong> that you, as the implementer, can write. Each formula type plays a different role:</p>

<ul>
<li><strong>Time Entry Rules (TER)</strong> — run when the worker tries to save or submit. They validate the data and either let it through or flag it with messages the worker can see. <em>This is what the series is about.</em></li>
<li><strong>Time Calculation Rules (TCR)</strong> — run after validation passes. They derive new values from the worker's entries: overtime, premium pay, shift differentials. The worker's original entries stay untouched; TCR adds calculated rows on top.</li>
<li><strong>Time Device Rules (TDR)</strong> — handle integration with physical badge readers and punch clocks. They map raw punch events into the OTL data model.</li>
</ul>

<p>Each rule type sees a different shape of data, gets different inputs from the framework, and is allowed to do different things. TER is the strictest of the three because it runs <em>before</em> the data is accepted — its job is to be a guard. Calculations and device integration come later.</p>

<h2>Why TER Is the Hard One</h2>

<p>OTL's framework gives you some validation for free. If a worker leaves a required field blank, OTL catches it. If they type letters into a numeric field, OTL catches that too. These are <em>declarative validations</em> — you configure them in the timecard layout, and the framework enforces them with no code.</p>

<p>But declarative validation can only check one cell at a time. The validations that actually matter in production are about relationships between cells, between rows, and between days. Things like:</p>

<ul>
<li>"Did this worker take a meal break after 6 hours of continuous work?" — spans multiple rows on the same day</li>
<li>"Do any of these entries overlap with each other?" — pairwise comparison across rows</li>
<li>"Is this meal break inside the worker's scheduled hours?" — requires reading the schedule, which lives elsewhere in HCM</li>
<li>"Has this worker exceeded their weekly hours cap?" — cumulative across days</li>
</ul>

<p>None of these can be expressed in declarative configuration. They need code that loops, remembers, and compares. That's where TER formulas earn their place — and that's where most teams either skip the validation entirely or get it subtly wrong.</p>

<p>This series walks through one production TER formula end-to-end, using a real five-rule validation example. By the end of Part 4 you'll know how the framework hands data to the formula, how the formula loops through it, and how to encode every common validation pattern you'll encounter on a TER implementation.</p>
<h2>What This Formula Does</h2>

<p>The job is straightforward to describe and surprisingly subtle to build. When a worker submits their timecard, OTL needs to verify that what they entered makes sense — not just structurally (which the framework handles for free), but according to the company's actual labour rules.</p>

<div style="background:#fff; padding:48px 36px 56px 36px; margin:32px 0 24px 0; border-radius:8px; border:1px solid #e8e3d8;">

<!-- Header: title + tagline -->
<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:36px; flex-wrap:wrap; gap:16px;">
<div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#1f5fa8; letter-spacing:-0.5px;">Five rules.</div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#2d2926; letter-spacing:-0.5px; margin-top:4px;">One enforces them all.</div>
</div>
<div style="text-align:right;">
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:14px; font-weight:700; color:#2d2926; letter-spacing:0.5px;">WHAT THIS FORMULA DOES</div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:11px; color:#7a7570; margin-top:2px; letter-spacing:0.5px;">Validation rules at a glance</div>
</div>
</div>

<!-- Tile grid: 5 rule tiles with Rule 04 highlighted -->
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-1/diagram-1.png" alt="Diagram 1: Oracle Fast Formula: Time Entry Rule (Part 1)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

<!-- Caption beneath -->
<p style="margin:24px 0 0 0; font-size:13px; color:#5a544e; line-height:1.65; text-align:center;">
Rules 1 and 3 only need a single row. Rules 2, 4, and 5 are <strong>multi-row validations</strong> — they need to know about other rows on the same day, or remember state from earlier iterations. That single architectural requirement — <em>seeing more than one row at a time</em> — is what separates TER from anything you can do with declarative configuration.
</p>

</div>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:18px 22px; margin:24px 0; font-size:14px; line-height:1.7; color:#2d2926; border-radius:0 4px 4px 0;">
<div style="font-size:10px; letter-spacing:1.8px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Expert framing</div>
<p style="margin-top:0;">Rules 4 and 5 (the continuous-work checks) are the genuinely hard ones — not because the maths is complex, but because they require <strong>state that persists across loop iterations</strong>. You can't just look at row 3 and decide whether continuous work has been exceeded; you need to know what rows 1 and 2 said, whether a meal break has been logged yet, and whether yesterday's data has been correctly cleared.</p>
<p style="margin-bottom:0;">Most TER implementations I've reviewed in client environments either get this wrong (the formula incorrectly extends a stretch across a meal break) or skip it entirely (declaring the validation "out of scope" and pushing it to a manager-review step). Both outcomes are bad. By the end of Part 2, you'll know exactly how to do it right.</p>
</div>

<h3>Where TER fits in OTL's processing chain</h3>

<p>Before we get into the formula's internals, it helps to know where TER sits in OTL's bigger picture. When a worker hits Submit on their timecard, OTL runs through a sequence of stages — and TER is just one of them. Understanding the sequence tells you why TER receives the data it does, and why your validation logic belongs here and not somewhere else.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-1/diagram-2.png" alt="Diagram 2: Oracle Fast Formula: Time Entry Rule (Part 1)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>The pipeline is sequential and the failure paths are unforgiving. If built-in validations reject the data, your TER never even runs — the timecard bounces back to the worker before reaching Stage 2. If your TER returns errors, the timecard bounces back at Stage 2, before Stages 3 and 4 ever execute. Only when every stage passes does the data land in the time repository where payroll can pick it up.</p>

<p>This sequencing has practical consequences for what your TER should and shouldn't try to do:</p>

<ul>
<li><strong>Don't reimplement Stage 1.</strong> Built-in validations already check that required fields are filled and types are correct. Your TER will never see malformed data, so don't waste code defending against it. Trust the framework.</li>
<li><strong>Don't try to do Stage 3's job.</strong> Calculations like overtime, shift premiums, and allowances belong in TCR formulas, not TER. TER's job is "is this data valid?" — not "what should we pay them?"</li>
<li><strong>Don't push Stage 2 logic into Stage 4.</strong> If a rule has a clear yes/no answer, validate it here. Sending every borderline case to a manager for sign-off creates an approval bottleneck that becomes the team's full-time job.</li>
</ul>

<p>TER is the right home for everything in our five-rule list above — cross-row, calendar-aware, stateful checks with deterministic answers. With that placement clear, let's look at what an actual problem timecard looks like.</p>

<!-- A REAL WORLD EXAMPLE -->
<h2>A Real World Example</h2>

<p>The fastest way to understand what a TER formula actually does is to watch one fail a timecard. Abstract talk about "validation rules" and "stateful checks" doesn't stick; a real broken submission does. Let me introduce you to Sarah, a software engineer at a product company. Her workday is scheduled 9:00 AM to 6:00 PM, and her employer has one labour-policy rule worth knowing: <strong>no worker may log more than 6 hours of continuous Regular Hours without a meal break in between</strong>.</p>

<p>Tuesday is a deadline day. Sarah gets pulled into a code review at 10 AM and forgets to take lunch. By 6:15 PM she sits down to fill in her timecard, looks at the half-finished entries she made earlier, decides the rows look "messy," and tries to fix things by adding one big block covering the whole day. Then she clicks Submit.</p>

<p>This is what her timecard looks like at the moment of submission — four rows in OTL's grid, exactly as the framework will hand them to your formula:</p>

<div class="excel-wrap">
<div class="excel-titlebar">
<span class="filename">Sarah_Timecard_14Apr2026.xlsx</span>
<span class="app">Excel</span>
</div>
<table class="excel-sheet">
<thead>
<tr>
<th style="min-width:36px; white-space:nowrap; background:#e8e8e8; color:#555;"> </th>
<th>Date</th>
<th>Time Type</th>
<th>Start Time</th>
<th>Stop Time</th>
<th>Hours</th>
<th>What the formula does</th>
</tr>
</thead>
<tbody>
<tr class="row-clean">
<td class="row-num">1</td>
<td>14-Apr-2026</td>
<td>Regular Hours</td>
<td class="time-cell">08:30</td>
<td class="time-cell">10:00</td>
<td class="num">1.5</td>
<td class="status-cell">✓ Clean — no flag</td>
</tr>
<tr class="row-flagged">
<td class="row-num">2</td>
<td>14-Apr-2026</td>
<td>Regular Hours</td>
<td class="time-cell">10:00</td>
<td class="time-cell">14:45</td>
<td class="num">4.75</td>
<td class="status-cell">✗ Continuous work over 6 hours</td>
</tr>
<tr class="row-flagged">
<td class="row-num">3</td>
<td>14-Apr-2026</td>
<td>Meal Break</td>
<td class="time-cell">19:00</td>
<td class="time-cell">20:00</td>
<td class="num">1.0</td>
<td class="status-cell">✗ Break outside working hours</td>
</tr>
<tr class="row-flagged">
<td class="row-num">4</td>
<td>14-Apr-2026</td>
<td>Regular Hours</td>
<td class="time-cell">08:00</td>
<td class="time-cell">20:00</td>
<td class="num">12.0</td>
<td class="status-cell">✗ Overlapping entries</td>
</tr>
</tbody>
</table>
</div>
<div class="excel-caption">Sarah's submission — one clean row, three problem rows. Before reading the analysis below, take a moment to spot the three errors yourself. They're all visible if you know what to look for.</div>

<h3>The day, drawn on a timeline</h3>

<p>Tables are good for precise data; timelines are better for understanding the <em>shape</em> of a day. Here's Sarah's same four rows plotted against the actual hours of Tuesday, 14 April. The schedule window (9 AM to 6 PM, in pale orange) shows when she was supposed to be working. Each row from the timecard sits as a coloured bar where she logged it:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-1/diagram-3.png" alt="Diagram 3: Oracle Fast Formula: Time Entry Rule (Part 1)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>The picture makes the violations visible at a glance:</p>

<ul>
<li><strong>Rows 1 and 2 touch.</strong> Row 1 ends at 10:00 and row 2 starts at 10:00 — no gap. From the formula's perspective this is a single 6h 15m stretch of continuous work, sitting clearly above the 6-hour cap.</li>
<li><strong>Row 3 sits outside the schedule window.</strong> The shaded amber band shows where Sarah was scheduled to work (9 AM to 6 PM). Her meal break at 19:00–20:00 falls a full hour past the schedule's edge. Whatever she was doing then, it wasn't a workplace meal break.</li>
<li><strong>Row 4 covers the entire day in one massive bar.</strong> You can see it physically overlap with rows 1, 2, and 3 simultaneously. This is the consolidated entry Sarah added without removing the originals — three overlap conflicts in a single row.</li>
</ul>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Practitioner's tip</div>
When I'm sketching out a TER's behaviour for a client, I always start with a timeline like this one. Tables hide temporal relationships; timelines surface them. If you're explaining to a non-technical stakeholder why their data is producing strange results, draw a timeline. Five minutes of pen-and-paper sketching will save you an hour of meeting time.
</div>

<h4>The same data as a row-by-hour grid</h4>

<p>The timeline above shows <em>where</em> the entries sit. The grid below shows <em>how each entry occupies hours</em> — one row per timecard entry, one column per hour. Cells light up where the entry is active. The cell numbers count consecutive hours within each entry, so you can see at a glance when an entry crosses a threshold.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04); overflow-x:auto;">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-1/diagram-4.png" alt="Diagram 4: Oracle Fast Formula: Time Entry Rule (Part 1)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>The grid view makes two things obvious that the timeline doesn't. <strong>First,</strong> the 6-hour cap breach in Row 2 is visible as soon as the cumulative-hour counter passes 6 — you can <em>see</em> the exact cell where the rule fires. <strong>Second,</strong> Row 4's overlap problem is undeniable: its row of red cells sits directly below the same hour-columns occupied by rows 1, 2, and 3. The timeline shows the same data; the grid surfaces the relationships between rows in a way bars stacked vertically can't.</p>

<h3>What the formula does, row by row</h3>

<p>Now we trace the algorithm's response. When Sarah hits Submit, OTL packages her four rows into the input arrays we'll dissect later in this post and hands them to your TER formula. The formula walks the rows one at a time, applies its checks, and decides what to flag:</p>

<p><strong>Row 1 (Regular Hours, 08:30–10:00).</strong> The first real entry. The formula starts a "continuous work" tracker at 8:30, with the stretch currently at 1.5 hours — well below any threshold. Nothing to flag.</p>

<p><strong>Row 2 (Regular Hours, 10:00–14:45).</strong> The formula looks at this row's start time and sees it matches the previous row's stop time exactly. That's not "two separate work blocks" — that's <em>continuation of the same block</em>. The tracker extends the stretch from 8:30 to 14:45, which totals 6 hours and 15 minutes. The continuous-work cap is 6 hours. The formula flags row 2: <em>"Continuous work exceeds 6 hours."</em></p>

<p><strong>Row 3 (Meal Break, 19:00–20:00).</strong> The formula checks every meal break against the schedule window. Sarah's schedule is 09:00 to 18:00. Her meal at 19:00–20:00 falls outside that window. Row 3 flagged: <em>"Break outside working hours."</em></p>

<p><strong>Row 4 (Regular Hours, 08:00–20:00).</strong> At every day boundary, the formula compares each Regular Hours entry against every other one to detect overlapping intervals. Row 4 spans 08:00–20:00, which contains row 1's interval, row 2's interval, and row 3's interval. Three overlaps. Row 4 flagged: <em>"Overlapping entries."</em></p>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Expert insight</div>
Notice that the formula always flags the <em>later</em> row in any conflict. Row 1 is clean even though row 4 collides with it — because row 1 was already there when row 4 was added. This matches Sarah's mental model: <em>the entry I just added is the one that's wrong</em>. Flagging row 1 instead would turn a previously-correct entry red, which is profoundly confusing for the worker. It's a small UX choice that reflects a deep understanding of how people use timecard software.
</div>

<h3>What Sarah sees on screen</h3>

<p>The formula's output is a single sparse array called <code>OUT_MSG</code>, indexed by row number. Most slots stay empty — those rows passed every check. The flagged rows have error message strings in their slots:</p>

<div class="code-wrap">
<div class="code-header"><span>Formula return · sparse output array</span><span class="label-right">OUT_MSG</span></div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="cm">/* Row 1 has no entry — it's clean. */</span>
<span class="v">OUT_MSG[2]</span> = <span class="s">"Continuous work exceeds 6 hours"</span>
<span class="v">OUT_MSG[3]</span> = <span class="s">"Break outside working hours"</span>
<span class="v">OUT_MSG[4]</span> = <span class="s">"Overlapping entries"</span></code></pre>
</div>

<p>The OTL framework reads this array, walks it, and renders red error markers next to rows 2, 3, and 4 in Sarah's timecard screen. Row 1 has no marker because its slot is empty. Sarah now sees clearly which entries are wrong and what each problem is.</p>

<p>She fixes them — deletes row 4 entirely, moves the meal break to a real lunch slot like 12:00–13:00, and breaks up the long stretch by inserting that meal break. Then she resubmits. The formula re-runs from scratch on the corrected timecard. This time, every row passes. The submission goes through to approval, and on to payroll.</p>

<p>That's the entire job of a TER formula in one example: <strong>catch problems early, tell the worker exactly what's wrong, let them fix it before bad data lands in payroll</strong>. Now we'll look at how the formula actually does this internally, starting with the most important thing: the data shape it works with.</p>

<!-- ARRAY CONTRACT -->



<!-- NEXT IN SERIES -->
<div style="background:#fff8e8; border:1px solid #b97417; border-radius:6px; padding:20px 24px; margin:40px 0 32px 0;">
<div style="font-size:10px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Next in The TER Series</div>
<div style="font-size:18px; font-weight:700; color:#2d2926; margin-bottom:8px;">Part 2 — The Input Contract</div>
<div style="font-size:13.5px; color:#5a544e; line-height:1.6;">OTL doesn't hand your formula a timecard object. It hands you six parallel arrays with shared row indexes, plus a strict contract about what goes in and what must come out. Part 2 dissects the data shape, every input variable, and the naming conventions that keep production TER code maintainable.</div>
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