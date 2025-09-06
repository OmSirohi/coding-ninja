
import argparse
from agents.orchestrator import Orchestrator

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default="arrays", choices=["arrays"])
    ap.add_argument("--difficulty", default="easy", choices=["easy","medium"])
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    orch = Orchestrator(artifacts_dir="artifacts")
    state = orch.run(topic=args.topic, difficulty=args.difficulty, seed=args.seed)

    print("Generated files in ./artifacts:")
    for p in state.get("artifact_paths", []):
        print(" -", p)
    print("Verification:", state.get("verification", {}))

if __name__ == "__main__":
    main()
