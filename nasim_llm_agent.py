import argparse
import json
import os
import random

import nasim
import pandas as pd

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None


def make_env(scenario: str, seed: int):
    """Create NASIM benchmark environment."""
    return nasim.make_benchmark(scenario, seed=seed)


def init_hosts(env):
    """Initialize host knowledge base."""
    return {
        str(h.address): {
            "os": None,
            "services": [],
            "processes": [],
            "access": 0,
            "compromised": False,
        }
        for h in env.scenario.hosts.values()
    }


def update_knowledge(hosts, target, info):
    """Update knowledge base with info from environment."""
    if info.get("os"):
        hosts[target]["os"] = next(iter(info["os"]))
    if info.get("services"):
        hosts[target]["services"] = list(info["services"])
    if info.get("processes"):
        hosts[target]["processes"] = list(info["processes"])
    access = info.get("access")
    if access:
        hosts[target]["access"] = access
        hosts[target]["compromised"] |= access >= 2


def choose_action_llm(hosts, actions, used, model):
    """Ask an LLM to choose the next action."""
    prompt = f"""
State: {json.dumps(hosts)}
Available actions (index: description):
{json.dumps(actions, indent=2)}
Used actions: {list(used)}

Rules:
- Choose a new action index not in Used actions.
- Return JSON {{"action": int, "reason": str}} only.
- Exploit services only when OS/service info suggests it.
"""
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a NASIM penetration tester."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    data = json.loads(response.choices[0].message["content"])
    return int(data["action"])


def choose_action_random(actions, used):
    available = [i for i in range(len(actions)) if i not in used]
    if not available:
        return None
    return random.choice(available)


def run_episode(env, model, max_steps):
    actions = {i: str(a) for i, a in enumerate(env.action_space.actions)}
    hosts = init_hosts(env)
    obs, _ = env.reset()
    used_actions = set()
    history = []
    total = 0
    for step in range(max_steps):
        if openai and os.getenv("OPENAI_API_KEY"):
            try:
                a = choose_action_llm(hosts, actions, used_actions, model)
            except Exception:
                a = choose_action_random(actions, used_actions)
        else:
            a = choose_action_random(actions, used_actions)
        if a is None:
            print("No available actions remain.")
            break
        if a in used_actions:
            continue
        used_actions.add(a)
        action = env.action_space.actions[a]
        obs, reward, done, truncated, info = env.step(a)
        total += reward
        target = str(action.target)
        update_knowledge(hosts, target, info)
        history.append(
            {
                "step": step,
                "action": str(action),
                "reward": reward,
                "total_reward": total,
                "target": target,
                "known_os": hosts[target]["os"],
                "known_services": hosts[target]["services"],
                "known_processes": hosts[target]["processes"],
                "compromised": hosts[target]["compromised"],
            }
        )
        if done or truncated:
            break
    return pd.DataFrame(history)


def main():
    parser = argparse.ArgumentParser(
        description="NASIM LLM-driven penetration testing example"
    )
    parser.add_argument("--scenario", default="tiny", help="Benchmark scenario name")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max_steps", type=int, default=50)
    parser.add_argument(
        "--model", default="gpt-4o-mini", help="OpenAI model for decision making"
    )
    args = parser.parse_args()

    env = make_env(args.scenario, args.seed)
    df = run_episode(env, args.model, args.max_steps)
    print(df)


if __name__ == "__main__":
    main()
