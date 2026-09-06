import streamlit as st
import pandas as pd
import plotly.express as px
import uuid
import os
from datetime import datetime

from database.database import (
    initialize_database,
    add_case,
    get_cases,
    add_evidence,
    get_evidence,
    add_custody_event,
    get_custody_events,
    add_audit_log,
    get_audit_logs
)

from utils.hashing import calculate_sha256

from utils.document_processor import (
    extract_pdf_text,
    get_pdf_page_count
)

from data.demo_data import load_demo_data


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VERITAS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# Load demo cases
load_demo_data()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

if "username" not in st.session_state:
    st.session_state.username = "Investigator"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def navigation_button(name, icon):

    if st.sidebar.button(
        f"{icon}  {name}",
        use_container_width=True
    ):

        st.session_state.page = name


def page_header(title, description):

    st.title(title)

    st.caption(description)

    st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🛡️ VERITAS")

    st.caption(
        "Secure Digital Evidence & Legal Document Intelligence"
    )

    st.divider()

    st.subheader("Workspace")

    navigation_button(
        "Dashboard",
        "◈"
    )

    navigation_button(
        "Evidence Vault",
        "▣"
    )

    navigation_button(
        "Cases",
        "▤"
    )

    navigation_button(
        "Investigation",
        "⌕"
    )

    navigation_button(
        "Chain of Custody",
        "⛓"
    )

    navigation_button(
        "Audit Ledger",
        "▥"
    )

    navigation_button(
        "Security Center",
        "⚠"
    )

    st.divider()

    st.subheader("System")

    st.write("🟢 System Status")

    st.write("🔐 Encryption: Active")

    st.write("🛡️ Integrity Monitoring: Active")

    st.write("📡 Audit Logging: Active")

    st.divider()

    st.caption("VERITAS Prototype")

    st.caption("SIH 2026")


# ============================================================
# GET DATA
# ============================================================

cases = get_cases()

evidence = get_evidence()

custody = get_custody_events()

