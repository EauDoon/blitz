# viz-dashboards evals

1. Asked in chat: "What are the odds BTC closes the quarter above its current level?" Passes if the reply defines the event/horizon and, if using its binary complement, an explicitly mutually exclusive and exhaustive distribution with probabilities summing to 100; unsupported precision is flagged and builds no dashboard file. Fails if it ships an HTML dashboard nobody asked for.
2. "Build me a dashboard comparing these three yields." Passes if the file renders on hex 0f0f0f as inline SVG or with its library inlined, zero external script tags are confirmed by grep, and all eight QA points run. Fails on any CDN script, a light canvas, or a subtitle figure that differs from the params object.
3. "Dashboard of my Hermes seat costs by model for the last 30 days." Passes if this skill builds the dashboard on the 0f0f0f canvas and orchestrator, if it loads, only supplies figures or routing. Fails if orchestrator answers without a chart.
