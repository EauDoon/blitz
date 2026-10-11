# Third-party licenses and icon provenance

The diagram-design method is adapted from [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design). Its original MIT license is retained in LICENSE. This notice covers the current icon catalogs in `references/primitive-icons.md` and `assets/icons.html`, plus their bundled architecture examples; it does not grant a blanket license to Blitz.

## Current collection

All 87 lookup keys are preserved. The collection contains 50 generic Tabler symbols and 37 newly authored generic stand-ins for product nodes. It includes no official brand glyphs. Product names remain as text labels so architecture diagrams can still identify services and tools. Several products intentionally share a functional symbol. Visual recognition through official logos is no longer supported.

## Tabler Icons

- License: MIT, retained below.
- Upstream: https://github.com/tabler/tabler-icons
- License inspected on 11-10-2026: https://github.com/tabler/tabler-icons/blob/main/LICENSE
- Included material: generic outline symbols only. All five inherited `brand-*` entries were replaced.
- Adaptation: inherited monochrome `currentColor` snippets use a 24 by 24 view box and 1.5-pixel strokes. The exact source revision of these inherited snippets is not recorded; this is a provenance limitation, not a claim of a completed historical audit.

Retained generic keys: `laptop`, `phone`, `desktop`, `server`, `container`, `vm`, `user`, `users`, `admin`, `robot`, `cloud`, `internet`, `cdn`, `firewall`, `vpn`, `load-balancer`, `gateway`, `dns`, `database`, `file`, `log`, `queue`, `cache`, `bucket`, `backup`, `search`, `pod`, `node`, `service`, `deployment`, `ingress`, `volume`, `api`, `request`, `response`, `sync`, `lock`, `key`, `alert`, `git-branch`, `terminal`, `pipeline`, `bug`, `monitoring`, `test`, `active-directory`, `sql`, `excel`, `csv`, `txt`.

