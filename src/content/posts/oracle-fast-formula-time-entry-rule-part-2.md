---
title: "Oracle Fast Formula: Time Entry Rule (Part 2)"
pubDate: 2026-05-22
description: "Oracle Fast Formula: Time Entry Rule (Part 2)"
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

<div style="font-size:13px; color:#7a7570; margin-bottom:18px;">May 21, 2026 • 15 min read • Oracle HCM Cloud</div>

<!-- SERIES BREADCRUMB -->
<div style="background:#f5f1e8; border-left:3px solid #b97417; padding:10px 14px; margin-bottom:24px; border-radius:0 3px 3px 0; font-size:12px;">
<span style="font-weight:700; color:#b97417; letter-spacing:0.5px; text-transform:uppercase; font-size:10px;">The TER Series</span>
<span style="color:#5a544e; margin-left:8px;">Part 2 of 4</span>
<div style="margin-top:6px; color:#7a7570; font-size:11.5px; line-height:1.5;">
1. OTL Foundations ·
2. The Input Contract ·
3. Algorithm: Routing & Overlap ·
4. The State Machine
</div>
</div>

<h1>The Input Contract: How OTL Hands Data to Your Formula<br><span style="color:#7a7570; font-size:0.7em; font-weight:400; font-style:italic;">Part 2 of 4 — The TER Series</span></h1>

<div class="byline">
<div class="avatar">AM</div>
<div class="author-block">
<div class="author-name">Abhishek Mohanty</div>
<div class="author-creds">Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead</div>
</div>
</div>

<div class="opening">In Part 1 we saw what TER does and where it fits in OTL's submission flow. Now we look at the data the framework hands your formula — the input array contract, the seven input variables, and the naming conventions that keep production code readable.</div>

<h2>The Input Array Contract</h2>

<p>Here's the single most important thing to internalise before you write any code: <strong>the timecard the worker sees is not the timecard your formula receives</strong>. OTL inserts extra rows between the worker's entries to mark structural boundaries — where each day starts, where it ends, where the whole period closes out. Miss this distinction and your loop counter, your day-buffer logic, and your <code>.exists()</code> guards will all be subtly wrong. Get it right, and the rest of the formula falls into place naturally.</p>

<p>I'll show you both views, then a transformation diagram that bridges them, then the formal contract.</p>

<h3>The view the worker sees</h3>

<p>When Sarah opens her timecard, she's looking at a spreadsheet-like grid. She types entries one row at a time. Here's what her week looks like after she's done entering Tuesday and Wednesday:</p>

<div class="excel-wrap">
<div class="excel-titlebar">
<span class="filename">My_Timecard_Week_14Apr2026.xlsx</span>
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
</tr>
</thead>
<tbody>
<tr>
<td class="row-num">1</td>
<td>14-Apr-2026 (Tue)</td>
<td>Regular Hours</td>
<td class="time-cell">09:00</td>
<td class="time-cell">12:00</td>
<td class="num">3.0</td>
</tr>
<tr>
<td class="row-num">2</td>
<td>14-Apr-2026 (Tue)</td>
<td>Meal Break</td>
<td class="time-cell">12:00</td>
<td class="time-cell">13:00</td>
<td class="num">1.0</td>
</tr>
<tr>
<td class="row-num">3</td>
<td>14-Apr-2026 (Tue)</td>
<td>Regular Hours</td>
<td class="time-cell">13:00</td>
<td class="time-cell">18:00</td>
<td class="num">5.0</td>
</tr>
<tr>
<td class="row-num">4</td>
<td>15-Apr-2026 (Wed)</td>
<td>Regular Hours</td>
<td class="time-cell">09:00</td>
<td class="time-cell">18:00</td>
<td class="num">8.0</td>
</tr>
</tbody>
</table>
</div>
<div class="excel-caption">Four entries across two days — this is exactly what Sarah types into OTL. Clean, simple, no surprises.</div>

<h3>What OTL does between submission and your formula</h3>

<p>The moment Sarah hits Submit, OTL's pre-processor wakes up. It can't just hand the formula four rows of data — the formula needs to know where day boundaries fall, where the period ends, and where to pause for day-level processing like overlap detection. So OTL inserts <strong>marker rows</strong> at the structural breakpoints. The diagram below shows exactly what changes:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-1.png" alt="Diagram 1: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>Three things to take away from this diagram:</p>

<ul>
<li><strong>HEADER always sits at index [1].</strong> Your loop counter starts at 1, but you'll never read real worker data at that index. The first real entry begins at [2].</li>
<li><strong>END_DAY appears wherever a calendar day ends.</strong> If the timecard period covers seven days, expect seven END_DAY markers (one for each day, even if some days have zero worker entries).</li>
<li><strong>END_PERIOD always sits at the very last index.</strong> When your formula's loop sees END_PERIOD, you're done.</li>
</ul>

<p>Here's the same eight-row view as a table, with the original column names OTL uses:</p>

<h3>The view the formula sees, as a table</h3>

<div class="excel-wrap">
<div class="excel-titlebar">
<span class="filename">As_The_Formula_Sees_It.xlsx</span>
<span class="app">Excel</span>
</div>
<table class="excel-sheet">
<thead>
<tr>
<th style="min-width:36px; white-space:nowrap; background:#e8e8e8; color:#555;">Idx</th>
<th>Record Position</th>
<th>Time Type</th>
<th>Start Time</th>
<th>Stop Time</th>
<th>Hours</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff3e0;">
<td class="row-num" style="background:#ffd180;">[1]</td>
<td><strong>HEADER</strong></td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
</tr>
<tr>
<td class="row-num">[2]</td>
<td style="color:#999;">—</td>
<td>Regular Hours</td>
<td class="time-cell">09:00</td>
<td class="time-cell">12:00</td>
<td class="num">3.0</td>
</tr>
<tr>
<td class="row-num">[3]</td>
<td style="color:#999;">—</td>
<td>Meal Break</td>
<td class="time-cell">12:00</td>
<td class="time-cell">13:00</td>
<td class="num">1.0</td>
</tr>
<tr>
<td class="row-num">[4]</td>
<td style="color:#999;">—</td>
<td>Regular Hours</td>
<td class="time-cell">13:00</td>
<td class="time-cell">18:00</td>
<td class="num">5.0</td>
</tr>
<tr style="background:#fce8e8;">
<td class="row-num" style="background:#f5cccc;">[5]</td>
<td style="color:#c0392b;"><strong>END_DAY</strong></td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
</tr>
<tr>
<td class="row-num">[6]</td>
<td style="color:#999;">—</td>
<td>Regular Hours</td>
<td class="time-cell">09:00</td>
<td class="time-cell">18:00</td>
<td class="num">8.0</td>
</tr>
<tr style="background:#fce8e8;">
<td class="row-num" style="background:#f5cccc;">[7]</td>
<td style="color:#c0392b;"><strong>END_DAY</strong></td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
</tr>
<tr style="background:#fce8e8;">
<td class="row-num" style="background:#f5cccc;">[8]</td>
<td style="color:#c0392b;"><strong>END_PERIOD</strong></td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
</tr>
</tbody>
</table>
</div>
<div class="excel-caption">Same four entries, now wrapped with HEADER, END_DAY, and END_PERIOD marker rows. Notice the dashes — marker rows have no time-type, no punches, no hours. Trying to read those slots will crash your formula.</div>

<h3>How the formula reads it — three questions per row</h3>

<p>For every index from [1] to [N], your formula asks the same three questions in order. The answers determine the entire flow of validation logic:</p>

<p><strong>Question 1: Is this a marker row?</strong> Read <code>RECORD_POSITIONS[idx]</code>. If it's HEADER, skip everything; if it's END_DAY, run day-level checks (overlap detection, day buffer reset); if it's END_PERIOD, the loop ends; if it's empty, this is a real worker entry — proceed to Question 2.</p>

<p><strong>Question 2: What kind of time type?</strong> Read <code>PayrollTimeType[idx]</code>. Regular Hours go through the continuous-work tracker and the day buffer for overlap testing. Meal Break runs through the schedule-window check and signals "the worker took a break." Other types (Annual Leave, Sick Leave) typically pass through with no validation.</p>

<p><strong>Question 3: What are the exact punch times?</strong> Read <code>StartTime[idx]</code> and <code>StopTime[idx]</code>. Use them for stretch tracking, overlap math, qty-only detection, and any time-window checks.</p>

<div style="background:#fff5f0; border-left:4px solid #c0392b; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#c0392b; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Production trap</div>
Marker rows are why you can't read input arrays directly. <code>StartTime[1]</code> doesn't exist as a value — HEADER rows have no punch time. Read it without protection and Fast Formula throws a runtime error and crashes the whole submission. Every read in the formula must be wrapped in <code>.exists()</code>:
<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; margin-top:10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:11px;">
IF (StartTime.exists(nidx)) THEN ( aiStartTime = StartTime[nidx] )
</div>
Skip this guard and the formula passes UAT cleanly — test data rarely covers the edge case — then breaks day one in production when a real submission arrives. <strong>This is the single most common reason a TER formula goes live and immediately blocks every submission</strong>. Don't be that consultant.
</div>

<h3>The Formula's Contract: What Goes In, What Comes Out</h3>

<p class="section-lead">A Time Entry Rule formula is like a checkpoint at the airport. The OTL framework hands it a stack of paperwork (the timecard rows), the formula inspects every page, and hands back a list of which pages have problems. The framework defines exactly what shape that paperwork arrives in and exactly what shape the response must take — that's the <strong>contract</strong>. Neither side can deviate.</p>

