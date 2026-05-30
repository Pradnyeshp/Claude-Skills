---
name: regex
description: Build, explain, or debug a regular expression from a plain-English description, with worked examples and test cases. Use when the user says "write a regex", "regex for", "explain this regex", "why doesn't this pattern match", "match a pattern like", or pastes a regex and asks what it does.
argument-hint: "[describe what to match, or paste a regex to explain]"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Instructions

Handle the regex task in `$ARGUMENTS`. Two modes — detect which from the request:

### Mode A — build a regex from a description

1. **Clarify the target flavor** if it matters: regex dialects differ (PCRE, JavaScript, Python `re`, Go RE2, POSIX, grep/ripgrep). Infer from context (the file type or tool mentioned); if genuinely ambiguous, ask or state the flavor you're assuming.
2. **Write the pattern**, then explain it **token by token** so the user understands and can adjust it.
3. **Show test cases:** a table of inputs that should match and inputs that should *not*, with the expected result. Cover the tricky edges (empty string, boundaries, unicode/accents, greedy vs. lazy).
4. **Give a ready-to-paste snippet** in the user's language showing how to use it (with the right flags — `i`, `m`, `g`, etc.).
5. **Warn about footguns** you introduced or avoided: catastrophic backtracking, unanchored matches, unescaped metacharacters, `.` matching newlines.

### Mode B — explain or debug an existing regex

1. Break it into components and explain what each does in plain language.
2. State exactly what it matches and what it rejects, with examples.
3. If the user says it's not working, identify why (missing anchor, wrong flag, escaping, greedy quantifier) and give the corrected version.

### Rules

1. Prefer **readable, maintainable** patterns over clever one-liners. Suggest named groups or verbose/`x` mode for complex patterns.
2. Always provide concrete match / no-match examples — never hand over a bare pattern.
3. Flag any catastrophic-backtracking risk and offer a safer rewrite.
4. If a regex is the wrong tool (e.g. parsing HTML or deeply nested structures), say so and suggest the proper approach.
