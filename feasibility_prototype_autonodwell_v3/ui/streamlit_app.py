import streamlit as st
import requests
st.set_page_config(page_title='Autonodwell Feasibility Demo', layout='centered')
st.title('Autonodwell — Parcel Intelligence (Demo v3)')
st.write('Enter a street address in California to fetch parcel & zoning intelligence.')
address = st.text_input('Address (e.g. 1015 Los Robles Ave, Palo Alto, CA)', value='1015 Los Robles Ave, Palo Alto, CA')
if st.button('Analyze'):
    with st.spinner('Analyzing...'):
        try:
            resp = requests.post('http://localhost:8000/analyze_address', json={'address': address}, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                st.subheader('Summary')
                st.write(data.get('llm_summary'))
                st.subheader('Parcel & Jurisdiction')
                st.json({'county': data.get('county'), 'service_used': data.get('service_used')})
                st.subheader('Parcel Record')
                st.json(data.get('parcel'))
                st.subheader('Deterministic Checks')
                st.json(data.get('deterministic'))
                st.subheader('Document Matches (local)')
                for d in data.get('document_matches', []):
                    st.markdown(f"**{d['doc']}**")
                    st.write(d.get('snippet','')[:800] + '...')
                if st.button('Download PDF Report'):
                    r2 = requests.post('http://localhost:8000/report_pdf', json={'address': address}, timeout=120)
                    if r2.status_code == 200:
                        st.download_button('Download PDF', r2.content, file_name='autonodwell_report.pdf', mime='application/pdf')
                    else:
                        st.error('Failed to generate PDF report.')
            else:
                st.error(f"Backend error: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"Connection error: {e}")
