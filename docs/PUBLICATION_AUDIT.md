# Component rights and artwork audit

This edition retains component-specific licenses and attribution. The custom [Blitz Internal Use License 1.0](../LICENSE) now covers original material only, excluding third-party material and prior separate grants. The [licensing guide](LICENSING.md) and [file inventory](license-inventory.csv) record that scope; no authorship is inferred merely from possession of the source archive. Public viewing, permitted internal use and broader redistribution remain separate. This is a bounded source review, not a guarantee about unrecorded lineage or future downstream use.

## Component notices

| Component | Applicable evidence and treatment |
|---|---|
| Anti-slop | The owner-authorized CC BY-SA 4.0 adapter scope covers exactly `SKILL.md` and `references/post-pass.md`. Seven upstream MIT licenses and source attributions remain in the component. See [LICENSE](../Blitz/skills/anti-slop/LICENSE.txt) and [NOTICE](../Blitz/skills/anti-slop/NOTICE.md). |
| Gauntlet Verify | The upstream adaptations carry CC BY 4.0; the identified Claude of Duty contribution retains MIT. Creator/source attribution, modification information and the MIT notice remain in [NOTICE](../Blitz/skills/gauntlet-verify/NOTICE.md), alongside the CC license. |
| Meta Skill | Anthropic's Apache-2.0 text and attribution are retained. Modified inherited files carry modification notices. See [NOTICE](../Blitz/skills/meta-skill/NOTICE.md). |
| Google Slides | Both consulting-deck and executive-slide-skill Apache source licenses are retained, with the consulting-deck NOTICE, copyright attributions and adaptation marker. See [NOTICE](../Blitz/skills/google-slides/NOTICE.md). |
| Diagram Design | The main method's Cathryn Lavery MIT notice and the retained generic Tabler icon MIT notice remain. Product-specific artwork is replaced with generic functional symbols. See [icon provenance](../Blitz/skills/diagram-design/THIRD_PARTY_LICENSES.md). |
| Frontend Scroll Craft and Website Cloner | Their identified upstream MIT attributions remain with the components. See [method provenance](../Blitz/skills/provenance.md). |
| Frontend Taste | The licensing inventory identified a previously omitted taste-skill MIT and Impeccable Apache-2.0 attribution chain in the inherited source statements. Pinned license texts, the Impeccable notice and modification notices are now retained. See [NOTICE](../Blitz/skills/frontend-taste/NOTICE.md). |

### Anti-slop attribution chain

The [pinned upstream credits](https://github.com/kjmagnan1s/anti-slop/blob/a3807e5d9030738eb66cb61df47844e87963cc43/CREDITS.md) expressly retain CC BY-SA 4.0 for Wikipedia-derived material. The scoped adapter treatment preserves that lineage rather than applying a blanket MIT claim. [CC BY-SA 4.0 sections 3(a)/(b)](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en) permit a link to the legal code and require applicable attribution, changes and adapter terms.

The identified MIT texts for Kevin Magnan, Conor Bronsdon, Siqi Chen, Brandon Wise, Hardik Pandya, Peter Yang and aasha were compared with pinned primary sources. Kevin's credits and Conor's upstream NOTICE are also retained. Wikipedia contributors are attributed through the article and author history, consistent with [Wikimedia's reuse terms](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use/en#7._Licensing_of_Content). Exact historical synchronization revisions remain unrecorded; no grant is invented for an unknown source.

### Other identified grants

The Gauntlet license text matches the [EauDoon adaptation](https://github.com/EauDoon/gauntlet-verify/blob/4c0f066e2018dc6bcc3761f069c361442bd84f66/LICENSE) and [RoboNuggets source](https://github.com/robonuggets/gauntlet-loop/blob/9b1975a1b8f01981f3f1e6b667ad3aaf907178ea/LICENSE). Attribution identifies Jay E/RoboNuggets and Matt Shumer, with the [Claude of Duty MIT notice](https://github.com/mshumer/Claude-of-Duty/blob/d9b237b75c9304ab8d9ef4cfa0c3568c7c11a853/LICENSE).

Meta Skill's license matches the [pinned Anthropic source](https://github.com/anthropics/skills/blob/b0cbd3df1533b396d281a6886d5132f623393a9c/skills/skill-creator/LICENSE.txt). The identified root third-party notice covers imageio, FFmpeg, Pillow and fonts not bundled in this adaptation; no additional applicable notice was identified for the inherited skill text/scripts. Unknown synchronization timing remains disclosed in its NOTICE.

The presentation notices preserve the [consulting-deck license](https://github.com/zairuilab/consulting-deck/blob/25f533497594eb8ab27082a4c0c16a9e40c63fc2/LICENSE) and its upstream NOTICE, plus the separate [executive-slide-skill license](https://github.com/trev0rr/executive-slide-skill/blob/917978165680f77f249a6f169f9edf5121543099/LICENSE). A shortened license text from one source does not replace the other source's complete grant.

## Product artwork replacement

The catalog preserves 87 lookup keys: 50 generic Tabler symbols and 37 newly authored functional stand-ins for product nodes. The latter include two formerly empty entries. Across 12 bundled architecture examples, 92 product glyph placements use these generic symbols. Labels, positions, dimensions, colors, connections and method lookup keys remain useful. Official-logo recognition is no longer supplied.

The broader repair followed an independent finding that a collection-level license did not establish every individual logo's terms. For example, the [R Foundation](https://www.r-project.org/logo/) identifies CC BY-SA 4.0 or GPL-2 terms for its artwork; the [ASF policy](https://www.apache.org/foundation/marks/) treats Apache graphic logos separately. The [Simple Icons disclaimer](https://github.com/simple-icons/simple-icons/blob/dc7b10662a0a2cfdfc9305e2a2b06c023c30724a/DISCLAIMER.md) explicitly distinguishes its collection license from individual artwork licenses. Those old brand shapes are not retained under a blanket CC0 assertion.

The replacement author inspected prior material, so no clean-room claim is made. New symbols use simple authored geometry. Some products intentionally share a functional symbol; text supplies the product identity. The retained Tabler snippets have an unrecorded exact import revision, which remains a provenance limitation. Product names do not imply endorsement or grant permission for separately added artwork.

The README artwork and motion illustration have separate [source and generation notes](assets/README.md). No external image or font file is bundled in the authored hero. Image approval is tied to exact reviewed bytes, including decoded frames and metadata; it does not exempt future images from review.

## Publication boundary

Current-source repairs do not retroactively clear older raw snapshots. Public distribution therefore uses a fresh reviewed source snapshot, with earlier development history and originals kept private under the approved [publication procedure](PUBLICATION_PLAN.md). Required current component notices remain in the master kit and runtime resource closure.

The later licensing inventory identified the Frontend Taste source chain in addition to the earlier recorded components and added its notices. No further named bundled implementation was identified by that bounded attribution-marker review. That result cannot prove authorship of every unrecorded byte. Optional renderers, connectors, libraries, fonts and external tools are not granted or bundled merely because a method mentions them. Consult the applicable component notice and task-specific rights before dependent use.
