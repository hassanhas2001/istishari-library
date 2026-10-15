# الإسناد والتراخيص

## مصادر استُفيد منها في المهارات

| المصدر | الترخيص | ما أُخذ منه |
| --- | --- | --- |
| [Mermaid](https://github.com/mermaid-js/mermaid) | MIT | صيغة المخططات وأنواعها في `arabic-diagrams` و`arabic-timelines`. لم يُنسخ منه نص. |
| [Graphviz](https://graphviz.org) | EPL 2.0 | صيغة DOT في `arabic-diagrams`. لم يُنسخ منه نص. |
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit): مهارة `mermaid-diagrams` | MIT، حقوق النسخ © 2026 Leonardo Flores | فكرة دليل اختيار نوع المخطط. المهارة الأصلية موجهة للبرمجيات، فكُتبت `arabic-diagrams` من جديد للمخططات المؤسسية العربية. |
| [obra/superpowers](https://github.com/obra/superpowers) الإصدار 6.2 | MIT | فكرة جدول «الذريعة والرد» في قسم «ذرائع لا تُقبل» من `istishari-core`. لم يُنسخ منه نص. |
| [blader/humanizer](https://github.com/blader/humanizer) الإصدار 3.1 | MIT | أفكار الأنماط ٢٠–٢٢ وتوسيع النمطين ٣ و١٦ وقاعدة «كل جملة تضيف» في `arabic-institutional-writing`. لم يُنسخ منه نص. |
| [antvis/chart-visualization-skills](https://github.com/antvis/chart-visualization-skills): مهارة `antv-infographic` | MIT، حقوق النسخ © 2025 AntV Visualization Team | فكرة تصنيف القوالب بحسب شكل المحتوى (قائمة، تسلسل، مقارنة) والبدء بالبنية قبل الشكل في `arabic-infographic`. جُرّبت المكتبة الأصلية بالعربية فلم تدعم الاتجاه من اليمين إلى اليسار، وتجلب أيقوناتها من خدمة خارجية، فكُتبت المهارة والسكربت من جديد. |
| [W3C WCAG 2](https://www.w3.org/TR/WCAG22/) | W3C Document License | حدود التباين 4.5:1 و3:1 في `visual-identity`. |
| [Google Fonts](https://github.com/google/fonts) | SIL Open Font License 1.1 | الخطوط المقترحة. لا تُوزَّع ملفات الخطوط في هذا المستودع؛ تُنزَّل من مصدرها عند الحاجة. |

## اختبارات أُجريت

القوالب والسكربتات في `arabic-diagrams` و`arabic-timelines` جُرّبت في أكتوبر ٢٠٢٦ على Graphviz، وMermaid CLI ‏11.4.2، وmatplotlib ‏3.11.2، مع خط IBM Plex Sans Arabic، وفُحصت صورها الناتجة بصريًا. وسكربت `arabic-infographic` جُرّب بقوالبه الخمسة على Chromium عبر Playwright، بخط مضمَّن وبخطوط النظام، وفُحصت صوره بصريًا.

## مهارات النواة

مهارات مجلد `core/` من إعداد صاحب المستودع.
