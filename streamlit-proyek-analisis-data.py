import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium

# Gathering Data

Aotizhongxin_df = pd.read_csv("Air set-Aotizhongxin.csv")
Changping_df = pd.read_csv("Air set-Changping.csv")
Dingling_df = pd.read_csv("Air set-Dingling.csv")
Dongsi_df = pd.read_csv("Air set-Dongsi.csv")
Guanyuan_df = pd.read_csv("Air set-Guanyuan.csv")
Gucheng_df = pd.read_csv("Air set-Gucheng.csv")
Huairou_df = pd.read_csv("Air set-Huairou.csv")
Nongzhanguan_df = pd.read_csv("Air set-Nongzhanguan.csv")
Shunyi_df = pd.read_csv("Air set-Shunyi.csv")
Tiantan_df = pd.read_csv("Air set-Tiantan.csv")
Wanliu_df = pd.read_csv("Air set-Wanliu.csv")
Wanshouxigong_df = pd.read_csv("Air set-Wanshouxigong.csv")

list_data = [Aotizhongxin_df, Changping_df, Dingling_df, Dongsi_df, Guanyuan_df, Gucheng_df,
             Huairou_df, Nongzhanguan_df, Shunyi_df, Tiantan_df, Wanliu_df, Wanshouxigong_df]

PRSA_df_first = pd.concat(list_data, ignore_index=True)

NUMBER_OF_ROW_FOR_EVERY_STATION = 35064

# Data Wragling

# Konversi kolom ke tipe numerik jika masih ada yang object
PRSA_columns = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "RAIN", "DEWP", "WSPM", "PRES"]
for column in PRSA_columns:
    PRSA_df_first[column] = PRSA_df_first[column].interpolate(method='linear', limit_direction='forward')

for i in range(12):
    modus_wd = PRSA_df_first.loc[0*i:NUMBER_OF_ROW_FOR_EVERY_STATION, "wd"].mode()
    PRSA_df_first['wd'] = PRSA_df_first['wd'].fillna(value=str(modus_wd))

PRSA_df_first["date"] = pd.to_datetime(PRSA_df_first[["year", "month", "day", "hour"]])
PRSA_df = PRSA_df_first.drop(columns=["year", "month", "day"])

min_date = PRSA_df["date"].min()
max_date = PRSA_df["date"].max()


with st.sidebar:
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    page = st.selectbox(
        label='Pergi ke',  
        options=('Utama', 'Cek Kulitas Udara Stasiun China', 'Stasiun mana yang paling tercemar?',  
                 'Faktor Alam vs Polusi Udara', 'Peta Geospasial')  
    )

# Setting jalaman

st.write('Kamu di Halaman', page + '!')

PRSA_df = PRSA_df_first[(PRSA_df_first["date"] >= str(start_date)) & 
                (PRSA_df_first["date"] <= str(end_date))]