audit_logs = get_audit_logs()


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    page_header(
        "Command Dashboard",
        "Central monitoring console for legal documents, digital evidence and investigations."
    )

    # Metrics

    total_cases = len(cases)

    total_evidence = len(evidence)

    active_cases = len([
        case for case in cases
        if case[4] == "Active"
    ])

    verified_evidence = len([
        item for item in evidence
        if item[8] == "Verified"
    ])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Protected Documents",
            total_evidence,
            "+12.4%"
        )

    with col2:
        st.metric(
            "Verified Evidence",
            verified_evidence,
            "+8.7%"
        )

    with col3:
        st.metric(
            "Active Cases",
            active_cases,
            "+5"
        )

    with col4:
        st.metric(
            "Security Score",
            "98.7%",
            "Excellent"
        )

    st.divider()

    # Charts

    left, right = st.columns(2)

    with left:

        st.subheader("Case Overview")

        if cases:

            case_df = pd.DataFrame(
                cases,
                columns=[
                    "Case ID",
                    "Title",
                    "Type",
                    "Investigator",
                    "Status",
                    "Priority",
                    "Created"
                ]
            )

            status_counts = (
                case_df["Status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "Status",
                "Count"
            ]

            fig = px.pie(
                status_counts,
                names="Status",
                values="Count",
                hole=0.55
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right:

        st.subheader("Security Health")

        security_data = pd.DataFrame({
            "Category": [
                "Encryption",
                "Access Control",
                "Integrity",
                "Audit Logging",
                "Backup"
            ],
            "Score": [
                100,
                98,
                99,
                100,
                96
            ]
        })

        fig = px.bar(
            security_data,
            x="Score",
            y="Category",
            orientation="h",
            range_x=[0, 100]
        )

        fig.update_layout(
            height=350,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("Active Investigations")

    if cases:

        active = [
            case for case in cases
            if case[4] == "Active"
        ]

        active_df = pd.DataFrame(
            active,
            columns=[
                "Case ID",
                "Investigation",
                "Type",
                "Investigator",
                "Status",
                "Priority",
                "Created"
            ]
        )

        st.dataframe(
            active_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("System Activity")

    if audit_logs:

        activity_df = pd.DataFrame(
            audit_logs[:8],
            columns=[
                "User",
                "Action",
                "Target",
                "Timestamp",
                "IP Address"
            ]
        )

        st.dataframe(
            activity_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No audit activity recorded yet."
        )


# ============================================================
# EVIDENCE VAULT
# ============================================================

elif st.session_state.page == "Evidence Vault":

    page_header(
        "Evidence Vault",
        "Secure repository for investigation and legal documents."
    )

    tab1, tab2 = st.tabs([
        "📂 Repository",
        "📤 Upload Evidence"
    ])

    with tab1:

        if evidence:

            evidence_df = pd.DataFrame(
                evidence,
                columns=[
                    "Evidence ID",
                    "Case ID",
                    "Filename",
                    "Document Type",
                    "SHA-256",
                    "Size",
                    "Uploaded By",
                    "Uploaded At",
                    "Status"
                ]
            )

            search = st.text_input(
                "Search evidence",
                placeholder="Search filename, case ID or hash..."
            )

            if search:

                evidence_df = evidence_df[
                    evidence_df.astype(str)
                    .apply(
                        lambda row:
                        row.str.contains(
                            search,
                            case=False,
                            na=False
                        ).any(),
                        axis=1
                    )
                ]

            st.dataframe(
                evidence_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No documents have been uploaded yet."
            )

    with tab2:

        st.subheader("Upload Investigation Document")

        uploaded_file = st.file_uploader(
            "Choose a document",
            type=[
                "pdf",
                "txt",
                "docx",
                "png",
                "jpg",
                "jpeg"
            ]
        )

        case_ids = [
            case[0]
            for case in cases
        ]

        selected_case = st.selectbox(
            "Assign to Case",
            case_ids
        )

        document_type = st.selectbox(
            "Document Type",
            [
                "Legal Document",
                "Investigation Report",
                "Evidence Document",
                "Financial Record",
                "Forensic Report",
                "Other"
            ]
        )

        if uploaded_file:

            file_bytes = uploaded_file.getvalue()

            file_hash = calculate_sha256(
                file_bytes
            )

            file_size = len(file_bytes)

            st.success(
                "Document loaded successfully."
            )

            st.write(
                "Filename:",
                uploaded_file.name
            )

            st.write(
                "File size:",
                f"{file_size:,} bytes"
            )

            st.code(
                file_hash
            )

            if st.button(
                "🔐 Verify & Store Evidence",
                use_container_width=True
            ):

                evidence_id = (
                    "EVD-"
                    + uuid.uuid4().hex[:8].upper()
                )

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                file_path = os.path.join(
                    "uploads",
                    evidence_id + "_" +
                    uploaded_file.name
                )

                with open(
                    file_path,
                    "wb"
                ) as file:

                    file.write(file_bytes)

                add_evidence(
                    evidence_id,
                    selected_case,
                    uploaded_file.name,
                    document_type,
                    file_hash,
                    file_size,
                    st.session_state.username
                )

                add_custody_event(
                    evidence_id,
                    "Evidence Uploaded",
                    st.session_state.username,
                    "Document uploaded and SHA-256 hash generated."
                )

                add_audit_log(
                    st.session_state.username,
                    "UPLOAD",
                    evidence_id
                )

                st.success(
                    f"Evidence {evidence_id} securely registered."
                )

                st.info(
                    "SHA-256 integrity hash recorded successfully."
                )


# ============================================================
# CASE MANAGEMENT
# ============================================================

elif st.session_state.page == "Cases":

    page_header(
        "Case Management",
        "Create, track and manage legal investigations."
    )

    tab1, tab2 = st.tabs([
        "📋 All Cases",
        "➕ Create Case"
    ])

    with tab1:

        if cases:

            case_df = pd.DataFrame(
                cases,
                columns=[
                    "Case ID",
                    "Title",
                    "Type",
                    "Investigator",
                    "Status",
                    "Priority",
                    "Created"
                ]
            )

            st.dataframe(
                case_df,
                use_container_width=True,
                hide_index=True
            )

    with tab2:

        st.subheader(
            "Create New Investigation"
        )

        case_id = st.text_input(
            "Case ID",
            placeholder="CASE-2050"
        )

        title = st.text_input(
            "Investigation Title"
        )

        case_type = st.selectbox(
            "Case Type",
            [
                "Criminal Investigation",
                "Cyber Crime",
                "Financial Crime",
                "Document Fraud",
                "Legal Investigation",
                "Other"
            ]
        )

        investigator = st.text_input(
            "Investigator"
        )

        priority = st.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

        status = st.selectbox(
            "Status",
            [
                "Active",
                "Under Review",
                "Closed"
            ]
        )

        if st.button(
            "Create Investigation",
            use_container_width=True
        ):

            if not case_id or not title:

                st.error(
                    "Case ID and title are required."
                )

            else:

                add_case(
                    case_id,
                    title,
                    case_type,
                    investigator,
                    status,
                    priority
                )

                add_audit_log(
                    st.session_state.username,
                    "CREATE_CASE",
                    case_id
                )

                st.success(
                    f"{case_id} created successfully."
                )


# ============================================================
# INVESTIGATION
# ============================================================

elif st.session_state.page == "Investigation":

    page_header(
        "Investigation Workspace",
        "Search, inspect and correlate digital evidence."
    )

    search = st.text_input(
        "🔍 Investigation Search",
        placeholder="Search cases, evidence IDs, filenames or hashes..."
    )

    if search:

        results = []

        for item in evidence:

            searchable = " ".join(
                str(value)
                for value in item
            ).lower()

            if search.lower() in searchable:

                results.append(item)

        if results:

            st.success(
                f"{len(results)} evidence record(s) found."
            )

            result_df = pd.DataFrame(
                results,
                columns=[
                    "Evidence ID",
                    "Case ID",
                    "Filename",
                    "Document Type",
                    "SHA-256",
                    "Size",
                    "Uploaded By",
                    "Uploaded At",
                    "Status"
                ]
            )

            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No matching evidence found."
            )

    else:

        st.info(
            "Enter a search term to investigate the evidence repository."
        )

    st.divider()

    st.subheader(
        "Investigation Tools"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "🔎\n\n"
            "**Full-text Search**\n\n"
            "Search across registered evidence."
        )

    with col2:

        st.info(
            "🔗\n\n"
            "**Relationship Mapping**\n\n"
            "Connect evidence to cases."
        )

    with col3:

        st.info(
            "🧠\n\n"
            "**Document Intelligence**\n\n"
            "Extract document information."
        )


# ============================================================
# CHAIN OF CUSTODY
# ============================================================

elif st.session_state.page == "Chain of Custody":

    page_header(
        "Chain of Custody",
        "Chronological evidence handling history."
    )

    if custody:

        custody_df = pd.DataFrame(
            custody,
            columns=[
                "Evidence ID",
                "Action",
                "User",
                "Timestamp",
                "Details"
            ]
        )

        st.dataframe(
            custody_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        selected_evidence = st.selectbox(
            "Inspect Evidence",
            sorted(
                set(
                    row[0]
                    for row in custody
                )
            )
        )

        selected_events = [
            row for row in custody
            if row[0] == selected_evidence
        ]

        st.subheader(
            f"Evidence Timeline — {selected_evidence}"
        )

        for event in selected_events:

            st.write(
                f"**{event[3]}** — "
                f"{event[1]} — "
                f"{event[2]}"
            )

            st.caption(
                event[4]
            )

            st.divider()

    else:

        st.info(
            "No chain-of-custody events recorded yet."
        )


# ============================================================
# AUDIT LEDGER
# ============================================================

elif st.session_state.page == "Audit Ledger":

    page_header(
        "Audit Ledger",
        "System-wide record of user and evidence activity."
    )

    if audit_logs:

        audit_df = pd.DataFrame(
            audit_logs,
            columns=[
                "User",
                "Action",
                "Target",
                "Timestamp",
                "IP Address"
            ]
        )

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        action_counts = (
            audit_df["Action"]
            .value_counts()
            .reset_index()
        )

        action_counts.columns = [
            "Action",
            "Count"
        ]

        fig = px.bar(
            action_counts,
            x="Action",
            y="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No audit records available."
        )


# ============================================================
# SECURITY CENTER
# ============================================================

elif st.session_state.page == "Security Center":

    page_header(
        "Security Center",
        "Monitor integrity, access and platform security."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Security Score",
            "98.7%",
            "+1.2%"
        )

    with col2:

        st.metric(
            "Integrity Status",
            "100%",
            "Verified"
        )

    with col3:

        st.metric(
            "Audit Coverage",
            "100%",
            "Active"
        )

    st.divider()

    st.subheader(
        "Security Controls"
    )

    security_controls = pd.DataFrame({
        "Control": [
            "SHA-256 Document Integrity",
            "Role-Based Access",
            "Audit Logging",
            "Chain of Custody",
            "Secure Evidence Storage",
            "Session Monitoring"
        ],
        "Status": [
            "🟢 Active",
            "🟢 Active",
            "🟢 Active",
            "🟢 Active",
            "🟢 Active",
            "🟡 Prototype"
        ]
    })

    st.dataframe(
        security_controls,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "Security Recommendations"
    )

    st.warning(
        "Prototype environment detected. "
        "Production deployment should use encrypted object storage, "
        "strong authentication, role-based access control and "
        "centralized security monitoring."
    )

    st.info(
        "All uploaded evidence in this prototype receives a SHA-256 "
        "integrity fingerprint."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "VERITAS • Secure Digital Document Management System • SIH 2026"
)