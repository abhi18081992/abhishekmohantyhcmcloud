---
title: "Oracle Fast Formula: Time Entry Rule (Part 3)"
pubDate: 2026-05-29
description: "Oracle Fast Formula: Time Entry Rule (Part 3)"
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
<span style="color:#5a544e; margin-left:8px;">Part 3 of 4</span>
<div style="margin-top:6px; color:#7a7570; font-size:11.5px; line-height:1.5;">
1. OTL Foundations ·
2. The Input Contract ·
3. Algorithm: Routing & Overlap ·
4. The State Machine
</div>
</div>

<h1>The Algorithm: Setup, Routing, and Overlap Detection<br><span style="color:#7a7570; font-size:0.7em; font-weight:400; font-style:italic;">Part 3 of 4 — The TER Series</span></h1>

<div class="byline">
<div class="avatar">AM</div>
<div class="author-block">
<div class="author-name">Abhishek Mohanty</div>
<div class="author-creds">Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead</div>
</div>
</div>

<div class="opening">Parts 1 and 2 covered what TER does and the data it receives. Now we get into the algorithm. This post covers the setup phase, the per-line routing logic that decides which checks apply to which rows, and the day-boundary pairwise overlap test. Part 4 will finish with the state machine.</div>

<h2>Setup — What Runs Before the Loop</h2>

<p class="section-lead">Five blocks of scaffolding run once at the top of the formula, before the loop touches a single timecard line. Each block has one job:</p>

<ul>
<li><strong>Block 1</strong> declares the input arrays so the formula won't crash on an empty slot.</li>
<li><strong>Block 2</strong> grabs identifiers from the framework and writes a startup log line.</li>
<li><strong>Block 3</strong> binds the worker's assignment context once for the entire formula body.</li>
<li><strong>Block 4</strong> reads tunable values from the rule configuration so the formula stays portable across legal entities.</li>
<li><strong>Block 5</strong> initialises the variables the loop will need — output array, counters, day buffer, stretch tracker, meal flag.</li>
</ul>

<p>Each annotated block below pairs the actual code with a numbered breakdown of what it does and, where helpful, a short Excel snippet showing the data being shaped.</p>

<div class="annot-wrap">
<div class="annot-head">
<span>Setup phase · Blocks 1–5</span>
<span class="label-right">Annotated</span>
</div>
<div class="annot-body">

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="k">DEFAULT FOR</span> <span class="v">RECORD_POSITIONS</span> <span class="k">IS</span> <span class="v">EMPTY_TEXT_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">measure</span>          <span class="k">IS</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">PayrollTimeType</span>  <span class="k">IS</span> <span class="v">EMPTY_TEXT_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">StartTime</span>        <span class="k">IS</span> <span class="v">EMPTY_DATE_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">StopTime</span>         <span class="k">IS</span> <span class="v">EMPTY_DATE_NUMBER</span>

<span class="k">INPUTS ARE</span> <span class="v">RECORD_POSITIONS</span>, <span class="v">measure</span>, <span class="v">PayrollTimeType</span>,
           <span class="v">StartTime</span>, <span class="v">StopTime</span></code></pre></div>
<div class="annot-note">
<span class="nt">Block 1 · Crash prevention</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1: The shape — six parallel arrays -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The shape: six parallel arrays sharing row indexes</div>

<div style="overflow-x:auto; margin-bottom:10px;">
<table style="width:100%; min-width:540px; border-collapse:collapse; font-size:10.5px;">
<thead>
<tr style="background:#dbe5f4;">
<th style="padding:5px 7px; border:1px solid #4472c4; color:#2d2926; font-weight:700;">Idx</th>
<th style="padding:5px 7px; border:1px solid #4472c4; color:#2d2926; font-weight:700;">RECORD_POSITIONS</th>
<th style="padding:5px 7px; border:1px solid #4472c4; color:#2d2926; font-weight:700;">measure</th>
<th style="padding:5px 7px; border:1px solid #4472c4; color:#2d2926; font-weight:700;">PayrollTimeType</th>
<th style="padding:5px 7px; border:1px solid #4472c4; color:#2d2926; font-weight:700;">StartTime</th>
<th style="padding:5px 7px; border:1px solid #4472c4; color:#2d2926; font-weight:700;">StopTime</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff8e7;">
<td style="padding:5px 7px; border:1px solid #999; text-align:center; font-weight:700; color:#5a544e;">[1]</td>
<td style="padding:5px 7px; border:1px solid #b97417; text-align:center; font-weight:700; color:#b97417;">HEADER</td>
<td style="padding:5px 7px; border:1px solid #c0392b; background:#fff5f0; text-align:center; font-style:italic; color:#c0392b;">missing</td>
<td style="padding:5px 7px; border:1px solid #c0392b; background:#fff5f0; text-align:center; font-style:italic; color:#c0392b;">missing</td>
<td style="padding:5px 7px; border:1px solid #c0392b; background:#fff5f0; text-align:center; font-style:italic; color:#c0392b;">missing</td>
<td style="padding:5px 7px; border:1px solid #c0392b; background:#fff5f0; text-align:center; font-style:italic; color:#c0392b;">missing</td>
</tr>
<tr style="background:#fff;">
<td style="padding:5px 7px; border:1px solid #999; text-align:center; font-weight:700; color:#5a544e;">[2]</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; font-style:italic; color:#999;">empty</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; color:#5a544e;">1.5</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; color:#5a544e;">Reg Hours</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; color:#5a544e;">08:30</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; color:#5a544e;">10:00</td>
</tr>
<tr style="background:#fff;">
<td style="padding:5px 7px; border:1px solid #999; text-align:center; font-weight:700; color:#5a544e;">[3]</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; font-style:italic; color:#999;">empty</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; color:#5a544e;">4.75</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; color:#5a544e;">Reg Hours</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; color:#5a544e;">10:00</td>
<td style="padding:5px 7px; border:1px solid #999; text-align:center; color:#5a544e;">14:45</td>
</tr>
<tr style="background:#fce8e8;">
<td style="padding:5px 7px; border:1px solid #999; text-align:center; font-weight:700; color:#5a544e;">[4]</td>
<td style="padding:5px 7px; border:1px solid #c0392b; text-align:center; font-weight:700; color:#c0392b;">END_DAY</td>
<td style="padding:5px 7px; border:1px solid #c0392b; background:#fff5f0; text-align:center; font-style:italic; color:#c0392b;">missing</td>
<td style="padding:5px 7px; border:1px solid #c0392b; background:#fff5f0; text-align:center; font-style:italic; color:#c0392b;">missing</td>
<td style="padding:5px 7px; border:1px solid #c0392b; background:#fff5f0; text-align:center; font-style:italic; color:#c0392b;">missing</td>
<td style="padding:5px 7px; border:1px solid #c0392b; background:#fff5f0; text-align:center; font-style:italic; color:#c0392b;">missing</td>
</tr>
</tbody>
</table>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-bottom:18px;">Marker rows ([1] HEADER, [4] END_DAY) carry a value only in RECORD_POSITIONS — the other columns are <strong style="color:#c0392b;">genuinely missing</strong>, not blank, not zero.</div>

<!-- PART 2: What DEFAULT FOR does -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · What DEFAULT FOR does at runtime</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">WITHOUT DEFAULT FOR — CRASH</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#5a544e;">Code:</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10.5px; margin:4px 0 10px;">aiStartTime = StartTime[1]</div>
<div style="font-size:10.5px; font-weight:700; color:#5a544e;">Result:</div>
<div style="font-size:10.5px; color:#c0392b; font-weight:700; margin-top:4px; line-height:1.7;">✗ Fast Formula has no instruction<br>✗ Throws FFL-09100<br>✗ Crashes the entire submission</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:6px;">Worker sees: "Submission failed, contact administrator"</div>
</div>
</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">WITH DEFAULT FOR — SAFE</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#5a544e;">Code:</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10.5px; margin:4px 0 10px;">DEFAULT FOR StartTime IS<br>  EMPTY_DATE_NUMBER</div>
<div style="font-size:10.5px; font-weight:700; color:#5a544e;">Result:</div>
<div style="font-size:10.5px; color:#3d7a52; font-weight:700; margin-top:4px; line-height:1.7;">✓ FF treats array as empty<br>✓ .exists(1) returns FALSE<br>✓ Formula skips and continues</div>
</div>
</div>
</div>

<!-- PART 3: Naming convention -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · The naming convention: <span style="font-family:'JetBrains Mono', monospace; font-size:11px;">EMPTY_<value-type>_<key-type></span></div>

<div style="display:grid; grid-template-columns:auto auto auto; gap:0; margin-bottom:10px; max-width:340px;">
<div style="background:#dbe5f4; border:1px solid #4472c4; padding:8px 12px; text-align:center;">
<div style="font-family:'JetBrains Mono', monospace; font-size:12px; font-weight:700; color:#2d2926;">EMPTY_</div>
<div style="font-size:9px; color:#5a544e; margin-top:2px;">prefix</div>
</div>
<div style="background:#a8c1e0; border:1px solid #4472c4; padding:8px 12px; text-align:center;">
<div style="font-family:'JetBrains Mono', monospace; font-size:12px; font-weight:700; color:#2d2926;">TEXT_</div>
<div style="font-size:9px; color:#5a544e; margin-top:2px;">value-type</div>
</div>
<div style="background:#7da5d3; border:1px solid #4472c4; padding:8px 12px; text-align:center;">
<div style="font-family:'JetBrains Mono', monospace; font-size:12px; font-weight:700; color:#fff;">NUMBER</div>
<div style="font-size:9px; color:#fff; margin-top:2px;">key-type</div>
</div>
</div>

<div style="overflow-x:auto;">
<table style="width:100%; border-collapse:collapse; font-size:10.5px;">
<thead>
<tr style="background:#e8e8e8;">
<th style="padding:6px 10px; border:1px solid #999; text-align:left; color:#5a544e;">Constant</th>
<th style="padding:6px 10px; border:1px solid #999; text-align:left; color:#5a544e;">Use it for</th>
</tr>
</thead>
<tbody>
<tr><td style="padding:6px 10px; border:1px solid #999; font-family:'JetBrains Mono', monospace; color:#2d2926;">EMPTY_TEXT_NUMBER</td><td style="padding:6px 10px; border:1px solid #999; color:#5a544e;">RECORD_POSITIONS, PayrollTimeType</td></tr>
<tr><td style="padding:6px 10px; border:1px solid #999; font-family:'JetBrains Mono', monospace; color:#2d2926;">EMPTY_DATE_NUMBER</td><td style="padding:6px 10px; border:1px solid #999; color:#5a544e;">StartTime, StopTime</td></tr>
<tr><td style="padding:6px 10px; border:1px solid #999; font-family:'JetBrains Mono', monospace; color:#2d2926;">EMPTY_NUMBER_NUMBER</td><td style="padding:6px 10px; border:1px solid #999; color:#5a544e;">measure</td></tr>
</tbody>
</table>
</div>

<!-- Bottom takeaway -->
<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:3px; margin-top:14px; font-size:10.5px; line-height:1.6;">
<span style="font-family:'JetBrains Mono', monospace; font-weight:700; color:#f0d68a;">TAKEAWAY:</span> Every framework array needs its own DEFAULT FOR matched to its data type. One line saved → production crash. One line spent → submission survives marker rows.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The shape of the input</div>
<ul class="ann-bullets">
<li>When a worker submits a timecard, OTL doesn't pass the rows one-by-one to the formula. It hands over <strong>six parallel arrays</strong> — one per data column — that all share the same row indexes.</li>
<li>Picture this as a giant spreadsheet: each row in the timecard becomes one slot across all six arrays. Slot [3] in <code>StartTime</code> describes the same row as slot [3] in <code>PayrollTimeType</code> and <code>StopTime</code>.</li>
<li>The catch: <strong>not every row fills every column</strong>. Boundary rows like HEADER, END_DAY, and END_PERIOD only carry a value in <code>RECORD_POSITIONS</code>; their slots in the other five arrays are genuinely missing — not blank, not zero, but absent.</li>
<li>If your formula reads <code>StartTime[1]</code> on a HEADER row, you're asking for data that isn't there. Fast Formula will not silently return null. It will crash the entire submission with <code>FFL-09100</code>.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>What DEFAULT FOR actually does</div>
<ul class="ann-bullets">
<li><code>DEFAULT FOR ... IS EMPTY_TEXT_NUMBER</code> tells Fast Formula: <em>"this is an array variable. If it shows up empty at runtime, give me an empty array, not an error."</em></li>
<li>Without it, the moment the formula starts and Fast Formula tries to bind the input variable, it has no instruction for how to handle an empty array. Compilation succeeds (the syntax is fine) but execution dies on first read.</li>
<li>Worse, the failure is opaque to the worker. They don't see <em>"missing default declaration on input array"</em>. They see <em>"submission failed, please contact your administrator"</em>. Hours of investigation follow.</li>
<li>The cost of adding the declaration is one line per input. The cost of skipping it is a production incident.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The naming convention, decoded</div>
<ul class="ann-bullets">
<li>The constant names look cryptic but follow a strict pattern: <em>{value-type}_{key-type}</em>.</li>
<li><code>EMPTY_TEXT_NUMBER</code> is an array of <strong>text values</strong> indexed by <strong>numbers</strong>. That's what <code>RECORD_POSITIONS</code> needs — values like 'HEADER' and 'END_DAY' keyed by row number.</li>
<li><code>EMPTY_DATE_NUMBER</code> matches <code>StartTime</code> and <code>StopTime</code>: dates indexed by row number.</li>
<li><code>EMPTY_NUMBER_NUMBER</code> matches <code>measure</code>: numeric quantities indexed by row number.</li>
<li>Pick the wrong constant and you get a type-mismatch error at compile time — loud and easy to fix. The truly dangerous bug is forgetting the declaration entirely, which compiles silently.</li>
</ul>
</div>
<div class="ann-takeaway">Every framework array needs its own <code>DEFAULT FOR</code> declaration matched to its data type. The cost is one line; skipping it ships a formula that compiles fine but crashes the first time it meets a real-world timecard with marker rows.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="v">ffName</span>  <span class="op">=</span> <span class="s">'XX_TER_CONTINUOUS_HOURS_VALIDATION'</span>
<span class="v">ffs_id</span>  <span class="op">=</span> <span class="f">GET_CONTEXT</span>(<span class="v">HWM_FFS_ID</span>, <span class="n">0</span>)
<span class="v">rule_id</span> <span class="op">=</span> <span class="f">GET_CONTEXT</span>(<span class="v">HWM_RULE_ID</span>, <span class="n">0</span>)

<span class="v">NullDate</span> <span class="op">=</span> <span class="s">'01-JAN-1900'</span> (<span class="k">DATE</span>)
<span class="v">NullText</span> <span class="op">=</span> <span class="s">'**FF_NULL**'</span>

<span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>,
                <span class="s">'>>> Enter '</span> <span class="op">||</span> <span class="v">ffName</span>)</code></pre></div>
<div class="annot-note">
<span class="nt">Block 2 · Self-identification</span>
<div class="ann-excel">
<div class="ax-bar"><span>Analyze_Rule_Processing_Details.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th style="width:60px;">Time</th><th>Worker</th><th>Log Line</th></tr></thead>
<tbody>
<tr><td class="tc">18:15:02</td><td>Sarah B.</td><td><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">>>> Enter XX_TER_CONTINUOUS_HOURS_VALIDATION</code></td></tr>
<tr><td class="tc">18:15:02</td><td>Sarah B.</td><td style="font-size:10.5px;">idx=2 type=Reg start=08:30 stop=10:00</td></tr>
<tr class="row-fail"><td class="tc">18:15:02</td><td>Sarah B.</td><td class="tag" style="font-size:10.5px;">FLAG idx=3: contHrs=6.25</td></tr>
</tbody>
</table>
</div>
<div class="ann-excel-cap">Each <code>add_rlog</code> call surfaces here, scoped by <code>ffs_id</code> and <code>rule_id</code>.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1: Identity capture -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The formula introduces itself — capture identity from framework</div>

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px;">
<div style="background:#fff; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:9.5px; font-weight:700; text-align:center; padding:5px; letter-spacing:0.4px;">ffName · YOUR LOCAL VAR</div>
<div style="padding:10px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#2d2926;">'XX_TER_CONTINUOUS_<br>  HOURS_VALIDATION'</div>
<div style="font-size:10px; color:#5a544e; margin-top:8px; line-height:1.5;">Return-address stamp. Travels with every log line.</div>
</div>
</div>
<div style="background:#fff; border:1.5px solid #1f5fa8; border-radius:4px; overflow:hidden;">
<div style="background:#1f5fa8; color:#fff; font-size:9.5px; font-weight:700; text-align:center; padding:5px; letter-spacing:0.4px;">ffs_id · FROM GET_CONTEXT</div>
<div style="padding:10px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#2d2926;">GET_CONTEXT(<br>  HWM_FFS_ID, 0)</div>
<div style="font-size:10px; color:#5a544e; margin-top:8px; line-height:1.5;">Unique per submission. Set when worker clicks Submit.</div>
</div>
</div>
<div style="background:#fff; border:1.5px solid #b97417; border-radius:4px; overflow:hidden;">
<div style="background:#b97417; color:#fff; font-size:9.5px; font-weight:700; text-align:center; padding:5px; letter-spacing:0.4px;">rule_id · FROM GET_CONTEXT</div>
<div style="padding:10px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#2d2926;">GET_CONTEXT(<br>  HWM_RULE_ID, 0)</div>
<div style="font-size:10px; color:#5a544e; margin-top:8px; line-height:1.5;">Identifies which rule triggered this run.</div>
</div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:10px;"><strong style="color:#2d2926;">Together, ffs_id + rule_id form the address</strong> the support team uses to filter production logs to just this worker's submission.</div>

<!-- PART 2: Sentinel values -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · Sentinel values — standing in for "logically empty"</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">THE FAST FORMULA QUIRK</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#2d2926; margin-bottom:6px;">Once a slot exists, it MUST hold a value.</div>
<div style="font-size:10px; color:#5a544e; line-height:1.55;">There is no "declared but contains nothing" state. It either holds something or doesn't exist at all.</div>
<div style="font-size:10.5px; font-weight:700; color:#c0392b; margin-top:10px;">The problem this creates:</div>
<div style="font-size:10px; color:#5a544e; line-height:1.55; margin-top:2px;">Need a way to say "this variable is logically empty" while it still holds something.</div>
</div>
</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">THE SENTINEL FIX</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#2d2926; margin-bottom:6px;">Pick impossible values as stand-ins.</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10.5px; margin:6px 0;">NullDate = '01-JAN-1900'</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10.5px; margin:6px 0;">NullText = '**FF_NULL**'</div>
<div style="font-size:10px; color:#5a544e; line-height:1.55; margin-top:6px;">A date a century in the past or text with double-asterisks — values real data could <strong style="color:#3d7a52;">never</strong> produce. If one reaches a worker's screen, the bug is visible.</div>
</div>
</div>
</div>

<!-- PART 3: Opening log line decoded -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · The opening log line — three segments, each with a job</div>

