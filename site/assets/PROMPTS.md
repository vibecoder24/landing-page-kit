# Prompt log

Every generation, kept (rejects too). Newest at the bottom. The scripts in `scripts/` append here automatically; add a line by hand marking each one **keeper** or **reject** and why.

Format of an entry:

```
### assets/raw/<set>/<file>.png
- <date> · <model> · <aspect> · <quality> · <refs if any> · prediction <id>

> <the prompt, verbatim>

keeper · why
```