if page == "Utama":
    st.write(
    """
    # Dashboard Info Kualitas Udara Stasiun China

    Silakan pilih salah satu opsi di menu 'Pergi Ke' di sidebar sebelah kiri untuk melanjutkan.

    Catatan : Pada Cek Info Kualitas Udara di Stasiun China ini, PM 2.5 dan PM 10 digunakan sebagai 
    indikator utama penilaian pencemaran udara. PM 2.5 (Particulate Matter 2.5) adalah partikel udara 
    dengan diameter ≤ 2.5 mikrometer, sedangkan PM 10 (Particulate Matter 10) memiliki diameter ≤ 10 mikrometer. 
    Kedua partikel ini merupakan polutan utama yang dapat berdampak buruk pada kesehatan manusia, 
    terutama sistem pernapasan. Selain itu, kadar PM 2.5 dan PM 10 mencerminkan tingkat pencemaran udara 
    dari berbagai sumber, seperti kendaraan bermotor, industri, dan aktivitas domestik 
    """

)
elif page == "Cek Kulitas Udara Stasiun China":
    st.markdown(f"# Kadar PM 2.5 vs PM 10")

    import streamlit as st
    import pandas as pd

    # Resample data untuk mendapatkan rata-rata bulanan
    monthly_PM25_mean_df = PRSA_df.resample(rule='M', on='date')["PM2.5"].mean().reset_index()
    monthly_PM10_mean_df = PRSA_df.resample(rule='M', on='date')["PM10"].mean().reset_index()

    latest_month = monthly_PM25_mean_df["date"].max().strftime("%B %Y")
    latest_pm25 = monthly_PM25_mean_df.iloc[-1]["PM2.5"]
    latest_pm10 = monthly_PM10_mean_df.iloc[-1]["PM10"]

    delta_PM25 = latest_pm25-monthly_PM25_mean_df.iloc[-2]["PM2.5"]
    delta_PM10 = latest_pm10-monthly_PM10_mean_df.iloc[-2]["PM10"]

    st.markdown("### Rerata PM 2.5 dan PM 10 per bulan")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label=f"Latest PM 2.5 at {latest_month}", value=f"{latest_pm25:.2f} µg/m³", delta = f"{delta_PM25:.4f} µg/m³", delta_color="inverse")

    with col2:
        st.metric(label=f"Latest PM 10 at {latest_month}", value=f"{latest_pm10:.2f} µg/m³", delta = f"{delta_PM10:.4f} µg/m³", delta_color="inverse")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_PM25_mean_df["date"], monthly_PM25_mean_df["PM2.5"], marker='o', linewidth=2, color="skyblue", label="PM 2.5")
    ax.plot(monthly_PM10_mean_df["date"], monthly_PM10_mean_df["PM10"], marker='o', linewidth=2, color="steelblue", label="PM 10")
    ax.set_title(f"Average of PM 2.5 dan PM 10 per Month ($\mu g/m^3$)", fontsize=20)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend()
    st.pyplot(fig)


### Plotting mengenai kadar PM 2.5 dan PM 10

    hour_mean_PM25_df = PRSA_df.groupby("hour")["PM2.5"].mean()
    hour_mean_PM10_df = PRSA_df.groupby(by="hour")["PM10"].mean()

    # Grafik 1: Rata-rata PM 2.5 per tahun

    st.markdown("### Rerata PM 2.5 per jam")

    indexOfMaksimumMean = hour_mean_PM10_df.idxmax()
    highest_hour = indexOfMaksimumMean
    highest_value = hour_mean_PM25_df.loc[highest_hour]

    st.metric(f"Highest Hour at {highest_hour}:00", value=f"{highest_value:.2f} µg/m³")

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(x=hour_mean_PM25_df.index, y=hour_mean_PM25_df.values, color="skyblue", ax=ax)
    ax.set_title(f"Average PM 2.5 per Hour", fontsize=20)
    ax.set_xlabel("Hour (:00)", fontsize=14) 
    st.pyplot(fig)


    # Grafik 2: Rata-rata PM 10 per jam

    st.markdown("### Rerata PM 10 per jam")

    indexOfMaksimumMean = hour_mean_PM10_df.idxmax()
    highest_hour = indexOfMaksimumMean
    highest_value = hour_mean_PM10_df.loc[highest_hour]

    st.metric(f"Highest Hour at {highest_hour}:00", value=f"{highest_value:.2f} µg/m³")

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(x=hour_mean_PM10_df.index, y=hour_mean_PM10_df.values, color="skyblue", ax=ax)
    ax.set_title(f"Average PM 10 per Hour", fontsize=20)
    ax.set_xlabel("Hour (:00)", fontsize=14)
    st.pyplot(fig)



