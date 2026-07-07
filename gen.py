import xml.etree.ElementTree as ET, re, os, html as hl
XML = "blogpost.xml"
OUT = "src/content/posts"
tree = ET.parse(XML)
root = tree.getroot()
A = "{http://www.w3.org/2005/Atom}"
posts = []
for e in root.findall(f"{A}entry"):
    te = e.find(f"{A}title")
    pe = e.find(f"{A}published")
    ce = e.find(f"{A}content")
    if te is None or pe is None: continue
    title = (te.text or "").strip()
    if not title: continue
    links = e.findall(f"{A}link")
    url = next((l.get("href","") for l in links if l.get("rel")=="alternate"),"")
    if url and "blogspot.com" not in url: continue
    posts.append({"title":title,"date":pe.text[:10],"content":ce.text if ce is not None else "","url":url})
posts.sort(key=lambda x:x["date"])
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith((".md",".mdx")): os.remove(os.path.join(OUT,f))
REMAP = {
    "oracle-fast-formula-time-entry-rule":"oracle-fast-formula-time-entry-rule-part-1",
    "oracle-fast-formula-time-entry-rule_01813668993":"oracle-fast-formula-time-entry-rule-part-2",
    "oracle-fast-formula-time-entry-rule_01788502086":"oracle-fast-formula-time-entry-rule-part-3",
    "oracle-fast-formula-time-entry-rule_01764150804":"oracle-fast-formula-time-entry-rule-part-4",
}
def slug(title,url):
    m=re.search(r"/([^/]+)\.html$",url or "")
    if m:
        s=m.group(1); s=re.sub(r"_\d{8,}$","",s); return REMAP.get(s,s)
    s=re.sub(r"[^\w\s-]","",title.lower()); s=re.sub(r"[\s_]+","-",s); return s[:70]
def get_tags(t):
    t=t.lower(); out=["Fast Formula","Oracle HCM Cloud"]
    if "hdl" in t or "wsa" in t: out+=["HDL"]
    if "benefit" in t or "periodiz" in t or "election" in t: out+=["Benefits"]
    if "recruit" in t: out+=["Recruiting"]
    if "tcr" in t or "night" in t or "day-type" in t or "ot bucket" in t or "regular and ot" in t: out+=["TCR","OTL","Time and Labor"]
    if "ter" in t or "time entry" in t: out+=["TER","Time Entry Rule","OTL"]
    if "absence" in t or "plan_balance" in t: out+=["Absence Management"]
    if "null" in t or "defaulted" in t or "isnull" in t or "alias" in t: out+=["Null Handling"]
    if "debug" in t or "log" in t: out+=["Debugging"]
    seen=set();r=[]
    for x in out:
        if x not in seen: seen.add(x);r.append(x)
    return r[:8]
def clean(raw):
    if not raw: return ""
    t=hl.unescape(raw)
    t=re.sub(r"<style[^>]*>.*?</style>","",t,flags=re.DOTALL|re.I)
    t=re.sub(r"<script[^>]*>.*?</script>","",t,flags=re.DOTALL|re.I)
    t=re.sub(r"<!--.*?-->","",t,flags=re.DOTALL)
    return t.strip()
def get_desc(title,content):
    t=re.sub(r"<[^>]+>"," ",content); t=hl.unescape(t); t=re.sub(r"\s+"," ",t).strip()
    s=[x.strip() for x in t.split(".") if len(x.strip())>30]
    d=s[0] if s else title
    return re.sub(r'["\'{}[\]\\]',"",d)[:200]
seen_slugs=set(); n=0
for p in posts:
    sl=slug(p["title"],p["url"])
    if sl in seen_slugs: sl=sl+"-"+p["date"]
    seen_slugs.add(sl)
    body=clean(p["content"])
    tg=get_tags(p["title"])
    tg_yaml="["+", ".join(f'"{x}"' for x in tg)+"]"
    ti=p["title"].replace('"',"'")
    de=get_desc(p["title"],p["content"])
    fm=f'---\ntitle: "{ti}"\ndescription: "{de}"\npubDate: {p["date"]}\ntags: {tg_yaml}\n---\n\n'
    path=os.path.join(OUT,sl+".md")
    open(path,"w",encoding="utf-8").write(fm+body)
    print(f"  {sl}.md"); n+=1
print(f"Written: {n}")
