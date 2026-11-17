"""
Interactive demo  --  OWNER: Person 6
Run with:  streamlit run app.py
"""
import time

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
    file_bytes = uploaded.getvalue()
    img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        st.error("Could not decode the uploaded image. Please try another file.")
        st.stop()

    h, w = img.shape[:2]
    st.image(img, channels="BGR", caption=f"Original ({w} x {h})")

    method = st.selectbox("Algorithm", list(FINDERS))
    new_w = st.slider("New width", 1, w, w)
    new_h = st.slider("New height", 1, h, h)
    seams_to_remove = (w - new_w) + (h - new_h)
    if seams_to_remove > 0:
        st.caption(f"Seams to remove: {seams_to_remove}")
    if method == "Dynamic Programming" and seams_to_remove > 250:
        st.warning(
            "Large DP resize selected. This may still take a while. "
            "Use Greedy for faster preview."
        )

    if st.button("Carve"):
        if new_w == w and new_h == h:
            st.info("No resize needed: selected size is the same as original.")
            st.stop()

        # Graph cut implementation here is educational and very slow on large images.
        # Fail fast with guidance instead of appearing to hang.
        if method == "Graph Cut (small images only)" and (h * w > 50 * 50):
            st.error(
                "Graph Cut is only practical for small images in this project. "
                "Use Dynamic Programming or Greedy for larger images, or downscale first."
            )
            st.stop()

        # TODO (Person 6): use resize(..., on_seam=...) to draw seams in red
        # step by step, show timing, and offer a download button.
        try:
            t0 = time.perf_counter()
            with st.spinner("Carving seams..."):
                out = resize(img, new_w, new_h, FINDERS[method])
            elapsed = time.perf_counter() - t0
            st.image(out, channels="BGR", caption=f"Result ({new_w} x {new_h})")
            st.success(f"Done in {elapsed:.2f}s")
        except NotImplementedError as e:
            st.warning(f"Not implemented yet: {e}")
        except Exception as e:
            st.error(f"Carving failed: {e}")