### Plotting mengenai CO, O3, SO2, SO4

    unsur = ["CO", "O3", "SO2", "NO2"]

    for elemen in unsur:
        monthly_mean_df = PRSA_df.resample(rule='M', on='date')[elemen].mean().reset_index()
        yearly_mean_df = PRSA_df.resample(rule='Y', on='date')[elemen].mean().reset_index()
        hour_mean_df = PRSA_df.groupby(by="hour")[elemen].mean()

        st.markdown(f"## Kadar ${elemen}$ di udara")

        latest_month = monthly_mean_df["date"].max().strftime("%B %Y")
        latest_value = monthly_mean_df.iloc[-1][elemen]
        delta_elemen = latest_value-monthly_mean_df.iloc[-2][elemen]

        st.markdown(f"### Rerata {elemen} per bulan")

        # Membuat grafik timeseries untuk rerata per bulan

        st.metric(label=f"Latest at {latest_month}", value=f"{latest_value:.2f} µg/m³", delta = f"{delta_elemen:.4f} µg/m³", delta_color="inverse")

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(monthly_mean_df["date"], monthly_mean_df[elemen], marker='o', linewidth=2, color="steelblue")
        ax.set_title(f"Average of {elemen} per Month ($\mu g/m^3$)", fontsize=20)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.grid(True, linestyle="--", alpha=0.7)
        st.pyplot(fig)

        # Membuat grafik timeseries untuk rerata per bulan

        st.markdown(f"### Rerata {elemen} per jam")

        indexOfMaksimumMean = hour_mean_df.idxmax()
        highest_hour = indexOfMaksimumMean 
        highest_value = hour_mean_df.loc[highest_hour]
        st.metric(label= f"Highest Hour at {highest_hour}:00", value=f"{highest_value:.2f} µg/m³")

        fig, ax = plt.subplots(figsize=(12, 4))
        sns.barplot(x=hour_mean_df.index, y=hour_mean_df.values, color="skyblue")
        ax.set_title(f"Average ${elemen}$ per Hour ($\mu g/m^3$)", fontsize=20)
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=8)
        st.pyplot(fig)


### Plotting mengenai stasiun dengan polusi PM 2.5 dan PM 10 terbesar dan terkecil

if page == "Stasiun mana yang paling tercemar?":
    unsur = ["PM2.5", "PM10"]

    for elemen in unsur:
        st.markdown(f"## Kadar {elemen} Tiap Satisun")

        average_per_station = PRSA_df.groupby(by="station")[elemen].mean().sort_values()

        col1, col2 = st.columns(2)

        # Membuat grafik urutan stasiun dengan kadar PM 2.5 tertinggi

        with col1:
            highest_station = average_per_station.idxmax()
            highest_value = average_per_station.max()

            st.metric(label=f"Highest PM2.5: {highest_station} Station", value=f"{highest_value:.2f} µg/m³")

        # Membuat grafik urutan stasiun dengan kadar PM 2.5 tertinggi

        with col2:
            lowest_station = average_per_station.idxmin()
            lowest_value = average_per_station.min()

            st.metric(label=f"Lowest PM2.5: {lowest_station} station", value=f"{lowest_value:.2f} µg/m³")

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=average_per_station.values, y=average_per_station.index, color='skyblue')
        ax.set_title(f"Average {elemen} per Stasiun", fontsize=20)
        ax.set_xlabel(f"{elemen} ($\mu g/m^3$)", fontsize=14) 
        ax.set_ylabel("")
        st.pyplot(fig)

### Plotting korelasi PM 2.5 dan PM 10 terhadap faktor Alam

elif page == "Faktor Alam vs Polusi Udara":

    st.markdown(f"## Faktor Alam vs PM 2.5 dan PM 10")
    nature = ["RAIN", "TEMP", "PRES", "WSPM"]
    nature_title = ["hujan", "temperatur", "tekanan"]

    for idx, elemen in enumerate(nature):    

        col1, col2 = st.columns(2) 

        # Membuat diagram korelasi PM 2.5 dan faktor alam

        with col1:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.scatterplot(data=PRSA_df,
                             x=elemen, 
                             y="PM2.5",
                            facecolor="steelblue")
            ax.set_title(f"Correlation of PM 2.5 and {nature_title[idx]}", fontsize=20)
            st.pyplot(fig)
            corr_value = PRSA_df["PM2.5"].corr(PRSA_df["RAIN"])
            st.write(f"Korelasi antara PM 2.5 dan {nature_title[idx]}: {corr_value}")

        # Membuat diagram korelasi PM 10 dan faktor alam

        with col2:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.scatterplot(data=PRSA_df,
                             x=elemen,
                            y="PM10", facecolor="skyblue")
            ax.set_title(f"Correlation of 10 and {elemen}", fontsize=20)
            st.pyplot(fig)
            corr_value = PRSA_df["PM2.5"].corr(PRSA_df["TEMP"])
            st.write(f"Korelasi antara PM 10 dan {nature_title[idx]}: {corr_value}")

