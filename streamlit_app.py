import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from field_generator import generate_synthetic_field
from ndvi_core import compute_ndvi, classify_ndvi


st.set_page_config(
    page_title="NDVI Interactive Demo",
    layout="wide"
)


def ndvi_colormap():
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list(
        "ndvi",
        [   (0.0, "#8B5E34"),
            (0.5, "#D9C34B"),
            (1.0, "#4C8C4A")
        ]
    )


def create_field(stress):
    red, nir = generate_synthetic_field(size=128, stress_level=stress)
    ndvi = compute_ndvi(red, nir)

    return red, nir, ndvi


if "stress" not in st.session_state:
    st.session_state.stress = 0.35

if "field" not in st.session_state:
    st.session_state.field = create_field(
        st.session_state.stress
    )

st.title("NDVI Compute Demo")
st.caption("Synthetic Red / NIR field → per-pixel NDVI → vegetation health map")

red, nir, ndvi = st.session_state.field


col1, col2 = st.columns([2,1])


with col2:
    mode = st.radio("Display", ["RED BAND", "NIR BAND", "NDVI MAP"])
    stress = st.slider("Field stress level", 0.0, 1.0,st.session_state.stress)

    if stress != st.session_state.stress:
        st.session_state.stress = stress
        st.session_state.field = create_field(stress)
        st.rerun()

    if st.button("Regenerate field"):
        st.session_state.field = create_field(st.session_state.stress)
        st.rerun()


with col1:
    fig, ax = plt.subplots(figsize=(6,6))

    if mode == "RED BAND":
        ax.imshow(red, cmap="Reds")
        ax.set_title("RED BAND (~660nm)")

    elif mode == "NIR BAND":
        ax.imshow(nir, cmap="Blues")
        ax.set_title("NIR BAND (~850nm)")

    else:
        ax.imshow(ndvi, cmap=ndvi_colormap(), vmin=-0.2, vmax=0.8)
        ax.set_title("NDVI MAP")

    ax.axis("off")
    st.pyplot(fig)


#stats
st.divider()
st.subheader("NDVI Summary")
c1, c2, c3 = st.columns(3)

c1.metric("Mean NDVI", f"{ndvi.mean():.3f}")
c2.metric("Minimum", f"{ndvi.min():.3f}")
c3.metric("Maximum", f"{ndvi.max():.3f}")

st.subheader("Vegetation Classification")

for label, pct in classify_ndvi(ndvi).items():
    st.write(f"{label}: **{pct:.1f}%**")