<div style="overflow-x:auto;">
<div style="display:flex; min-width:520px; margin-bottom:10px;">
<div style="flex:0 0 60px; background:#1f1c19; padding:10px; text-align:center; border:1px solid #1f1c19;">
<div style="font-family:'JetBrains Mono', monospace; font-size:18px; font-weight:700; color:#3d7a52;">>>></div>
</div>
<div style="flex:0 0 90px; background:#2a2825; padding:10px; text-align:center; border:1px solid #1f1c19;">
<div style="font-family:'JetBrains Mono', monospace; font-size:12px; color:#e6e1d8;">Enter</div>
</div>
<div style="flex:1; background:#37322d; padding:10px; text-align:center; border:1px solid #1f1c19;">
<div style="font-family:'JetBrains Mono', monospace; font-size:12px; color:#e6e1d8;">XX_TER_CONTINUOUS_HOURS_VALIDATION</div>
</div>
</div>
<div style="display:flex; min-width:520px; font-size:9.5px;">
<div style="flex:0 0 60px; text-align:center; padding:0 4px;">
<div style="font-weight:700; color:#3d7a52;">grep prefix</div>
<div style="color:#5a544e; margin-top:2px;">filter for entry/exit</div>
</div>
<div style="flex:0 0 90px; text-align:center; padding:0 4px;">
<div style="font-weight:700; color:#5a544e;">verb</div>
<div style="color:#5a544e; margin-top:2px;">"started running"</div>
</div>
<div style="flex:1; text-align:center; padding:0 4px;">
<div style="font-weight:700; color:#1f5fa8;">formula name (ffName)</div>
<div style="color:#5a544e; margin-top:2px;">return-address stamp on every log line in production</div>
</div>
</div>
</div>

<!-- Bottom takeaway -->
<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:3px; margin-top:14px; font-size:10.5px; line-height:1.6;">
<span style="font-family:'JetBrains Mono', monospace; font-weight:700; color:#f0d68a;">TAKEAWAY:</span> Capture session and rule IDs in scope. Tag every log line with the formula name. Future-you, debugging at 11 PM under deadline, will thank present-you for the extra minute.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The formula introduces itself</div>
<ul class="ann-bullets">
<li>The formula starts by recording its own name in a local variable (<code>ffName</code>). This name will travel through every log line the formula writes — effectively a return-address stamp on each entry so you can grep production logs and find every line this specific formula produced.</li>
<li>Two more values come from the framework via <code>GET_CONTEXT</code>. <code>ffs_id</code> is a unique identifier for this <em>specific submission</em> — assigned by OTL the moment the worker clicks Submit. <code>rule_id</code> identifies the validation rule that triggered this formula run.</li>
<li>Together these two IDs are <strong>the address used to look up this run's logs later</strong>. When a worker reports an issue, the support team filters logs by <code>ffs_id</code> and the noise of every other concurrent submission disappears, leaving just this worker's run.</li>
<li>Without these IDs in scope, every <code>add_rlog</code> call that follows would have nowhere to anchor itself — the logs would be untraceable.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>Sentinel values explained</div>
<ul class="ann-bullets">
<li>Fast Formula has a quirk that catches people coming from other languages: <strong>once an array slot exists, it must hold a value</strong>. There is no concept of "this slot has been declared but contains nothing." It either holds something or it doesn't exist at all.</li>
<li>That makes a problem. The formula needs to express "this variable is logically empty" while still holding <em>something</em>. The conventional fix is a sentinel — an impossible value that real data could never produce, used as a stand-in for emptiness.</li>
<li><code>NullDate = '01-JAN-1900'</code> picks a date so far in the past it could never appear on a real timecard. <code>NullText = '**FF_NULL**'</code> uses a string with double-asterisk markers that wouldn't survive any real data-entry process.</li>
<li>The choice of sentinel is deliberate. If you saw <code>'01-JAN-1900'</code> reach a worker's screen, you'd know immediately something went wrong — the value should have been overwritten before output. The sentinel is also a debugging tool: it makes broken code <em>visible</em> instead of letting it propagate silently as <code>NULL</code> would in other languages.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The opening log line</div>
<div class="ann-snippet"><span class="lbl">What appears in production logs</span>>>> Enter XX_TER_CONTINUOUS_HOURS_VALIDATION</div>
<ul class="ann-bullets">
<li>This single line writes a record to the OTL Formula Run Log announcing that the formula has started executing. The triple-arrow prefix (<code>>>></code>) is a convention that makes log entries grep-friendly — you can filter for entry/exit lines and ignore intermediate ones.</li>
<li>The verb <em>"Enter"</em> is paired with a corresponding <em>"Exit"</em> log line at the bottom of the formula, so a complete run shows up as a clean entry-exit pair in the log. Anything between them is intermediate work; anything outside them is somebody else's formula.</li>
<li>The formula name (<code>ffName</code>) acts as a return-address stamp on every subsequent log line. When you have ten formulas attached to one timecard run, this is what tells you which line came from which formula.</li>
<li>Together these three pieces — prefix, verb, formula name — turn a stream of log noise into a structured, filterable trail. The cost is one line of code; the payoff is hours saved during production triage.</li>
</ul>
</div>
<div class="ann-takeaway">Capture session and rule IDs in scope so every subsequent log line can be traced back to its origin. Tag every log line with the formula name. Future-you, debugging a production issue with a tight deadline, will be glad present-you took the extra minute.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="k">CHANGE_CONTEXTS</span>(<span class="v">HR_ASSIGNMENT_ID</span> <span class="op">=</span> <span class="v">HWM_PER_ASG_ASSIGNMENT_ID</span>)
(
  <span class="c">/* entire body lives inside this block */</span></code></pre></div>
<div class="annot-note">
<span class="nt">Block 3 · Single context wrap</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1: Sign-in analogy -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · CHANGE_CONTEXTS = signing in to the worker's session</div>

<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:10px;">
<div style="flex:1; min-width:120px; background:#fff; border:1px solid #1f5fa8; border-radius:4px; padding:10px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#1f5fa8;">SIGN IN</div>
<div style="font-size:10px; color:#5a544e; margin-top:4px;">load profile, set permissions</div>
</div>
<div style="color:#7a7570; font-size:14px;">→</div>
<div style="flex:1; min-width:120px; background:#e8f4ea; border:1px solid #3d7a52; border-radius:4px; padding:10px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#3d7a52;">DO WORK</div>
<div style="font-size:10px; color:#5a544e; margin-top:4px;">read DBI, value sets, etc.</div>
</div>
<div style="color:#7a7570; font-size:14px;">→</div>
<div style="flex:1; min-width:120px; background:#fff; border:1px solid #1f5fa8; border-radius:4px; padding:10px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#1f5fa8;">SIGN OUT</div>
<div style="font-size:10px; color:#5a544e; margin-top:4px;">teardown session</div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic;">Sign-in & sign-out are fixed costs (~2 ms), paid every wrap.</div>

<!-- PART 2: Two strategies -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · Two strategies, same work — the wrap pattern matters</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">STRATEGY A · PER-DBI WRAP — WRONG</div>
<div style="padding:10px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:9.5px; color:#c0392b; line-height:1.7;">CHANGE_CONTEXTS(...) ( DBI[1] )<br>CHANGE_CONTEXTS(...) ( DBI[2] )<br>CHANGE_CONTEXTS(...) ( DBI[3] )<br>    ...<br>CHANGE_CONTEXTS(...) ( DBI[200] )</div>
<hr style="border:none; border-top:1px dashed #c0392b; margin:8px 0;">
<div style="font-size:10.5px; font-weight:700; color:#c0392b;">200 wraps × ~2 ms each</div>
<div style="font-size:11px; font-weight:700; color:#c0392b; margin-top:2px;">= ~400 ms wasted on overhead</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:6px; line-height:1.5;">Most of the time isn't doing work — it's signing in and out, repeatedly.</div>
</div>
</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">STRATEGY B · SINGLE OUTER WRAP — RIGHT</div>
<div style="padding:10px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:9.5px; color:#3d7a52; line-height:1.7;">CHANGE_CONTEXTS(...)<br>(<br>  DBI[1]  DBI[2]  DBI[3]<br>  ...<br>  DBI[200]<br>)</div>
<hr style="border:none; border-top:1px dashed #3d7a52; margin:8px 0;">
<div style="font-size:10.5px; font-weight:700; color:#3d7a52;">1 wrap × ~2 ms total</div>
<div style="font-size:11px; font-weight:700; color:#3d7a52; margin-top:2px;">= ~2 ms total overhead</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:6px; line-height:1.5;">Sign in once, do all the work, sign out at the end.</div>
</div>
</div>
</div>

<!-- PART 3: Performance numbers -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · The performance numbers, in real terms</div>

<div style="margin-bottom:14px;">
<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
<div style="flex:0 0 80px; font-size:10px; font-weight:700; color:#c0392b;">Strategy A:</div>
<div style="flex:1; background:#c0392b; opacity:0.85; height:20px; border-radius:2px;"></div>
<div style="flex:0 0 60px; font-size:10px; font-weight:700; color:#c0392b;">~400 ms</div>
</div>
<div style="display:flex; align-items:center; gap:8px;">
<div style="flex:0 0 80px; font-size:10px; font-weight:700; color:#3d7a52;">Strategy B:</div>
<div style="flex:1; height:20px; position:relative;">
<div style="background:#3d7a52; opacity:0.85; width:0.5%; height:20px; border-radius:2px;"></div>
</div>
<div style="flex:0 0 60px; font-size:10px; font-weight:700; color:#3d7a52;">~2 ms</div>
</div>
<div style="display:flex; justify-content:space-between; margin-top:6px; padding-left:88px; padding-right:68px; font-size:9px; color:#5a544e;">
<span>0 ms</span><span>200 ms</span><span>400 ms</span>
</div>
</div>

<div style="background:#fff5f0; border:1px solid #c0392b; border-radius:3px; padding:10px 14px; margin-bottom:10px;">
<div style="font-size:10.5px; font-weight:700; color:#c0392b; margin-bottom:4px;">SCALE IMPLICATION:</div>
<div style="font-size:10.5px; color:#2d2926; line-height:1.55;">A pay run processes tens of thousands of timecards. At 400 ms wasted per submission, that's <strong>hours of CPU time and database session pressure</strong> across a single batch — enough to delay payroll cutoff.</div>
</div>

<!-- Bottom takeaway -->
<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:3px; margin-top:14px; font-size:10.5px; line-height:1.6;">
<span style="font-family:'JetBrains Mono', monospace; font-weight:700; color:#f0d68a;">TAKEAWAY:</span> One outer CHANGE_CONTEXTS wrap. Tag the closing paren so you can find it 200 lines later. The change is invisible to readers but saves hundreds of milliseconds per submission — and adds up fast across a pay run.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>What CHANGE_CONTEXTS actually does</div>
<ul class="ann-bullets">
<li><code>CHANGE_CONTEXTS</code> binds an HCM context value — in this case, <code>HR_ASSIGNMENT_ID</code> — for everything that runs inside its parentheses. Any DBI fetch, any value-set lookup, any worker-specific resolution that happens within the block automatically gets evaluated against this assignment.</li>
<li>Think of it like signing in to an application. Every sign-in carries a fixed cost: load the profile, validate the session, set up permissions, prime the personalisation cache. None of these are heavy individually, but they add up.</li>
<li>If you signed in, fetched one piece of data, signed out, and repeated this hundreds of times in sequence, most of your time would go to the sign-in/sign-out cycle — not the actual work. The pattern is wasteful.</li>
<li>Database queries inside Fast Formula behave the same way. Each <code>CHANGE_CONTEXTS</code> call has fixed setup and teardown overhead, perhaps two milliseconds. Inside a 200-iteration loop, that overhead compounds.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>Why one outer wrap beats many inner wraps</div>
<ul class="ann-bullets">
<li>The architectural choice is to wrap <strong>the entire formula body</strong> in one outer <code>CHANGE_CONTEXTS</code> at the top, rather than wrapping each individual DBI fetch as it appears.</li>
<li>The formula effectively "signs in" once at the top and stays signed in for the rest of its execution. Every database lookup, every holiday calendar query (<code>GET_VALUE_SET</code>), every <code>PER_*</code> DBI fetch, every worker-specific resolution that happens anywhere in the body automatically uses the same binding without re-binding.</li>
<li>The framework internally optimises for this pattern. A single deep context binding is far cheaper than 200 shallow ones, because most of the binding cost is paid once.</li>
<li>The trade-off is structural: your entire formula body now sits inside one giant pair of parentheses, which can make the code feel disconnected from where it opens. Mitigate by tagging the closing paren with a comment so you can find it when scrolling 200 lines later.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The performance numbers, in real terms</div>
<ul class="ann-bullets">
<li>Per-DBI wrap on a typical biweekly timecard with 200 entries: roughly <strong>400 milliseconds wasted on context-binding overhead alone</strong>, before any actual validation work happens.</li>
<li>Single outer wrap: about <strong>2 milliseconds total</strong>. The same work, 200× faster.</li>
<li>This sounds like a micro-optimisation, but it isn't. A pay run might process tens of thousands of timecards. At 400 ms wasted per submission, that's hours of CPU time and database session pressure across a single batch — enough to delay payroll cutoff in busy enterprises.</li>
<li>The fix costs nothing in code complexity (it's actually simpler), and the performance benefit scales with timecard size.</li>
</ul>
</div>
<div class="ann-takeaway">One outer <code>CHANGE_CONTEXTS</code> wrap binds the assignment context once for the entire formula body. Tag the closing paren with a comment so you can find it later. The change is invisible to readers but saves hundreds of milliseconds per submission — and adds up fast across an entire pay run.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code>  <span class="v">p_break_type</span>    <span class="op">=</span> <span class="s">'Meal Break'</span>
  <span class="v">p_reg_type</span>      <span class="op">=</span> <span class="s">'Regular Hours'</span>

  <span class="v">p_sched_start</span>   <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>,
                       <span class="s">'SCHEDULE_START_HOUR'</span>, <span class="n">9</span>)
  <span class="v">p_sched_end</span>     <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>,
                       <span class="s">'SCHEDULE_END_HOUR'</span>, <span class="n">18</span>)
  <span class="v">p_max_cont_err</span>  <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>,
                       <span class="s">'MAX_CONTINUOUS_HRS_ERR'</span>, <span class="n">6</span>)
  <span class="v">p_max_cont_warn</span> <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>,
                       <span class="s">'MAX_CONTINUOUS_HRS_WARN'</span>, <span class="n">5</span>)</code></pre></div>
<div class="annot-note">
<span class="nt">Block 4 · Per-LE configuration</span>
<div class="ann-excel">
<div class="ax-bar"><span>Per_LE_Parameter_Values.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th>Parameter</th><th>SG</th><th>HK</th><th>IN</th></tr></thead>
<tbody>
<tr><td>SCHEDULE_END_HOUR</td><td class="tc">18</td><td class="tc">17</td><td class="tc">18.5</td></tr>
<tr><td>MAX_CONT_HRS_ERR</td><td class="tc" style="color:#c0392b;font-weight:700;">5</td><td class="tc">6</td><td class="tc" style="color:#c0392b;font-weight:700;">5</td></tr>
<tr><td>MAX_CONT_HRS_WARN</td><td class="tc">4.5</td><td class="tc">5</td><td class="tc">4.5</td></tr>
</tbody>
</table>
</div>
<div class="ann-excel-cap">Same formula. Three rules. Three sets of values. No source change needed.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1: Two categories -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · Two categories of values — what to hardcode vs what to parameterise</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#fff; border:1.5px solid #7a7570; border-radius:4px; overflow:hidden;">
<div style="background:#7a7570; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">HARDCODED · shared across rollout</div>
<div style="padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#5a544e; margin-bottom:4px;">Examples in this formula:</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10px; margin:4px 0;">p_break_type = 'Meal Break'</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10px; margin:4px 0;">p_reg_type   = 'Regular Hours'</div>
<div style="font-size:10.5px; color:#2d2926; margin-top:10px;"><strong>Why hardcode is correct here:</strong></div>
<div style="font-size:10px; color:#5a544e; line-height:1.55; margin-top:2px;">These labels come from OTL's timecard layout, which is identical across every entity.</div>
</div>
</div>
<div style="background:#fff; border:1.5px solid #b97417; border-radius:4px; overflow:hidden;">
<div style="background:#b97417; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">RULE-DRIVEN · varies per LE</div>
<div style="padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#5a544e; margin-bottom:4px;">Examples in this formula:</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:9.5px; margin:4px 0;">p_max_cont_err = get_rvalue_number(...)</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:9.5px; margin:4px 0;">p_sched_start  = get_rvalue_number(...)</div>
<div style="font-size:10.5px; color:#2d2926; margin-top:10px;"><strong>Why parameterise here:</strong></div>
<div style="font-size:10px; color:#5a544e; line-height:1.55; margin-top:2px;">Legal thresholds vary per entity. Must be tunable per LE without touching source.</div>
</div>
</div>
</div>

<!-- PART 2: Multi-entity example -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · Same formula source, three legal entities, three behaviours</div>

<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:10.5px; margin-bottom:10px;">
<span style="color:#f0d68a; font-weight:700;">ONE FORMULA SOURCE:</span> XX_TER_CONTINUOUS_HOURS_VALIDATION<br>
<span style="color:#f0d68a;">  IF (contHrs > p_max_cont_err) THEN flag</span>
</div>

<div style="text-align:center; color:#7a7570; font-size:14px; margin:4px 0;">↓ ↓ ↓</div>

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">
<div style="background:#fff; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">ENTITY A · RULE</div>
<div style="padding:8px 10px; text-align:center;">
<div style="font-size:10px; color:#5a544e;">Statutory 5h cap</div>
<div style="background:#e8f4ea; border:1px solid #3d7a52; padding:5px 8px; margin:6px 0; font-family:'JetBrains Mono', monospace; font-size:10px; color:#3d7a52; font-weight:700;">MAX_CONT_ERR = 5</div>
<div style="font-size:9px; color:#5a544e;">Worker flagged at 5h</div>
</div>
</div>
<div style="background:#fff; border:1.5px solid #1f5fa8; border-radius:4px; overflow:hidden;">
<div style="background:#1f5fa8; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">ENTITY B · RULE</div>
<div style="padding:8px 10px; text-align:center;">
<div style="font-size:10px; color:#5a544e;">Self-imposed 6h policy</div>
<div style="background:#f0f4fa; border:1px solid #1f5fa8; padding:5px 8px; margin:6px 0; font-family:'JetBrains Mono', monospace; font-size:10px; color:#1f5fa8; font-weight:700;">MAX_CONT_ERR = 6</div>
<div style="font-size:9px; color:#5a544e;">Worker flagged at 6h</div>
</div>
</div>
<div style="background:#fff; border:1.5px solid #b97417; border-radius:4px; overflow:hidden;">
<div style="background:#b97417; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">ENTITY C · SUB-RULES</div>
<div style="padding:8px 10px; text-align:center;">
<div style="font-size:10px; color:#5a544e;">Multiple rules, not IF/ELSIF</div>
<div style="background:#fff3e0; border:1px solid #b97417; padding:5px 8px; margin:6px 0; font-family:'JetBrains Mono', monospace; font-size:9.5px; color:#b97417; font-weight:700;">R1:5 / R2:6 / R3:6</div>
<div style="font-size:9px; color:#5a544e;">One rule per region</div>
</div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:10px;"><strong style="color:#2d2926;">No source code change between entities.</strong> Configuration scales; conditional code does not.</div>