# Membuat peta geospasial

elif page == 'Peta Geospasial':

    st.markdown("## Peta Geospasial")

    station_coordinates = {
    "Aotizhongxin": (34.374734, 109.016205),
    "Changping": (40.219646, 116.225091),
    "Dingling": (40.162427, 117.653096),
    "Dongsi": (39.929247, 116.417731),
    "Guanyuan": (29.558719, 112.007610),
    "Gucheng": (37.349035, 115.964682),
    "Huairou": (40.315481, 116.626028),
    "Nongzhanguan": (39.943720, 116.466225),
    "Shunyi": (40.148750, 116.653875),
    "Tiantan": (39.887858, 116.392896),
    "Wanliu": (39.989313, 116.289428),
    "Wanshouxigong": (39.886500, 116.352400)
    }

    average_PM25_per_station = PRSA_df.groupby("station")["PM2.5"].mean().reset_index()

    df_stations = pd.DataFrame(station_coordinates.items(), columns=["stasiun", "coordinates"])
    df_stations[["lat", "lon"]] = pd.DataFrame(df_stations["coordinates"].tolist(), index=df_stations.index)
    df_stations.drop(columns=["coordinates"], inplace=True)

    # Hitung rata-rata WSPM per stasiun
    average_PM25_per_station = PRSA_df.groupby("station")["PM2.5"].mean().reset_index()
    average_PM25_per_station.rename(columns={"station": "stasiun"}, inplace=True)

    # Gabungkan data koordinat dengan PM2.5
    df_combined = pd.merge(df_stations, average_PM25_per_station, on="stasiun", how="left")

    m = folium.Map(location=[35, 116.4], zoom_start=5.5, tiles="OpenStreetMap")

    for _, row in df_combined.iterrows():
        if row["PM2.5"] < 70:
            color = "green"
        elif row["PM2.5"] < 80:
            color = "orange"
        else:
            color = "red"
        
        # Tambahkan lingkaran (titik)
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['stasiun']}<br>PM2.5: {row['PM2.5']:.2f}"
        ).add_to(m)
        
        # Tambahkan label nama stasiun
        folium.Marker(
            location=[row["lat"] + 0.02, row["lon"]],
            icon=folium.DivIcon(
                icon_size=(150,36),
                icon_anchor=(0,0),
                html=f'<div style="font-size: 11pt; color: black; background: white; padding: 1px; border-radius: 5px; font-weight: bold;">'
                     f'<b>{row["stasiun"]}</b></div>'
            )
        ).add_to(m)
    st_folium(m)
    st.write(
        """
            Terdapat kesamaan level PM 2.5 pada stasiun yang berdekatan. 
            Terlihat untuk stasiun wangliau hingga ke stasiun ayng ada di bagian selatannya memeiliki stastus merah yang artinya kadar PM 2.5 dalam level bahaya.
            Stasiun yang berada di bagian tengah, yaitu stasiun Changping dan Shunyi berstatus oranye yang artinya kadar PM 25 dalam level sedang.
            Stasiun di bagian utara, yaitu stasiun Huariou dan Dingling berada di level aman dan berstatus hijau.
            Dengan demikian, letak geografis dapat menjadi salah satu faktor tingkat polusi suatu wilayah, 
            wilayah yang berdekatan maupun berada di geografis yang searah akan memeiliki potensi polusi yang serupa.
            Hal ini dapat diakibatkan oleh arah angin dikarenakan angin dapat membawa polusi dan menghantarkannya ke daerah dimana angin bergerak.
        """
    )

