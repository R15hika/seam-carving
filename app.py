"""
Interactive demo  --  OWNER: Ang Yu Xuan
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

    show_progress = st.checkbox("Show seam removal animation", value=False)

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

        try:
            total_seams = seams_to_remove
            progress_bar = st.progress(0.0)
            status_text = st.empty()
            preview_spot = st.empty()
            step_counter = {"count": 0}

            # Callback passed into resize() via on_seam parameter.
            def handle_seam(current_img, seam=None, orientation="vertical", *args):
                step_counter["count"] += 1
                current_step = step_counter["count"]

                if total_seams > 0:
                    progress_bar.progress(min(current_step / total_seams, 1.0))
                status_text.text(f"Carving seam {current_step} / {total_seams}...")

                if not show_progress:
                    return

                annotated = current_img.copy()
                if seam is not None:
                    img_h, img_w = annotated.shape[:2]
                    for idx, val in enumerate(seam):
                        if orientation == "horizontal":
                            # In horizontal mode callback receives original orientation:
                            # idx is column, val is row.
                            r, c = int(val), int(idx)
                        else:
                            # In vertical mode idx is row, val is column.
                            r, c = int(idx), int(val)
                        if 0 <= r < img_h and 0 <= c < img_w:
                            annotated[r, c] = [0, 0, 255]

                preview_spot.image(
                    annotated,
                    channels="BGR",
                    caption=f"Step {current_step}/{total_seams} ({orientation})",
                )

            t0 = time.perf_counter()
            with st.spinner("Carving seams..."):
                out = resize(img, new_w, new_h, FINDERS[method], on_seam=handle_seam)
            elapsed = time.perf_counter() - t0

            progress_bar.progress(1.0)
            status_text.success(
                f"Done! Carved {total_seams} seams in {elapsed:.2f} seconds "
                f"({elapsed / max(1, total_seams) * 1000:.1f} ms/seam)."
            )
            st.image(out, channels="BGR", caption=f"Result ({new_w} x {new_h})")

            is_success, buffer = cv2.imencode(".png", out)
            if is_success:
                st.download_button(
                    label="Download Carved Image",
                    data=buffer.tobytes(),
                    file_name="carved_result.png",
                    mime="image/png",
                )
        except NotImplementedError as e:
            st.warning(f"Not implemented yet: {e}")
        except Exception as e:
            st.error(f"Carving failed: {e}")