<!-- PART 3: Fallback argument -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · The fallback argument — safety net, not production default</div>

<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:11px; margin-bottom:6px; overflow-x:auto;">
get_rvalue_number(rule_id, 'MAX_CONTINUOUS_HRS_ERR', <span style="color:#e07060; font-weight:700;">6</span>)
</div>
<div style="text-align:center; font-size:9.5px; color:#c0392b; font-weight:700; margin-bottom:14px;">↑ FALLBACK · the third arg</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#e8f4ea; border:1px solid #3d7a52; border-radius:3px; padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#3d7a52;">✓ Rule configured properly</div>
<div style="font-size:10px; color:#2d2926; margin-top:4px; line-height:1.5;">Returns the configured value (e.g. 5 for Entity A). Fallback never used. <em>This is normal.</em></div>
</div>
<div style="background:#fff5f0; border:1px solid #c0392b; border-radius:3px; padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#c0392b;">✗ Rule mis-configured / parameter missing</div>
<div style="font-size:10px; color:#2d2926; margin-top:4px; line-height:1.5;">Returns 6. Formula keeps running, doesn't crash. <em>This means a configuration gap to fix.</em></div>
</div>
</div>

<!-- Bottom takeaway -->
<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:3px; margin-top:14px; font-size:10.5px; text-align:center;">
<span style="font-family:'JetBrains Mono', monospace; color:#f0d68a;">Hardcode shared layout. Parameterise per-LE variation. One source, many entities.</span>
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The formula's settings page</div>
<ul class="ann-bullets">
<li>This block is where the formula declares everything that varies across runs — the values it needs but doesn't want to hardcode. Think of it as the settings page for the formula.</li>
<li>Crucially, the values fall into <strong>two distinct categories</strong>, and the difference matters for the formula's portability across legal entities.</li>
<li><strong>Hardcoded values</strong> are written directly into the source: time-type names like <code>'Meal Break'</code> and <code>'Regular Hours'</code>. These match the labels in the OTL timecard layout, which is shared across every entity in the rollout. Hardcoding them is correct because they genuinely don't vary.</li>
<li><strong>Rule-driven values</strong> come from <code>get_rvalue_number</code>, which reads from the rule's parameter configuration: schedule start hour, schedule end hour, continuous-work caps. These values change per legal entity, so they must be tunable without touching the formula source.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>Why this separation makes the formula multi-entity</div>
<ul class="ann-bullets">
<li>The principle: <strong>parameterise per-LE variation; hardcode shared layout.</strong> Get this distinction right and one formula source serves the entire rollout. Get it wrong and you're maintaining one formula per legal entity, with bug-fixes to apply N times.</li>
<li>Consider an entity whose local labour law caps continuous work at 5 hours. Its rule sets <code>MAX_CONTINUOUS_HRS_ERR = 5</code>, and the formula honours that limit for those workers automatically.</li>
<li>Another entity might have no statutory cap; the employer self-imposes 6 hours as company policy. Its rule sets the parameter to 6 and the same formula behaves differently for those workers, without a single line of source change.</li>
<li>A third entity might have nuance: a labour code that varies by region or sub-jurisdiction. The architectural answer is multiple rules, one per sub-jurisdiction, each parameterised independently — never an <code>IF region = 'A' THEN ... ELSIF region = 'B' THEN ... ELSIF</code> chain inside the formula. Configuration scales; conditional code doesn't.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The fallback argument explained</div>
<div class="ann-snippet"><span class="lbl">The third argument</span>get_rvalue_number(rule_id, 'MAX_CONTINUOUS_HRS_ERR', <span style="color:#e07060;">6</span>)
↑
fallback</div>
<ul class="ann-bullets">
<li>The third argument to <code>get_rvalue_number</code> is the fallback value — what the formula uses if the parameter wasn't configured on the rule attached to the worker's processing profile.</li>
<li>The fallback exists as a safety net, not as the production default. Pick a defensible number (here, 6 reflects the most permissive cap in the rollout) so that an accidentally unconfigured rule doesn't break submission entirely — the formula still runs, just with a generic threshold.</li>
<li>But <strong>never rely on the fallback in production</strong>. Always set the parameter explicitly on every LE rule, with the value the legal team has signed off on. The fallback is your last line of defence against a configuration mistake, not a substitute for proper setup.</li>
<li>A useful sanity check during go-live: query the rule configuration for every LE that should be active and confirm the threshold values match your rollout plan. If any LE shows the fallback value, that's a configuration gap.</li>
</ul>
</div>
<div class="ann-takeaway">Hardcode what's shared (layout-driven names). Parameterise what varies (legal thresholds and schedule bounds). One formula source, one rule per legal entity, configuration that scales. Hardcoding a numeric threshold locks the formula to one entity and is the most common architectural mistake in TER design.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code>  <span class="v">OUT_MSG</span> <span class="op">=</span> <span class="v">EMPTY_TEXT_NUMBER</span>

  <span class="v">wMaAry</span> <span class="op">=</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>.<span class="f">count</span>
  <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>,
                  <span class="s">'>>> Start bulk wMaAry='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">wMaAry</span>))

  <span class="v">cntr</span> <span class="op">=</span> <span class="n">0</span>
  <span class="v">nidx</span> <span class="op">=</span> <span class="n">0</span>

  <span class="c">/* day buffer — per-day lifetime */</span>
  <span class="v">dayStarts</span> <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
  <span class="v">dayStops</span>  <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
  <span class="v">dayIdxs</span>   <span class="op">=</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
  <span class="v">dayCnt</span>    <span class="op">=</span> <span class="n">0</span>

  <span class="c">/* stretch tracker — per-stretch lifetime */</span>
  <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">NullDate</span>
  <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">NullDate</span>
  <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'N'</span>

  <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>

  <span class="k">WHILE</span> (<span class="v">cntr</span> <span class="op"><</span> <span class="v">wMaAry</span>) <span class="k">LOOP</span> (
    <span class="v">cntr</span> <span class="op">=</span> <span class="v">cntr</span> <span class="op">+</span> <span class="n">1</span>
    <span class="c">/* per-line reset only */</span>
    <span class="v">aiTimeType</span>  <span class="op">=</span> <span class="v">NullText</span>
    <span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">NullDate</span>
    ...</code></pre></div>
<div class="annot-note">
<span class="nt">Block 5 · Three lifetimes</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three lifetimes coexist in one block</div>

<!-- PART 1: The three lifetime groups -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · Three groups of variables, three different reset triggers</div>

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px;">
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">PER-ROW SCRATCH</div>
<div style="padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#5a544e;">Variables:</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#3d7a52; line-height:1.6; margin-top:2px;">aiTimeType<br>aiStartTime, aiStopTime<br>aiRecPos, aiMeasure<br>l_qty_only</div>
<div style="font-size:10px; font-weight:700; color:#5a544e; margin-top:10px;">Reset trigger:</div>
<div style="font-size:10px; font-weight:700; color:#3d7a52; margin-top:2px;">Every iteration of WHILE loop</div>
<div style="font-size:9.5px; color:#5a544e; font-style:italic; margin-top:2px;">at the top, before reading row</div>
</div>
</div>
<div style="background:#fff3e0; border:1.5px solid #b97417; border-radius:4px; overflow:hidden;">
<div style="background:#b97417; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">PER-DAY STATE</div>
<div style="padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#5a544e;">Variables:</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#b97417; line-height:1.6; margin-top:2px;">dayStarts, dayStops<br>dayIdxs, dayCnt<br>stretchStart, stretchEnd<br>inStretch, l_meal_taken</div>
<div style="font-size:10px; font-weight:700; color:#5a544e; margin-top:10px;">Reset trigger:</div>
<div style="font-size:10px; font-weight:700; color:#b97417; margin-top:2px;">END_DAY marker (Block 7)</div>
<div style="font-size:9.5px; color:#5a544e; font-style:italic; margin-top:2px;">stretch also resets on Meal Break</div>
</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">FORMULA-WIDE</div>
<div style="padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#5a544e;">Variables:</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#c0392b; line-height:1.6; margin-top:2px;">OUT_MSG<br>cntr, nidx<br>wMaAry</div>
<div style="font-size:10px; font-weight:700; color:#5a544e; margin-top:10px;">Reset trigger:</div>
<div style="font-size:10px; font-weight:700; color:#c0392b; margin-top:2px;">Never reset after init</div>
<div style="font-size:9.5px; color:#5a544e; font-style:italic; margin-top:2px;">persist until formula returns</div>
</div>
</div>
</div>

<!-- PART 2: Timeline visualization -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · Timeline view — when each group resets through Sarah's submission</div>

<div style="overflow-x:auto;">
<table style="border-collapse:collapse; font-size:10px; min-width:560px;">
<thead>
<tr>
<th style="padding:4px 8px; text-align:left; color:#5a544e; font-weight:700;">Iter:</th>
<th style="padding:4px 8px; background:#fff; border:1px solid #999; text-align:center; color:#5a544e;">[1] HEADER</th>
<th style="padding:4px 8px; background:#fff; border:1px solid #999; text-align:center; color:#5a544e;">[2] Reg</th>
<th style="padding:4px 8px; background:#fff; border:1px solid #999; text-align:center; color:#5a544e;">[3] Reg</th>
<th style="padding:4px 8px; background:#fff; border:1px solid #999; text-align:center; color:#5a544e;">[4] Meal</th>
<th style="padding:4px 8px; background:#fce8e8; border:1px solid #c0392b; text-align:center; color:#c0392b; font-weight:700;">[5] END_DAY</th>
<th style="padding:4px 8px; background:#fff; border:1px solid #999; text-align:center; color:#5a544e;">[6] Reg</th>
<th style="padding:4px 8px; background:#fce8e8; border:1px solid #c0392b; text-align:center; color:#c0392b; font-weight:700;">[7] END_PERIOD</th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding:4px 8px; font-weight:700; color:#3d7a52;">Row:</td>
<td style="padding:4px 8px; background:#e8f4ea; border:1px solid #3d7a52; text-align:center; font-weight:700; color:#3d7a52;">R</td>
<td style="padding:4px 8px; background:#e8f4ea; border:1px solid #3d7a52; text-align:center; font-weight:700; color:#3d7a52;">R</td>
<td style="padding:4px 8px; background:#e8f4ea; border:1px solid #3d7a52; text-align:center; font-weight:700; color:#3d7a52;">R</td>
<td style="padding:4px 8px; background:#e8f4ea; border:1px solid #3d7a52; text-align:center; font-weight:700; color:#3d7a52;">R</td>
<td style="padding:4px 8px; background:#e8f4ea; border:1px solid #3d7a52; text-align:center; font-weight:700; color:#3d7a52;">R</td>
<td style="padding:4px 8px; background:#e8f4ea; border:1px solid #3d7a52; text-align:center; font-weight:700; color:#3d7a52;">R</td>
<td style="padding:4px 8px; background:#e8f4ea; border:1px solid #3d7a52; text-align:center; font-weight:700; color:#3d7a52;">R</td>
<td style="padding:4px 8px; font-size:9px; color:#3d7a52; font-style:italic; white-space:nowrap;">every iter</td>
</tr>
<tr>
<td style="padding:4px 8px; font-weight:700; color:#b97417;">Day:</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #b97417; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #b97417; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #b97417; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #b97417; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff3e0; border:1.5px solid #b97417; text-align:center; font-weight:700; color:#b97417;">R</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #b97417; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #b97417; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; font-size:9px; color:#b97417; font-style:italic; white-space:nowrap;">at END_DAY</td>
</tr>
<tr>
<td style="padding:4px 8px; font-weight:700; color:#c0392b;">F:</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #c0392b; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #c0392b; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #c0392b; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #c0392b; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #c0392b; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #c0392b; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; background:#fff; border:1px solid #c0392b; text-align:center; color:#999;">·</td>
<td style="padding:4px 8px; font-size:9px; color:#c0392b; font-style:italic; white-space:nowrap;">never</td>
</tr>
</tbody>
</table>
</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:8px;">Legend: <strong style="color:#3d7a52;">R</strong> = reset happens here. Each row's pattern shows the cadence for that group's variables.</div>

<!-- PART 3: The bug pattern -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · What goes wrong if you reset the wrong group</div>

<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">THE BUG: forgetting to reset per-row variables between iterations</div>
<div style="padding:12px 14px;">
<div style="font-size:10.5px; font-weight:700; color:#2d2926;">Scenario:</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:4px; line-height:1.55;">Iteration 4 reads a Reg Hours row and sets <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">aiTimeType = 'Regular Hours'</code>.</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:2px; line-height:1.55;">Iteration 5 hits a HEADER row that has <em>no</em> time type.</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:2px; line-height:1.55;">The read in iteration 5 doesn't overwrite <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">aiTimeType</code>...</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:8px 12px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10px; margin:10px 0; line-height:1.6;">
<span style="color:#e07060;">// iteration 5, HEADER row read:</span><br>
IF (PayrollTimeType.exists(5)) THEN aiTimeType = ... <span style="color:#b8b0a0;">// skipped, no value</span>
</div>
<div style="font-size:10.5px; color:#c0392b; font-weight:700;">Result: aiTimeType STILL holds 'Regular Hours' from iteration 4.</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:4px; line-height:1.55;">Downstream checks evaluate against stale data and silently produce wrong results.</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:4px;">No crash. No error. Just wrong validation, hard to trace.</div>
</div>
</div>

<!-- PART 4: The fix -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 4 · The fix — reset per-row scratch at the loop top</div>

<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10.5px; overflow-x:auto;">
aiTimeType = NullText; aiStartTime = NullDate; aiStopTime = NullDate; l_qty_only = 'N'
</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:8px;">Reset only per-row scratch. Day-level state stays alive across iterations — that's intentional.</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>Initialising the output array</div>
<div class="ann-snippet">OUT_MSG = EMPTY_TEXT_NUMBER</div>
<ul class="ann-bullets">
<li><code>OUT_MSG</code> is the formula's return value — a sparse array indexed by timecard row number, where each populated slot becomes a red error marker on the worker's screen.</li>
<li>Initialising it as <code>EMPTY_TEXT_NUMBER</code> means the array exists but holds no entries. Validation logic later in the loop only writes to slots where it finds problems — clean rows never get a slot at all.</li>
<li>This <strong>sparse output pattern</strong> is intentional. A dense array (one entry per row, with empty strings for clean rows) would force the framework to walk every slot looking for messages. The sparse array lets the framework iterate only over flagged rows, which is faster and cleaner.</li>
<li>The formula doesn't explicitly return <code>OUT_MSG</code> at the bottom — Fast Formula returns it implicitly because it's declared as the output of this formula type. The framework reads whatever's in <code>OUT_MSG</code> at the moment the formula completes.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>Measuring the input and announcing the run</div>
<div class="ann-snippet">wMaAry = HWM_CTXARY_RECORD_POSITIONS.count
rLog   = add_rlog(..., '>>> Start bulk wMaAry=' || TO_CHAR(wMaAry))</div>
<ul class="ann-bullets">
<li><code>.count</code> on a Fast Formula array returns the number of populated slots. <code>wMaAry</code> is short for "while-max-array" — the upper bound for the WHILE loop. Without this, the loop wouldn't know when to stop.</li>
<li>The framework guarantees <code>RECORD_POSITIONS</code> is populated for every row the worker has on their timecard, including marker rows. So <code>RECORD_POSITIONS.count</code> reliably gives the total row count for any timecard.</li>
<li>The "Start bulk" log line is more useful than it looks. In production, this is the line that confirms <em>the formula actually received data and how much</em>. If a worker reports a problem and the log shows <code>wMaAry = 0</code>, you immediately know the timecard arrived empty — the bug isn't in your validation logic, it's upstream.</li>
<li>The <code>>>></code> prefix is a grep-friendly convention. Filtering production logs for entry/exit lines becomes a one-second task.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>Why two counters, not one</div>
<div class="ann-snippet">cntr = 0   <span style="color:#d4c896;">// drives loop termination</span>
nidx = 0   <span style="color:#d4c896;">// indexes into input arrays</span></div>
<ul class="ann-bullets">
<li>In this version of the formula, <code>cntr</code> and <code>nidx</code> always advance together — both increment by 1 every iteration. So why have two?</li>
<li>The reason is intent-based separation. <code>cntr</code> describes <em>"how many iterations have I completed?"</em> — it drives loop termination. <code>nidx</code> describes <em>"which row am I currently reading?"</em> — it's an index into the input arrays.</li>
<li>Today these are the same number, but they encode different ideas. Future enhancements that add skip-ahead logic (for example, processing a HEADER row's children together as a unit) would advance <code>nidx</code> without advancing <code>cntr</code>, or vice versa. Maintaining the distinction now leaves room for those changes without restructuring the loop.</li>
<li>This is a small example of writing code that documents its own intent. The variables are named for what they <em>mean</em>, not what they <em>do</em> — and the naming pays dividends when the code evolves.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">4</span>The day buffer — per-day lifetime</div>
<div class="ann-snippet">dayStarts = EMPTY_DATE_NUMBER
dayStops  = EMPTY_DATE_NUMBER
dayIdxs   = EMPTY_NUMBER_NUMBER
dayCnt    = 0</div>
<ul class="ann-bullets">
<li>The day buffer is a holding area for Regular Hours entries within a single day. As the loop encounters real Reg Hours rows, it appends each one's start time, stop time, and original row index to these three parallel arrays.</li>
<li>The buffer accumulates across iterations until the loop hits an <code>END_DAY</code> marker. At that point, Block 7 takes over: it tests every pair of buffered entries for time overlap, fires errors on conflicts, and clears the buffer for the next day.</li>
<li><strong><code>dayIdxs</code> is the architectural insight in this group.</strong> The buffer's internal indexing is sequential (1, 2, 3...) but those indexes don't match the worker's view. On a real timecard, the same Reg Hours entries might appear at row positions [2], [4], and [7] — with markers and other time types in between.</li>
<li>Without <code>dayIdxs</code>, when the overlap test detects a conflict between buffer entries 2 and 3, the formula would have no way to translate that back into the worker's row numbers. Errors would land on the wrong rows, confusing the worker. <code>dayIdxs</code> is the chain of custody that connects buffer indexes to original timecard indexes.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">5</span>The stretch tracker — per-stretch lifetime</div>
<div class="ann-snippet">stretchStart = NullDate
stretchEnd   = NullDate
inStretch    = 'N'</div>
<ul class="ann-bullets">
<li>The stretch tracker measures the longest unbroken run of Regular Hours work, used by Block 8 to enforce the continuous-work cap (legally typically 5 or 6 hours).</li>
<li>Unlike the day buffer, the stretch tracker has a <strong>different reset trigger</strong>. It resets when one of two things happens: the worker takes a meal break (proving continuous work was interrupted) or the day ends.</li>
<li>This dual-reset behaviour mirrors the legal definition. The cap measures uninterrupted work; eating interrupts it; the next stretch is a fresh start. Resetting only at end-of-day would miss the meal-break case and produce a falsely-too-large stretch value.</li>
<li>The three variables work as a unit: <code>inStretch</code> is the on/off switch ('Y' means a stretch is currently active), and <code>stretchStart</code>/<code>stretchEnd</code> hold the start and end times of that stretch. When all three reset, the tracker is off and waiting for the next qualifying entry.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">6</span>The day-level meal flag</div>
<div class="ann-snippet">l_meal_taken = 'N'</div>
<ul class="ann-bullets">
<li>This single-character flag has outsized importance. It tracks whether the worker has logged a meal break <em>at any point during the current day</em>.</li>
<li>When Block 6 detects a meal break, it flips this flag to <code>'Y'</code>. Block 8's continuous-hours gate checks this flag; if it's <code>'Y'</code>, the gate stays closed and the stretch tracker silently stops counting for the rest of the day.</li>
<li>The reasoning is legal: the cap measures continuous work <em>before a meal</em>. Once the meal happens, the worker has interrupted the run that mattered for compliance. Continuing to track stretches afterward would generate noise without legal meaning.</li>
<li>The flag resets at every <code>END_DAY</code> so each new day starts fresh — tomorrow's tracking is independent of today's meal status.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">7</span>The per-row reset inside the loop</div>
<div class="ann-snippet">WHILE (cntr < wMaAry) LOOP (
cntr = cntr + 1
aiTimeType  = NullText
aiStartTime = NullDate
...</div>
<ul class="ann-bullets">
<li>This is the line that catches developers coming from other languages. <strong>Fast Formula does not automatically clear local variables between loop iterations.</strong> Whatever value a variable held at the end of iteration N is still there at the start of iteration N+1, unless explicitly overwritten.</li>
<li>The bug pattern: iteration 4 reads a Regular Hours row and sets <code>aiTimeType = 'Regular Hours'</code>. Iteration 5 hits a HEADER row that has no time type. The read in iteration 5 doesn't overwrite <code>aiTimeType</code>, so the variable still holds <code>'Regular Hours'</code>. Downstream checks evaluate against stale data and silently produce wrong results.</li>
<li>This is the worst kind of bug to debug because it doesn't crash. The formula runs, returns output, but the output is subtly wrong. UAT data rarely exposes it; production data eventually does.</li>
<li>The fix is explicit: at the top of every iteration, reset the per-row scratch variables (<code>aiTimeType</code>, <code>aiStartTime</code>, <code>aiStopTime</code>, <code>l_qty_only</code>) to their sentinel values before reading the new row. This guarantees a clean slate.</li>
<li><strong>Critical distinction:</strong> only reset per-row scratch here. Day-level state (the day buffer, the stretch tracker, the meal flag) is <em>supposed</em> to live across iterations — resetting them by mistake breaks the algorithm in ways that are nearly impossible to trace. Two categories, never confused.</li>
</ul>
</div>
<div class="ann-takeaway">Three lifetimes coexist in this block: per-row scratch (reset every iteration at the loop top), per-day state (reset at <code>END_DAY</code>), and the output array (never reset, persists until return). The boundaries between these lifetimes are where the formula's correctness lives. Reset the wrong group at the wrong moment and validation breaks subtly — loud crashes are easier to fix than silent wrongness.</div>
</div></div>
</div>
</div>

</div>
</div>

<p>That's the entire setup phase. From here, every iteration of the WHILE loop classifies one row and routes it through the right validation. The remaining three blocks — per-line processing, day-boundary work, and the continuous-hours state machine — are where the algorithmic decisions live, so each gets a focused deep-dive below.</p>

<h2>The Algorithm — What Happens Inside the Loop</h2>

<p class="section-lead">Three blocks carry the actual validation logic. They live inside the WHILE loop, executing once per timecard row:</p>

<ul>
<li><strong>Block 6</strong> reads each row, identifies whether it's a real entry or a marker, and routes it to the right validation based on its time type.</li>
<li><strong>Block 7</strong> fires only at day boundaries. When it sees an END_DAY marker, it tests every Reg Hours entry from that day against every other one to detect time overlaps.</li>
<li><strong>Block 8</strong> maintains a small state machine that survives across iterations, tracking the longest unbroken stretch of Reg Hours work to enforce the legal cap on continuous work.</li>
</ul>

<p>Each annotation below pairs the formula code with a numbered breakdown of what's happening, plus an Excel snippet showing the data being operated on.</p>

<h3>Per-Line Routing & Qty-Only Detection</h3>

<p>Block 6 is the formula's <strong>switchboard</strong>. Every iteration of the loop comes through here first. The block reads the current row's data into local variables, classifies the row by time type, and decides which downstream validation it needs.</p>

<h4>The routing decision tree</h4>

<p>Before reading the code, look at the routing structure. Every timecard row falls into one of five paths based on two questions: <em>"is this a marker row?"</em> and <em>"what's the time type?"</em> The diagram below shows every possible path:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-3/diagram-1.png" alt="Diagram 1: Oracle Fast Formula: Time Entry Rule (Part 3)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>Five paths, each with clear next-steps. Path 1 (markers) routes to Block 7 for day-boundary work. Paths 2 and 4 fire flags directly inside Block 6. Path 3 (the most common) feeds the day buffer and the state machine. Path 5 is the silent default for time types this formula doesn't validate.</p>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Practitioner's tip</div>
Path 5 is where most TER scope-creep comes from. A client says "we also need to validate Annual Leave is at least 0.5 days" and the developer's reflex is to add a fifth or sixth time-type branch to Block 6. <strong>Resist this.</strong> Each new path adds complexity and obscures the existing logic. If you have multiple validation domains, write multiple TER formulas and attach them via separate rules — OTL supports this cleanly. Keep each formula's routing tree small enough to fit on one diagram.
</div>

<h4>The annotated code</h4>

<p>With the routing tree in mind, here's the actual code, annotated block by block:</p>

<div class="annot-wrap">
<div class="annot-head">
<span>Block 6 · Per-line processing</span>
<span class="label-right">Annotated</span>
</div>
<div class="annot-body">

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="c">/* read this row's data into local variables */</span>
<span class="k">IF</span> (<span class="v">RECORD_POSITIONS</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiRecPos</span> <span class="op">=</span> <span class="v">RECORD_POSITIONS</span>[<span class="v">nidx</span>]
<span class="k">IF</span> (<span class="v">PayrollTimeType</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">PayrollTimeType</span>[<span class="v">nidx</span>]
<span class="k">IF</span> (<span class="v">StartTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">StartTime</span>[<span class="v">nidx</span>]
<span class="k">IF</span> (<span class="v">StopTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiStopTime</span> <span class="op">=</span> <span class="v">StopTime</span>[<span class="v">nidx</span>]</code></pre></div>
<div class="annot-note">
<span class="nt">Block 6a · Defensive reads</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · What the .exists() guard is protecting against</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">NAIVE READ — CRASHES</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#5a544e;">Code:</div>
<div style="background:#1f1c19; color:#e07060; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10.5px; margin:4px 0 10px;">aiStartTime = StartTime[1]</div>
<div style="font-size:10.5px; font-weight:700; color:#5a544e;">[1] is HEADER — no value:</div>
<div style="font-size:10.5px; color:#c0392b; font-weight:700; margin-top:6px; line-height:1.7;">✗ FF doesn't return null<br>✗ FF throws an exception<br>✗ Submission lost</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:6px;">Worker must re-enter everything</div>
</div>
</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">GUARDED READ — SAFE</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#5a544e;">Code:</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10.5px; margin:4px 0 10px;">IF (StartTime.exists(1)) THEN<br>  aiStartTime = StartTime[1]</div>
<div style="font-size:10.5px; font-weight:700; color:#5a544e;">[1] is HEADER — no value:</div>
<div style="font-size:10.5px; color:#3d7a52; font-weight:700; margin-top:6px; line-height:1.7;">✓ .exists(1) returns FALSE<br>✓ Read is skipped<br>✓ aiStartTime keeps sentinel</div>
</div>
</div>
</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · Why both DEFAULT FOR and .exists() — two layers, two failure modes</div>

<div style="background:#fff; border:1.5px solid #1f5fa8; border-radius:4px; overflow:hidden; margin-bottom:10px;">
<div style="display:flex; flex-wrap:wrap;">
<div style="flex:1; min-width:160px; background:#dbe5f4; padding:14px 16px; border-right:1.5px solid #1f5fa8; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#1f5fa8;">LAYER 1</div>
<div style="font-size:13px; font-weight:700; color:#2d2926; margin-top:2px;">DEFAULT FOR</div>
<div style="font-size:9px; color:#5a544e; margin-top:2px;">at INPUTS ARE level</div>
</div>
<div style="flex:3; padding:12px 16px;">
<div style="font-size:10px; font-weight:700; color:#5a544e;">Protects against:</div>
<div style="font-size:10.5px; color:#2d2926; margin-top:3px;">The whole array variable being unbound or empty.</div>
<div style="font-size:9.5px; color:#5a544e; font-style:italic; margin-top:4px;">Without this, the formula can't even start.</div>
</div>
</div>
</div>

<div style="background:#fff; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="display:flex; flex-wrap:wrap;">
<div style="flex:1; min-width:160px; background:#cfe6d6; padding:14px 16px; border-right:1.5px solid #3d7a52; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#3d7a52;">LAYER 2</div>
<div style="font-size:13px; font-weight:700; color:#2d2926; margin-top:2px;">.exists(idx)</div>
<div style="font-size:9px; color:#5a544e; margin-top:2px;">at per-slot level</div>
</div>
<div style="flex:3; padding:12px 16px;">
<div style="font-size:10px; font-weight:700; color:#5a544e;">Protects against:</div>
<div style="font-size:10.5px; color:#2d2926; margin-top:3px;">Individual slots being absent within a valid array.</div>
<div style="font-size:9.5px; color:#5a544e; font-style:italic; margin-top:4px;">The array is bound; this index just isn't populated.</div>
</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:10px;"><strong style="color:#2d2926;">Belt and braces:</strong> in code that gates payroll, redundancy is a feature. Both layers are cheap; both are non-negotiable.</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · The ai* naming convention — snapshot pattern</div>

<div style="display:grid; grid-template-columns:1fr auto 1fr auto 1.5fr; gap:8px; align-items:center;">
<div style="background:#dbe5f4; border:1.5px solid #1f5fa8; border-radius:4px; padding:10px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#1f5fa8;">FRAMEWORK INPUT</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#2d2926; margin-top:4px;">StartTime[nidx]</div>
<div style="font-size:9px; color:#5a544e; margin-top:2px;">read once</div>
</div>
<div style="color:#7a7570; font-size:14px;">→</div>
<div style="background:#fff3e0; border:1.5px solid #b97417; border-radius:4px; padding:10px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#b97417;">LOCAL SNAPSHOT</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#2d2926; margin-top:4px;">aiStartTime</div>
<div style="font-size:9px; color:#5a544e; margin-top:2px;">"array input"</div>
</div>
<div style="color:#7a7570; font-size:14px;">→</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; padding:10px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#3d7a52;">REST OF ITERATION</div>
<div style="font-size:9.5px; color:#2d2926; margin-top:4px;">Block 6b/c/d/e, Block 7, Block 8</div>
<div style="font-size:9px; color:#5a544e; margin-top:2px;">all reference aiStartTime, never StartTime</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; margin-top:12px; line-height:1.6;">
<strong style="color:#2d2926;">Why copy? Three reasons:</strong><br>
• <strong>Consistent snapshot</strong> — rest of iteration sees one value, not whatever the array might be next time<br>
• <strong>Single source of update</strong> — if framework input changes, only the read block needs editing<br>
• <strong>Code review signal</strong> — <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ai*</code> on the left of an assignment instantly tells reader "this is per-row data"
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>What the guard is protecting against</div>
<ul class="ann-bullets">
<li>Recall the input shape from Block 1: the framework hands the formula six parallel arrays, but not every row populates every array. Marker rows (HEADER, END_DAY, END_PERIOD) only carry a value in <code>RECORD_POSITIONS</code>. Their slots in <code>StartTime</code>, <code>StopTime</code>, <code>PayrollTimeType</code>, and <code>measure</code> are simply absent.</li>
<li>If the formula naively reads <code>StartTime[nidx]</code> when <code>nidx</code> points at a marker row, it's asking for data that isn't there. <strong>Fast Formula doesn't return null in that case — it throws.</strong> The submission fails with an unhandled exception, and you've lost the worker's timecard.</li>
<li>The <code>.exists(nidx)</code> method is the safe-read pattern. It asks <em>"does this array actually have a value at this index?"</em> as a boolean. If yes, read; if no, skip the read entirely and let the local variable keep its previously-reset value (which Block 5's per-row reset just made into a clean sentinel).</li>
<li>Notice every input read in this block follows the same pattern: check first, then read. There's no shortcut path that skips the check — the discipline is total because the cost of forgetting it is total (a crashed run).</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>Why both DEFAULT FOR and .exists()</div>
<ul class="ann-bullets">
<li>Block 1's <code>DEFAULT FOR</code> declarations and these <code>.exists()</code> checks might seem redundant — both protect against the same problem. But they operate at different levels of the stack and catch different failure modes.</li>
<li><strong>DEFAULT FOR</strong> protects against the array variable itself being unbound or empty at runtime. Without it, the formula can't even start the loop — the framework can't bind the input.</li>
<li><strong>.exists()</strong> protects against individual slots being unpopulated within an otherwise valid array. The array is bound and has some data; this particular index just isn't one of them.</li>
<li>Belt and braces. In safety-critical code paths — and validation that gates payroll qualifies — redundancy is a feature, not a bug. The runtime cost is negligible; the safety benefit is total.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The "ai" naming convention and why it matters</div>
<ul class="ann-bullets">
<li>The variables that receive the read values use an <code>ai</code> prefix — <code>aiRecPos</code>, <code>aiTimeType</code>, <code>aiStartTime</code>, <code>aiStopTime</code>. The prefix stands for <strong>"array input"</strong>, signalling at a glance that these are local copies of input array values for the current iteration.</li>
<li>Why copy at all? Why not just read directly from the input arrays everywhere? Because copying creates a <strong>consistent snapshot</strong>. Once the read block finishes, the rest of the iteration uses these local variables. If anywhere later in the loop body something tweaks the read pattern (or someone refactors), there's a single place to update — the read block at the top of the iteration — not 30 scattered references.</li>
<li>The convention also reads well in code review. Seeing <code>ai*</code> on the left of an assignment in the read block is one signal; using those same locals everywhere else carries that signal forward. The naming makes the data flow obvious.</li>
<li>If the framework's input array structure ever changes (a future OTL release renames or restructures something), only this read block needs updating. The downstream code, already working in terms of <code>ai*</code> locals, doesn't need to know.</li>
</ul>
</div>
<div class="ann-takeaway">Every input array read in this formula is wrapped in <code>.exists()</code>, and every read populates a local <code>ai*</code> variable rather than working directly off the input. Two patterns; both contribute to robustness. Forget the guard on even one read and the next marker row crashes the submission — and marker rows are guaranteed to appear in any production timecard.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="c">/* qty-only detection — placeholder vs real punch */</span>
<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span>
    <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span>
    <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
( <span class="v">l_st_hr</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'HH24'</span>))
            <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
  <span class="v">l_sp_hr</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'HH24'</span>))
            <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
  <span class="k">IF</span> (<span class="v">l_st_hr</span> <span class="op"><</span> <span class="n">0.01</span> <span class="k">AND</span> <span class="v">l_sp_hr</span> <span class="op">></span> <span class="n">23.9</span>) <span class="k">THEN</span>
  ( <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'Y'</span> )
)</code></pre></div>
<div class="annot-note">
<span class="nt">Block 6b · Pattern match</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Four concepts together</div>

<!-- PART 1: Data shape — real vs qty-only -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The two data shapes — same hours, different reality</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:18px;">
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">REAL PUNCH (clean shape)</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#5a544e; margin-bottom:4px;">Worker entered:</div>
<div style="background:#fff; border:1px solid #3d7a52; padding:4px 6px; font-family:'JetBrains Mono', monospace; font-size:10.5px; color:#2d2926;">Reg Hours · 09:00 → 17:00 · 8h</div>
<div style="font-size:10.5px; font-weight:700; color:#3d7a52; margin-top:8px;">✓ Specific work at specific times</div>
<div style="font-size:10px; color:#5a544e; margin-top:2px;">Real interval. Goes to overlap test, stretch tracker.</div>
</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">QTY-ONLY (placeholder shape)</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#5a544e; margin-bottom:4px;">Worker entered:</div>
<div style="background:#fff; border:1px solid #c0392b; padding:4px 6px; font-family:'JetBrains Mono', monospace; font-size:10.5px; color:#2d2926;">Reg Hours · 8h <span style="color:#c0392b;">(no times)</span></div>
<div style="font-size:10.5px; font-weight:700; color:#c0392b; margin-top:8px;">✗ Layout fills 00:00 → 23:59</div>
<div style="font-size:10px; color:#5a544e; margin-top:2px;">Fake interval. Hides overlaps from later blocks.</div>
</div>
</div>
</div>

<!-- PART 2: Fractional-hour conversion -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · The fractional-hour conversion trick</div>

<div style="background:#1f1c19; color:#e6e1d8; padding:12px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:11px; line-height:1.6; margin-bottom:10px; overflow-x:auto;">
l_st_hr = TO_NUMBER(TO_CHAR(t,'HH24')) + TO_NUMBER(TO_CHAR(t,'MI'))/60
</div>
<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; font-size:10.5px;">
<div style="background:#fff; border:1px solid #e8e3d8; padding:8px 10px; border-radius:3px;">
<div style="font-weight:700; color:#1f5fa8;">09:30</div>
<div style="color:#5a544e;">becomes <strong>9.5</strong></div>
</div>
<div style="background:#fff; border:1px solid #e8e3d8; padding:8px 10px; border-radius:3px;">
<div style="font-weight:700; color:#1f5fa8;">17:45</div>
<div style="color:#5a544e;">becomes <strong>17.75</strong></div>
</div>
<div style="background:#fff; border:1px solid #e8e3d8; padding:8px 10px; border-radius:3px;">
<div style="font-weight:700; color:#1f5fa8;">00:00</div>
<div style="color:#5a544e;">becomes <strong>0.0</strong></div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:8px;">Single decimal number means a single comparison can detect the qty-only pattern.</div>

<!-- PART 3: The 0.01 / 23.9 buffer -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · Why <em style="font-style:normal; font-family:'JetBrains Mono', monospace;">0.01</em> and <em style="font-style:normal; font-family:'JetBrains Mono', monospace;">23.9</em>, not exactly 0 and 24</div>

<div style="background:#fff8e8; border-left:3px solid #b97417; padding:10px 14px; margin-bottom:10px; border-radius:0 3px 3px 0; font-size:11.5px; line-height:1.6; color:#2d2926;">
What <em>should</em> be 0.0 after TO_NUMBER conversion can end up as 0.0000003 due to IEEE 754 floating-point drift. Strict equality <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">l_st_hr = 0</code> would silently fail.
</div>
<div style="background:#1f1c19; color:#e6e1d8; padding:10px 12px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:11px; margin-bottom:10px; overflow-x:auto;">
IF (l_st_hr < 0.01 AND l_sp_hr > 23.9) THEN l_qty_only = 'Y'
</div>
<div style="font-size:10.5px; color:#5a544e; line-height:1.55;">
Buffer windows: anything from <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">00:00:00</code> to <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">~00:00:36</code> reads as "near zero"; anything from <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">23:54</code> onward reads as "near end". Wide enough to absorb drift, narrow enough that no real punch can fall there.
</div>

<!-- PART 4: What happens after the flag — 3 consumers -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 4 · What happens after the flag — one detector, three consumers</div>

<div style="background:#fff; border:1px dashed #b97417; padding:10px 12px; border-radius:3px; margin-bottom:10px; text-align:center;">
<div style="font-size:10px; letter-spacing:1.4px; color:#b97417; text-transform:uppercase; font-weight:700;">Detector</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:12px; font-weight:700; color:#2d2926; margin-top:4px;">l_qty_only = 'Y'</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:2px;">single-char flag, set once</div>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; padding:10px;">
<div style="font-size:10px; font-weight:700; color:#c0392b; letter-spacing:0.6px;">CONSUMER 1</div>
<div style="font-size:10.5px; font-weight:700; color:#2d2926; margin-top:2px;">Block 6c</div>
<div style="font-size:10px; color:#5a544e; margin-top:6px; line-height:1.5;">Fires error: <em>"real punches required"</em>. Treats qty-only as missing punch.</div>
</div>
<div style="background:#f0f4fa; border:1.5px solid #1f5fa8; border-radius:4px; padding:10px;">
<div style="font-size:10px; font-weight:700; color:#1f5fa8; letter-spacing:0.6px;">CONSUMER 2</div>
<div style="font-size:10.5px; font-weight:700; color:#2d2926; margin-top:2px;">Block 6d</div>
<div style="font-size:10px; color:#5a544e; margin-top:6px; line-height:1.5;">Excludes from day buffer. No fake interval in overlap test.</div>
</div>
<div style="background:#fff8e8; border:1.5px solid #b97417; border-radius:4px; padding:10px;">
<div style="font-size:10px; font-weight:700; color:#b97417; letter-spacing:0.6px;">CONSUMER 3</div>
<div style="font-size:10.5px; font-weight:700; color:#2d2926; margin-top:2px;">Block 8</div>
<div style="font-size:10px; color:#5a544e; margin-top:6px; line-height:1.5;">Excludes from stretch tracker. Don't count placeholder hours.</div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:10px; text-align:center;">One detector decides; three consumers respond. Each block stays focused on its own logic.</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The data shape this block exists to detect</div>
<ul class="ann-bullets">
<li>OTL's timecard layout typically allows two ways to log Regular Hours. The clean way is to enter explicit punch times: start at 09:00, stop at 17:30. The shortcut way is to enter just a quantity — "8 hours" — and let the system figure out the rest.</li>
<li>The system can't really figure out the rest, of course. It needs <em>something</em> in the StartTime and StopTime fields because the database column is non-null. So OTL writes a default range: start <code>00:00</code> (very beginning of day), stop <code>23:59</code> (very end of day).</li>
<li>The end result is a row that <em>looks</em> like a 24-hour shift but isn't. The hours value (8) is correct; the punch times are decorative. The formula needs to recognise this shape because qty-only entries shouldn't be treated as real work intervals — they don't represent specific work happening at specific times.</li>
<li>Without detection, the formula would put a 24-hour interval into the day buffer, which would falsely overlap with every other entry on the day. Cascading errors would flag rows that aren't actually wrong.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>The fractional-hour conversion</div>
<div class="ann-snippet">l_st_hr = TO_NUMBER(TO_CHAR(t,'HH24')) + TO_NUMBER(TO_CHAR(t,'MI'))/60</div>
<ul class="ann-bullets">
<li>Times in Fast Formula are stored as Oracle dates, which are awkward to compare directly. The trick is to extract the time-of-day as a single decimal number representing hours-since-midnight.</li>
<li><code>TO_CHAR(t, 'HH24')</code> pulls out the hour (0–23), and <code>TO_CHAR(t, 'MI')</code> pulls out the minutes (0–59). Dividing minutes by 60 converts them into the fractional part of an hour. Add the two together and you get a single number: <code>09:30</code> becomes <code>9.5</code>, <code>17:45</code> becomes <code>17.75</code>, <code>00:00</code> becomes <code>0.0</code>.</li>
<li>This makes the qty-only check a single comparison: <em>"is start near zero AND is stop near 24?"</em> Without this conversion, you'd need to compare hours and minutes separately and combine the results — verbose and error-prone.</li>
<li>The pattern is reusable elsewhere too. Block 8's continuous-hours calculation uses a similar approach (with the addition of Julian Day arithmetic for cross-midnight handling).</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>Why 0.01 and 23.9 instead of exactly 0 and 24</div>
<ul class="ann-bullets">
<li>The intuition might say to test <code>l_st_hr = 0 AND l_sp_hr = 23.9833</code> for an exact match against the qty-only pattern. The intuition is wrong, because computers don't store decimals perfectly.</li>
<li>This is IEEE 754 floating-point representation, the same maths that means <code>0.1 + 0.2</code> equals <code>0.30000000000000004</code> in most languages. A value that should be <code>0.0</code> can end up as <code>0.0000003</code> due to representation drift through TO_NUMBER conversion.</li>
<li>The buffers <code>0.01</code> and <code>23.9</code> absorb that imprecision. Anything from <code>00:00:00.000</code> to roughly <code>00:00:36</code> reads as start "near zero"; anything from <code>23:54</code> onward reads as stop "near end". Real timecards never enter punches in those windows because layouts don't permit it.</li>
<li>The chosen buffers are wide enough to absorb floating-point drift but narrow enough that no real punch can ever cross them — eliminating false positives entirely.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">4</span>What happens once an entry is flagged qty-only</div>
<ul class="ann-bullets">
<li>Setting <code>l_qty_only = 'Y'</code> doesn't generate an error message by itself — it sets a flag that affects how subsequent blocks treat this row.</li>
<li>Block 6c (the RegHours hard requirement) treats qty-only entries the same as missing punches and fires an explicit error so the worker knows real times are needed.</li>
<li>Block 6d (the day buffer) excludes qty-only entries from overlap testing — the formula doesn't pretend a placeholder represents real work.</li>
<li>Block 8 (the stretch tracker) excludes qty-only entries from continuous-hours counting, for the same reason.</li>
<li>The flag is a single character but its effects ripple through the rest of the formula. This is composition working correctly — one detector, multiple consumers.</li>
</ul>
</div>
<div class="ann-takeaway">The pattern <code>(start < 0.01 AND stop > 23.9)</code> reliably distinguishes a qty-only placeholder from a real punch, even with floating-point imprecision. The detection happens once; the flag it sets affects three downstream blocks. Composition like this keeps each block's logic focused while the overall formula stays correct.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="c">/* RegHours start/stop missing — flag the row */</span>
<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span>
    <span class="k">AND</span> (<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">NullDate</span>
         <span class="k">OR</span> <span class="v">aiStopTime</span> <span class="op">=</span> <span class="v">NullDate</span>
         <span class="k">OR</span> <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'Y'</span>)) <span class="k">THEN</span>
( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span>
    <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span>
    <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_reghrs</span>)
)</code></pre></div>
<div class="annot-note">
<span class="nt">Block 6c · Hard requirement</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1: Three failure modes -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The hard requirement — three failure modes, all flagged</div>

<div style="background:#fff; border:1px solid #e8e3d8; border-radius:4px; padding:12px 14px; margin-bottom:8px;">
<div style="font-size:10.5px; font-weight:700; color:#2d2926;">Rule:</div>
<div style="font-size:11.5px; color:#5a544e; margin-top:4px; line-height:1.6;">Every Regular Hours entry must carry <strong>both</strong> a real start time and a real stop time. No exceptions, no warnings — this is a blocker.</div>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; padding:10px;">
<div style="font-size:10px; font-weight:700; color:#c0392b; letter-spacing:0.5px;">FAILURE 1</div>
<div style="font-size:11px; font-weight:700; color:#2d2926; margin-top:4px;">Missing start time</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#5a544e; margin-top:6px;">start = NullDate<br>stop = 17:00</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; padding:10px;">
<div style="font-size:10px; font-weight:700; color:#c0392b; letter-spacing:0.5px;">FAILURE 2</div>
<div style="font-size:11px; font-weight:700; color:#2d2926; margin-top:4px;">Missing stop time</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#5a544e; margin-top:6px;">start = 09:00<br>stop = NullDate</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; padding:10px;">
<div style="font-size:10px; font-weight:700; color:#c0392b; letter-spacing:0.5px;">FAILURE 3</div>
<div style="font-size:11px; font-weight:700; color:#2d2926; margin-top:4px;">Qty-only (no real punches)</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#5a544e; margin-top:6px;">l_qty_only = 'Y'</div>
</div>
</div>

<!-- PART 2: The message-prefix convention -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · The message-prefix convention — vague vs targeted errors</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">WITHOUT PREFIX — vague</div>
<div style="padding:10px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; background:#1f1c19; color:#e6e1d8; padding:6px 8px; border-radius:3px; overflow-x:auto;">OUT_MSG[nidx] = get_output_msg(...)</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:8px;"><strong style="color:#c0392b;">✗ Worker sees:</strong></div>
<div style="font-size:10.5px; color:#5a544e; line-height:1.5; margin-top:2px;">Generic red marker on row. <em>"start time required"</em> — but the worker thinks <em>"my start time IS filled, what's wrong?"</em></div>
</div>
</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">WITH PREFIX — targeted</div>
<div style="padding:10px 12px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; background:#1f1c19; color:#e6e1d8; padding:6px 8px; border-radius:3px; overflow-x:auto;">get_msg_attribute('StartTime') || get_output_msg(...)</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:8px;"><strong style="color:#3d7a52;">✓ Worker sees:</strong></div>
<div style="font-size:10.5px; color:#5a544e; line-height:1.5; margin-top:2px;">StartTime column itself lights up red. Eye goes straight to the field. Fix is obvious.</div>
</div>
</div>
</div>

<!-- PART 3: Why Reg Hours and Meal Break differ -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · Why Reg Hours and Meal Break have different rules</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#fff; border:1.5px solid #c0392b; border-radius:4px; padding:12px;">
<div style="font-size:10px; font-weight:700; color:#c0392b; letter-spacing:0.5px;">REG HOURS</div>
<div style="font-size:11px; font-weight:700; color:#2d2926; margin-top:4px;">Both punches required</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:6px; line-height:1.5;">Logic: <em>"I worked from X to Y."</em> Work has a beginning AND an end. Both endpoints matter for time accounting. <strong>Hard requirement — no exceptions.</strong></div>
</div>
<div style="background:#fff; border:1.5px solid #b97417; border-radius:4px; padding:12px;">
<div style="font-size:10px; font-weight:700; color:#b97417; letter-spacing:0.5px;">MEAL BREAK</div>
<div style="font-size:11px; font-weight:700; color:#2d2926; margin-top:4px;">Flexible (Block 6e)</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:6px; line-height:1.5;">Logic: <em>"I took a break."</em> Some companies record only when break starts (event marker rather than interval). Layout decides — <strong>tolerant.</strong></div>
</div>
</div>
<div style="background:#fff8e8; border-left:3px solid #b97417; padding:10px 14px; margin-top:12px; border-radius:0 3px 3px 0; font-size:11px; color:#5a544e; line-height:1.55;">
<strong style="color:#b97417;">Architectural lesson:</strong> not every time type follows the same validation rules. Resist applying uniform requirements across all rows.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The rule, stated plainly</div>
<ul class="ann-bullets">
<li>Every Regular Hours entry must carry <strong>both</strong> a real start time and a real stop time. The formula treats this as a non-negotiable hard requirement — not a warning, not a suggestion, but a blocker that prevents submission.</li>
<li>Three failure modes trigger the flag: start time is missing, stop time is missing, or the entry was flagged as qty-only by Block 6b.</li>
<li>The qty-only case is interesting because the entry technically <em>has</em> punch times — OTL filled them in as 00:00 and 23:59. But the previous block detected those as placeholders, not real punches. From this block's perspective, qty-only is functionally equivalent to "no real punch times" and gets the same treatment.</li>
<li>Why is this a hard requirement? Because Regular Hours represents work intervals on the timecard, and intervals need both endpoints to be meaningful. A start time without a stop is "I started working but never finished" — which the formula cannot interpret. Forcing real punches keeps the rest of the validation logic well-defined.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>Telling OTL which column to highlight</div>
<div class="ann-snippet">OUT_MSG[nidx] = get_msg_attribute(<span style="color:#7fc8a0;">'StartTime'</span>) || get_output_msg(...)</div>
<ul class="ann-bullets">
<li>Notice the structure of the assignment to <code>OUT_MSG</code>. It's not just the message text — it's a concatenation of <code>get_msg_attribute('StartTime')</code> with <code>get_output_msg(...)</code>. The first piece is doing something subtle but important.</li>
<li><code>get_msg_attribute('StartTime')</code> tells the OTL framework <strong>which timecard column to highlight</strong> when the worker sees this error. The function returns a special prefix string that the UI parses out and uses for visual targeting.</li>
<li>Without this prefix, the worker sees a generic red error marker on the row but no indication of which field caused it. They'd have to read the message text and guess: <em>"the message says 'start time required' — but my start time is filled in, what's wrong?"</em></li>
<li>With the prefix, the StartTime column itself lights up red on that row. The worker's eye goes straight to the column that needs attention. The fix is obvious; the friction disappears.</li>
<li>This is a small UX detail that makes a huge difference in worker experience. Every error message your formula generates should include the field-attribute prefix where it's relevant.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The asymmetry between Reg Hours and Meal Break</div>
<ul class="ann-bullets">
<li>This is the <strong>only validation in the entire formula</strong> that demands both start and stop punches. Block 6e's schedule-window check on Meal Break uses different logic that can tolerate just a start time, depending on the layout configuration.</li>
<li>The asymmetry mirrors real-life timekeeping. <em>"I worked from X to Y"</em> intrinsically needs both endpoints — the work has a beginning and an end, and both matter for accurate time accounting.</li>
<li>A meal break is more flexible. Some companies record only when the break starts (treating it as an event marker rather than an interval) and rely on schedule defaults to fill in the duration. Others insist on both. The formula respects whatever the OTL layout has been configured to allow.</li>
<li>The architectural lesson: <strong>not every time type follows the same validation rules</strong>. Resist the urge to apply uniform requirements across all types — the rules differ for legitimate reasons, and the formula should reflect that.</li>
</ul>
</div>
<div class="ann-takeaway">When generating an error message, always tell OTL which column to highlight via <code>get_msg_attribute</code>. A vague error frustrates the worker; a specific one lets them fix it instantly. And remember that not every time type needs the same validation — Reg Hours demands both punches; Meal Break may not.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="c">/* buffer Reg Hours into the day-level buffer */</span>
<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span>
    <span class="k">AND</span> <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'N'</span>
    <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span>
    <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
( <span class="v">dayCnt</span> <span class="op">=</span> <span class="v">dayCnt</span> <span class="op">+</span> <span class="n">1</span>
  <span class="v">dayStarts</span>[<span class="v">dayCnt</span>] <span class="op">=</span> <span class="v">aiStartTime</span>
  <span class="v">dayStops</span>[<span class="v">dayCnt</span>]  <span class="op">=</span> <span class="v">aiStopTime</span>
  <span class="v">dayIdxs</span>[<span class="v">dayCnt</span>]   <span class="op">=</span> <span class="v">nidx</span>
)</code></pre></div>
<div class="annot-note">
<span class="nt">Block 6d · Buffer for overlap</span>
<div class="ann-excel">
<div class="ax-bar"><span>Day_Buffer_Accumulating.xlsx</span><span class="app">Excel</span></div>
<table>
<thead><tr><th style="min-width:36px; white-space:nowrap;">Iter</th><th>dayCnt</th><th>dayStarts[]</th><th>dayStops[]</th></tr></thead>
<tbody>
<tr><td class="idx">[2]</td><td class="tc">1</td><td class="tc">08:30</td><td class="tc">10:00</td></tr>
<tr><td class="idx">[3]</td><td class="tc">2</td><td class="tc">08:30, 10:00</td><td class="tc">10:00, 14:45</td></tr>
<tr><td class="idx">[4]</td><td class="tc">3</td><td class="tc">08:30, 10:00, 15:00</td><td class="tc">10:00, 14:45, 18:00</td></tr>
</tbody>
</table>
</div>
<div class="ann-excel-cap">Each Reg Hours line appends to the parallel arrays. END_DAY triggers pairwise overlap on this buffer.</div>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Four concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · Evidence-gathering — what gets included, what stays out</div>

<div style="background:#1f1c19; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:10.5px; line-height:1.6; margin-bottom:10px; overflow-x:auto;">
<span style="color:#f0d68a;">// the gate</span><br>
<span style="color:#e6e1d8;">IF aiTimeType = p_reg_type AND l_qty_only = 'N'<br>
   AND aiStartTime <> NullDate AND aiStopTime <> NullDate</span>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">INCLUDED — goes into buffer</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; font-weight:700; color:#3d7a52;">✓ Real Reg Hours rows only</div>
<div style="font-size:10.5px; color:#5a544e; line-height:1.7; margin-top:4px;">Time type = 'Regular Hours'<br>Both punches present<br>Not a qty-only placeholder</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:8px;">These are the rows that compete for the same time</div>
</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">EXCLUDED — deliberately filtered out</div>
<div style="padding:10px 12px;">
<div style="font-size:10.5px; color:#c0392b; font-weight:700; line-height:1.7;">✗ Marker rows (HEADER, END_DAY)<br>✗ Qty-only placeholders<br>✗ Meal Breaks</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:6px; line-height:1.5;">If Meal Break went in, it would falsely overlap with adjacent Reg Hours by construction.</div>
</div>
</div>
</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · Three parallel arrays, all written together</div>

<div style="background:#1f1c19; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:10.5px; margin-bottom:10px; overflow-x:auto;">
<span style="color:#f0d68a;">// dayCnt increments first, then all three writes go to the same slot</span><br>
<span style="color:#e6e1d8;">dayCnt = dayCnt + 1; dayStarts[dayCnt]=aiStartTime; dayStops[dayCnt]=aiStopTime; dayIdxs[dayCnt]=nidx</span>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">
<div style="background:#fff; border:1.5px solid #1f5fa8; border-radius:4px; overflow:hidden;">
<div style="background:#1f5fa8; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">dayStarts[ ]</div>
<div style="padding:8px 10px; font-size:10px; color:#5a544e; line-height:1.7;">
slot 1: <span style="font-family:'JetBrains Mono', monospace;">08:30</span><br>
slot 2: <span style="font-family:'JetBrains Mono', monospace;">10:00</span><br>
slot 3: <span style="font-family:'JetBrains Mono', monospace;">15:00</span>
</div>
</div>
<div style="background:#fff; border:1.5px solid #b97417; border-radius:4px; overflow:hidden;">
<div style="background:#b97417; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">dayStops[ ]</div>
<div style="padding:8px 10px; font-size:10px; color:#5a544e; line-height:1.7;">
slot 1: <span style="font-family:'JetBrains Mono', monospace;">10:00</span><br>
slot 2: <span style="font-family:'JetBrains Mono', monospace;">14:45</span><br>
slot 3: <span style="font-family:'JetBrains Mono', monospace;">18:00</span>
</div>
</div>
<div style="background:#fff; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">dayIdxs[ ] · chain of custody</div>
<div style="padding:8px 10px; font-size:10px; color:#5a544e; line-height:1.7;">
slot 1: <span style="font-family:'JetBrains Mono', monospace;">[2]</span> <em style="color:#7a7570;">← original</em><br>
slot 2: <span style="font-family:'JetBrains Mono', monospace;">[4]</span> <em style="color:#7a7570;">← original</em><br>
slot 3: <span style="font-family:'JetBrains Mono', monospace;">[7]</span> <em style="color:#7a7570;">← original</em>
</div>
</div>
</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:8px;">All three arrays use the same internal indexing (1, 2, 3...). Three writes per row. Always in lockstep.</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · Why dayIdxs matters — buffer index ≠ timecard row</div>

<div style="margin-bottom:10px;">
<div style="font-size:10px; font-weight:700; color:#1f5fa8; margin-bottom:6px;">Buffer indexing (sequential, 1, 2, 3):</div>
<div style="display:flex; gap:0;">
<div style="background:#dbe5f4; border:1px solid #1f5fa8; padding:8px 14px; font-weight:700; color:#2d2926;">1</div>
<div style="background:#dbe5f4; border:1px solid #1f5fa8; padding:8px 14px; font-weight:700; color:#2d2926;">2</div>
<div style="background:#dbe5f4; border:1px solid #1f5fa8; padding:8px 14px; font-weight:700; color:#2d2926;">3</div>
<div style="padding:8px 12px; font-size:10px; color:#c0392b; font-style:italic;">via dayIdxs[]</div>
</div>
<div style="text-align:center; color:#c0392b; font-size:14px; padding:4px 0;">↓ ↓ ↓</div>
<div style="font-size:10px; font-weight:700; color:#3d7a52; margin-bottom:6px;">Worker's actual timecard rows:</div>
<div style="display:flex; gap:0; align-items:center;">
<div style="background:#e8f4ea; border:1px solid #3d7a52; padding:8px 14px; font-weight:700; color:#2d2926;">[2]</div>
<div style="background:#e8f4ea; border:1px solid #3d7a52; padding:8px 14px; font-weight:700; color:#2d2926;">[4]</div>
<div style="background:#e8f4ea; border:1px solid #3d7a52; padding:8px 14px; font-weight:700; color:#2d2926;">[7]</div>
<div style="padding:8px 12px; font-size:10px; color:#5a544e; font-style:italic;">positions 3, 5, 6 are markers/meal — not in buffer</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; line-height:1.6;">
Without dayIdxs: Block 7 detects buffer entries 2 & 3 overlap, but it would put the error on rows [2] and [3]:<br>
<strong style="color:#c0392b;">✗ Worker baffled. Wrong rows highlighted. Bug impossible to debug.</strong><br>
<strong style="color:#3d7a52;">✓ With dayIdxs: error correctly lands on rows [4] and [7] — matches what the worker entered.</strong>
</div>

<!-- PART 4 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 4 · Per-day lifecycle — accumulate, judge, reset</div>

<div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
<div style="background:#3d7a52; color:#fff; padding:6px 14px; border-radius:3px; font-size:10.5px; font-weight:700;">Accumulate</div>
<div style="color:#7a7570; font-size:14px;">→</div>
<div style="background:#fff; border:1px solid #7a7570; color:#5a544e; padding:6px 12px; border-radius:3px; font-size:10.5px; font-weight:700;">END_DAY hits → Block 7</div>
<div style="color:#7a7570; font-size:14px;">→</div>
<div style="background:#b97417; color:#fff; padding:6px 14px; border-radius:3px; font-size:10.5px; font-weight:700;">Pairwise overlap test</div>
<div style="color:#7a7570; font-size:14px;">→</div>
<div style="background:#c0392b; color:#fff; padding:6px 14px; border-radius:3px; font-size:10.5px; font-weight:700;">Reset to empty</div>
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The role this block plays</div>
<ul class="ann-bullets">
<li>This block doesn't fire any errors itself. Its job is to <strong>collect evidence</strong> for the overlap test that will fire later in Block 7. Think of it as evidence-gathering before a trial — the actual judgment happens elsewhere.</li>
<li>What gets collected: every <em>real</em> Regular Hours entry. The qualifier "real" is doing important work here. The block deliberately excludes anything that shouldn't participate in overlap testing — marker rows (HEADER, END_DAY), qty-only placeholders (which don't represent real time intervals), and Meal Breaks (which have their own validation path in Block 6e).</li>
<li>What stays excluded matters as much as what gets included. If Meal Breaks went into the day buffer, they'd overlap with their adjacent Reg Hours rows by construction (a 12:00–13:00 lunch overlaps with the 09:00–12:00 morning shift if you treat it as just another interval). The formula would generate noise instead of signal.</li>
<li>This selective collection is a small architectural decision with large consequences. It's the difference between a formula that works correctly on real data and one that fires constantly false flags.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>The three parallel arrays, in detail</div>
<div class="ann-snippet">dayStarts[dayCnt] = aiStartTime
dayStops[dayCnt]  = aiStopTime
dayIdxs[dayCnt]   = nidx</div>
<ul class="ann-bullets">
<li>Each qualifying entry adds three items in lockstep: a start time, a stop time, and a row index. <code>dayCnt</code> increments first so all three writes go to the same new slot.</li>
<li><code>dayStarts</code> and <code>dayStops</code> together describe the time interval for each entry. These are what the overlap test in Block 7 actually compares pairwise to detect collisions.</li>
<li><code>dayIdxs</code> is the metadata that ties each buffered entry back to its original timecard row. Block 7 uses this to identify <em>which</em> row to flag when an overlap is detected.</li>
<li>Storing these as three parallel arrays (rather than one array of records) is a Fast Formula idiom — the language doesn't have native record types, so parallel arrays serve the same purpose. The three arrays must always be kept in sync (same length, same indexing), which is why every append updates all three at once.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The crucial role of dayIdxs</div>
<ul class="ann-bullets">
<li>Why bother storing the original row index at all? Couldn't the formula just use the buffer's internal indexing? The answer is no, and the reason reveals a subtle aspect of the formula's correctness.</li>
<li>The buffer's internal indexing starts at 1 and increments sequentially as entries are added. So buffer position 1 might be the day's first Reg Hours entry, position 2 the second, and so on.</li>
<li>But the worker's view of the timecard is different. On a real timecard, those Reg Hours entries might appear at row positions [2], [4], and [7] — with marker rows and Meal Break rows interleaved between them. The buffer indexing (1, 2, 3) and the timecard indexing ([2], [4], [7]) don't match.</li>
<li>When Block 7 detects that buffer entries 2 and 3 overlap, it can't just put the error on rows [2] and [3]. It needs to translate buffer indexes back to timecard indexes. <code>dayIdxs</code> is that translation table.</li>
<li>Without it, error messages would land on the wrong rows. The worker would see <em>"row 2 overlaps with row 3"</em> when actually rows [4] and [7] are the conflicting ones — baffling, ungrounded, impossible to debug.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">4</span>Lifetime: when the buffer resets</div>
<ul class="ann-bullets">
<li>The buffer accumulates across iterations as the loop processes more rows of the same day. It doesn't get touched again by this block — further additions just keep extending it.</li>
<li>The buffer's life ends at the next <code>END_DAY</code> or <code>END_PERIOD</code> marker, where Block 7 takes over. Block 7 runs the pairwise overlap test, fires flags on conflicting rows (using <code>dayIdxs</code> to target correctly), and then resets all three arrays back to empty.</li>
<li>The next day starts with empty lists, ready to accumulate again. The cycle repeats for every day in the timecard period.</li>
<li>This <strong>per-day lifecycle</strong> is what keeps the formula correct across multi-day timecards. Without the reset, day 2's overlap test would also see day 1's entries, producing nonsense results.</li>
</ul>
</div>
<div class="ann-takeaway">The day buffer is evidence-gathering for Block 7's overlap trial. The selective inclusion (real Reg Hours only) prevents false flags. <code>dayIdxs</code> is the chain of custody that connects the evidence to the right timecard row in the worker's view. Three pieces of metadata, one purpose — correct and actionable error messages.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="c">/* Meal Break — schedule window check */</span>
<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_break_type</span>
    <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
( <span class="v">bk_st</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'HH24'</span>))
  <span class="v">bk_sp</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'HH24'</span>))
  <span class="k">IF</span> ((<span class="v">bk_st</span> <span class="op"><</span> <span class="v">p_sched_start</span>
       <span class="k">OR</span> <span class="v">bk_sp</span> <span class="op">></span> <span class="v">p_sched_end</span>)
      <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span>
      <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span>) <span class="k">THEN</span>
  ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> ... <span class="v">p_msg_break</span> )
  <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'Y'</span>
)</code></pre></div>
<div class="annot-note">
<span class="nt">Block 6e · Schedule window</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Four concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The rule — meal break must fall inside scheduled hours (weekdays only)</div>

