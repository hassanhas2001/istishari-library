# الرسم الفعلي: الأوامر والقوالب المجرّبة

جُرّبت هذه القوالب في أكتوبر ٢٠٢٦ على Graphviz وMermaid CLI ‏11، وظهرت فيها الحروف العربية صحيحة.

## ١. التأكد من وجود خط عربي

```bash
fc-list | grep -i "arabic" | head -3
```

إذا لم يظهر شيء، فثبّت خطًا مفتوح الترخيص من مستودع Google Fonts:

```bash
mkdir -p ~/.fonts && cd ~/.fonts
for w in Regular Bold; do
  curl -fsSLO "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsansarabic/IBMPlexSansArabic-$w.ttf"
done
fc-cache -f
```

إذا تعذّر التنزيل، فاذكر ذلك للمستخدم، واقترح عرض المخطط داخل المحادثة بشيفرة Mermaid بدل الصورة.

## ٢. هيكل تنظيمي بـGraphviz

```dot
digraph G {
  graph [rankdir=TB, splines=ortho, nodesep=0.4, ranksep=0.5];
  node  [shape=box, style=filled, fillcolor="#FFFFFF", color="#1F3A5F",
         fontname="IBM Plex Sans Arabic", fontsize=14, margin="0.25,0.12"];
  edge  [color="#6B7785", arrowhead=none];

  A [label="مجلس الأمناء",   fillcolor="#1F3A5F", fontcolor="#FFFFFF"];
  B [label="الرئيس التنفيذي", fillcolor="#1F3A5F", fontcolor="#FFFFFF"];
  A -> B;

  // الترتيب الرسمي: المنح، ثم الاستراتيجية، ثم الخدمات المشتركة
  // يُكتب معكوسًا لتظهر «المنح» في أقصى اليمين
  B -> E; B -> D; B -> C;
  C [label="إدارة المنح"];
  D [label="إدارة الاستراتيجية والأداء"];
  E [label="الخدمات المشتركة"];
}
```

```bash
dot -Tpng -Gdpi=200 org.dot -o org.png
```

- `splines=ortho` يعطي خطوطًا قائمة الزوايا، وهو الشكل المألوف في الهياكل التنظيمية.
- للعلاقات الاستشارية (لجنة تتبع المجلس دون أن تكون في خط السلطة) يُستعمل خط متقطع: `edge [style=dashed]`.
- لوضع وحدات في المستوى نفسه: `{rank=same; C; D; E;}`.

## ٣. مخطط تدفق بـMermaid

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"IBM Plex Sans Arabic","primaryColor":"#FFFFFF","primaryBorderColor":"#1F3A5F","primaryTextColor":"#1F2933","lineColor":"#6B7785","fontSize":"16px"}}}%%
flowchart RL
  A(["استلام الطلب"]) --> B["الفحص الأولي"]
  B --> C{"مستوفٍ للشروط؟"}
  C -- نعم --> D["التقييم الفني"]
  C -- لا --> E(["إشعار المتقدم"])
```

الأشكال: `([...])` بداية أو نهاية، و`[...]` خطوة، و`{...}` قرار.

مسارات حسب الجهة:

```mermaid
flowchart RL
  subgraph S1["الجهة المتقدمة"]
    A["تقديم الطلب"]
  end
  subgraph S2["إدارة المنح"]
    B["الفحص"] --> C["التقييم"]
  end
  A --> B
```

## ٤. تحويل Mermaid إلى صورة

يحتاج إلى Node.js ومتصفح Chromium.

```bash
npm i -s @mermaid-js/mermaid-cli@11.4.2
echo '{"args":["--no-sandbox"]}' > pp.json
npx mmdc -p pp.json -i flow.mmd -o flow.png -s 2 -b white
```

- إذا لم يجد الأداة متصفحًا، فأضف إلى `pp.json` المفتاح `"executablePath"` بمسار Chromium المثبت.
- إذا تعذّر تثبيت الأداة، فأعد رسم المخطط بـGraphviz (`rankdir=RL` لمخطط التدفق)، أو اعرضه داخل المحادثة.

## ٥. أشكال PowerPoint الأصلية

عند بناء ملف PowerPoint برمجيًا وطلب المستخدم مخططًا قابلًا للتعديل:
- مربع لكل عقدة، ونص محاذى لليمين واتجاه فقرة من اليمين إلى اليسار.
- موصلات (connectors) بين المربعات، لا خطوط حرة، حتى تبقى متصلة عند التحريك.
- يُحسب موقع كل مستوى من اليمين: العقدة الأولى في أقصى اليمين.
