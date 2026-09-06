import sqlite3
from datetime import datetime


DATABASE = "veritas.db"


def get_connection():
    return sqlite3.connect(DATABASE, check_same_thread=False)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Cases table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT UNIQUE,
            title TEXT,
            case_type TEXT,
            investigator TEXT,
            status TEXT,
            priority TEXT,
            created_at TEXT
        )
    """)

    # Evidence table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evidence_id TEXT UNIQUE,
            case_id TEXT,
            filename TEXT,
            document_type TEXT,
            file_hash TEXT,
            size INTEGER,
            uploaded_by TEXT,
            uploaded_at TEXT,
            status TEXT
        )
    """)

    # Chain of custody
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custody (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evidence_id TEXT,
            action TEXT,
            user TEXT,
            timestamp TEXT,
            details TEXT
        )
    """)

    # Audit log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            action TEXT,
            target TEXT,
            timestamp TEXT,
            ip_address TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_case(
    case_id,
    title,
    case_type,
    investigator,
    status,
    priority
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO cases
        (
            case_id,
            title,
            case_type,
            investigator,
            status,
            priority,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        title,
        case_type,
        investigator,
        status,
        priority,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_cases():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            case_id,
            title,
            case_type,
            investigator,
            status,
            priority,
            created_at
        FROM cases
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def add_evidence(
    evidence_id,
    case_id,
    filename,
    document_type,
    file_hash,
    size,
    uploaded_by
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO evidence
        (
            evidence_id,
            case_id,
            filename,
            document_type,
            file_hash,
            size,
            uploaded_by,
            uploaded_at,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        evidence_id,
        case_id,
        filename,
        document_type,
        file_hash,
        size,
        uploaded_by,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Verified"
    ))

    connection.commit()
    connection.close()


def get_evidence():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            evidence_id,
            case_id,
            filename,
            document_type,
            file_hash,
            size,
            uploaded_by,
            uploaded_at,
            status
        FROM evidence
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def add_custody_event(
    evidence_id,
    action,
    user,
    details
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO custody
        (
            evidence_id,
            action,
            user,
            timestamp,
            details
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        evidence_id,
        action,
        user,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        details
    ))

    connection.commit()
    connection.close()


def get_custody_events():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            evidence_id,
            action,
            user,
            timestamp,
            details
        FROM custody
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def add_audit_log(
    user,
    action,
    target,
    ip_address="127.0.0.1"
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO audit
        (
            user,
            action,
            target,
            timestamp,
            ip_address
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user,
        action,
        target,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ip_address
    ))

    connection.commit()
    connection.close()


def get_audit_logs():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            user,
            action,
            target,
            timestamp,
            ip_address
        FROM audit
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows
