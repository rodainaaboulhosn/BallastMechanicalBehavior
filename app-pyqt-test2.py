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

D50 = st.sidebar.number_input("Particle diameter D50 (mm)", value=30.0)
Cu = st.sidebar.number_input("Coefficient of uniformity", value=2.0)
Cc = st.sidebar.number_input("Coefficient of curvature", value=0.85)
e = st.sidebar.number_input("Void ratio", value=0.8)
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
    outp1=0.0
    outp2=0.0
    Delta_Ei = 0.2
    Ei = 0.1
    nincr = 19

    inp[0], inp[1], inp[2], inp[3], inp[4], inp[5] = D50, Cu, Cc, e, gamma, sigma3

    # ---------------- normalize inputs ----------------
    if inp[0] < 17.4:
        inp[0] = 17.4
    elif inp[0] > 38.9:
        inp[0] = 38.9

    # normalize
    inp[0] = (inp[0] - 17.4) / 21.5

    if inp[1] < 1.5:
        inp[1] = 1.5
    elif inp[1] > 2.93:
        inp[1] = 2.93

    inp[1] = (inp[1] - 1.5) / 1.43
    
    if inp[2] <0.84:
        inp[2]=0.84
    elif inp[2]>1.0:
        inp[2]=1.0
    inp[2] = (inp[2] - 0.84) / 0.16

    if inp[3]<0.64:
        inp[3]=0.63
    elif inp[3]>0.835:
        inp[3]=0.835
    inp[3] = (inp[3] - 0.64) / 0.195

    if inp[4]<14.7:
        inp[4]=14.7
    elif inp[4]>17.0:
        inp[4]=17.0
    inp[4] = (inp[4] - 14.7) / 2.3

    if inp[5]<15.0:
        inp[5]=15.0
    elif inp[5]>310.3:
        inp[5]=310.3
    inp[5] = (inp[5] - 15.0) / 295.3

    for i in range(nincr):

        inp[6] = Ei
        inp[7] = Delta_Ei

        if inp[6]<0.1:
            inp[6]=0.1
        elif inp[6]>19.0:
            inp[6]=19.0
        inp[6] = (inp[6] - 0.1) / 18.9

        if inp[7]<0.2:
            inp[7]=0.2
        elif inp[7]>2.0:
            inp[7]=2.0
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
        netsum += feature4[0] * (-1.141728E-03)
        netsum += feature4[1] * (3.975101E-02)
        feature2[0] = math.tanh(netsum)

        netsum = 1.398888
        netsum = netsum + inp[0] * 0.4030881
        netsum = netsum + inp[1] * (-1.145678)
        netsum = netsum + inp[2] * 1.7514
        netsum = netsum + inp[3] * (-4.851397E-02)
        netsum = netsum + inp[4] * 0.600504
        netsum = netsum + inp[5] * (-1.25401)
        netsum = netsum + inp[6] * 0.1212502
        netsum = netsum + inp[7] * (-1.370505)
        netsum = netsum + 1.409978
        netsum = netsum + feature4[0] * (-0.8171972)
        netsum = netsum + feature4[1] * (-0.2031538)
        feature2[1]= math.tanh(netsum)
            
        netsum = -0.5928574
        netsum = netsum + inp[0] * (-0.3640539)
        netsum = netsum + inp[1] * (-0.1992462)
        netsum = netsum + inp[2] * (-0.5953705)
        netsum = netsum + inp[3] * 0.9727836
        netsum = netsum + inp[4] * 0.5522084
        netsum = netsum + inp[5] * 0.4467421
        netsum = netsum + inp[6] * 0.190355
        netsum = netsum + inp[7] * 1.531258
        netsum = netsum + (-0.59403)
        netsum = netsum + feature4[0] * (-0.3724768)
        netsum = netsum + feature4[1] * 0.5388053
        feature2[2] = math.tanh(netsum)
            
        netsum = 0.1444716
        netsum = netsum + inp[0] * 0.3665255
        netsum = netsum + inp[1] * 0.3444198
        netsum = netsum + inp[2] * (-0.3420203)
        netsum = netsum + inp[3] * 0.2631427
        netsum = netsum + inp[4] * 0.5113632
        netsum = netsum + inp[5] * (-8.797734E-02)
        netsum = netsum + inp[6] * (-0.6501069)
        netsum = netsum + inp[7] * (-0.8124169)
        netsum = netsum + (-0.2340354)
        netsum = netsum + feature4[0] * 0.7072874
        netsum = netsum + feature4[1] * (-0.2255989)
        feature2[3] = math.tanh(netsum)
            
                     
        netsum = 0.5202681
        netsum = netsum + inp[0] * 0.1600636
        netsum = netsum + inp[1] * 0.243405
        netsum = netsum + inp[2] * (-0.5737442)
        netsum = netsum + inp[3] * 0.4030233
        netsum = netsum + inp[4] * (-0.2666483)
        netsum = netsum + inp[5] * (-1.497535)
        netsum = netsum + inp[6] * 1.621032
        netsum = netsum + inp[7] * (-0.8956463)
        netsum = netsum + 0.6595912
        netsum = netsum + feature4[0] * 8.659312E-02
        netsum = netsum + feature4[1] * (-0.0738372)
        feature2[4] = math.tanh(netsum)
        
        netsum = 1.042258
        netsum = netsum + inp[0] * 0.4779588
        netsum = netsum + inp[1] * 1.185758
        netsum = netsum + inp[2] * 9.611069E-02
        netsum = netsum + inp[3] * (-0.1345853)
        netsum = netsum + inp[4] * (-1.261218)
        netsum = netsum + inp[5] * 2.678253
        netsum = netsum + inp[6] * 0.8559374
        netsum = netsum + inp[7] * (-2.43513)
        netsum = netsum + 1.03949
        netsum = netsum + feature4[0] * (-7.752682E-02)
        netsum = netsum + feature4[1] * 0.6434758
        feature2[5] = math.tanh(netsum)
            
        netsum = 0.2147741
        netsum = netsum + inp[0] * (-1.746428)
        netsum = netsum + inp[1] * (-1.621715E-02)
        netsum = netsum + inp[2] * (-0.5050035)
        netsum = netsum + inp[3] * (-0.2943828)
        netsum = netsum + inp[4] * 0.1160996
        netsum = netsum + inp[5] * 1.312003
        netsum = netsum + inp[6] * 0.5568389
        netsum = netsum + inp[7] * (-0.6059821)
        netsum = netsum + 9.793694E-02
        netsum = netsum + feature4[0] * 0.1731099
        netsum = netsum + feature4[1] * 0.1616357
        feature2[6] = math.tanh(netsum)
            
        netsum = -0.6616849
        netsum = netsum + inp[0] * 5.509186E-02
        netsum = netsum + inp[1] * 0.8722677
        netsum = netsum + inp[2] * (-0.6158577)
        netsum = netsum + inp[3] * 0.8295627
        netsum = netsum + inp[4] * (-0.2739595)
        netsum = netsum + inp[5] * (-2.699235)
        netsum = netsum + inp[6] * 0.384888
        netsum = netsum + inp[7] * 1.136404
        netsum = netsum + (-0.8969032)
        netsum = netsum + feature4[0] * 0.568903
        netsum = netsum + feature4[1] * 5.099271E-02
        feature2[7] = math.tanh(netsum)
            
        netsum = -0.2869954
        netsum = netsum + inp[0] * (-0.2505337)
        netsum = netsum + inp[1] * (-6.212543E-02)
        netsum = netsum + inp[2] * (-0.9941342)
        netsum = netsum + inp[3] * 0.7242925
        netsum = netsum + inp[4] * (-0.4818746)
        netsum = netsum + inp[5] * 0.0344972
        netsum = netsum + inp[6] * (-0.1126954)
        netsum = netsum + inp[7] * 0.8301603
        netsum = netsum + ( -0.3414904)
        netsum = netsum + feature4[0] * 2.318101E-02
        netsum = netsum + feature4[1] * (-0.4897337)
        feature2[8] = math.tanh(netsum)
            
        netsum = 0.4857446
        netsum = netsum + inp[0] * (-0.5971019)
        netsum = netsum + inp[1] * 0.474021
        netsum = netsum + inp[2] * 0.5300007
        netsum = netsum + inp[3] * (-1.086891)
        netsum = netsum + inp[4] * (-1.107612)
        netsum = netsum + inp[5] * 0.1851085
        netsum = netsum + inp[6] * (-0.2056437)
        netsum = netsum + inp[7] * (-0.4852493)
        netsum = netsum + 0.2811413
        netsum = netsum + feature4[0] * (-4.750614E-02)
        netsum = netsum + feature4[1] * (-5.554906E-02)
        feature2[9] = math.tanh(netsum)

        # outputs
        netsum = -0.5142042
        netsum = netsum + feature2[0] * 1.786009
        netsum = netsum + feature2[1] * (-1.439854)
        netsum = netsum + feature2[2] * 0.980323
        netsum = netsum + feature2[3] * (-3.670824E-03)
        netsum = netsum + feature2[4] * (-2.066014)
        netsum = netsum + feature2[5] * 2.347498E-02
        netsum = netsum + feature2[6] * (-0.4720106)
        netsum = netsum + feature2[7] * (-1.267853)
        netsum = netsum + feature2[8] * 0.63671
        netsum = netsum + feature2[9] * (-0.6820487)
        outp1 = 1.0 / (1.0 + math.exp(-netsum))

        netsum = 4.520982E-02
        netsum = netsum + feature2[0] * 0.4744908
        netsum = netsum + feature2[1] * (-1.890552)
        netsum = netsum + feature2[2] * 0.7917076
        netsum = netsum + feature2[3] * 0.7901414
        netsum = netsum + feature2[4] * (-0.7322906)
        netsum = netsum + feature2[5] * 2.547449
        netsum = netsum + feature2[6] * (-1.116966)
        netsum = netsum + feature2[7] * (-1.09265)
        netsum = netsum + feature2[8] * 1.136998
        netsum = netsum + feature2[9] * (0.87844)
        outp2 = 1.0 / (1.0 + math.exp(-netsum))
            
        feature4[0] = feature4[0] + feature4[0] * -0.9
        feature4[0] = feature4[0] + outp1 * 0.9
        feature4[1] = feature4[1] + feature4[1] * -0.9
        feature4[1] = feature4[1] + outp2 * 0.9
        
        outp1 = 1449.45 *  (outp1 - 0.1) / 0.8  + 44.01553
        if (outp1<44.01553):
            outp1 = 44.01553
        elif (outp1>1493.466):
            outp1 = 1493.466
            
            
            
        outp2 = 16.00923 *  (outp2 - 0.1) / 0.8  + (-11.26868)
            
        if outp2<(-11.26868):
            outp2 = -11.26868
        elif outp2>4.74055:
            outp2 = 4.74055
        
        
        
        Ei += Delta_Ei
        Delta_Ei += 0.1

        if i>0:
            Str.append(Ei)
            Qi.append(outp1)
            ev.append(outp2)

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
        ax1.set_xlim([0,22.5])
        ax1.set_ylim(bottom=0)
        ymax_plot = max(Qi) * 1.05  # 5% margin
        ax1.set_ylim(0, ymax_plot)
        st.pyplot(fig1)
        

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.plot(Str, ev, color="black")
        ax2.set_title("Volumetric Strain Curve")
        ax2.set_xlabel("Axial strain (%)")
        ax2.set_ylabel("Volumetric deformation (%)")
        ax2.invert_yaxis()
        ax2.set_xlim([0,22.5])
        ymin_ev = math.floor(min(ev))
        ymax_ev = math.ceil(max(ev))

        ax2.set_ylim(ymax_ev, ymin_ev)   # because axis is inverted
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
