"""
Interactive demo  --  OWNER: Ang Yu Xuan
Run with:  streamlit run app.py
"""
import cv2
import numpy as np
import streamlit as st
import time

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
    
    show_progress = st.checkbox("Show seam removal animation", value=False)

    if st.button("Carve"):
        try:
            total_seams = (w - new_w) + (h - new_h)
            
            if total_seams == 0:
                st.info("Target dimensions match original dimensions. No carving needed.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                preview_spot = st.empty()
                
                step_counter = {"count": 0}

                # Callback function passed into resize() via on_seam parameter
                def handle_seam(current_img, seam=None, orientation="vertical", *args):
                    step_counter["count"] += 1
                    current_step = step_counter["count"]
                    
                    if total_seams > 0:
                        progress_bar.progress(min(current_step / total_seams, 1.0))
                    
                    status_text.text(f"Carving seam {current_step} / {total_seams}...")
                    
                    # If callback gives raw image + seam coordinates, draw red line:
                    if seam is not None:
                        annotated = current_img.copy()
                        img_h, img_w = annotated.shape[:2]
                        
                        for idx, val in enumerate(seam):
                            if orientation == "horizontal":
                                # For transposed images, idx represents column and val represents row
                                r, c = val, idx
                            else:
                                # For vertical seams, idx represents row and val represents column
                                r, c = idx, val
            
                            # Safe boundary check before assignment
                            if 0 <= r < img_h and 0 <= c < img_w:
                                annotated[r, c] = [0, 0, 255]

                        if orientation == "horizontal":
                            # Re-transpose back so Streamlit renders it upright
                            annotated = cv2.transpose(annotated)
                   
                    else:
                        annotated = current_img

                    if show_progress:
                        preview_spot.image(
                            annotated, 
                            channels="BGR", 
                            caption=f"Step {current_step}/{total_seams} ({orientation})"
                        )

                # Start timing performance
                start_time = time.perf_counter()

                # Call resize with on_seam callback
                out = resize(
                    img, 
                    new_w, 
                    new_h, 
                    FINDERS[method], 
                    on_seam=handle_seam
                )

                elapsed = time.perf_counter() - start_time

                # Update status displays
                progress_bar.progress(1.0)
                status_text.success(f"Done! Carved {total_seams} seams in {elapsed:.2f} seconds ({elapsed/max(1, total_seams)*1000:.1f} ms/seam).")
                
                # Show final image
                st.image(out, channels="BGR", caption=f"Result ({new_w} x {new_h})")

                # Prepare image buffer for download
                is_success, buffer = cv2.imencode(".png", out)
                if is_success:
                    st.download_button(
                        label="Download Carved Image",
                        data=buffer.tobytes(),
                        file_name="carved_result.png",
                        mime="image/png"
                    )

        except NotImplementedError as e:
            st.warning(f"Not implemented yet: {e}")
