"""
Interactive demo  --  OWNER: Person 6
Run with:  streamlit run app.py
"""
import cv2
import numpy as np
import streamlit as st

from seamcarve.carve import resize
from seamcarve.dp import find_seam_dp
from seamcarve.greedy import find_seam_greedy
from seamcarve.graphcut import find_seam_graphcut

FINDERS = {
    "Dynamic Programming": find_seam_dp,
    "Greedy": find_seam_greedy,
    "Graph Cut (small images only)": find_seam_graphcut,
}

st.title("Seam Carving")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded:
    img = cv2.imdecode(np.frombuffer(uploaded.read(), np.uint8), cv2.IMREAD_COLOR)
    h, w = img.shape[:2]
    st.image(img, channels="BGR", caption=f"Original ({w} x {h})")

    method = st.selectbox("Algorithm", list(FINDERS))
    new_w = st.slider("New width", 1, w, w)
    new_h = st.slider("New height", 1, h, h)

    if st.button("Carve"):
        # TODO (Person 6): use resize(..., on_seam=...) to draw seams in red
        # step by step, show timing, and offer a download button.
        try:
            out = resize(img, new_w, new_h, FINDERS[method])
            st.image(out, channels="BGR", caption=f"Result ({new_w} x {new_h})")
        except NotImplementedError as e:
            st.warning(f"Not implemented yet: {e}")
