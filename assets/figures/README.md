iClinic Concept Diagrams

Files (in this folder):
- `iClinic_concept.mmd` — Combined conceptual architecture (original single-diagram version).
- `figure1_overall.mmd` — Figure 1: Overall Conceptual Architecture.
- `figure2_dataflow.mmd` — Figure 2: Data Flow Architecture (Analytics Engine).
- `figure3_modular.mmd` — Figure 3: Modular System Architecture & External Integrations.

How to render / export

- VS Code: open any `.mmd` file and use a Mermaid preview extension such as "Markdown Preview Mermaid Support" or "Mermaid Preview" to export SVG/PNG.

- Mermaid CLI (Node.js): install and run `mmdc` to export files (example):

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i figure1_overall.mmd -o figure1_overall.svg
mmdc -i figure2_dataflow.mmd -o figure2_dataflow.svg
mmdc -i figure3_modular.mmd -o figure3_modular.svg
```

- Online: paste the Mermaid markup into https://mermaid.live to preview and export.

If you want, I can export SVG or PNG files and add them here — tell me which format you prefer and which figures to export.