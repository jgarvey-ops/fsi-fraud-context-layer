import os

import httpx
import streamlit as st

BASE = os.environ.get("CONTEXT_SERVICE_URL", "http://localhost:8080")


def main() -> None:
    st.title("FSI Fraud Context — Demo")
    st.caption(f"Context Service: {BASE}")

    try:
        health = httpx.get(f"{BASE}/health", timeout=5.0).json()
        st.success(f"Mode: {health.get('mode')} | injection={health.get('stream_injection_enabled')}")
    except httpx.HTTPError as exc:
        st.error(f"Context Service unreachable: {exc}")
        return

    injection = st.toggle("Stream injection (scripted alerts)", value=False)
    if st.button("Apply injection setting"):
        r = httpx.post(f"{BASE}/v1/admin/stream/injection", json={"enabled": injection}, timeout=5.0)
        st.json(r.json())

    case_id = st.selectbox("Case", ["CASE-001", "CASE-002", "CASE-003"])
    if st.button("Load case dossier"):
        r = httpx.get(f"{BASE}/v1/cases/{case_id}", timeout=10.0)
        st.json(r.json())

    if st.button("Recent stream"):
        r = httpx.get(f"{BASE}/v1/stream/recent", timeout=10.0)
        st.json(r.json())


if __name__ == "__main__":
    main()
