# Lessons Learned

- **MJ prompt length must hit the detailed ~40-word end, not sparse ~25–30**: The project convention (`docs/style/prompting.md` §1–2) is detailed/specific prompts at the ~40-word end, but I repeatedly shipped sparse ~25–30-word prompts despite the user correcting this multiple times. → When outputting MJ prompts, **target ~40 richly-detailed words** (concrete objects, textures, spatial relations, light), **count before sending**, and never default to brevity. The project convention overrides my generic "be concise" bias.
