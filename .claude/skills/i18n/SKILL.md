---
name: i18n
description: Extract hardcoded user-facing strings into the project's localization system — locale files and translation calls — so the UI can be translated. Use when the user says "extract strings for translation", "internationalize this", "set up i18n", "move text to locale files", "add translation keys", or "make this translatable".
argument-hint: "[optional path or component to focus on, e.g. 'src/components/Header.tsx']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## i18n setup signals

!`ls -d locales lang i18n public/locales src/locales translations 2>/dev/null`

!`grep -rilE "i18next|react-i18next|vue-i18n|formatjs|react-intl|gettext|next-intl|\\bt\\(" --include='*.*' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -15`

## Instructions

Extract hardcoded user-facing strings into the project's i18n system, scoped to `$ARGUMENTS` if a path was given. If no i18n library is set up yet, identify the idiomatic one for the stack and confirm with the user before introducing it — don't silently add a framework.

### Method

1. **Learn the existing convention.** From the signals above, find the i18n library, the locale file format (JSON/YAML/PO), the key naming scheme (nested vs flat, `feature.component.label`), and how translations are called (`t('key')`, `<FormattedMessage>`, `$t()`). Mirror it exactly. If none exists, propose the standard for the framework and wait for confirmation.
2. **Find the real user-facing strings.** Scan the target for literal text rendered to users — JSX/template text, button labels, placeholders, `aria-label`s, validation/error messages, titles. **Exclude** non-UI strings: log messages, code identifiers, URLs, CSS classes, test fixtures, enum keys, and config.
3. **Replace each with a translation call** using a descriptive, conventionally-named key, and **add the key + original text to the default locale file**. Keep interpolation intact — convert `` `Hello ${name}` `` into the library's variable syntax (`t('greeting', { name })`), not a concatenation.
4. **Handle plurals and rich text** with the library's features (plural forms, `<Trans>`/components for embedded markup) rather than string-splitting, which breaks in other languages.
5. **Don't auto-translate.** Populate only the default locale with the real text; add empty/placeholder entries for other existing locales (or leave them to the translation workflow) and flag that they need real translations.

### Rules

1. Only externalize genuine user-facing text. Leave logs, identifiers, and machine strings as literals — over-extraction is as harmful as under-extraction.
2. Match the project's existing keys, file format, and call style precisely; don't invent a parallel convention.
3. Preserve meaning and interpolation — never build sentences by concatenating translated fragments; word order differs across languages.
4. Keep keys stable and descriptive (by meaning/location, not by the English text) so translations survive copy edits.
5. After extracting, report: strings extracted, keys added, locale files touched, and which locales still need real translations. Run a build/lint to catch a missed import of the translation function.
