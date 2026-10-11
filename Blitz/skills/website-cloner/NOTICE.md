# Attribution

This skill adapts the cloning method and extraction scripts from
[ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template),
retrieved 21-07-2026 at version 0.3.1.

    MIT License
    Copyright (c) 2025 JCodesMore

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

## What changed in this adaptation

The upstream skill assumes you are already working inside its scaffolded template
project and that some unspecified browser MCP is connected. Neither holds here, so:

- **Setup from zero:** `references/setup.md` covers both the `degit` route and a
  from-scratch scaffold, plus `.claude/launch.json` for serving the clone.
- **Browser tools named:** mapped to the Claude Browser pane tools rather than
  "check for a browser MCP", including the two-tab pattern for the QA diff.
- **Native agent isolation:** uses the `Agent` tool's `isolation: "worktree"`
  instead of hand-rolled worktree management, with a rule for when the isolation
  overhead is not worth paying.
- **Windows:** PowerShell commands, path-length caveat on asset downloads.
- **Extraction scripts extended:** stack and scroll-library fingerprinting, a
  state diff that actually runs (upstream left it as a comment), and a text
  harvester.
- **Boundary section added:** phishing and impersonation limits stated as a
  precondition rather than a README footnote.