<div style="background:#fff; border:1px solid #b97417; border-radius:4px; padding:12px; margin-bottom:10px;">
<div style="text-align:center; font-size:10px; font-weight:700; color:#b97417; margin-bottom:6px;">SCHEDULE WINDOW · 09:00 — 18:00</div>
<div style="position:relative; height:60px; background:linear-gradient(to right, transparent 0%, transparent 18.75%, #fff3e0 18.75%, #fff3e0 75%, transparent 75%); border-bottom:1px solid #999;">
<!-- Three meal breaks plotted -->
<div style="position:absolute; left:9.5%; top:14px; width:3%; height:20px; background:#c0392b; opacity:0.85;"></div>
<div style="position:absolute; left:9.5%; top:38px; font-size:8px; font-weight:700; color:#c0392b;">7:30</div>
<div style="position:absolute; left:35%; top:14px; width:6%; height:20px; background:#3d7a52; opacity:0.85; display:flex; align-items:center; justify-content:center; color:#fff; font-size:8px; font-weight:700;">12-13</div>
<div style="position:absolute; left:75%; top:14px; width:6%; height:20px; background:#c0392b; opacity:0.85; display:flex; align-items:center; justify-content:center; color:#fff; font-size:8px; font-weight:700;">19-20</div>
</div>
<div style="display:flex; justify-content:space-between; font-size:9px; color:#5a544e; margin-top:4px;">
<span>06</span><span>08</span><span style="font-weight:700; color:#b97417;">09</span><span>11</span><span>13</span><span>15</span><span style="font-weight:700; color:#b97417;">18</span><span>20</span><span>22</span>
</div>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; font-size:10.5px; line-height:1.5;">
<div style="color:#3d7a52;"><strong>✓ Inside (12–13)</strong><br>— passes</div>
<div style="color:#c0392b;"><strong>✗ After 18 (19–20)</strong><br>— flag</div>
<div style="color:#c0392b;"><strong>✗ Before 9 (07:30)</strong><br>— flag</div>
</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:8px;">Weekend exception: validation suspended on Saturday and Sunday.</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · The operator-precedence trap — AND binds tighter than OR</div>

