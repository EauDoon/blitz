# Document pipeline cases

| ID | Request | Expected |
|---|---|---|
| D01 | Comprehensive business-document contract selected: "Write this up" with no format named | doc-style; a Google Doc from the HTML route with the verified .docx beside it; page budget stated before the build |
| D02 | A one pager for a partner | Built from one approved snapshot; every page rendered and looked at; verify.sh passes; cold-read LITE before delivery |
| D03 | A revision of a Doc already in Drive | One canonical version; the earlier upload goes to Archive in the same session; a rollback pointer recorded |
| D04 | The converted Google Doc drops a table | Caught on read back of the converted Doc, not only the local file |
| D05 | A deck | pitch-architect and google-slides; the deck leaves as .pptx with a browser upload step for Slides |
| D06 | A document with a screen figure | The figure comes from frontend-mockup at product density, from the same snapshot as the requirements |
| D07 | A private and a partner version of the one pager | Both from one snapshot; the partner version carries no private-lane content |