<div class="excel-wrap">
<div class="excel-titlebar">
<span class="filename">The_Contract_at_a_Glance.xlsx</span>
<span class="app">Excel</span>
</div>
<table class="excel-sheet">
<thead>
<tr>
<th>Direction</th>
<th>Variable</th>
<th>Type</th>
<th>What it represents</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong style="color:#4472c4;">IN</strong></td>
<td><code>HWM_CTXARY_RECORD_POSITIONS</code></td>
<td>Text array</td>
<td>Which rows are markers (HEADER, END_DAY) vs real entries</td>
</tr>
<tr style="opacity:0.6;">
<td><strong style="color:#4472c4;">IN</strong></td>
<td><code>HWM_CTXARY_HWM_MEASURE_DAY</code></td>
<td>Number array</td>
<td>Day-aggregated total (declared but unused by this formula)</td>
</tr>
<tr>
<td><strong style="color:#4472c4;">IN</strong></td>
<td><code>measure</code></td>
<td>Number array</td>
<td>Hours value for each row</td>
</tr>
<tr>
<td><strong style="color:#4472c4;">IN</strong></td>
<td><code>PayrollTimeType</code></td>
<td>Text array</td>
<td>What kind of time (Regular Hours, Meal Break, Annual Leave...)</td>
</tr>
<tr>
<td><strong style="color:#4472c4;">IN</strong></td>
<td><code>StartTime</code></td>
<td>Date array</td>
<td>Punch-in timestamp for each row</td>
</tr>
<tr>
<td><strong style="color:#4472c4;">IN</strong></td>
<td><code>StopTime</code></td>
<td>Date array</td>
<td>Punch-out timestamp for each row</td>
</tr>
<tr style="background:#fce8e8;">
<td><strong style="color:#c0392b;">OUT</strong></td>
<td><code>OUT_MSG</code></td>
<td>Text array (sparse)</td>
<td>Error message for each flagged row, empty for clean rows</td>
</tr>
</tbody>
</table>
</div>
<div class="excel-caption">Six inputs in. One output out. The framework enforces these names exactly — misspell one, omit one, return anything else, and the formula won't even compile.</div>

<h4>Three things to understand before reading further</h4>

<p>Before walking through each input one by one, hold these three properties in mind. Every line of code in this formula respects all three; understanding them now means the source reads naturally later.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:18px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram · The three properties of the input/output shape</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-2.png" alt="Diagram 2: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<p><strong>1. The inputs are parallel arrays, not records.</strong> Most languages would express a row of timecard data as a single object with named fields: <code>{type, start, stop, hours}</code>. Fast Formula doesn't have records like that. Instead, the framework gives the formula six separate arrays, all sharing the same row index. Row 3 of the timecard is <code>RECORD_POSITIONS[3]</code>, <code>StartTime[3]</code>, <code>StopTime[3]</code>, <code>PayrollTimeType[3]</code>, and <code>measure[3]</code>, each holding one column of that row's data. To work with a single row, you read the same index across all six arrays.</p>

<p><strong>2. Not every row populates every column.</strong> Marker rows (HEADER, END_DAY, END_PERIOD) only fill <code>RECORD_POSITIONS</code> — the other arrays have no slot at those indexes. Trying to read <code>StartTime[1]</code> on a HEADER row would crash. This is why every read in the formula is wrapped in <code>.exists(nidx)</code> — the formula has to check whether a slot is populated before reading from it.</p>

<p><strong>3. The output is sparse, not dense.</strong> <code>OUT_MSG</code> doesn't have one entry per timecard row — it only has entries for the rows the formula chose to flag. A clean row leaves its slot empty. The framework reads <code>OUT_MSG</code> when the formula returns and renders red error markers next to whatever row indexes appear in the array. Quiet rows stay quiet.</p>

<h4>The expert's view: framing the inputs before reading the names</h4>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:18px 22px; margin:24px 0; font-size:14px; line-height:1.7; color:#2d2926; border-radius:0 4px 4px 0;">
<div style="font-size:10px; letter-spacing:1.8px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Expert framing</div>
<p style="margin-top:0;">When I'm reviewing a junior developer's first TER formula, the question I always hear is: <em>"Why are some inputs called <code>HWM_CTXARY_RECORD_POSITIONS</code> and others just <code>StartTime</code>?"</em> The answer isn't really about names — it's about <strong>what kind of data each input represents</strong>, and Oracle's naming conventions reflect that distinction once you see the pattern.</p>
<p style="margin-bottom:0;">Fast Formula isn't a general-purpose programming language. It's a <strong>rule engine plugged into specific HCM modules</strong>. Each module (Payroll, Absence, Time and Labor, Benefits) defines its own <em>formula types</em>, and each formula type is a contract: <em>"If you write a formula of this type, you'll receive these inputs and you must return these outputs."</em> The TER formula type is one such contract, defined inside OTL. The six inputs we're about to dissect aren't arbitrary — they're exactly what OTL's validation pipeline hands every TER formula by design.</p>
</div>

<h4>How a TER formula fits into OTL's bigger picture</h4>

<p>To understand the inputs, you first need to see where the formula fires within OTL. A TER formula doesn't run in isolation — it sits inside a five-stage pipeline that begins the moment a worker clicks Submit on their timecard:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-3.png" alt="Diagram 3: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>Stage 3 is where your formula has agency. Stages 1, 2, 4, and 5 belong to OTL. The contract you're working against is: <em>OTL gives you six well-defined arrays; you give back one well-defined array; everything else is your business logic.</em></p>

<h4>Decoding the input names — what each part means</h4>

<p>Now that we know <em>where</em> the inputs come from, let's decode <em>why they're named the way they are</em>. Oracle's naming is structural, not arbitrary. Every prefix carries meaning. Here's the breakdown:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-4.png" alt="Diagram 4: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>Once you see this split, the naming makes sense. The <code>HWM_CTXARY_</code> prefix is Oracle saying <em>"this input is structural metadata that the framework needs to manage the iteration."</em> The short names (<code>measure</code>, <code>PayrollTimeType</code>, <code>StartTime</code>, <code>StopTime</code>) are saying <em>"this input is the worker's actual time data, the same names we've used since the OTL was first designed."</em></p>

<div style="background:#fff5f0; border-left:4px solid #c0392b; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#c0392b; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Expert insight</div>
You'll see this same <code>HWM_</code> prefix convention across other OTL formula types too — calculation rules, time-calculation formulas, time-card validation formulas. Once you internalise that <code>HWM_</code> means "framework-supplied" and <code>HWM_CTXARY_</code> means "framework-supplied per-row metadata", you can read any OTL formula and immediately know which variables come from the framework versus which ones the author created. <strong>This pattern recognition is what separates a fluent OTL developer from someone still puzzling over the syntax.</strong>
</div>

<h4>How to read one timecard row from the parallel arrays</h4>

<p>Now the practical part. Inside the formula's loop, each iteration processes one row. To get all the data for that row, you read all six arrays at the same index. Here's a visual showing how the parallel arrays line up:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-5.png" alt="Diagram 5: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>Six arrays, six reads, one row reconstructed. The formula's WHILE loop does this on every iteration, walking the index from 1 to N (where N is the total row count returned by <code>HWM_CTXARY_RECORD_POSITIONS.count</code>). On marker rows like [1] and [4], several of the reads return empty — which is why each read in the formula is wrapped in a <code>.exists()</code> guard.</p>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Practitioner's tip</div>
When debugging a TER formula in production, the first thing I check is the <code>HWM_CTXARY_RECORD_POSITIONS</code> array length. If <code>.count = 0</code>, the formula received nothing to validate — the bug is upstream in the OTL configuration, not in your formula logic. If <code>.count</code> is non-zero but no validations fire, your loop counter or your <code>.exists()</code> guards are wrong. <strong>Always log <code>.count</code> at the top of the formula via <code>add_rlog</code></strong> — it'll save you hours of guessing.
</div>

<h4>Now: each input in detail</h4>

<p>With the framing in place — how the formula fits in OTL's pipeline, what the names mean, how parallel access works — the cards below cover all six inputs (plus the <code>OUT_MSG</code> output) one by one. Each card shows what kind of values the input holds, the actual formula code that reads it, and what the formula does with the value.</p>



