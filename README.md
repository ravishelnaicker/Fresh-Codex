# Fresh-Codex

This repository includes a small example showing how to configure an
OpenAI API key and environment parameters directly in code, then use an
LLM to choose actions in the [NASim](https://github.com/Gilbeth/nasim)
network security environment.

* `config.py` defines `OPENAI_API_KEY`, an `ENVIRONMENT_SIZE` string
  (choose from `tiny`, `small`, `medium`, or `large-gen`), and a
  `MAX_STEPS` limit.
* `main.py` creates a NASim environment using these values and queries
  an OpenAI model for each action.  If the model call fails, a random
  action is taken instead so the script continues running.

Install the dependencies and run the example:

```bash
pip install nasim openai
python main.py
```

> **Note:** Hard-coding API keys is convenient for quick experiments but
> should be avoided for production applications.