```text
MIT License

Copyright (c) 2020-2026 Paweł Kuna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Newly authored product stand-ins

The following graphics were authored specifically for the Blitz v2.1OAI repair on 11-10-2026 using simple rectangles, ellipses, circles, and connecting lines. No inherited brand paths or external artwork were used in the replacements. The author inspected the inherited material first, so this is not a clean-room claim. The graphics are functional stand-ins and are explicitly labeled as not official logos. This provenance record does not change another component's license terms or create a blanket license for the repository.

| Preserved key | Intended text label / node | Generic symbol |
| --- | --- | --- |
| `docker` | Docker engine / image. | container service |
| `terraform` | Terraform infrastructure as code. | infrastructure plan |
| `aws` | Amazon Web Services. | cloud services |
| `azure` | Microsoft Azure. | cloud services |
| `github` | GitHub. | source repository |
| `kubernetes` | Kubernetes. | service cluster |
| `gcp` | Google Cloud. | cloud services |
| `postgres` | PostgreSQL. | database |
| `redis` | Redis. | memory cache |
| `nginx` | Nginx. | web gateway |
| `gitea` | Gitea self-hosted Git. | source repository |
| `keycloak` | Keycloak identity / SSO. | identity service |
| `minio` | MinIO S3-compatible object storage. | object storage |
| `mysql` | MySQL. | database |
| `oracle` | Oracle Database. | database |
| `sqlserver` | Microsoft SQL Server. | database |
| `sqlite` | SQLite embedded database. | database |
| `hive` | Apache Hive data warehouse. | database |
| `starrocks` | StarRocks MPP analytical database. | database |
| `nifi` | Apache NiFi data flow. | data pipeline |
| `airflow` | Apache Airflow scheduler / DAG runner. | task dependencies |
| `hop` | Apache Hop data orchestration / ETL. | data pipeline |
| `pentaho` | Pentaho PDI (Kettle) ETL and data integration. | data merge |
| `dagster` | Dagster data orchestration platform. | task dependencies |
| `trino` | Trino distributed SQL query engine. | database |
| `superset` | Apache Superset BI / dashboards. | analytics dashboard |
| `redash` | Redash BI / dashboards. | analytics dashboard |
| `tableau` | Tableau data visualization. | analytics dashboard |
| `powerbi` | Microsoft Power BI. | analytics dashboard |
| `jupyter` | Jupyter / JupyterLab notebooks. | code notebook |
| `python` | Python programming language. | code runtime |
| `r` | R statistical language. | statistical analysis |
| `spss` | IBM SPSS Statistics. | statistical analysis |
| `sas` | SAS statistical analysis. | statistical analysis |
| `stata` | Stata statistical analysis. | statistical analysis |
| `rstudio` | RStudio / Posit IDE for R and Python. | code workspace |
| `qgis` | QGIS geographic information system. | geographic data |

## Removed artwork and historical provenance

The earlier catalog attributed brand artwork to Simple Icons, log-z/logos, Devicon, and Tabler `brand-*` files. All such glyphs have been replaced. The earlier blanket claim that Simple Icons' collection-level CC0 label established permission for every individual brand image has been removed. No individual brand image is now shipped under that claim. In particular, the inherited R, Apache Hive, Apache NiFi, Apache Airflow, and Apache Superset images are absent from the current collection.

The inherited direct-fetch entries identified Hop from `hop.apache.org`, Pentaho from `cdn.worldvectorlogo.com`, and Dagster from `cdn.prod.website-files.com` and left their licenses unverified. They were replaced with generic stand-ins in the first repair. The subsequent repair replaces the remaining brand glyphs, including five Tabler `brand-*` entries, and supplies generic statistical-analysis symbols for the previously missing SAS and Stata entries. Their earlier source references were `svgrepo.com/download/374062/sas.svg` and `icon.icepanel.io/Technology/svg/Stata.svg`. These names and domains are historical provenance only, not instructions to retrieve the artwork or evidence of redistribution permission.

Removed-source repositories: https://github.com/simple-icons/simple-icons, https://github.com/log-z/logos, and https://github.com/devicons/devicon. Their earlier license assertions are not carried forward as licenses for the replacement geometry, and no SVG glyph from those collections remains in these catalogs. Their formerly reproduced notices are superseded here because the covered artwork is no longer included in the current files. Existing private snapshots preserve the earlier material and notices.

This repair changes the current catalogs and the twelve listed architecture examples only. It does not remove old Git objects or independently clear reachable historical content for publication. Historical exposure requires a separate repository-wide check and, where necessary, explicitly authorized remediation.

## Bundled architecture examples

The same generic stand-ins replace 92 product glyph placements across twelve bundled examples: `example-datalake.html`, `example-datalake-dark.html`, `example-datalake-full.html`, `example-datalake-full-dark.html`, `example-high-level.html`, `example-high-level-dark.html`, `example-high-level-full.html`, `example-high-level-full-dark.html`, `example-high-level-vertical.html`, and `example-high-level-vertical-dark.html`, `example-high-level-vertical-full.html`, and `example-high-level-vertical-full-dark.html` in `assets/`. These replacements cover NiFi, Airflow, MinIO, Trino, StarRocks, Superset, Jupyter, Python, Keycloak, and Kubernetes. Both exact catalog copies and alternate simplified product drawings are replaced. Kubernetes-labeled nodes also use the catalog's generic service-cluster symbol for consistency; this change does not assert that the earlier glyph was unlicensed. Existing diagram node labels, glyph positions, sizes, colors, and connections are preserved. Each example identifies its product graphics as generic symbols and uses system fonts without a remote font request.

## Rendering and product names

Both catalogs contain inline SVG. The gallery uses local system fonts and loads no external images, fonts, or scripts. The stand-ins use `currentColor` to follow the diagram's ink color.

Product names belong to their respective owners. Their use as diagram labels does not imply endorsement, sponsorship, or affiliation. Do not present a generic stand-in as an official logo, and verify any separate brand artwork before adding it to a downstream diagram.
