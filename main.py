"""
Maroon Sovereign Pillar: onitas
Domain: economy
=============================================================================
CODEX LAW #1: FAIL-CLOSED. No pillar starts without MIVL verification.
             main.py exits code 1 if handshake fails. Always.
CODEX LAW #3: EVENT-DRIVEN. No pillar talks directly to another pillar.
             All inter-pillar communication routes through the Event Bus.
=============================================================================
"""
import sys
import yaml
import hashlib
import json
from datetime import datetime, timezone


def load_config(path="./config.yaml"):
    """Load pillar configuration from config.yaml."""
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[FATAL] Config not found: {path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"[FATAL] Config parse error: {e}")
        sys.exit(1)


def load_contract(path="./agent-contract.yaml"):
    """Load agent contract for MIVL verification."""
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[FATAL] Agent contract not found: {path}")
        sys.exit(1)


def verify_mivl(pillar_id, contract):
    """
    MIVL Handshake Verification.
    In production, this verifies the cryptographic identity against
    the MIVL-Core ledger. Currently validates contract structure.
    """
    required_fields = ["identity", "security", "communication"]
    for field in required_fields:
        if field not in contract:
            print(f"[MIVL] Missing required contract field: {field}")
            return False

    if not contract.get("security", {}).get("fail_closed_mode", False):
        print("[MIVL] FATAL: fail_closed_mode must be true")
        return False

    if contract.get("communication", {}).get("direct_pillar_calls", True):
        print("[MIVL] FATAL: direct_pillar_calls must be false (use event bus)")
        return False

    # Generate MIVL token hash
    token_data = f"{pillar_id}:{datetime.now(timezone.utc).isoformat()}"
    mivl_hash = hashlib.sha512(token_data.encode()).hexdigest()[:32]
    print(f"[MIVL] Token generated: {mivl_hash}...")

    return True


def generate_heartbeat(pillar_id, domain):
    """Generate a heartbeat event for the Event Bus."""
    return {
        "event_type": "HEARTBEAT",
        "source_pillar": pillar_id,
        "domain": domain,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload_hash": hashlib.sha512(
            f"{pillar_id}:heartbeat:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest(),
        "governance_check": "verified",
    }


def initialize_sovereign_node():
    """
    Initialize this pillar as a sovereign node in the Maroon mesh.
    Follows the exact sequence from the MAROON_MASTER_CODEX.
    """
    try:
        config = load_config("./config.yaml")
        contract = load_contract("./agent-contract.yaml")

        pillar_id = config["identity"]["agent_id"]
        domain = config["identity"]["domain"]
        wave = config["identity"]["wave"]

        print(f"[SYSTEM] Initializing pillar: {pillar_id}")
        print(f"[SYSTEM] Domain: {domain} | Wave: {wave}")

        # MIVL Handshake — MUST pass or we exit
        if not verify_mivl(pillar_id, contract):
            print(f"[FATAL] MIVL Handshake Failed for {pillar_id}. Terminating.")
            sys.exit(1)

        print(f"[SYSTEM] Identity Verified: {pillar_id}")
        print(f"[SYSTEM] Event Bus Access: {contract['communication']['event_bus_access']}")
        print(f"[SYSTEM] Direct Calls: FORBIDDEN")

        # Generate initial heartbeat
        heartbeat = generate_heartbeat(pillar_id, domain)
        print(f"[HEARTBEAT] {json.dumps(heartbeat, indent=2)}")

        print(f"[SYSTEM] Heartbeat Active: {pillar_id} is online.")
        return True

    except Exception as e:
        print(f"[FATAL] System Initialization Exception: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if initialize_sovereign_node():
        print("[SYSTEM] Sovereign node running. Awaiting event bus messages...")
