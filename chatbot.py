import streamlit as st
import re

# Place holder fn to call the AI
def ai_audit_solidity_code(code):
    # list of common vulnerability patterns
    vulnerability_patterns = [
        r'call\.value\(.*\)\.gas',  
        r'require\(msg\.value\s*>=\s*\d+\)',
        r'tx\.origin',  
        r'block\.(timestamp|number)',  
        r'sha3',  
    ]

    # Initialize variables to store audit results
    vulnerabilities = []
    annotations = []

    # Split the code into lines
    lines = code.split('\n')

    # Iterate through each line of code
    for i, line in enumerate(lines):
        for pattern in vulnerability_patterns:
            if re.search(pattern, line):
                vulnerabilities.append(i + 1)  # Line numbers start from 1
                annotations.append((i + 1, f"Potential vulnerability: {pattern}"))

    return vulnerabilities, annotations



def main():
    st.set_page_config(page_title="AI Auditor")

    # Code input page
    if "code" not in st.session_state:
        st.session_state.code = ""

    st.title("Audit my code with AI")
    st.subheader("Code Input")

    language = st.radio("Select Language", ["Solidity", "Cairo"])

    code_input = st.text_area("Enter your code", st.session_state.code, height=300)
    st.session_state.code = code_input

    if st.button("Audit Now"):
        if language == "Solidity":
            vulnerabilities, annotations = ai_audit_solidity_code(code_input)
            st.session_state.audit_results = (code_input, vulnerabilities, annotations)
        else:
            st.warning("Cairo support is not implemented yet.")

        st.experimental_rerun()

    # Results page
    if "audit_results" in st.session_state:
        st.subheader("Audit Results")

        code, vulnerabilities, annotations = st.session_state.audit_results

        # Display original code
        st.subheader("Original Code")
        code_display = st.text_area("", value=code, height=300)

        # Display vulnerabilities
        st.subheader("Vulnerabilities")
        if vulnerabilities:
            for line_number in vulnerabilities:
                st.write(f"Line {line_number}: Vulnerability detected")
        else:
            st.write("No vulnerabilities found")

        # Display annotations
        st.subheader("Annotations")
        for line_number, annotation in annotations:
            st.write(f"Line {line_number}: {annotation}")

        # Share buttons and Telegram link
        st.subheader("Share and Join Community")
        share_url = "https://your-ai-auditor-url"  # Replace with your actual URL
        st.write(f"Share URL: {share_url}")
        st.markdown(f"[Copy]({share_url})")
        st.write("Share on:")
        st.markdown(
            f"[Twitter](https://twitter.com/intent/tweet?text=Check%20out%20this%20AI%20Auditor%20for%20Solidity%20code:%20{share_url}) | [Reddit](https://www.reddit.com/submit?url={share_url})"
        )
        st.write("Join our community on Telegram: [Join](https://t.me/your-telegram-group)")

if __name__ == "__main__":
    main()