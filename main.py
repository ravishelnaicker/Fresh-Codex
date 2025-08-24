"""Interact with a NASim environment using an OpenAI LLM to select actions."""

from __future__ import annotations

import nasim
from openai import OpenAI

from config import OPENAI_API_KEY, ENVIRONMENT_SIZE, MAX_STEPS


def llm_choose_action(client: OpenAI, obs, action_space) -> int:
    """Ask an LLM to choose an action based on the observation.

    If the LLM request fails for any reason, a random action is selected
    instead so the script can continue running.
    """
    prompt = (
        "You are an agent controlling attacks in a NASim network security "
        f"environment. Given the observation {obs}, choose an integer action "
        f"index from 0 to {action_space.n - 1} that will help compromise the network."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        text = response.choices[0].message.content.strip()
        action = int(text)
    except Exception as exc:  # pragma: no cover - network fallback
        print(f"LLM call failed ({exc}); selecting random action.")
        action = int(action_space.sample())
    return action


def main() -> None:
    """Run a single episode in the NASim environment."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    env = nasim.make_benchmark(ENVIRONMENT_SIZE)
    obs = env.reset()
    for step in range(1, MAX_STEPS + 1):
        action = llm_choose_action(client, obs, env.action_space)
        _, obs, reward, done, _ = env.step(action)
        print(f"Step {step}: action={action}, reward={reward}, done={done}")
        if done:
            break


if __name__ == "__main__":
    main()