<!-- Input 1: RECORD_POSITIONS -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Input 01 · Text Array</div>
<div class="ic-name">HWM_CTXARY_RECORD_POSITIONS</div>
</div>
<div class="ic-question">"What kind of row is this?"</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>RECORD_POSITIONS_examples.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Possible value</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td class="empty">(empty)</td><td>Real worker entry — check the data columns</td></tr>
<tr><td><strong>HEADER</strong></td><td>System marker at the top of the timecard</td></tr>
<tr><td><strong>END_DAY</strong></td><td>System marker at the end of each day — trigger day-level work</td></tr>
<tr><td><strong>END_PERIOD</strong></td><td>System marker at the end of the whole timecard period</td></tr>
</tbody>
</table>
</div>
<div class="ic-mini-excel-cap">Four possible values. Empty means real data; non-empty is a system-inserted marker telling the formula something about structure.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · Where each marker value appears in the array</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-6.png" alt="Diagram 6: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="c">/* read the marker for this index */</span>
<span class="k">IF</span> (<span class="v">HWM_CTXARY_RECORD_POSITIONS</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
<span class="v">aiRecPos</span> <span class="op">=</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>[<span class="v">nidx</span>]

<span class="c">/* branch on what kind of row this is */</span>
<span class="k">IF</span> (<span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_DAY'</span>
<span class="k">OR</span> <span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_PERIOD'</span>) <span class="k">THEN</span>
<span class="c">/* run pairwise overlap, reset day buffer */</span></div>
<div class="ic-explain">Empty value at this index → real worker entry, so the formula reads the data columns. Non-empty (HEADER, END_DAY, END_PERIOD) → system marker, so skip the data columns and trigger boundary logic if applicable. <strong>This is the first thing the formula reads every iteration</strong> — it decides everything else.</div>
</div>

<!-- Input 2: HWM_MEASURE_DAY (reserved, declared but unused) -->
<div class="input-card reserved">
<div class="ic-head">
<div class="ic-eyebrow">Input 02 · Number Array · Reserved</div>
<div class="ic-name">HWM_CTXARY_HWM_MEASURE_DAY</div>
</div>
<div class="ic-question">"Is this input actually used?" — <strong>No, but it must be declared.</strong></div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · The "declared but unused" pattern</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-7.png" alt="Diagram 7: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="ic-explain">
<p style="margin-top:0;">This input would hold day-level totals if the formula needed them. The framework hands it over because the TER formula type's contract requires it — <strong>but this particular formula never reads it</strong>. Three things to know:</p>
<ul style="margin:8px 0 0 0; padding-left:22px;">
<li><strong>You must declare it</strong> in the <code>INPUTS ARE</code> statement, otherwise the framework throws a binding error and the formula won't even start.</li>
<li><strong>You don't read from it.</strong> The validations work entirely off per-row punches (<code>StartTime</code>, <code>StopTime</code>) and per-row <code>measure</code>, never from day-level aggregates.</li>
<li><strong>You can ignore it from here on.</strong> It plays no role in any of Block 6, 7, or 8. A different formula type (like a calculation rule) might consume it; this one simply lists it and moves on.</li>
</ul>
</div>
</div>

<!-- Input 3: measure -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Input 03 · Number Array</div>
<div class="ic-name">measure</div>
</div>
<div class="ic-question">"How many hours on this row?"</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>measure_examples.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Sample value</th><th>What it represents</th></tr></thead>
<tbody>
<tr><td class="tc">2.5</td><td>2 hours 30 minutes — real punch interval</td></tr>
<tr><td class="tc">8.0</td><td>8 hours — could be real or a qty-only placeholder</td></tr>
<tr><td class="tc">0.5</td><td>30 minutes — short break or partial shift</td></tr>
<tr><td class="empty">(no value)</td><td>Marker rows have no <code>measure</code> — not applicable</td></tr>
</tbody>
</table>
</div>
<div class="ic-mini-excel-cap">Always a number when present. The same value can come from real punches or from a qty-only placeholder — <code>measure</code> alone can't tell which.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · Real punches vs qty-only — same measure, different intent</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-8.png" alt="Diagram 8: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="c">/* per-line measure, used for qty-only entries */</span>
<span class="k">IF</span> (<span class="v">measure</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
<span class="v">aiMeasure</span> <span class="op">=</span> <span class="v">measure</span>[<span class="v">nidx</span>]</div>
<div class="ic-explain"><strong>The formula uses this mainly for qty-only detection.</strong> If a worker types just "8 hours" without entering punch times, OTL fills <code>StartTime</code> as <code>00:00</code> and <code>StopTime</code> as <code>23:59</code> — the <code>measure</code> tells you the real intended hours (8) without needing to compute it from the placeholder punches. When the punches are genuine, <code>measure</code> simply equals <code>StopTime − StartTime</code> in hours, and the formula uses the punches directly anyway.</div>
</div>

<!-- Input 4: PayrollTimeType -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Input 04 · Text Array · Routing Key</div>
<div class="ic-name">PayrollTimeType</div>
</div>
<div class="ic-question">"What kind of time?"</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>PayrollTimeType_routes.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Time type value</th><th>Where the formula sends it</th></tr></thead>
<tbody>
<tr class="row-pass"><td>Regular Hours</td><td class="tag">Stretch tracker + Day buffer for overlap</td></tr>
<tr><td>Meal Break</td><td style="color:#b97417;">Schedule-window check + Reset stretch</td></tr>
<tr><td>Annual Leave</td><td style="color:#7a7570;">Skipped — no validation path</td></tr>
<tr><td>Sick Leave</td><td style="color:#7a7570;">Skipped — no validation path</td></tr>
<tr><td>Public Holiday</td><td style="color:#7a7570;">Skipped — no validation path</td></tr>
</tbody>
</table>
</div>
<div class="ic-mini-excel-cap">The string value drives the entire routing decision. Reg Hours and Meal Break have validation paths; everything else falls through silently.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · Time-type values fan out to validation paths</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-9.png" alt="Diagram 9: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="c">/* read the type, then route */</span>
<span class="k">IF</span> (<span class="v">PayrollTimeType</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">PayrollTimeType</span>[<span class="v">nidx</span>]

<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span>) <span class="k">THEN</span>
<span class="c">/* → stretch tracker + day buffer */</span>

<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_break_type</span>) <span class="k">THEN</span>
<span class="c">/* → schedule window + reset stretch */</span></div>
<div class="ic-explain">The most important routing decision in the formula. Reg Hours go into the continuous-stretch tracker and the day buffer for overlap testing. Meal Break runs through the schedule-window check and resets the stretch tracker. Other types (Annual Leave, Sick, etc) silently skip both paths.</div>
</div>

<!-- Input 5: StartTime -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Input 05 · Date Array</div>
<div class="ic-name">StartTime</div>
</div>
<div class="ic-question">"When did this row begin?"</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>StartTime_uses.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Used in</th><th>What for</th></tr></thead>
<tbody>
<tr><td>Stretch tracker</td><td>Compared to previous stretchEnd → decide EXTEND or RESTART</td></tr>
<tr><td>Pairwise overlap test</td><td>Combined with StopTime to define each row's interval</td></tr>
<tr><td>Schedule window check</td><td>Compared to <code>p_sched_start</code> for Meal Break entries</td></tr>
<tr><td>Qty-only detection</td><td>If start < 0.01 (near midnight), entry is a placeholder</td></tr>
</tbody>
</table>
</div>
<div class="ic-mini-excel-cap">A single date value, but it feeds four different validation paths depending on the time type.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · StartTime feeds four validation paths</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-10.png" alt="Diagram 10: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="k">IF</span> (<span class="v">StartTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">StartTime</span>[<span class="v">nidx</span>]

<span class="c">/* used in EXTEND vs RESTART decision */</span>
<span class="k">IF</span> (<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">stretchEnd</span>) <span class="k">THEN</span>
<span class="v">stretchEnd</span> <span class="op">=</span> <span class="v">aiStopTime</span>      <span class="c">// EXTEND</span>
<span class="k">ELSE</span>
<span class="v">stretchStart</span> <span class="op">=</span> <span class="v">aiStartTime</span>  <span class="c">// RESTART</span>

<span class="c">/* and in pairwise overlap test */</span>
<span class="k">IF</span> (<span class="v">dayStarts</span>[<span class="v">i</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">j</span>]
<span class="k">AND</span> <span class="v">dayStarts</span>[<span class="v">j</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">i</span>]) <span class="k">THEN</span></div>
<div class="ic-explain">Two jobs. <strong>Stretch tracking:</strong> compared against the previous stretch's end — if it matches, the worker continued seamlessly (extend); if there's a gap, a new stretch begins (restart). <strong>Overlap detection:</strong> paired with StopTime to define the row's interval; the strict-less-than test catches collisions while allowing back-to-back handovers.</div>
</div>

<!-- Input 6: StopTime -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Input 06 · Date Array</div>
<div class="ic-name">StopTime</div>
</div>
<div class="ic-question">"When did this row end?"</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>StopTime_uses.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Used in</th><th>What for</th></tr></thead>
<tbody>
<tr><td>Stretch tracker</td><td>Becomes the new <code>stretchEnd</code> when extending or restarting</td></tr>
<tr><td>Pairwise overlap test</td><td>Combined with StartTime to define each row's interval</td></tr>
<tr><td>Schedule window check</td><td>Compared to <code>p_sched_end</code> for Meal Break entries</td></tr>
<tr><td>Continuous-hours math</td><td>Feeds the <code>contHrs</code> calculation alongside <code>stretchStart</code></td></tr>
</tbody>
</table>
</div>
<div class="ic-mini-excel-cap">Always partnered with StartTime to define an interval, but it has its own role in the schedule-window check too.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · StopTime — partnered with StartTime, standalone for schedule check</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-11.png" alt="Diagram 11: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="k">IF</span> (<span class="v">StopTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
<span class="v">aiStopTime</span> <span class="op">=</span> <span class="v">StopTime</span>[<span class="v">nidx</span>]

<span class="c">/* schedule window check (Meal Break only) */</span>
<span class="k">IF</span> (<span class="v">aiStopTime</span> <span class="op">></span> <span class="v">p_sched_end</span>) <span class="k">THEN</span>
<span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="s">'Break outside hours'</span>

<span class="c">/* contHrs calculation */</span>
<span class="v">contHrs</span> <span class="op">=</span> (<span class="v">stretchEnd</span> <span class="op">-</span> <span class="v">stretchStart</span>) <span class="op">*</span> <span class="n">24</span></div>
<div class="ic-explain">With StartTime, defines the row's interval for overlap testing. Drives the schedule-window check — if a Meal Break ends after <code>sched_end</code>, the row gets flagged. Also feeds the continuous-hours calculation as the running stretchEnd.</div>
</div>

<div class="phase-divider">↓   FORMULA RUNS   ↓</div>

<!-- Output: OUT_MSG -->
<div class="input-card output">
<div class="ic-head">
<div class="ic-eyebrow">Output · Text Array (Sparse)</div>
<div class="ic-name">OUT_MSG</div>
</div>
<div class="ic-question">"Which rows are bad and why?"</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>OUT_MSG_messages.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Possible message</th><th>Fired by</th></tr></thead>
<tbody>
<tr class="row-pass"><td class="empty">(slot left empty)</td><td class="tag">Clean row — no validation issue</td></tr>
<tr class="row-fail"><td class="msg">"Continuous work exceeds 6 hours"</td><td class="tag">Block 8 (state machine)</td></tr>
<tr class="row-fail"><td class="msg">"Overlapping entries"</td><td class="tag">Block 7 (overlap test)</td></tr>
<tr class="row-fail"><td class="msg">"Break outside working hours"</td><td class="tag">Block 6e (schedule window)</td></tr>
<tr class="row-fail"><td class="msg">"RegHours start/stop required"</td><td class="tag">Block 6c (hard requirement)</td></tr>
</tbody>
</table>
</div>
<div class="ic-mini-excel-cap">Sparse array indexed by row number. The framework reads each populated slot and renders a red error marker next to that row in the timecard UI; empty slots stay clean.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · Sparse output — only flagged rows have entries</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-12.png" alt="Diagram 12: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="ic-snippet">
<span class="lbl">How the formula writes it</span><span class="c">/* declared at the top of the loop */</span>
<span class="v">OUT_MSG</span> <span class="op">=</span> <span class="v">EMPTY_TEXT_NUMBER</span>

<span class="c">/* populated only for flagged rows */</span>
<span class="k">IF</span> (<span class="v">contHrs</span> <span class="op">></span> <span class="v">p_max_cont_err</span>) <span class="k">THEN</span>
<span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>)
<span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_cont_err</span>)

<span class="c">/* returned implicitly at end of formula */</span>
<span class="k">RETURN</span> <span class="v">OUT_MSG</span></div>
<div class="ic-explain"><strong>Mandatory return.</strong> Sparse — only flagged rows have entries; clean rows leave their slot empty. The framework reads the array after the formula finishes and renders red error markers next to those line numbers in the worker's timecard UI.</div>
</div>

<h4>How the Six Inputs Fit Together: Six Columns of One Spreadsheet</h4>

<p>The six inputs aren't independent values — they're <strong>six parallel arrays sharing one index space</strong>. Picture a spreadsheet: each input is a column, and every timecard row occupies the same row index across all six columns at once. Reading all six arrays at index [3] gives the complete picture of one timecard row.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:18px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram · Six arrays, one shared index space</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-13.png" alt="Diagram 13: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="excel-wrap">
<div class="excel-titlebar">
<span class="filename">Six_Arrays_One_Spreadsheet.xlsx</span>
<span class="app">Excel</span>
</div>
<table class="excel-sheet">
<thead>
<tr>
<th style="min-width:36px; white-space:nowrap; background:#e8e8e8; color:#555;">Idx</th>
<th>RECORD_POSITIONS</th>
<th>PayrollTimeType</th>
<th>StartTime</th>
<th>StopTime</th>
<th>measure</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff3e0;">
<td class="row-num" style="background:#ffd180;">[1]</td>
<td><strong>HEADER</strong></td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
</tr>
<tr>
<td class="row-num">[2]</td>
<td style="color:#999;">(empty)</td>
<td>Regular Hours</td>
<td class="time-cell">09:00</td>
<td class="time-cell">12:00</td>
<td class="num">3.0</td>
</tr>
<tr>
<td class="row-num">[3]</td>
<td style="color:#999;">(empty)</td>
<td>Meal Break</td>
<td class="time-cell">12:00</td>
<td class="time-cell">13:00</td>
<td class="num">1.0</td>
</tr>
<tr>
<td class="row-num">[4]</td>
<td style="color:#999;">(empty)</td>
<td>Regular Hours</td>
<td class="time-cell">13:00</td>
<td class="time-cell">17:00</td>
<td class="num">4.0</td>
</tr>
<tr style="background:#fce8e8;">
<td class="row-num" style="background:#f5cccc;">[5]</td>
<td style="color:#c0392b;"><strong>END_DAY</strong></td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
<td style="color:#999;">—</td>
</tr>
</tbody>
</table>
</div>
<div class="excel-caption">A simple one-day timecard. Marker rows ([1] HEADER and [5] END_DAY) only fill the <code>RECORD_POSITIONS</code> column; their other slots are blank. Real worker entries leave RECORD_POSITIONS empty and fill the data columns. The formula reads <code>RECORD_POSITIONS</code> first to decide which path to take.</div>

<p>The formula's WHILE loop walks the index from 1 to N, reading the same index across all six arrays each iteration. There's no concept of a "row object" — each row is reassembled at the moment of reading from the parallel slices. This pattern is consistent across all of OTL's formula types, so once you internalise it once, you'll see it everywhere.</p>

<p>Return anything other than <code>OUT_MSG</code> — an extra variable, a misspelled name — and the OTL submission throws a contract error. Return exactly this and nothing else.</p>

<!-- COMPLETE FORMULA CODE -->
<h2>The Complete Formula</h2>

<p>Here it is in full. Every line in this listing is exactly what gets pasted into <strong>Manage Fast Formulas</strong>. Read it once top-to-bottom — don't try to understand every line yet. We'll walk through it block by block in the next section.</p>

<div class="code-wrap">
<div class="code-header"><span>XX_TER_CONTINUOUS_HOURS_VALIDATION.ff</span><span class="label-right">Time Entry Rule</span></div>
<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="c">/* ============================================================
   Formula Name: XX_TER_CONTINUOUS_HOURS_VALIDATION
   Formula Type: Time Entry Rules
   Description: The Fast formula is required to validate the entry of timecard
                and show error or warning messages if entries are not accurate
                according to the requirements.
   ============================================================ */</span>
<span class="k">DEFAULT FOR</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span> <span class="k">IS</span> <span class="v">EMPTY_TEXT_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">HWM_CTXARY_HWM_MEASURE_DAY</span>  <span class="k">IS</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">HWM_PER_ASG_ASSIGNMENT_ID</span>   <span class="k">IS</span> <span class="n">0</span>
<span class="k">DEFAULT FOR</span> <span class="v">measure</span>         <span class="k">IS</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">PayrollTimeType</span> <span class="k">IS</span> <span class="v">EMPTY_TEXT_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">StartTime</span>       <span class="k">IS</span> <span class="v">EMPTY_DATE_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">StopTime</span>        <span class="k">IS</span> <span class="v">EMPTY_DATE_NUMBER</span>

<span class="k">INPUTS ARE</span>
  <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>,
  <span class="v">HWM_CTXARY_HWM_MEASURE_DAY</span>,
  <span class="v">measure</span>,
  <span class="v">PayrollTimeType</span>,
  <span class="v">StartTime</span>,
  <span class="v">StopTime</span>

<span class="v">ffName</span>  <span class="op">=</span> <span class="s">'XX_TER_CONTINUOUS_HOURS_VALIDATION'</span>
<span class="v">ffs_id</span>  <span class="op">=</span> <span class="f">GET_CONTEXT</span>(<span class="v">HWM_FFS_ID</span>, <span class="n">0</span>)
<span class="v">rule_id</span> <span class="op">=</span> <span class="f">GET_CONTEXT</span>(<span class="v">HWM_RULE_ID</span>, <span class="n">0</span>)

<span class="v">NullDate</span> <span class="op">=</span> <span class="s">'01-JAN-1900'</span> (<span class="k">DATE</span>)
<span class="v">NullText</span> <span class="op">=</span> <span class="s">'**FF_NULL**'</span>

<span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> Enter '</span> <span class="op">||</span> <span class="v">ffName</span>)

<span class="k">CHANGE_CONTEXTS</span>(<span class="v">HR_ASSIGNMENT_ID</span> <span class="op">=</span> <span class="v">HWM_PER_ASG_ASSIGNMENT_ID</span>)
(
  <span class="v">sumLvl</span> <span class="op">=</span> <span class="f">Get_Hdr_Text</span>(<span class="v">rule_id</span>, <span class="s">'RUN_SUMMATION_LEVEL'</span>, <span class="s">'DAY'</span>)
  <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> sumLvl='</span> <span class="op">||</span> <span class="v">sumLvl</span>)

  <span class="v">p_break_type</span> <span class="op">=</span> <span class="s">'Meal Break'</span>
  <span class="v">p_reg_type</span>   <span class="op">=</span> <span class="s">'Regular Hours'</span>

  <span class="v">p_sched_start</span>   <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>, <span class="s">'SCHEDULE_START_HOUR'</span>,     <span class="n">9</span>)
  <span class="v">p_sched_end</span>     <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>, <span class="s">'SCHEDULE_END_HOUR'</span>,      <span class="n">18</span>)
  <span class="v">p_max_cont_err</span>  <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>, <span class="s">'MAX_CONTINUOUS_HRS_ERR'</span>,  <span class="n">6</span>)
  <span class="v">p_max_cont_warn</span> <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>, <span class="s">'MAX_CONTINUOUS_HRS_WARN'</span>, <span class="n">5</span>)

  <span class="v">p_msg_break</span>     <span class="op">=</span> <span class="s">'XX_BREAK_OUTSIDE_HOURS_ERR'</span>
  <span class="v">p_msg_cont_err</span>  <span class="op">=</span> <span class="s">'XX_CONT_HOURS_ERR_MSG'</span>
  <span class="v">p_msg_cont_warn</span> <span class="op">=</span> <span class="s">'XX_CONT_HOURS_WRN_MSG'</span>
  <span class="v">p_msg_overlap</span>   <span class="op">=</span> <span class="s">'XX_OVERLAP_ENTRIES_MSG'</span>
  <span class="v">p_msg_reghrs</span>    <span class="op">=</span> <span class="s">'XX_REG_HOURS_PUNCHES_REQUIRED'</span>

  <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>,
                  <span class="s">'>>> Parms sched='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">p_sched_start</span>) <span class="op">||</span> <span class="s">'-'</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">p_sched_end</span>) <span class="op">||</span>
                  <span class="s">' cErr='</span>  <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">p_max_cont_err</span>) <span class="op">||</span>
                  <span class="s">' cWarn='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">p_max_cont_warn</span>))

  <span class="v">OUT_MSG</span> <span class="op">=</span> <span class="v">EMPTY_TEXT_NUMBER</span>

  <span class="v">wMaAry</span> <span class="op">=</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>.<span class="f">count</span>
  <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> Start bulk wMaAry='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">wMaAry</span>))

  <span class="v">cntr</span> <span class="op">=</span> <span class="n">0</span>
  <span class="v">nidx</span> <span class="op">=</span> <span class="n">0</span>

  <span class="v">dayStarts</span> <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
  <span class="v">dayStops</span>  <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
  <span class="v">dayIdxs</span>   <span class="op">=</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
  <span class="v">dayCnt</span>    <span class="op">=</span> <span class="n">0</span>

  <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">NullDate</span>
  <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">NullDate</span>
  <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'N'</span>

  <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>

  <span class="k">WHILE</span> (<span class="v">cntr</span> <span class="op"><</span> <span class="v">wMaAry</span>) <span class="k">LOOP</span>
  (
    <span class="v">cntr</span> <span class="op">=</span> <span class="v">cntr</span> <span class="op">+</span> <span class="n">1</span>
    <span class="v">nidx</span> <span class="op">=</span> <span class="v">nidx</span> <span class="op">+</span> <span class="n">1</span>

    <span class="v">aiRecPos</span>    <span class="op">=</span> <span class="v">NullText</span>
    <span class="v">aiMeasure</span>   <span class="op">=</span> <span class="n">0</span>
    <span class="v">aiTimeType</span>  <span class="op">=</span> <span class="v">NullText</span>
    <span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">NullDate</span>
    <span class="v">aiStopTime</span>  <span class="op">=</span> <span class="v">NullDate</span>
    <span class="v">l_qty_only</span>  <span class="op">=</span> <span class="s">'N'</span>

    <span class="v">aiRecPos</span> <span class="op">=</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>[<span class="v">nidx</span>]

    <span class="k">IF</span> (<span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'HEADER'</span>) <span class="k">THEN</span>
    (
      <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> HEADER skipped idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
    )
    <span class="k">ELSE</span>
    (
      <span class="k">IF</span> (<span class="v">MEASURE</span>.<span class="f">exists</span>(<span class="v">nidx</span>))         <span class="k">THEN</span> ( <span class="v">aiMeasure</span>   <span class="op">=</span> <span class="v">MEASURE</span>[<span class="v">nidx</span>] )
      <span class="k">IF</span> (<span class="v">PayrollTimeType</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span> ( <span class="v">aiTimeType</span>  <span class="op">=</span> <span class="v">PayrollTimeType</span>[<span class="v">nidx</span>] )
      <span class="k">IF</span> (<span class="v">StartTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>))       <span class="k">THEN</span> ( <span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">StartTime</span>[<span class="v">nidx</span>] )
      <span class="k">IF</span> (<span class="v">StopTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>))        <span class="k">THEN</span> ( <span class="v">aiStopTime</span>  <span class="op">=</span> <span class="v">StopTime</span>[<span class="v">nidx</span>] )

      <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>,
                      <span class="s">'>>> idx='</span>  <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>)        <span class="op">||</span>
                      <span class="s">' pos='</span>     <span class="op">||</span> <span class="v">aiRecPos</span>             <span class="op">||</span>
                      <span class="s">' type=['</span>   <span class="op">||</span> <span class="v">aiTimeType</span>   <span class="op">||</span> <span class="s">']'</span>  <span class="op">||</span>
                      <span class="s">' st='</span>      <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>) <span class="op">||</span>
                      <span class="s">' sp='</span>      <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>)  <span class="op">||</span>
                      <span class="s">' m='</span>       <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">aiMeasure</span>))

      <span class="k">IF</span> (<span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_DAY'</span> <span class="k">OR</span> <span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_PERIOD'</span>) <span class="k">THEN</span>
      (
        <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> Boundary dayCnt='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">dayCnt</span>))

        <span class="k">IF</span> (<span class="v">dayCnt</span> <span class="op">></span> <span class="n">1</span>) <span class="k">THEN</span>
        ( <span class="v">i</span> <span class="op">=</span> <span class="n">1</span>
          <span class="k">WHILE</span> (<span class="v">i</span> <span class="op"><</span> <span class="v">dayCnt</span>) <span class="k">LOOP</span>
          ( <span class="v">j</span> <span class="op">=</span> <span class="v">i</span> <span class="op">+</span> <span class="n">1</span>
            <span class="k">WHILE</span> (<span class="v">j</span> <span class="op"><=</span> <span class="v">dayCnt</span>) <span class="k">LOOP</span>
            ( <span class="k">IF</span> (<span class="v">dayStarts</span>[<span class="v">i</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">j</span>] <span class="k">AND</span> <span class="v">dayStarts</span>[<span class="v">j</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">i</span>]) <span class="k">THEN</span>
              ( <span class="v">flagIdx</span> <span class="op">=</span> <span class="v">dayIdxs</span>[<span class="v">j</span>]
                <span class="v">OUT_MSG</span>[<span class="v">flagIdx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_overlap</span>)
                <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> OVERLAP fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">flagIdx</span>))
              )
              <span class="v">j</span> <span class="op">=</span> <span class="v">j</span> <span class="op">+</span> <span class="n">1</span>
            )
            <span class="v">i</span> <span class="op">=</span> <span class="v">i</span> <span class="op">+</span> <span class="n">1</span>
          )
        )

        <span class="v">dayStarts</span>    <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
        <span class="v">dayStops</span>     <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
        <span class="v">dayIdxs</span>      <span class="op">=</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
        <span class="v">dayCnt</span>       <span class="op">=</span> <span class="n">0</span>
        <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">NullDate</span>
        <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">NullDate</span>
        <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'N'</span>
        <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>
      )
      <span class="k">ELSE</span>
      (
        <span class="c">/* QTY-ONLY DETECTION */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span> <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span> <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
        ( <span class="v">l_st_hr</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'HH24'</span>)) <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
          <span class="v">l_sp_hr</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'HH24'</span>)) <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
          <span class="k">IF</span> (<span class="v">l_st_hr</span> <span class="op"><</span> <span class="n">0.01</span> <span class="k">AND</span> <span class="v">l_sp_hr</span> <span class="op">></span> <span class="n">23.9</span>) <span class="k">THEN</span>
          ( <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'Y'</span>
            <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> QTY-ONLY detected idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
          )
        )

        <span class="c">/* Overlap collection - skip qty-only */</span>
        <span class="k">IF</span> (<span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'N'</span> <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span> <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
        ( <span class="v">dayCnt</span> <span class="op">=</span> <span class="v">dayCnt</span> <span class="op">+</span> <span class="n">1</span>
          <span class="v">dayStarts</span>[<span class="v">dayCnt</span>] <span class="op">=</span> <span class="v">aiStartTime</span>
          <span class="v">dayStops</span>[<span class="v">dayCnt</span>]  <span class="op">=</span> <span class="v">aiStopTime</span>
          <span class="v">dayIdxs</span>[<span class="v">dayCnt</span>]   <span class="op">=</span> <span class="v">nidx</span>
        )

        <span class="c">/* Reg Hours qty-only */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span> <span class="k">AND</span> <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'Y'</span>) <span class="k">THEN</span>
        ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_reghrs</span>)
          <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> REGHRS QTY-ONLY fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
        )

        <span class="c">/* Reg Hours null start/stop */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span> <span class="k">AND</span> (<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">NullDate</span> <span class="k">OR</span> <span class="v">aiStopTime</span> <span class="op">=</span> <span class="v">NullDate</span>)) <span class="k">THEN</span>
        ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_reghrs</span>)
          <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> REGHRS NULL fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
        )

        <span class="c">/* Meal break stretch reset */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_break_type</span>) <span class="k">THEN</span>
        ( <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">NullDate</span>
          <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">NullDate</span>
          <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'N'</span>
          <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'Y'</span>
          <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> MEAL RESET idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
        )

        <span class="v">l_day</span> <span class="op">=</span> <span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'DY'</span>)

        <span class="v">l_sch_date_day</span> <span class="op">=</span> <span class="f">get_date_day_of_week</span>(<span class="v">aiStartTime</span>)
        <span class="v">l_dow_char</span>     <span class="op">=</span> <span class="f">UPPER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'DY'</span>))
        <span class="v">hol</span> <span class="op">=</span> <span class="f">GET_VALUE_SET</span>(<span class="s">'XX_HOLIDAY_CALENDAR_VS'</span>,
                            <span class="s">'|=p_date='''</span> <span class="op">||</span> <span class="f">to_char</span>(<span class="v">aiStartTime</span>, <span class="s">'YYYY/MM/DD'</span>) <span class="op">||</span> <span class="s">''''</span>)

        <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>,
                        <span class="s">'dow_fn='</span>    <span class="op">||</span> <span class="v">l_sch_date_day</span> <span class="op">||</span>
                        <span class="s">' dow_char='</span> <span class="op">||</span> <span class="v">l_dow_char</span>     <span class="op">||</span>
                        <span class="s">' hol='</span>      <span class="op">||</span> <span class="v">hol</span>)

        <span class="c">/* Break outside working hours */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_break_type</span> <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span> <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
        ( <span class="v">bkStart</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'HH24'</span>)) <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
          <span class="v">bkEnd</span>   <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'HH24'</span>)) <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
          <span class="k">IF</span> ((<span class="v">bkStart</span> <span class="op"><</span> <span class="v">p_sched_start</span> <span class="k">OR</span> <span class="v">bkEnd</span> <span class="op">></span> <span class="v">p_sched_end</span>)
              <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span> <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span> <span class="k">AND</span> <span class="f">length</span>(<span class="v">hol</span>) <span class="op">=</span> <span class="n">0</span>) <span class="k">THEN</span>
          ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_break</span>)
            <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> BREAK OUT fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
          )
        )

        <span class="c">/* Continuous stretch */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span> <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span> <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>
            <span class="k">AND</span> <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'N'</span> <span class="k">AND</span> <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>) <span class="k">THEN</span>
        (
          <span class="k">IF</span> (<span class="v">inStretch</span> <span class="op">=</span> <span class="s">'N'</span>) <span class="k">THEN</span>
          ( <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">aiStartTime</span>
            <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">aiStopTime</span>
            <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'Y'</span>
          )
          <span class="k">ELSE</span>
          ( <span class="k">IF</span> (<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">stretchEnd</span>) <span class="k">THEN</span>
            ( <span class="v">stretchEnd</span> <span class="op">=</span> <span class="v">aiStopTime</span> )
            <span class="k">ELSE</span>
            ( <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">aiStartTime</span>
              <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">aiStopTime</span>
            )
          )

          <span class="v">endMins</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>,   <span class="s">'J'</span>))<span class="op">*</span><span class="n">1440</span>
                  <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>,   <span class="s">'HH24'</span>))<span class="op">*</span><span class="n">60</span>
                  <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>,   <span class="s">'MI'</span>))
          <span class="v">stMins</span>  <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'J'</span>))<span class="op">*</span><span class="n">1440</span>
                  <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'HH24'</span>))<span class="op">*</span><span class="n">60</span>
                  <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'MI'</span>))
          <span class="v">contHrs</span> <span class="op">=</span> (<span class="v">endMins</span> <span class="op">-</span> <span class="v">stMins</span>) <span class="op">/</span> <span class="n">60</span>

          <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> ContHrs='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">contHrs</span>) <span class="op">||</span> <span class="s">' idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))

          <span class="k">IF</span> (<span class="v">contHrs</span> <span class="op">></span> <span class="v">p_max_cont_err</span>
              <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span> <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span> <span class="k">AND</span> <span class="f">length</span>(<span class="v">hol</span>) <span class="op">=</span> <span class="n">0</span>) <span class="k">THEN</span>
          ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_cont_err</span>)
            <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> CONT ERR fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
          )
          <span class="k">ELSE</span>
          ( <span class="k">IF</span> (<span class="v">contHrs</span> <span class="op">></span> <span class="v">p_max_cont_warn</span>
                <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span> <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span> <span class="k">AND</span> <span class="f">length</span>(<span class="v">hol</span>) <span class="op">=</span> <span class="n">0</span>) <span class="k">THEN</span>
            ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_cont_warn</span>)
              <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> CONT WARN fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
            )
          )
        )
      ) <span class="c">/* end ELSE - non-boundary processing */</span>
    ) <span class="c">/* end ELSE - non-HEADER */</span>

    <span class="k">IF</span> (<span class="v">nidx</span> <span class="op">></span> <span class="n">1000</span>) <span class="k">THEN</span>
    ( <span class="v">ex</span> <span class="op">=</span> <span class="f">raise_error</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'Formula '</span> <span class="op">||</span> <span class="v">ffName</span> <span class="op">||</span> <span class="s">' terminated - possible endless loop.'</span>) )

    <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> End bulk '</span> <span class="op">||</span> <span class="v">ffName</span>)
  ) <span class="c">/* end WHILE body */</span>
) <span class="c">/* end CHANGE_CONTEXTS */</span>

<span class="k">RETURN</span> <span class="v">OUT_MSG</span></code></pre>
</div>

<p>That's the entire formula. ~200 lines, three nested control structures, one state machine, and five validations all in one pass through the array. Now let's break it down piece by piece.</p>

<!-- BLOCK BY BLOCK WALKTHROUGH -->
<h2>The Formula's Architecture</h2>

<p class="section-lead">Before reading the code line-by-line, it helps to see the shape of the whole thing. The formula has eight blocks that fall into <strong>two clean halves</strong>: the first five blocks run <em>once</em> as scaffolding (set up arrays, capture identity, bind context, read configuration, initialise state), and the last three blocks run <em>repeatedly</em> inside the WHILE loop where the actual validation happens. Every line of code belongs to exactly one of these eight blocks.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:18px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram · Eight blocks, two halves — data flow from input arrays to OUT_MSG return</div>
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-14.png" alt="Diagram 14: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />
</div>

<div class="arch-flow">
<div class="arch-eyebrow">Architecture · eight blocks, two halves</div>
<div class="arch-title">From input array to OUT_MSG return</div>

<div class="arch-stages">

<div class="arch-stage active">
<div class="stage-label">
<div class="stage-num">Stage 01</div>
<div class="stage-name">Block 1</div>
</div>
<div class="stage-rail"><div class="stage-dot"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>
<div class="stage-headline" style="margin-top:6px;">Declare inputs and their empty-array defaults</div>
<div class="stage-meta"><code>DEFAULT FOR</code> for every input prevents <code>FFL-09100</code> at runtime when the framework hands over a sparse array.</div>
</div>
</div>

<div class="arch-stage active">
<div class="stage-label">
<div class="stage-num">Stage 02</div>
<div class="stage-name">Block 2</div>
</div>
<div class="stage-rail"><div class="stage-dot"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>
<div class="stage-headline" style="margin-top:6px;">Capture identity, define sentinels, log entry</div>
<div class="stage-meta">Capture <code>ffs_id</code> and <code>rule_id</code> from context, declare <code>NullDate</code> and <code>NullText</code> sentinels, and write the formula's first log line so every subsequent message is scoped and traceable.</div>
</div>
</div>

<div class="arch-stage active">
<div class="stage-label">
<div class="stage-num">Stage 03</div>
<div class="stage-name">Block 3</div>
</div>
<div class="stage-rail"><div class="stage-dot"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>
<div class="stage-headline" style="margin-top:6px;">Wrap the body in <code>CHANGE_CONTEXTS</code></div>
<div class="stage-meta">One outer wrap binds <code>HR_ASSIGNMENT_ID</code> for every DBI and value-set lookup inside — <strong>200× faster</strong> than re-binding per iteration.</div>
</div>
</div>

<div class="arch-stage active">
<div class="stage-label">
<div class="stage-num">Stage 04</div>
<div class="stage-name">Block 4</div>
</div>
<div class="stage-rail"><div class="stage-dot"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>
<div class="stage-headline" style="margin-top:6px;">Read configuration via <code>get_rvalue_number</code></div>
<div class="stage-meta">Schedule bounds and continuous-hours thresholds come from the rule definition. <strong>One formula serves every LE</strong> — per-entity variation lives in the rule, not the source.</div>
</div>
</div>

<div class="arch-stage active">
<div class="stage-label">
<div class="stage-num">Stage 05</div>
<div class="stage-name">Block 5</div>
</div>
<div class="stage-rail"><div class="stage-dot"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>
<div class="stage-headline" style="margin-top:6px;">Initialise day buffer, stretch tracker, OUT_MSG</div>
<div class="stage-meta">Three pieces of state with three different lifetimes — per-line, per-day, per-formula. The lifecycle distinction is what makes the rest of the formula correct.</div>
</div>
</div>

<div class="arch-stage">
<div class="stage-label">
<div class="stage-num">Stage 06</div>
<div class="stage-name">Block 6</div>
</div>
<div class="stage-rail"><div class="stage-dot"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-loop">Per line</span><span class="stage-pill">in WHILE loop</span></div>
<div class="stage-headline" style="margin-top:6px;">Read line, classify, route by time type</div>
<div class="stage-meta">Detect qty-only placeholders (<code>00:00–23:59</code>), buffer Reg Hours for overlap, route Meal Breaks to the schedule-window check.</div>
</div>
</div>

<div class="arch-stage">
<div class="stage-label">
<div class="stage-num">Stage 07</div>
<div class="stage-name">Block 7</div>
</div>
<div class="stage-rail"><div class="stage-dot"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-loop">Per day</span><span class="stage-pill">at END_DAY marker</span></div>
<div class="stage-headline" style="margin-top:6px;">Pairwise overlap test on the day buffer</div>
<div class="stage-meta">Strict less-than (<code><</code>) intersection test. Catches collisions; allows back-to-back 12:00→12:00 handovers without false flags.</div>
</div>
</div>

<div class="arch-stage">
<div class="stage-label">
<div class="stage-num">Stage 08</div>
<div class="stage-name">Block 8</div>
</div>
<div class="stage-rail"><div class="stage-dot"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-loop">Per line</span><span class="stage-pill">cross-iteration state</span></div>
<div class="stage-headline" style="margin-top:6px;">Continuous-hours state machine</div>
<div class="stage-meta">Idle ↔ Active. EXTEND when adjacent, RESTART on gap, RESET on meal break. Compares <code>contHrs</code> against soft-warn (5h) and hard-error (6h) thresholds.</div>
</div>
</div>

<div class="arch-stage">
<div class="stage-label">
<div class="stage-num">Return</div>
<div class="stage-name" style="color:var(--accent);">OUT_MSG</div>
</div>
<div class="stage-rail"><div class="stage-dot" style="background:var(--accent);"></div></div>
<div class="stage-body">
<div><span class="stage-pill scope-exit">Exit</span><span class="stage-pill">framework reads sparse array</span></div>
<div class="stage-headline" style="margin-top:6px;">Sparse array of error messages by line index</div>
<div class="stage-meta">Empty slots = clean rows. Populated slots become red error markers in the worker's timecard UI.</div>
</div>
</div>

</div>
</div>

<p>The first five blocks (Stages 01–05) make up the <strong>setup half</strong> — they run exactly once at the top of the formula, before any timecard row is processed. The last three (Stages 06–08) make up the <strong>loop half</strong> — they execute once per row inside the WHILE loop, with Block 7 firing only at day boundaries. Every line in the formula source belongs to one of these eight blocks. The Part 2 walkthrough goes through each block in detail; for now, this overview is enough to navigate the complete code listing above.</p>

<h2>Variable Naming Conventions in This Formula</h2>

<p class="section-lead">Fast Formula doesn't enforce naming rules — you can call any variable anything — but the formula in this post follows a deliberate convention. <strong>Each prefix signals the variable's role</strong>: where its value comes from, what its lifetime is, what code is allowed to write to it. Once you internalise the prefixes, the rest of the formula reads itself. This section is worth a few minutes upfront because Part 2 of this series uses these prefixes throughout the code walkthrough.</p>

<p>Seven naming patterns do all the work in this formula. The reference table below summarises them; the cards that follow explain each one in detail.</p>

<div class="excel-wrap">
<div class="excel-titlebar">
<span class="filename">Naming_Conventions_Reference.xlsx</span>
<span class="app">Excel</span>
</div>
<table class="excel-sheet">
<thead>
<tr>
<th>Prefix</th>
<th>Means</th>
<th>Examples in this formula</th>
<th>Lifetime</th>
<th>Who writes to it?</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>HWM_*</code></td>
<td>Framework-supplied context or input</td>
<td><code>HWM_FFS_ID</code>, <code>HWM_RULE_ID</code>, <code>HWM_PER_ASG_ASSIGNMENT_ID</code></td>
<td>Whole formula</td>
<td>The OTL framework (read-only)</td>
</tr>
<tr>
<td><code>HWM_CTXARY_*</code></td>
<td>Framework input <em>array</em> (one slot per timecard row)</td>
<td><code>HWM_CTXARY_RECORD_POSITIONS</code>, <code>HWM_CTXARY_HWM_MEASURE_DAY</code></td>
<td>Whole formula</td>
<td>The framework (read-only)</td>
</tr>
<tr>
<td><code>p_*</code></td>
<td>Parameter read from rule configuration</td>
<td><code>p_sched_start</code>, <code>p_max_cont_err</code>, <code>p_msg_overlap</code></td>
<td>Whole formula</td>
<td>Set once in Block 4, read everywhere</td>
</tr>
<tr>
<td><code>ai*</code></td>
<td>"Array input" — per-row local snapshot of input data</td>
<td><code>aiTimeType</code>, <code>aiStartTime</code>, <code>aiStopTime</code>, <code>aiRecPos</code></td>
<td>One iteration</td>
<td>Reset at top of every loop iteration</td>
</tr>
<tr>
<td><code>l_*</code></td>
<td>Local working variable or flag</td>
<td><code>l_qty_only</code>, <code>l_meal_taken</code>, <code>l_day</code>, <code>l_st_hr</code></td>
<td>Per-row or per-day</td>
<td>Set inside the loop body</td>
</tr>
<tr>
<td><code>day*</code> / <code>stretch*</code></td>
<td>State variables with named lifetimes</td>
<td><code>dayStarts</code>, <code>dayCnt</code>, <code>stretchStart</code>, <code>inStretch</code></td>
<td>Per-day / per-stretch</td>
<td>Updated inside loop, reset at boundaries</td>
</tr>
<tr style="background:#fce8e8;">
<td><code>OUT_MSG</code></td>
<td>The formula's return value (sparse error array)</td>
<td><code>OUT_MSG</code></td>
<td style="color:#c0392b;">Whole formula</td>
<td>Written only when a row needs flagging</td>
</tr>
</tbody>
</table>
</div>
<div class="excel-caption">Seven naming patterns. Each one signals a different role and lifetime, making the formula's intent visible without reading the surrounding code.</div>

<p>Now the prefixes in detail, with examples and the reasoning behind each convention:</p>

<!-- Prefix card 1: HWM_* -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Prefix 01 · Framework Context</div>
<div class="ic-name">HWM_*</div>
</div>
<div class="ic-question">"Where does this value come from?" → The OTL framework, before the formula even runs.</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>HWM_Examples.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Variable</th><th>What it holds</th><th>Set by</th></tr></thead>
<tbody>
<tr><td><code>HWM_FFS_ID</code></td><td>This run's session ID</td><td>Framework, on submission</td></tr>
<tr><td><code>HWM_RULE_ID</code></td><td>The rule that triggered this formula</td><td>Framework, on rule binding</td></tr>
<tr><td><code>HWM_PER_ASG_ASSIGNMENT_ID</code></td><td>The worker's HR assignment ID</td><td>Framework, from worker context</td></tr>
</tbody>
</table>
</div>
<div class="ic-explain">The <code>HWM_</code> prefix — short for <em>HCM Workforce Management</em> — marks variables the OTL framework injects into the formula's scope. They're not declared by the formula author; they appear automatically when the formula runs. The values are read-only from the formula's perspective; trying to assign to them does nothing useful and can break the binding.<br><br>Their purpose is to give the formula access to <strong>contextual information about the current run</strong>: whose timecard is being validated (<code>HWM_PER_ASG_ASSIGNMENT_ID</code>), which rule fired the formula (<code>HWM_RULE_ID</code>), and what unique session ID identifies this specific submission for log tracing (<code>HWM_FFS_ID</code>). Block 2 captures these into shorter local variables (<code>ffs_id</code>, <code>rule_id</code>) for convenience throughout the rest of the formula.</div>
</div>

<!-- Prefix card 2: HWM_CTXARY_* -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Prefix 02 · Framework Input Array</div>
<div class="ic-name">HWM_CTXARY_*</div>
</div>
<div class="ic-question">"Is this a single value or a parallel array indexed by row number?" → An array, one slot per timecard row.</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>HWM_CTXARY_Examples.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Variable</th><th>Holds (per row)</th><th>Type</th></tr></thead>
<tbody>
<tr><td><code>HWM_CTXARY_RECORD_POSITIONS</code></td><td>Marker text or empty</td><td>TEXT_NUMBER array</td></tr>
<tr><td><code>HWM_CTXARY_HWM_MEASURE_DAY</code></td><td>Day-aggregated quantity</td><td>NUMBER_NUMBER array</td></tr>
</tbody>
</table>
</div>
<div class="ic-explain">The <code>HWM_CTXARY_</code> prefix — short for <em>HCM Workforce Management Context Array</em> — marks the framework's <strong>parallel input arrays</strong>. Where <code>HWM_*</code> holds a single value, <code>HWM_CTXARY_*</code> holds one slot per timecard row, all indexed by the same row number.<br><br>You access them like arrays: <code>HWM_CTXARY_RECORD_POSITIONS[3]</code> retrieves the value for row 3. The naming feels heavy, but it's deliberately verbose so you can never mistake a per-row array for a single-value context. Confusing the two would cause type errors at compile time — loud and easy to fix — so the convention pays off.<br><br>Note that some inputs in the <code>INPUTS ARE</code> declaration (like <code>measure</code>, <code>StartTime</code>, <code>StopTime</code>) <em>also</em> behave as parallel arrays but use cleaner names. They're framework arrays too; they just don't use the <code>HWM_CTXARY_</code> prefix because OTL's design predates the convention. Treat them the same way: per-row, indexed by row number, read-only.</div>
</div>

<!-- Prefix card 3: p_* -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Prefix 03 · Parameter</div>
<div class="ic-name">p_*</div>
</div>
<div class="ic-question">"Is this value tunable per legal entity?" → Yes — read once from the rule, then used as a constant.</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>p_Examples.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Variable</th><th>Source</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>p_sched_start</code></td><td>Rule param SCHEDULE_START_HOUR</td><td>Schedule window check</td></tr>
<tr><td><code>p_max_cont_err</code></td><td>Rule param MAX_CONTINUOUS_HRS_ERR</td><td>Hard cap on continuous work</td></tr>
<tr><td><code>p_max_cont_warn</code></td><td>Rule param MAX_CONTINUOUS_HRS_WARN</td><td>Soft warning threshold</td></tr>
<tr><td><code>p_msg_overlap</code></td><td>Hardcoded message name</td><td>Error message lookup key</td></tr>
<tr><td><code>p_break_type</code></td><td>Hardcoded layout label</td><td>Time-type matching</td></tr>
</tbody>
</table>
</div>
<div class="ic-explain">The <code>p_</code> prefix marks <strong>parameter-style variables</strong> — values set once in Block 4 and used throughout the rest of the formula as effectively constant. The lowercase <code>p</code> distinguishes them from framework-supplied values (<code>HWM_*</code>) and per-row scratch (<code>ai*</code>, <code>l_*</code>).<br><br>Most <code>p_*</code> variables are read from the rule configuration via <code>get_rvalue_number</code>, which fetches numeric parameters that legal entities can tune independently — this is how one entity can use a 5-hour cap while another uses 6 with the same formula source. A few <code>p_*</code> variables (the message names like <code>p_msg_overlap</code>, the time-type labels like <code>p_break_type</code>) are hardcoded because they don't vary across the rollout.<br><br>The convention serves a code-review purpose: when you see <code>p_*</code> being assigned anywhere outside Block 4, that's a code smell — parameters should be set once at setup and treated as constant during the loop. Mutation indicates a bug or a misuse.</div>
</div>

<!-- Prefix card 4: ai* -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Prefix 04 · Array Input Snapshot</div>
<div class="ic-name">ai*</div>
</div>
<div class="ic-question">"Is this a per-row local copy of input data?" → Yes — refreshed at the top of every iteration.</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>ai_Examples.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Variable</th><th>Source array</th><th>Used for</th></tr></thead>
<tbody>
<tr><td><code>aiRecPos</code></td><td>RECORD_POSITIONS[nidx]</td><td>Row-type routing (HEADER vs END_DAY vs data)</td></tr>
<tr><td><code>aiTimeType</code></td><td>PayrollTimeType[nidx]</td><td>Validation routing (Reg Hours vs Meal Break)</td></tr>
<tr><td><code>aiStartTime</code></td><td>StartTime[nidx]</td><td>Stretch tracking, overlap testing</td></tr>
<tr><td><code>aiStopTime</code></td><td>StopTime[nidx]</td><td>Stretch tracking, overlap testing</td></tr>
</tbody>
</table>
</div>
<div class="ic-explain">The <code>ai</code> prefix stands for <strong>"array input"</strong> — per-row local snapshots of values pulled from the framework's input arrays. At the top of every loop iteration, the formula reads from the input arrays (with <code>.exists()</code> guards) and copies the values into matching <code>ai*</code> locals.<br><br>Why copy rather than reading the input arrays directly throughout the iteration? Three reasons. First, it creates a <strong>consistent snapshot</strong>: the rest of the iteration always sees the same values for "this row", even if downstream code logic gets restructured. Second, it provides a single place to apply guards (the <code>.exists()</code> checks in the read block) so you can never accidentally trigger an unguarded read elsewhere. Third, it makes the data flow obvious in code review — seeing <code>ai*</code> on the left of an assignment in the read block flags it as the "snapshot point", and the rest of the iteration cleanly works from those locals.<br><br>The <code>ai*</code> variables are reset at the top of every iteration to their sentinel values (<code>NullText</code>, <code>NullDate</code>) before the new row's reads happen. This explicit reset prevents the stale-value bug discussed in Block 5.</div>
</div>

<!-- Prefix card 5: l_* -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Prefix 05 · Local Working Variable</div>
<div class="ic-name">l_*</div>
</div>
<div class="ic-question">"Is this a temporary working value or flag inside the loop body?" → Yes.</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>l_Examples.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Variable</th><th>Type</th><th>Lifetime & purpose</th></tr></thead>
<tbody>
<tr><td><code>l_qty_only</code></td><td>'Y'/'N' flag</td><td>Per-row: was this row detected as a qty-only placeholder?</td></tr>
<tr><td><code>l_meal_taken</code></td><td>'Y'/'N' flag</td><td>Per-day: has the worker logged a meal break yet today?</td></tr>
<tr><td><code>l_day</code></td><td>3-letter day code</td><td>Per-row: 'MON', 'SAT', etc., for weekend exception checks</td></tr>
<tr><td><code>l_st_hr</code> / <code>l_sp_hr</code></td><td>fractional hour</td><td>Per-row: punch times converted to decimal hours</td></tr>
</tbody>
</table>
</div>
<div class="ic-explain">The <code>l_</code> prefix marks <strong>local working variables</strong> created inside the loop body for intermediate computation or state-tracking. Some are per-row (computed fresh each iteration), some are per-day (set once on a triggering event and persisting until the next day boundary).<br><br>The prefix's main job is to distinguish working state from input snapshots (<code>ai*</code>) and parameters (<code>p_*</code>). A formula reader scanning the code can immediately tell <code>l_qty_only</code> is a flag the formula sets itself, not data from the framework or a configuration value.<br><br>Within <code>l_*</code> there's an unwritten sub-convention: variables that hold <code>'Y'</code>/<code>'N'</code> flags use names ending in past-tense or descriptive adjectives (<code>l_meal_taken</code>, <code>l_qty_only</code>), while variables that hold computed numeric or string values use abbreviated names (<code>l_st_hr</code>, <code>l_day</code>). The convention isn't enforced, but consistency makes the code easier to scan.</div>
</div>

<!-- Prefix card 6: day* / stretch* -->
<div class="input-card">
<div class="ic-head">
<div class="ic-eyebrow">Prefix 06 · Named-Lifetime State</div>
<div class="ic-name">day*  ·  stretch*</div>
</div>
<div class="ic-question">"Does this variable have a specific multi-row lifetime tied to a domain concept?" → Yes.</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>State_Group_Examples.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Group</th><th>Variables</th><th>Resets when</th></tr></thead>
<tbody>
<tr><td><strong>day*</strong></td><td><code>dayStarts</code>, <code>dayStops</code>, <code>dayIdxs</code>, <code>dayCnt</code></td><td>At END_DAY/END_PERIOD marker</td></tr>
<tr><td><strong>stretch*</strong></td><td><code>stretchStart</code>, <code>stretchEnd</code>, <code>inStretch</code></td><td>On meal break or END_DAY</td></tr>
</tbody>
</table>
</div>
<div class="ic-explain">Some variables can't be neatly classified as "per-row" or "whole-formula" — they live for a domain-specific period that the formula explicitly manages. The convention here is to <strong>group these by domain prefix</strong>: <code>day*</code> for variables related to a single day's accumulated state, <code>stretch*</code> for variables tracking the current continuous-work stretch.<br><br>The grouping makes the code's structure self-documenting. When a reader sees <code>dayStarts</code>, <code>dayStops</code>, <code>dayIdxs</code>, and <code>dayCnt</code> together, they immediately recognise these as the day buffer — four pieces of one logical structure. Same for <code>stretchStart</code>, <code>stretchEnd</code>, <code>inStretch</code> as the stretch tracker.<br><br>The grouping also signals that these variables must be <strong>reset together</strong>. Block 7c (the END_DAY reset) clears all four day buffer variables in one block, and clears the stretch tracker variables in the same block. Resetting some without others would corrupt state. The naming makes it obvious which variables belong in the same reset block.</div>
</div>

<!-- Prefix card 7: OUT_MSG -->
<div class="input-card output">
<div class="ic-head">
<div class="ic-eyebrow">Prefix 07 · Formula Output (Reserved Name)</div>
<div class="ic-name">OUT_MSG</div>
</div>
<div class="ic-question">"Is this the value the formula returns to the framework?" → Yes — and the name is reserved.</div>
<div class="ic-mini-excel">
<div class="me-bar"><span>OUT_MSG_Behaviour.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Idx</th><th>OUT_MSG content</th><th>Meaning</th></tr></thead>
<tbody>
<tr class="row-clean"><td>[2]</td><td class="empty">(no entry)</td><td class="tag">clean row</td></tr>
<tr class="row-flagged"><td>[3]</td><td class="msg">"Continuous work exceeds 6 hours"</td><td class="tag">flagged row</td></tr>
<tr class="row-flagged"><td>[5]</td><td class="msg">"Overlapping entries"</td><td class="tag">flagged row</td></tr>
<tr class="row-clean"><td>[6]</td><td class="empty">(no entry)</td><td class="tag">clean row</td></tr>
</tbody>
</table>
</div>
<div class="ic-explain"><code>OUT_MSG</code> is the only variable in this formula whose name is <strong>not chosen by the author</strong> — it's reserved by the TER formula type contract. The framework expects the formula to write error messages into a variable with this exact name, and reads from it after the formula returns.<br><br>The naming is uppercase to signal "framework-reserved", distinguishing it from the lowercase prefixes (<code>p_</code>, <code>ai</code>, <code>l_</code>, <code>day</code>, <code>stretch</code>) used for author-chosen names. The pattern carries over to other formula types: payroll formulas have their own reserved output names, absence formulas have theirs.<br><br>The <code>_MSG</code> suffix hints at the data type (a sparse array of message strings indexed by row number). The combination — uppercase name plus underscore-separated suffix — is a strong visual signal that this variable is a contract surface, not a working variable. Treat it as such: write to it sparingly, only for rows that need flagging, and never reset it during the run.</div>
</div>

<h3>Why these conventions matter beyond style</h3>

<p>Naming conventions might feel like decoration, but in Fast Formula they carry real engineering value. Three benefits worth being explicit about:</p>

<p><strong>Self-documenting role.</strong> Fast Formula has no type signatures, no scope modifiers, no access controls. Every variable looks the same to the compiler. The naming convention is the only signal a reader has about whether they're looking at framework data, parameter config, per-row input, working state, or output. Without conventions, you'd have to read the variable's declaration site to understand its role — which is often hundreds of lines away.</p>

<p><strong>Code-review heuristics.</strong> When reviewing TER formulas, certain patterns are immediately suspicious. <code>p_*</code> being assigned outside Block 4 means a parameter is being mutated mid-loop — almost certainly a bug. <code>HWM_*</code> being assigned anywhere means someone tried to write to a framework value — broken. <code>ai*</code> being read without first being reset means stale data leakage. The conventions turn code review into a pattern-matching exercise; you can spot bugs by shape before reading the logic.</p>

<p><strong>Onboarding cost.</strong> A developer joining the team can read this convention table in two minutes and then read the formula's variables fluently. Without conventions, every new variable is a small puzzle — "what does <code>x</code> do? where does <code>y</code> come from?" — and onboarding takes weeks instead of days.</p>

<div class="aside">
<div class="head">A note on consistency across formulas</div>
Different teams use different conventions, and Oracle's documentation doesn't mandate any specific style. The patterns shown here (<code>HWM_</code>, <code>p_</code>, <code>ai</code>, <code>l_</code>, <code>day*</code>, <code>stretch*</code>, <code>OUT_MSG</code>) are common in OTL implementations but you'll see variations elsewhere. The principle that matters is <em>consistency within a project</em>. Pick a convention, document it, and apply it uniformly. The specific letters matter less than the discipline of using them.
</div>

<div style="background:#fff; padding:48px 36px 56px 36px; margin:48px 0 24px 0; border-radius:8px; border:1px solid #e8e3d8;">

<!-- Header: title + tagline -->
<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:36px; flex-wrap:wrap; gap:16px;">
<div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#1f5fa8; letter-spacing:-0.5px;">Same formula.</div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#2d2926; letter-spacing:-0.5px; margin-top:4px;">The algorithm in detail.</div>
</div>
<div style="text-align:right;">
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:14px; font-weight:700; color:#2d2926; letter-spacing:0.5px;">PART 2 OF 2</div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:11px; color:#7a7570; margin-top:2px; letter-spacing:0.5px;">Coming next</div>
</div>
</div>

<!-- Tile grid: 6 tiles in a row -->
<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-2/diagram-15.png" alt="Diagram 15: Oracle Fast Formula: Time Entry Rule (Part 2)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

<!-- Caption beneath highlighted tile -->
<p style="margin:24px 0 0 0; font-size:13px; color:#5a544e; line-height:1.6; text-align:center;">
Part 2 walks through every block of the formula in detail — with the <strong style="color:#1f5fa8;">continuous-hours state machine</strong> as the centrepiece. You'll also get the per-line routing decisions, the day-boundary overlap test, the setup dependencies that must exist for the formula to fire, and a worked end-to-end trace of Sarah's full timecard.
</p>

</div>




<!-- NEXT IN SERIES -->
<div style="background:#fff8e8; border:1px solid #b97417; border-radius:6px; padding:20px 24px; margin:40px 0 32px 0;">
<div style="font-size:10px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Next in The TER Series</div>
<div style="font-size:18px; font-weight:700; color:#2d2926; margin-bottom:8px;">Part 3 — The Algorithm: Setup, Routing, and Overlap Detection</div>
<div style="font-size:13.5px; color:#5a544e; line-height:1.6;">The data shape is settled. Now the algorithm. Part 3 walks through the formula's setup phase (crash prevention, identity capture, per-LE configuration), the per-line routing that decides which checks apply to each row, and the day-boundary pairwise overlap test — the first half of the eight-block algorithm.</div>
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