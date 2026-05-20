import mysql.connector
import sys
sys.path.insert(0, '.')
from config import DB_CONFIG

def run():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    results = {}

    cursor.execute("""
        SELECT label, COUNT(*) as cnt
        FROM connections
        GROUP BY label
        ORDER BY cnt DESC
    """)
    results["traffic_breakdown"] = cursor.fetchall()

    cursor.execute("""
        SELECT protocol_type, service, COUNT(*) as cnt
        FROM connections
        WHERE duration = 0 AND src_bytes < 100
        GROUP BY protocol_type, service
        HAVING cnt > 500
        ORDER BY cnt DESC
        LIMIT 10
    """)
    results["port_scan_suspects"] = cursor.fetchall()

    cursor.execute("""
        SELECT service, COUNT(*) as attempts
        FROM connections
        WHERE num_failed_logins > 0
        GROUP BY service
        ORDER BY attempts DESC
    """)
    results["brute_force"] = cursor.fetchall()

    cursor.execute("""
        SELECT label, service, src_bytes, dst_bytes
        FROM connections
        WHERE dst_bytes > 1000000
        ORDER BY dst_bytes DESC
        LIMIT 10
    """)
    results["exfil_suspects"] = cursor.fetchall()

    anomalies = [
        ("port_scan", len(results["port_scan_suspects"]), str(results["port_scan_suspects"])),
        ("brute_force", len(results["brute_force"]), str(results["brute_force"])),
        ("data_exfil", len(results["exfil_suspects"]), str(results["exfil_suspects"])),
    ]
    cursor.executemany("""
        INSERT INTO anomaly_log (detection_type, affected_count, details)
        VALUES (%s, %s, %s)
    """, anomalies)
    conn.commit()

    cursor.close()
    conn.close()
    return results