<div style="background:#1f1c19; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:10.5px; line-height:1.6; margin-bottom:10px; overflow-x:auto;">
<span style="color:#f0d68a;">// In Fast Formula, AND binds tighter than OR — just like × binds tighter than +</span><br>
<span style="color:#e6e1d8;">2 + 3 × 4 = 14, not 20   //   A OR B AND C = A OR (B AND C)</span>
</div>

<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden; margin-bottom:8px;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">THE BUG — missing parens</div>
<div style="padding:10px 12px;">
<div style="background:#fff; border:1px solid #c0392b; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10px; color:#2d2926; overflow-x:auto;">IF bk_st < sched_start OR bk_sp > sched_end AND l_day <> 'SAT' AND l_day <> 'SUN'</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:6px;">Parsed as: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">(start-too-early) OR (stop-too-late AND weekday)</code></div>
<div style="font-size:10.5px; color:#c0392b; font-weight:700; margin-top:6px;">✗ Saturday 07:30 break: first OR clause TRUE → OR short-circuits → weekend never checked → FALSE FLAG</div>
</div>
</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · The fix — one pair of parentheses around the OR</div>

<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden; margin-bottom:8px;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">THE FIX — explicit grouping</div>
<div style="padding:10px 12px;">
<div style="background:#fff; border:1px solid #3d7a52; padding:6px 10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:10px; color:#2d2926; overflow-x:auto;">IF <span style="color:#3d7a52; font-weight:700;">(</span>bk_st < sched_start OR bk_sp > sched_end<span style="color:#3d7a52; font-weight:700;">)</span> AND l_day <> 'SAT' AND l_day <> 'SUN'</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:6px;">Now reads as: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">(out-of-window) AND weekday</code></div>
<div style="font-size:10.5px; color:#3d7a52; font-weight:700; margin-top:6px;">✓ Saturday 07:30: out-of-window TRUE, weekday FALSE → AND short-circuits → no flag → CORRECT</div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:8px;"><strong style="color:#2d2926;">General rule:</strong> any time you mix AND and OR in the same expression, wrap the OR clause explicitly. Trust nothing to default precedence.</div>

