import streamlit as st
import requests

API_URL = "http://backend:8000"  
st.title("📡 Peer-to-Peer File Sharing Interface")

menu = st.sidebar.selectbox("Select Option", ["Create User", "Upload File", "View Users", "View Files"])

if menu == "Create User":
    st.subheader("➕ Create New User")
    username = st.text_input("Username")
    email = st.text_input("Email")
    if st.button("Create User"):
        payload = {"username": username, "email": email}
        res = requests.post(f"{API_URL}/users/", json=payload)
        if res.status_code == 200:
            st.success("User created!")
        else:
            st.error("Failed to create user.")

elif menu == "Upload File":
    st.subheader("📤 Share a File")
    
    users = requests.get(f"{API_URL}/users/").json()
    user_map = {u["username"]: u["id"] for u in users}

    filename = st.text_input("Filename")
    uploader = st.selectbox("Uploaded By", list(user_map.keys()))
    receiver = st.selectbox("Shared With", list(user_map.keys()))

    if st.button("Upload"):
        if uploader == receiver:
            st.warning("Uploader and receiver cannot be the same.")
        else:
            payload = {
                "filename": filename,
                "uploaded_by": user_map[uploader],
                "shared_with": user_map[receiver]
            }
            res = requests.post(f"{API_URL}/files/", json=payload)
            if res.status_code == 200:
                st.success("File shared successfully!")
            else:
                st.error("Upload failed.")

elif menu == "View Users":
    st.subheader("👥 Registered Users")
    res = requests.get(f"{API_URL}/users/")
    if res.status_code == 200:
        for user in res.json():
            st.write(f"**ID**: {user['id']} | **Username**: {user['username']} | **Email**: {user['email']}")
    else:
        st.error("Could not fetch users.")

elif menu == "View Files":
    st.subheader("📁 Shared Files")
    res = requests.get(f"{API_URL}/files/")
    users = {u["id"]: u["username"] for u in requests.get(f"{API_URL}/users/").json()}

    if res.status_code == 200:
        for f in res.json():
            st.write(f"**Filename**: {f['filename']} | **Uploader**: {users.get(f['uploaded_by'], 'Unknown')} | "
                     f"**Receiver**: {users.get(f['shared_with'], 'Unknown')} | "
                     f"**Time**: {f['upload_time']}")
    else:
        st.error("Could not fetch files.")

