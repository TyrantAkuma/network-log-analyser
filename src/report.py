def print_report(results):
    print("\n" + "="*50)
    print("  NETWORK INTRUSION ANALYSIS REPORT")
    print("="*50)

    print("\n[1] Traffic breakdown by type:")
    for label, cnt in results["traffic_breakdown"]:
        bar = "█" * min(cnt // 500, 40)
        print(f"  {label:<20} {cnt:>7}  {bar}")

    print("\n[2] Potential port scans:")
    if results["port_scan_suspects"]:
        for proto, svc, cnt in results["port_scan_suspects"]:
            print(f"  {proto}/{svc:<15} {cnt} connections")
    else:
        print("  None detected.")

    print("\n[3] Brute force attempts:")
    if results["brute_force"]:
        for svc, attempts in results["brute_force"]:
            print(f"  {svc:<15} {attempts} failed attempts")
    else:
        print("  None detected.")

    print("\n[4] Possible data exfiltration:")
    if results["exfil_suspects"]:
        for label, svc, src, dst in results["exfil_suspects"]:
            print(f"  [{label}] {svc} — {dst:,} bytes out")
    else:
        print("  None detected.")

    print("\n  Findings saved to anomaly_log table.")
    print("="*50 + "\n")