<!-- PART 4 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 4 · The l_meal_taken side-effect — nervous-system signalling</div>

<div style="display:grid; grid-template-columns:1fr auto 1fr auto 1fr; gap:6px; align-items:center; margin-bottom:10px;">
<div style="background:#fff; border:1.5px solid #1f5fa8; border-radius:4px; overflow:hidden;">
<div style="background:#1f5fa8; color:#fff; font-size:9.5px; font-weight:700; text-align:center; padding:4px;">BLOCK 6e · sets the flag</div>
<div style="padding:8px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#2d2926;">l_meal_taken = 'Y'</div>
<div style="font-size:9px; color:#5a544e; font-style:italic; margin-top:4px;">set even if validation failed (worker did eat regardless)</div>
</div>
</div>
<div style="color:#7a7570; font-size:12px;">→</div>
<div style="background:#fff; border:1.5px solid #b97417; border-radius:4px; overflow:hidden;">
<div style="background:#b97417; color:#fff; font-size:9.5px; font-weight:700; text-align:center; padding:4px;">BLOCK 8 · reads the flag</div>
<div style="padding:8px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#2d2926;">if l_meal_taken='Y' →</div>
<div style="font-size:9.5px; color:#b97417; font-weight:700; margin-top:2px;">gate stays closed</div>
<div style="font-size:9px; color:#5a544e; font-style:italic; margin-top:2px;">stretch tracker stops counting</div>
</div>
</div>
<div style="color:#7a7570; font-size:12px;">→</div>
<div style="background:#fff; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:9.5px; font-weight:700; text-align:center; padding:4px;">BLOCK 7c</div>
<div style="padding:8px;">
<div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#2d2926;">l_meal_taken = 'N'</div>
<div style="font-size:9px; color:#5a544e; font-style:italic; margin-top:4px;">resets at day boundary — tomorrow starts fresh</div>
</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; line-height:1.55;">
<strong style="color:#2d2926;">Why set the flag even on validation failure?</strong> The worker did eat — even if they entered the wrong time. Treating an invalid meal as "didn't happen" would let the stretch tracker keep counting past lunch, generating cascading false errors.
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:6px;">Cross-block coordination via shared flags. Each block does its own job; the flags are the connective tissue.</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The validation this block enforces</div>
<ul class="ann-bullets">
<li>This block handles meal break entries with one rule: <strong>a meal break should fall within scheduled working hours</strong>. The schedule is defined by the rule parameters <code>p_sched_start</code> (typically 9) and <code>p_sched_end</code> (typically 18).</li>
<li>Examples that fail: a meal logged at 19:00–20:00 (after the 18:00 schedule end), a meal at 07:30–08:00 (before the 09:00 schedule start), a meal at 22:00–23:00 (well outside any normal workday).</li>
<li>Why does this rule matter? Two reasons. First, a meal outside working hours strongly suggests the worker mis-entered the time — perhaps they meant 12:00–13:00 instead of 19:00–20:00. Second, a meal break that doesn't interrupt actual work doesn't satisfy the legal purpose of the meal break (giving the worker rest during their shift).</li>
<li>The validation is suspended on weekends. If the worker is logging hours on Saturday, the schedule-window check doesn't apply — weekend work has its own logic and shouldn't be falsely blocked by weekday assumptions.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>The operator-precedence trap that catches everyone</div>
<ul class="ann-bullets">
<li>Fast Formula evaluates logical operators in a specific order: <code>AND</code> binds tighter than <code>OR</code>. This mirrors how multiplication binds tighter than addition in arithmetic — <code>2 + 3 × 4</code> equals 14, not 20.</li>
<li>Apply that to a logical expression. <code>bkStart < sched_start OR bkEnd > sched_end AND l_day <> 'SAT' AND l_day <> 'SUN'</code> — without parentheses — gets parsed as <em>"start-too-early OR (stop-too-late AND weekday)"</em>.</li>
<li>Now picture a Saturday morning early break: a worker logs <code>07:30–08:00</code> on a Saturday. The first condition (<code>bkStart < sched_start</code>) is TRUE because 7:30 is before 9:00. The OR short-circuits at TRUE before it ever gets to the weekend check.</li>
<li>The result: the formula flags a perfectly legitimate weekend break, telling the worker their entry is out of working hours — even though working hours don't apply on Saturdays. The worker is confused, support gets a ticket, and the bug is buried in operator precedence rather than business logic.</li>
<li>This trap is universal: any time you mix <code>AND</code> and <code>OR</code> in the same condition without explicit grouping, the result is unlikely to match what you intended.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The fix is one pair of parentheses</div>
<div class="ann-snippet">IF <span style="color:#e07060;">(</span>bk_st < p_sched_start OR bk_sp > p_sched_end<span style="color:#e07060;">)</span>
AND l_day <> 'SAT' AND l_day <> 'SUN' THEN ...</div>
<ul class="ann-bullets">
<li>Wrapping <code>(bkStart < sched_start OR bkEnd > sched_end)</code> in parentheses forces the OR to evaluate first. Now the expression reads as <em>"(out-of-window) AND weekday"</em>.</li>
<li>The Saturday morning early break: the inner OR fires TRUE, but the outer AND requires the weekend exception to also be true. <code>l_day = 'SAT'</code>, so the weekend guard fails, the AND short-circuits, and no flag fires. Correct behaviour.</li>
<li>The fix is two characters added to the source. The bug it prevents would have been buried, hard to reproduce, and might survive several rounds of UAT before someone tested a Saturday timecard.</li>
<li>The general lesson: <strong>any time your formula mixes <code>AND</code> and <code>OR</code> in the same expression, wrap the OR clause in explicit parentheses</strong>. Don't trust default precedence to match your intent. The parens cost nothing; missing them costs production bugs.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">4</span>The l_meal_taken side-effect</div>
<ul class="ann-bullets">
<li>The very last line in this block is <code>l_meal_taken = 'Y'</code>. It's tucked away after the schedule check, easy to overlook, but it has consequences that reach across the formula.</li>
<li>Block 8 (the continuous-hours state machine) checks this flag at the top of its gate. If <code>l_meal_taken = 'Y'</code>, the gate stays closed and the stretch tracker stops counting for the rest of the day.</li>
<li>The reasoning is legal: the continuous-work cap measures work <em>before</em> a meal break. The meal itself proves continuity was interrupted. Any work after the meal is fresh and doesn't accumulate against the pre-meal stretch.</li>
<li>Notice that the flag is set <em>regardless of whether the meal break passed validation</em>. Even a meal logged outside hours flips the flag — the formula trusts that the worker did eat, even if they entered the time wrong, because the alternative (treating an invalid meal as if it didn't happen) would generate cascading errors.</li>
<li>This kind of cross-block coordination is why the formula has so many shared state variables. Each block does its own job, but they coordinate through shared flags like <code>l_meal_taken</code>, <code>l_qty_only</code>, and <code>inStretch</code>. The flags are the formula's nervous system.</li>
</ul>
</div>
<div class="ann-takeaway">One pair of parentheses is the difference between the formula working on weekends and falsely flagging legitimate weekend entries. The general rule: any time you mix <code>AND</code> and <code>OR</code> in a single condition, wrap the OR clause explicitly. Trust nothing to default precedence.</div>
</div></div>
</div>
</div>

</div>
</div>

<h3>Day Boundary & Pairwise Overlap</h3>

<p>Block 7 is the only block in the formula that runs <em>conditionally</em>. While Blocks 6 and 8 fire on every iteration, Block 7 only activates when the loop hits an <code>END_DAY</code> or <code>END_PERIOD</code> marker. That's a deliberate design choice with a real performance benefit: overlap detection is an O(n²) operation, and running it on every row would scale badly for workers with 30+ entries per timecard. By batching the work to fire once per day, we keep the cost bounded.</p>

<h4>The sequence: what fires when END_DAY hits</h4>

<p>When the loop reaches an END_DAY marker, five things happen in order. The buffer that's been quietly filling up across previous iterations gets read, tested, and cleared.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<img src="/images/posts/oracle-fast-formula-time-entry-rule-part-3/diagram-2.png" alt="Diagram 2: Oracle Fast Formula: Time Entry Rule (Part 3)" style="max-width:100%;height:auto;margin:26px auto;display:block;border-radius:6px;border:1px solid #e5e0d8" loading="lazy" />

</div>

<p>Three things worth holding on to:</p>

<ul>
<li><strong>The buffer fills earlier, drains here.</strong> Block 6d adds entries to the buffer on every Reg Hours row. Block 7 just consumes what Block 6d collected.</li>
<li><strong>Use strict <code><</code>, not <code><=</code>.</strong> Touching entries (one ends at 12:00, the next starts at 12:00) are a continuation, not an overlap. Strict less-than is the difference between a working formula and one that flags every back-to-back entry.</li>
<li><strong>Reset everything, not just the buffer.</strong> The stretch tracker and meal-taken flag also reset. Skip this and yesterday's state leaks into today.</li>
</ul>

<div style="background:#fff5f0; border-left:4px solid #c0392b; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#c0392b; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Production trap</div>
Forgetting to reset the stretch tracker at END_DAY is one of the most common bugs in continuous-hours code. The symptom looks weird: a worker who took yesterday's meal break correctly suddenly gets flagged today on their first entry — because yesterday's stretch never died. <strong>Reset the buffer, the stretch tracker, and the meal-taken flag together.</strong> Treat the day boundary as a hard reset.
</div>

<h4>The annotated code</h4>

<div class="annot-wrap">
<div class="annot-head">
<span>Block 7 · Pairwise overlap test</span>
<span class="label-right">Annotated</span>
</div>
<div class="annot-body">

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code><span class="c">/* fire on day or period boundary */</span>
<span class="k">IF</span> (<span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_DAY'</span>
    <span class="k">OR</span> <span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_PERIOD'</span>) <span class="k">THEN</span>
(
  <span class="v">i</span> <span class="op">=</span> <span class="n">1</span>
  <span class="k">WHILE</span> (<span class="v">i</span> <span class="op"><</span> <span class="v">dayCnt</span>) <span class="k">LOOP</span>
  ( <span class="v">j</span> <span class="op">=</span> <span class="v">i</span> <span class="op">+</span> <span class="n">1</span>
    <span class="k">WHILE</span> (<span class="v">j</span> <span class="op"><=</span> <span class="v">dayCnt</span>) <span class="k">LOOP</span>
    (
      ...</code></pre></div>
<div class="annot-note">
<span class="nt">Block 7a · Trigger on marker</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The trigger gates everything — only fires at day or period boundary</div>

<div style="overflow-x:auto; margin-bottom:10px;">
<div style="display:flex; min-width:560px; gap:0;">
<div style="flex:1; background:#fff8e7; border:1px solid #b97417; padding:8px; text-align:center;">
<div style="font-size:9px; color:#5a544e;">[1] HEADER</div>
<div style="font-size:9px; color:#7a7570; font-style:italic;">silent</div>
</div>
<div style="flex:1; background:#fff; border:1px solid #999; padding:8px; text-align:center;">
<div style="font-size:9px; color:#5a544e;">[2] Reg</div>
<div style="font-size:9px; color:#7a7570; font-style:italic;">silent</div>
</div>
<div style="flex:1; background:#fff; border:1px solid #999; padding:8px; text-align:center;">
<div style="font-size:9px; color:#5a544e;">[3] Reg</div>
<div style="font-size:9px; color:#7a7570; font-style:italic;">silent</div>
</div>
<div style="flex:1; background:#fff; border:1px solid #999; padding:8px; text-align:center;">
<div style="font-size:9px; color:#5a544e;">[4] Meal</div>
<div style="font-size:9px; color:#7a7570; font-style:italic;">silent</div>
</div>
<div style="flex:1.5; background:#fce8e8; border:2px solid #c0392b; padding:8px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#c0392b;">[5] END_DAY</div>
<div style="font-size:9px; font-weight:700; color:#c0392b;">FIRES ⚡</div>
</div>
<div style="flex:1; background:#fff; border:1px solid #999; padding:8px; text-align:center;">
<div style="font-size:9px; color:#5a544e;">[6] Reg</div>
<div style="font-size:9px; color:#7a7570; font-style:italic;">silent</div>
</div>
<div style="flex:2; background:#fce8e8; border:2px solid #c0392b; padding:8px; text-align:center;">
<div style="font-size:10px; font-weight:700; color:#c0392b;">[7] END_PERIOD</div>
<div style="font-size:9px; font-weight:700; color:#c0392b;">FIRES ⚡</div>
</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e; line-height:1.55;">
Block 6d quietly accumulates entries into the buffer on every Reg Hours iteration.<br>
Block 7 stays silent until a marker arrives. <strong style="color:#2d2926;">Marker = clean checkpoint — every entry has been collected.</strong>
</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · The pairwise loop — every pair tested once, no duplicates</div>

<div style="font-size:10.5px; color:#5a544e; margin-bottom:8px;"><strong style="color:#2d2926;">Buffer has 4 entries (dayCnt = 4):</strong></div>
<div style="display:flex; gap:0; margin-bottom:14px;">
<div style="background:#dbe5f4; border:1px solid #1f5fa8; padding:8px 16px; font-weight:700; color:#2d2926;">A</div>
<div style="background:#dbe5f4; border:1px solid #1f5fa8; padding:8px 16px; font-weight:700; color:#2d2926;">B</div>
<div style="background:#dbe5f4; border:1px solid #1f5fa8; padding:8px 16px; font-weight:700; color:#2d2926;">C</div>
<div style="background:#dbe5f4; border:1px solid #1f5fa8; padding:8px 16px; font-weight:700; color:#2d2926;">D</div>
</div>

<div style="font-size:10.5px; color:#5a544e; margin-bottom:8px;"><strong style="color:#2d2926;">Six comparisons fire — in this order:</strong></div>

<div style="display:grid; grid-template-columns:auto 1fr; gap:8px; align-items:center; margin-bottom:6px;">
<div style="font-size:10.5px; font-weight:700; color:#3d7a52; white-space:nowrap;">i=1 (A):</div>
<div style="display:flex; gap:4px; flex-wrap:wrap;">
<div style="background:#e8f4ea; border:1px solid #3d7a52; padding:5px 10px; font-size:10.5px; font-weight:700; color:#3d7a52;">A vs B</div>
<div style="background:#e8f4ea; border:1px solid #3d7a52; padding:5px 10px; font-size:10.5px; font-weight:700; color:#3d7a52;">A vs C</div>
<div style="background:#e8f4ea; border:1px solid #3d7a52; padding:5px 10px; font-size:10.5px; font-weight:700; color:#3d7a52;">A vs D</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; padding:5px;">(j=2,3,4)</div>
</div>
</div>
<div style="display:grid; grid-template-columns:auto 1fr; gap:8px; align-items:center; margin-bottom:6px;">
<div style="font-size:10.5px; font-weight:700; color:#b97417; white-space:nowrap;">i=2 (B):</div>
<div style="display:flex; gap:4px; flex-wrap:wrap;">
<div style="background:#fff3e0; border:1px solid #b97417; padding:5px 10px; font-size:10.5px; font-weight:700; color:#b97417;">B vs C</div>
<div style="background:#fff3e0; border:1px solid #b97417; padding:5px 10px; font-size:10.5px; font-weight:700; color:#b97417;">B vs D</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; padding:5px;">(j=3,4) — A vs B done</div>
</div>
</div>
<div style="display:grid; grid-template-columns:auto 1fr; gap:8px; align-items:center; margin-bottom:10px;">
<div style="font-size:10.5px; font-weight:700; color:#c0392b; white-space:nowrap;">i=3 (C):</div>
<div style="display:flex; gap:4px; flex-wrap:wrap;">
<div style="background:#fff5f0; border:1px solid #c0392b; padding:5px 10px; font-size:10.5px; font-weight:700; color:#c0392b;">C vs D</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; padding:5px;">(j=4) — others done</div>
</div>
</div>

<div style="font-size:10.5px; color:#5a544e;">Six unique pairs from four entries: <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">n(n-1)/2 = 4×3/2 = 6</code>.</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:4px;">If j started at 1, every pair would be tested twice and entries would compare against themselves — false flags everywhere.</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · The performance reality — pairwise is O(n²)</div>

<div style="overflow-x:auto;">
<table style="width:100%; border-collapse:collapse; font-size:10.5px; min-width:500px;">
<thead>
<tr style="background:#e8e8e8;">
<th style="padding:6px 10px; border:1px solid #999; text-align:left; color:#5a544e;">Buffer entries (n)</th>
<th style="padding:6px 10px; border:1px solid #999; text-align:left; color:#5a544e;">Comparisons</th>
<th style="padding:6px 10px; border:1px solid #999; text-align:left; color:#5a544e;">Cost (rough)</th>
<th style="padding:6px 10px; border:1px solid #999; text-align:left; color:#5a544e;">Verdict</th>
</tr>
</thead>
<tbody>
<tr style="background:#e8f4ea;">
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">Typical day: 5</td>
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">10</td>
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">trivial</td>
<td style="padding:6px 10px; border:1px solid #999; color:#3d7a52; font-weight:700;">✓ comfortably fast</td>
</tr>
<tr style="background:#fff8e7;">
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">Heavy day: 30</td>
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">435</td>
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">manageable</td>
<td style="padding:6px 10px; border:1px solid #999; color:#b97417; font-weight:700;">⚠ still OK</td>
</tr>
<tr style="background:#fff5f0;">
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">Edge case: 100</td>
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">4,950</td>
<td style="padding:6px 10px; border:1px solid #999; color:#2d2926;">noticeable</td>
<td style="padding:6px 10px; border:1px solid #999; color:#c0392b; font-weight:700;">✗ would need attention</td>
</tr>
</tbody>
</table>
</div>

<div style="font-size:10.5px; color:#5a544e; margin-top:10px; line-height:1.55;">
In real production, day buffers rarely exceed 5–10 entries.<br>
By batching the work to fire <strong style="color:#2d2926;">once per day</strong> instead of row-by-row, the cost stays bounded for realistic timecards.
</div>

<div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; border-radius:3px; margin-top:12px; font-size:10.5px; line-height:1.6;">
<span style="font-family:'JetBrains Mono', monospace; font-weight:700; color:#f0d68a;">DESIGN INSIGHT:</span> Marker-driven activation keeps an O(n²) algorithm safe in practice. Same algorithm running per-row would multiply this cost by the number of iterations — unacceptable.
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The trigger condition that gates everything</div>
<ul class="ann-bullets">
<li>This entire block sits behind a single guard: <code>IF (aiRecPos = 'END_DAY' OR aiRecPos = 'END_PERIOD') THEN</code>. Nothing inside fires unless that condition is true.</li>
<li>The result is that overlap testing happens <strong>only at day boundaries</strong>, never row-by-row. As the loop processes Reg Hours rows in the middle of a day, Block 6d quietly accumulates them into the day buffer. This block stays silent.</li>
<li>Then the loop encounters an <code>END_DAY</code> marker. The buffer at this moment holds every Reg Hours entry from the day just completed. Now the block fires — this is the moment of truth, where every pair gets checked against every other pair.</li>
<li>Why batch the work this way instead of testing each new entry against existing entries as it arrives? Because the marker-driven approach guarantees every entry has been collected before testing begins. There's no risk of testing entry A against entry B before realising entry C will arrive next and complicate the picture. The day boundary is a clean checkpoint.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>The pairwise loop pattern, walked through</div>
<div class="ann-snippet">i = 1
WHILE (i < dayCnt) LOOP (
j = i + 1
WHILE (j <= dayCnt) LOOP (
... compare (i, j) ...
j = j + 1
)
i = i + 1
)</div>
<ul class="ann-bullets">
<li>This is the textbook pairwise comparison pattern, found in any algorithms course. Two nested loops, with the inner counter starting one position past the outer counter.</li>
<li>Outer counter <code>i</code> walks from 1 to n−1 (where n is <code>dayCnt</code>). Inner counter <code>j</code> walks from <code>i+1</code> to n. The constraint <code>j > i</code> is what guarantees every unordered pair is tested exactly once.</li>
<li>The progression for a 4-entry buffer: i=1 pairs with j=2,3,4. Then i=2 pairs with j=3,4. Then i=3 pairs with j=4. Six total comparisons, each pair seen once. (1,3) is tested but (3,1) isn't — that would be redundant since overlap is symmetric.</li>
<li>The pattern would be wrong if <code>j</code> started at 1 instead of <code>i+1</code> — that would test every pair twice (once as A,B and once as B,A) and also test entries against themselves (A,A always overlaps trivially), generating false flags.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The performance reality check</div>
<ul class="ann-bullets">
<li>The pairwise pattern is <strong>O(n²)</strong> — for n entries, it does n(n−1)/2 comparisons. In computer science, anything quadratic is suspicious because it scales badly: 100 entries means 4,950 comparisons, 1000 entries means 499,500.</li>
<li>Should we worry about this here? No, and the reason is the constraint on <code>n</code>. The buffer holds Reg Hours entries for <em>one day only</em>. A worker logging 10 separate Reg Hours entries on a single day is already unusual. 20 would be extreme. 100 entries on one day doesn't happen on real timecards.</li>
<li>Doing the maths at realistic scales: 5 entries → 10 comparisons. 10 entries → 45 comparisons. 20 entries (extremely unusual) → 190 comparisons. All execute in well under a millisecond.</li>
<li>This is a case where understanding the data shape matters more than understanding algorithmic complexity. Quadratic is fine when n is bounded by problem constraints — trying to optimise with sorted-interval tricks (sweep-line algorithms, interval trees) would add real complexity for zero measurable gain. Premature optimisation; resist it.</li>
</ul>
</div>
<div class="ann-takeaway">Pairwise comparison is the right pattern when <code>n</code> is small by definition (one day's entries). The marker-driven trigger gives a clean checkpoint where every entry has been collected before testing begins. Don't be tempted to optimise for n² here — the problem constraints already keep <code>n</code> manageable.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code>      <span class="c">/* the intersection test, once */</span>
      <span class="k">IF</span> (<span class="v">dayStarts</span>[<span class="v">i</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">j</span>]
          <span class="k">AND</span> <span class="v">dayStarts</span>[<span class="v">j</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">i</span>]) <span class="k">THEN</span>
      ( <span class="v">flagIdx</span> <span class="op">=</span> <span class="v">dayIdxs</span>[<span class="v">j</span>]
        <span class="v">OUT_MSG</span>[<span class="v">flagIdx</span>] <span class="op">=</span>
            <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span>
            <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_overlap</span>)
      )
      <span class="v">j</span> <span class="op">=</span> <span class="v">j</span> <span class="op">+</span> <span class="n">1</span>
    )
    <span class="v">i</span> <span class="op">=</span> <span class="v">i</span> <span class="op">+</span> <span class="n">1</span>
  )</code></pre></div>
<div class="annot-note">
<span class="nt">Block 7b · Strict less-than</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Four concepts together</div>

<!-- PART 1: The intersection rule -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · The interval intersection rule — one test, every case covered</div>

<div style="background:#1f1c19; color:#e6e1d8; padding:12px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:11px; line-height:1.6; margin-bottom:10px; overflow-x:auto;">
IF (dayStarts[j] < dayStops[i] AND dayStops[j] > dayStarts[i]) THEN overlap
</div>
<div style="font-size:10.5px; color:#5a544e; line-height:1.6; font-style:italic;">
Two intervals overlap if — and only if — each one starts before the other ends. One rule covers every case.
</div>

<!-- PART 2: The three cases visualised -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · The three cases — overlap, touching, disjoint</div>

<div style="display:grid; grid-template-columns:1fr; gap:8px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; padding:10px 12px;">
<div style="display:flex; justify-content:space-between; align-items:baseline;">
<div style="font-size:10px; font-weight:700; color:#c0392b; letter-spacing:0.5px;">CASE A · OVERLAP</div>
<div style="font-size:10.5px; font-weight:700; color:#c0392b;">✗ Flagged</div>
</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; color:#2d2926; margin-top:4px;">Entry i: 09:00 → 12:00    Entry j: 11:00 → 14:00</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:2px;">j starts (11:00) before i ends (12:00), j ends (14:00) after i starts (09:00).</div>
</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; padding:10px 12px;">
<div style="display:flex; justify-content:space-between; align-items:baseline;">
<div style="font-size:10px; font-weight:700; color:#3d7a52; letter-spacing:0.5px;">CASE B · TOUCHING</div>
<div style="font-size:10.5px; font-weight:700; color:#3d7a52;">✓ Clean</div>
</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; color:#2d2926; margin-top:4px;">Entry i: 09:00 → 12:00    Entry j: 12:00 → 14:00</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:2px;">Strict <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace"><</code> means 12:00 is NOT before 12:00. Touch isn't overlap.</div>
</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; padding:10px 12px;">
<div style="display:flex; justify-content:space-between; align-items:baseline;">
<div style="font-size:10px; font-weight:700; color:#3d7a52; letter-spacing:0.5px;">CASE C · DISJOINT</div>
<div style="font-size:10.5px; font-weight:700; color:#3d7a52;">✓ Clean</div>
</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; color:#2d2926; margin-top:4px;">Entry i: 09:00 → 12:00    Entry j: 14:00 → 16:00</div>
<div style="font-size:10px; color:#5a544e; font-style:italic; margin-top:2px;">j starts (14:00) after i ends (12:00). Clearly separate.</div>
</div>
</div>

<!-- PART 3: Why strict less-than -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · Why strict <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace"><</code> — the most consequential operator choice</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#c0392b; letter-spacing:0.5px;">WRONG — uses <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace"><=</code></div>
<div style="font-size:10.5px; color:#5a544e; margin-top:6px; line-height:1.5;">Every back-to-back entry gets flagged. Worker enters 09–12 then 12–14 (clean break) and the system says <em>"overlap!"</em></div>
</div>
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#3d7a52; letter-spacing:0.5px;">RIGHT — uses <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace"><</code></div>
<div style="font-size:10.5px; color:#5a544e; margin-top:6px; line-height:1.5;">Touching entries pass cleanly. Only real overlap fires the flag.</div>
</div>
</div>

<!-- PART 4: Which entry gets the flag -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 4 · Which entry gets the flag — always the later one</div>

<div style="background:#fff; border:1px solid #e8e3d8; border-radius:4px; padding:12px;">
<div style="background:#1f1c19; color:#e6e1d8; padding:10px 12px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:11px; overflow-x:auto;">
<div style="color:#7a7570;">// j is always > i, so dayIdxs[j] is the entry added more recently</div>
<div style="margin-top:4px;">flagIdx = dayIdxs[j]   <span style="color:#7a7570;">// the LATER entry — matches worker's mental model</span></div>
</div>
<div style="font-size:10.5px; color:#5a544e; margin-top:8px; line-height:1.55;">
The pairwise loop uses <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">i < j</code> ordering, so <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">j</code> is always the later-added entry. Flagging it (not the earlier one) matches the worker's mental model: <em>"I just added this entry and it conflicts."</em>
</div>
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The interval intersection rule, derived</div>
<ul class="ann-bullets">
<li>The fundamental insight powering this entire block fits in one sentence: <strong>two intervals overlap if and only if each one starts before the other ends</strong>. That single rule covers every possible case — touching boundaries, partial overlap, complete containment, disjoint intervals.</li>
<li>Why this rule works can be derived geometrically. Place two intervals A and B on a timeline. If they don't overlap, one of two things must be true: A ends before B starts, or B ends before A starts. Equivalently — flipping each — A.start is at-or-after B.stop, or B.start is at-or-after A.stop. Negate both for "they DO overlap": A.start < B.stop AND B.start < A.stop.</li>
<li>The elegance of this is that you don't need to handle each shape of overlap (left-overlapping, right-overlapping, contained, identical) as separate cases. The two-condition test catches them all uniformly.</li>
<li>Algorithms textbooks call this the <em>interval intersection</em> test. It's one of those small mathematical tools that pays back its mental cost many times over — once you internalise it, you'll see opportunities to apply it everywhere from scheduling code to graphics clipping.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>A worked example to ground the rule</div>
<div class="ann-snippet">A: 09:00–12:00     B: 10:00–13:00

A.start < B.stop  →  9 < 13  →  TRUE
B.start < A.stop  →  10 < 12 →  TRUE
—————
OVERLAP</div>
<ul class="ann-bullets">
<li>A is 09:00–12:00 and B is 10:00–13:00. Both conditions evaluate true — A starts at 9 (before B ends at 13), and B starts at 10 (before A ends at 12). The intersection runs from 10:00 to 12:00, two hours of genuine overlap.</li>
<li>Try a non-overlapping case to verify the rule's negation. A: 09:00–11:00, B: 13:00–15:00. First condition: 9 < 15? TRUE. Second condition: 13 < 11? FALSE. The AND fails, no overlap detected. Correct.</li>
<li>Try a touching case. A: 09:00–12:00, B: 12:00–13:00. First: 9 < 13? TRUE. Second: 12 < 12? FALSE (because the comparison is strict). No overlap. Also correct — this is the case the strict less-than was chosen for.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>The single character that decides everything</div>
<ul class="ann-bullets">
<li>The <code><</code> symbol in this test is <strong>strict less-than</strong>, not <code>≤</code>. That single character distinction is the difference between a usable formula and a useless one.</li>
<li>Picture the most common timecard pattern in the world: a morning shift ending at 12:00 immediately followed by a lunch break starting at 12:00. The two entries <em>touch</em> at noon — they share an endpoint — but they don't overlap. There's no double-booking; the worker stopped one activity and started another at the same instant.</li>
<li>With strict <code><</code>, the second condition becomes <em>"is 12 less than 12?"</em> The answer is FALSE. The AND fails, no overlap detected, no flag. The clean handover is recognised as clean. This is what you want.</li>
<li>If you used <code>≤</code> instead, the test becomes <em>"is 12 less than or equal to 12?"</em> The answer is TRUE. Now both conditions are true, the AND fires, an overlap is reported. Every clean back-to-back transition in every timecard would falsely flag. The formula would be unusable in production.</li>
<li>This is a one-character decision with massive consequences. If you're ever tempted to "tighten" the comparison from <code><</code> to <code>≤</code>, don't. The looser comparison is <em>correct</em>; the tighter one would break everything.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">4</span>Which entry gets the flag, and why it matters</div>
<div class="ann-snippet">flagIdx = dayIdxs[<span style="color:#e07060;">j</span>]   <span style="color:#d4c896;">// the LATER entry</span></div>
<ul class="ann-bullets">
<li>When an overlap is detected, the formula has to choose <em>which</em> of the two entries to flag. Both rows are involved in the conflict; only one gets the error message. The choice is not arbitrary.</li>
<li>The code uses <code>dayIdxs[j]</code> — the later entry in the pair. Recall that <code>j</code> always starts past <code>i</code>, so when the formula gets here, <code>j</code> is the entry that was added to the buffer <em>after</em> entry <code>i</code>. In other words, <code>j</code> is what the worker added more recently.</li>
<li>This matches how workers think about their own data. When they see an error, the natural assumption is <em>"the row I just added is the problem"</em>, not <em>"a row I added earlier is suddenly broken"</em>. Flagging <code>j</code> aligns with that mental model.</li>
<li>If the formula flagged <code>i</code> instead (the earlier entry), the worker would see something deeply unsettling: a row that was fine a moment ago suddenly turning red because of an entry they made later. They'd waste time looking at the flagged row, trying to figure out what's wrong with it — when the actual problem is the new entry that caused the conflict.</li>
<li>Choosing the later entry is a small UX detail with a large effect on debuggability. Small decisions in error-messaging compound; respect the user's mental model.</li>
</ul>
</div>
<div class="ann-takeaway">Two intervals overlap if and only if each one starts before the other ends. Strict less-than (<code><</code>, never <code>≤</code>) handles touching boundaries correctly — the difference between a usable formula and a useless one. Flag the later entry in any conflicting pair, because that matches how workers naturally think about their own errors.</div>
</div></div>
</div>
</div>

<div class="annot-line">
<div class="annot-code"><pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><code>  <span class="c">/* reset day-level state for next day */</span>
  <span class="v">dayStarts</span> <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
  <span class="v">dayStops</span>  <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
  <span class="v">dayIdxs</span>   <span class="op">=</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
  <span class="v">dayCnt</span>    <span class="op">=</span> <span class="n">0</span>
  <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>
  <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">NullDate</span>
  <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'N'</span>
)</code></pre></div>
<div class="annot-note">
<span class="nt">Block 7c · Boundary reset</span>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:14px 0;">
<div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram for this annotation · Three concepts together</div>

<!-- PART 1 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:6px 0 10px;">Part 1 · Seven lines, one atomic group — what gets reset, what doesn't</div>

<div style="background:#1f1c19; padding:12px 14px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:11px; line-height:1.7; margin-bottom:8px; overflow-x:auto;">
<span style="color:#f0d68a;">// runs at every END_DAY / END_PERIOD</span><br>
<span style="color:#7fc8a0;">dayStarts    = EMPTY_DATE_NUMBER</span><br>
<span style="color:#7fc8a0;">dayStops     = EMPTY_DATE_NUMBER</span><br>
<span style="color:#7fc8a0;">dayIdxs      = EMPTY_NUMBER_NUMBER</span><br>
<span style="color:#7fc8a0;">dayCnt       = 0</span> <span style="color:#f0d68a; font-style:italic;">← clear day buffer (4 lines)</span><br>
<span style="color:#e8b96a;">l_meal_taken = 'N'</span> <span style="color:#f0d68a; font-style:italic;">← reset the meal flag</span><br>
<span style="color:#7fa8e8;">stretchStart = NullDate</span><br>
<span style="color:#7fa8e8;">inStretch    = 'N'</span> <span style="color:#f0d68a; font-style:italic;">← clear stretch tracker (2 lines)</span><br>
<hr style="border:none; border-top:1px dashed #666; margin:6px 0;">
<span style="color:#e07060;">// OUT_MSG is NOT reset — it must persist across all days, until RETURN</span>
</div>

<!-- PART 2 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 2 · What goes wrong if you forget any one of these resets</div>

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">FORGET DAY BUFFER</div>
<div style="padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#2d2926;">Symptom: false flags</div>
<div style="font-size:9.5px; color:#5a544e; line-height:1.5; margin-top:4px;">Day 2 entries appended on top of yesterday's leftovers. Pairwise test sees mixed days. 09:00 day-1 falsely overlaps 11:00 day-2 (date ignored).</div>
<div style="font-size:10px; color:#c0392b; font-weight:700; margin-top:8px;">Over-flag — visible noise</div>
</div>
</div>
<div style="background:#fff5f0; border:2.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">FORGET l_meal_taken</div>
<div style="padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#c0392b;">Symptom: NO flags (worst)</div>
<div style="font-size:9.5px; color:#5a544e; line-height:1.5; margin-top:4px;">Once flag flips 'Y' on day 1, stays 'Y' for entire timecard. Block 8's gate stays closed. Stretch tracker silently dies. Workers exceed legal cap freely.</div>
<div style="font-size:10px; color:#c0392b; font-weight:700; margin-top:8px;">Under-flag — legally dangerous</div>
</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">FORGET STRETCH TRACKER</div>
<div style="padding:10px 12px;">
<div style="font-size:10px; font-weight:700; color:#2d2926;">Cross-day false flags</div>
<div style="font-size:9.5px; color:#5a544e; line-height:1.5; margin-top:4px;">Day-1 stretch survives into day 2. Day-2 first entry extends or restarts that ghost. contHrs calculations include yesterday's hours. Falsely 13+h.</div>
<div style="font-size:10px; color:#c0392b; font-weight:700; margin-top:8px;">Over-flag — wrong metrics</div>
</div>
</div>
</div>
<div style="font-size:10.5px; color:#5a544e; font-style:italic; margin-top:10px;">Each missing reset breaks the formula in a different way. None crash. All ship to production silently.</div>

<!-- PART 3 -->
<div style="font-size:11px; letter-spacing:1.4px; color:#1f5fa8; text-transform:uppercase; font-weight:700; margin:18px 0 10px;">Part 3 · Why this category of bug evades testing</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
<div style="background:#e8f4ea; border:1.5px solid #3d7a52; border-radius:4px; overflow:hidden;">
<div style="background:#3d7a52; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">UAT — bug stays dormant</div>
<div style="padding:10px 12px; font-size:10.5px; color:#5a544e; line-height:1.7;">
Test timecards: 1–2 days only<br>
Single-day data never crosses END_DAY<br>
Reset code never executes<br>
<strong style="color:#3d7a52;">✓ Tests pass — sign-off given</strong>
</div>
</div>
<div style="background:#fff5f0; border:1.5px solid #c0392b; border-radius:4px; overflow:hidden;">
<div style="background:#c0392b; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">PRODUCTION — bug fires immediately</div>
<div style="padding:10px 12px; font-size:10.5px; color:#5a544e; line-height:1.7;">
Real timecards: 10–14 days (biweekly)<br>
END_DAY hits on day 2, then every day<br>
Missing reset fires on first multi-day<br>
<strong style="color:#c0392b;">✗ Production incident on day 1</strong>
</div>
</div>
</div>

<div style="background:#fff; border:1.5px solid #1f5fa8; border-radius:4px; overflow:hidden;">
<div style="background:#1f5fa8; color:#fff; font-size:10px; font-weight:700; text-align:center; padding:5px;">THE DEFENCE — treat the reset block as atomic</div>
<div style="padding:10px 14px; font-size:10.5px; color:#2d2926; line-height:1.6;">
Every day-level state variable declared anywhere in the formula <strong>must</strong> appear in this reset.<br>
Code review for this block: scan for any per-day state that's missing from the reset list.<br>
<em style="color:#5a544e;">More careful testing won't catch this. The fix is structural — never edit one line of the reset without considering the others.</em>
</div>
</div>

</div>

<div class="ann-text"><div class="ann-parts">
<div class="ann-part">
<div class="ann-part-head"><span class="num">1</span>The reset block, line by line</div>
<div class="ann-snippet">dayStarts    = EMPTY_DATE_NUMBER
dayStops     = EMPTY_DATE_NUMBER
dayIdxs      = EMPTY_NUMBER_NUMBER
dayCnt       = 0
l_meal_taken = 'N'
stretchStart = NullDate
inStretch    = 'N'</div>
<ul class="ann-bullets">
<li>This sequence runs immediately after the pairwise overlap test fires (or doesn't). Whatever flags the test produced have already landed in <code>OUT_MSG</code>; this block's job is to prepare the formula's state for the next day's data.</li>
<li>The first four lines clear the day buffer. Reassigning <code>dayStarts</code>, <code>dayStops</code>, and <code>dayIdxs</code> to their empty array constants discards every entry the buffer accumulated during the day just completed. <code>dayCnt</code> resets to zero so the next append-and-increment cycle starts fresh at position 1.</li>
<li>The fifth line resets <code>l_meal_taken</code> to <code>'N'</code>. This flag has been tracking whether the worker logged a meal break today; tomorrow is a new day with a new meal-tracking cycle, so the flag must reset.</li>
<li>The last two lines clear the stretch tracker. <code>stretchStart</code> goes back to <code>NullDate</code> (the sentinel for "no active stretch"), and <code>inStretch</code> flips to <code>'N'</code> to signal the tracker is currently idle.</li>
<li>Notice that <code>OUT_MSG</code> is <em>not</em> reset here. That array accumulates flags across the entire formula run and persists until the formula returns. Resetting it here would erase every flag generated so far — a catastrophic bug.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">2</span>What each missing reset would silently break</div>
<ul class="ann-bullets">
<li><strong>Forget the day buffer reset:</strong> Day 1's Reg Hours entries stay in the buffer when day 2 starts. Block 6d on day 2 appends new entries on top of yesterday's leftovers. The pairwise overlap test now sees entries from two different days mixed together. Time intervals from different days can falsely overlap (a 09:00 entry on day 1 conflicts with an 11:00 entry on day 2 if you ignore the date component). Cascading false flags follow, all impossible to debug because the bug is in <em>state</em>, not in <em>logic</em>.</li>
<li><strong>Forget <code>l_meal_taken</code>:</strong> Once the worker logs a meal on day 1, this flag flips to <code>'Y'</code>. Without the reset, it stays <code>'Y'</code> for every subsequent day in the timecard period. Block 8's continuous-hours gate checks this flag and stays closed forever. The formula stops tracking continuous work entirely from day 2 onwards. <strong>Workers can exceed the legal cap by hours and the formula won't notice</strong>, because tracking is silently disabled. This is the most dangerous of the missing-reset bugs because it produces <em>under</em>-flagging, not over-flagging — the lack of errors looks like the formula is working correctly.</li>
<li><strong>Forget the stretch tracker reset:</strong> Day 1's final stretch stays alive into day 2. The first Reg Hours entry on day 2 either extends or restarts that stretch, but either way the resulting <code>contHrs</code> calculation includes time from yesterday. False flags fire on day-2 entries because the tracked stretch falsely appears to span 13+ hours.</li>
<li>The takeaway: <strong>each missing reset breaks the formula in a different way</strong>. Some over-flag (false positives, annoying), some under-flag (false negatives, dangerous), some produce nonsense. None of them crash. All of them ship to production silently.</li>
</ul>
</div>
<div class="ann-part">
<div class="ann-part-head"><span class="num">3</span>Why this category of bug evades testing</div>
<ul class="ann-bullets">
<li>UAT timecards are typically constructed for specific test scenarios — one day of work, two days at most. Test data is curated to exercise particular validation paths cleanly.</li>
<li>A missing reset only misbehaves when the formula crosses a day boundary. <strong>Single-day test timecards never cross that boundary</strong>, so the bug stays dormant. UAT passes. Sign-off happens. The formula goes to production.</li>
<li>Then real workers submit real biweekly timecards. Real biweekly timecards have 10 to 14 days of data. The missing reset fires on day 2, and every day after that. The bug surfaces on the very first real submission, but by then it's a production incident.</li>
<li>The defence against this category of bug isn't more careful testing — it's <strong>treating the reset block as atomic</strong>. Every state variable that has a per-day lifetime must be reset at every day boundary. Code review for this block should specifically look for any day-level state declared elsewhere in the formula but missing from this reset.</li>
</ul>
</div>
<div class="ann-takeaway">Every reset line in this block is part of one atomic group. They live together; they reset together. The bug type they prevent is uniquely dangerous because it produces wrong-but-not-crashing behaviour that survives single-day UAT and only surfaces on the first multi-day production submission. Treat the reset block as sacred — never edit one line without considering the others.</div>
</div></div>
</div>
</div>

</div>
</div>




<!-- NEXT IN SERIES -->
<div style="background:#fff8e8; border:1px solid #b97417; border-radius:6px; padding:20px 24px; margin:40px 0 32px 0;">
<div style="font-size:10px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Next in The TER Series</div>
<div style="font-size:18px; font-weight:700; color:#2d2926; margin-bottom:8px;">Part 4 — The State Machine</div>
<div style="font-size:13.5px; color:#5a544e; line-height:1.6;">The hardest part of the formula is the continuous-hours tracker — a two-state machine with four transitions that survives across loop iterations. Part 4 walks through every transition (START, EXTEND, RESTART, RESET), the setup dependencies in OTL that must exist for the formula to fire, and a full end-to-end trace of Sarah's broken timecard.</div>
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