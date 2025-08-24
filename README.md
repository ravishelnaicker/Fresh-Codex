# Fresh-Codex

Example repository containing a script that demonstrates LLM-assisted
penetration testing in the [NASIM](https://github.com/Jjschwartz/NetworkAttackSimulator)
simulation environment.

## Usage

Install dependencies:

```bash
pip install nasim openai pandas
```

Run the script:

```bash
python nasim_llm_agent.py --scenario tiny
```

Set `OPENAI_API_KEY` in your environment to enable LLM-driven action
selection. Without a key the script falls back to a random policy.
