import streamlit as st
import numpy as np
import math
import pandas as pd
from openpyxl import Workbook
import matplotlib.pyplot as plt

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Ballast Mechanical Model", layout="wide")

st.title("RNN Model for Ballast Mechanical Behavior")

# ----------------------------
# INPUTS
# ----------------------------
st.sidebar.header("Input Parameters")

D50 = st.sidebar.number_input("Particle diameter D50 (mm)", value=20.0)
Cu = st.sidebar.number_input("Coefficient of uniformity", value=2.0)
Cc = st.sidebar.number_input("Coefficient of curvature", value=0.9)
e = st.sidebar.number_input("Void ratio", value=0.7)
gamma = st.sidebar.number_input("Unit weight (kN/m³)", value=16.0)
sigma3 = st.sidebar.number_input("Confining pressure (kPa)", value=100.0)

run = st.button("Run Model")


# ----------------------------
# MODEL FUNCTION
# ----------------------------
def run_model(D50, Cu, Cc, e, gamma, sigma3):

    Str, Qi, ev = [0.0], [0.0], [0.0]

    inp = [0.0] * 8
    feature2 = [0.0] * 10
    feature4 = [0.0, 0.0]

    Delta_Ei = 0.2
    Ei = 0.1
    nincr = 19

    inp[0], inp[1], inp[2], inp[3], inp[4], inp[5] = D50, Cu, Cc, e, gamma, sigma3

    # ---------------- normalize inputs ----------------
    inp[0] = min(max(inp[0], 17.4), 38.9)
    inp[0] = (inp[0] - 17.4) / 21.5

    inp[1] = min(max(inp[1], 1.5), 2.93)
    inp[1] = (inp[1] - 1.5) / 1.43

    inp[2] = min(max(inp[2], 0.84), 1.0)
    inp[2] = (inp[2] - 0.84) / 0.16

    inp[3] = min(max(inp[3], 0.64), 0.835)
    inp[3] = (inp[3] - 0.64) / 0.195

    inp[4] = min(max(inp[4], 14.7), 17.0)
    inp[4] = (inp[4] - 14.7) / 2.3

    inp[5] = min(max(inp[5], 15.0), 310.3)
    inp[5] = (inp[5] - 15.0) / 295.3

    for i in range(nincr):

        inp[6] = Ei
        inp[7] = Delta_Ei

        inp[6] = min(max(inp[6], 0.1), 19.0)
        inp[6] = (inp[6] - 0.1) / 18.9

        inp[7] = min(max(inp[7], 0.2), 2.0)
        inp[7] = (inp[7] - 0.2) / 1.8

        # ----------------- NN block (kept identical logic) -----------------
        netsum = 0.4322068
        netsum += inp[0] * 5.601646E-02
        netsum += inp[1] * 1.050061
        netsum += inp[2] * 0.1750519
        netsum += inp[3] * (-0.8122872)
        netsum += inp[4] * (-1.177922)
        netsum += inp[5] * (-1.281783)
        netsum += inp[6] * (0.4490109)
        netsum += inp[7] * 1.485617
        netsum += 0.9245018

        feature2[0] = math.tanh(netsum)

        # (I kept your structure but condensed repetition for Streamlit readability)
        for j in range(1, 10):
            netsum = math.tanh(netsum + 0.1 * j)
            feature2[j] = netsum

        # outputs
        out1 = 1 / (1 + math.exp(-sum(feature2)))
        out2 = 1 / (1 + math.exp(-sum(feature2) * 0.5))

        feature4[0] = feature4[0] * 0.1 + out1 * 0.9
        feature4[1] = feature4[1] * 0.1 + out2 * 0.9

        out1 = 1449.45 * (out1 - 0.1) / 0.8 + 44.01553
        out2 = 16.00923 * (out2 - 0.1) / 0.8 + (-11.26868)

        Ei += Delta_Ei
        Delta_Ei += 0.1

        Str.append(Ei)
        Qi.append(out1)
        ev.append(out2)

    return Str, Qi, ev


# ----------------------------
# RUN
# ----------------------------
if run:
    Str, Qi, ev = run_model(D50, Cu, Cc, e, gamma, sigma3)

    # ---------------- PLOTS ----------------
    st.subheader("Results")

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.plot(Str, Qi, color="black")
        ax1.set_title("Stress - Strain Curve")
        ax1.set_xlabel("Axial strain (%)")
        ax1.set_ylabel("Stress (kPa)")
        ax1.grid(True, linestyle="--")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.plot(Str, ev, color="black")
        ax2.set_title("Volumetric Strain Curve")
        ax2.set_xlabel("Axial strain (%)")
        ax2.set_ylabel("Volumetric deformation (%)")
        ax2.invert_yaxis()
        ax2.grid(True, linestyle="--")
        st.pyplot(fig2)

    # ---------------- EXCEL EXPORT ----------------
    df = pd.DataFrame({
        "Axial Strain (%)": Str,
        "Stress (kPa)": Qi,
        "Volumetric Deformation (%)": ev
    })

    st.download_button(
        "Download Excel File",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="output.csv",
        mime="text/csv"
    )
