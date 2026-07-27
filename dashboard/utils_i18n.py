import streamlit as st

def init_translation():
    """Initializes the localized dictionary selection controls in the Streamlit sidebar."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "EN"
        
    st.sidebar.markdown("---")
    st.sidebar.subheader("Language / Bahasa")
    lang = st.sidebar.radio(
        "Select Language / Pilih Bahasa:", 
        ["English", "Bahasa Indonesia"], 
        index=0 if st.session_state["lang"] == "EN" else 1
    )
    st.session_state["lang"] = "EN" if lang == "English" else "ID"

def fmt_rp(value):
    """Formats numeric value as Indonesian Rupiah."""
    if value >= 1e9: return f"Rp {value/1e9:.2f} B"
    elif value >= 1e6: return f"Rp {value/1e6:.2f} M"
    else: return f"Rp {value:,.0f}"

# Localization lookup dictionary
T = {
    "EN": {
        # Home
        "home_title": "[Chart] SwiftHub Super App: Executive Home",
        "home_welcome": "Welcome to the Diamond Data Platform",
        "home_desc": "This portal visualizes the **SwiftHub Data Ecosystem**, an Indonesian Super App simulating millions of transactions across logistics, food, and finances.",
        "home_stack": "[Stack] Architecture Stack",
        "home_nav": "[Nav] Navigation Guide",
        "home_nav_desc": "Use the sidebar to explore detailed analytics:\n1. **01_Executive_Overview**: High-level KPIs and business health.\n2. **02_Geospatial_Intelligence**: Heatmaps of Indonesian city hubs.\n3. **03_Fleet_Operations**: RideWay and ParcelPro logistics performance.\n4. **04_Data_SLA**: Contract validation compliance monitoring.",
        "system_status": "[Status] System Connectivity Status",
        "batch_lake": "Batch Data Lake",
        "dbt_warehouse": "dbt Analytical Warehouse",
        "last_refresh": "Last Data Refresh",
        "today": "Today",
        "online": "[OK] ONLINE",
        "offline": "[ERR] OFFLINE",
        "active": "[OK] ACTIVE",
        "pending": "[OK] PENDING",
        
        # Executive Overview
        "exec_title": "[Chart] Executive Overview",
        "exec_subtitle": "Aggregated Real-Time Intelligence from the dbt Analytical Warehouse.",
        "total_revenue": "Total Revenue",
        "transactions": "Transactions",
        "active_users": "Active Users",
        "avg_order": "Avg Order Value",
        "revenue_trend": "[Calendar] Gross Revenue Trend",
        
        # Geospatial
        "geo_title": "[Globe] Geospatial Hub Intelligence",
        "geo_subtitle": "Mapping service density across metropolitan city hubs in Indonesia.",
        "select_city": "Select Hub City to Filter",
        "all_cities": "All Cities",
        "demand_dist": "[BarChart] Demand Distribution",
        "city_hub": "City Hub",
        "request_count": "Request Count",
        "total_in_view": "Total Requests in View",
        "avg_lat": "Average Latitude",
        "avg_lon": "Average Longitude",
        "hotspot": "[Volcano] Hotspot Analysis (Interactive Map)",
        "pro_tip": "[Lightbulb] Pro-Tip: Double click on map categories to isolate specific hubs. You can drag and zoom to analyze district level density.",
        
        # Fleet
        "fleet_title": "[Tractor] Fleet & Logistics Operations",
        "fleet_subtitle": "Analyzing ride-sharing and logistics fulfillment metrics, capacity distribution, and driver performance.",
        "fleet_size": "Active Fleet Size",
        "fleet_rating": "Average Fleet Rating",
        "fulfillment_sla": "Fulfillment SLA",
        "fleet_comp": "[Donut] Fleet Composition",
        "driver_perf": "[Star] Driver Performance Distribution",
        "city_density": "[Building] Logistical Request Density by City Hub",
        "drivers": "Drivers",
        
        # SLA
        "sla_title": "[Shield] Data Contract SLA & Quality Center",
        "sla_subtitle": "Monitor historical validation accuracy rates and SLA compliance levels across ingestion batches.",
        "rolling_sla": "ROLLING PLATFORM SLA",
        "total_runs": "TOTAL PIPELINE RUNS",
        "passed": "PASSED CONTRACTS",
        "failed": "FAILED CONTRACTS",
        "sla_trend": "[Trendline] SLA Compliance Trend (Target: 99.5%)",
        "sla_chart_title": "Ingestion Validation Pass Rate",
        "exec_time": "Execution Time",
        "pass_rate": "Pass Rate (%)",
        "job_history": "[History] Ingestion Job History Log",
        "no_history": "No historical SLA validation runs found. Run data generation to capture metrics.",
    },
    "ID": {
        # Home
        "home_title": "[Chart] SwiftHub Super App: Beranda Eksekutif",
        "home_welcome": "Selamat Datang di Platform Data Diamond",
        "home_desc": "Portal ini memvisualisasikan **Ekosistem Data SwiftHub**, sebuah Super App Indonesia yang mensimulasikan jutaan transaksi di bidang logistik, makanan, dan keuangan.",
        "home_stack": "[Stack] Tumpukan Arsitektur",
        "home_nav": "[Nav] Panduan Navigasi",
        "home_nav_desc": "Gunakan bilah sisi untuk menjelajahi analitik detail:\n1. **01_Executive_Overview**: KPI tingkat tinggi dan kesehatan bisnis.\n2. **02_Geospatial_Intelligence**: Peta panas hub kota Indonesia.\n3. **03_Fleet_Operations**: Kinerja logistik RideWay dan ParcelPro.\n4. **04_Data_SLA**: Pemantauan kepatuhan validasi kontrak data.",
        "system_status": "[Status] Status Konektivitas Sistem",
        "batch_lake": "Data Lake Batch",
        "dbt_warehouse": "Gudang Analitik dbt",
        "last_refresh": "Pembaruan Data Terakhir",
        "today": "Hari Ini",
        "online": "[OK] ONLINE",
        "offline": "[ERR] OFFLINE",
        "active": "[OK] AKTIF",
        "pending": "[OK] TERTUNDA",
        
        # Executive Overview
        "exec_title": "[Chart] Ringkasan Eksekutif",
        "exec_subtitle": "Intelijen Real-Time Teragregasi dari Gudang Analitik dbt.",
        "total_revenue": "Total Pendapatan",
        "transactions": "Transaksi",
        "active_users": "Pengguna Aktif",
        "avg_order": "Nilai Pesanan Rata-rata",
        "revenue_trend": "[Calendar] Tren Pendapatan Kotor",
        
        # Geospatial
        "geo_title": "[Globe] Intelijen Hub Geospasial",
        "geo_subtitle": "Memetakan densitas layanan di hub kota metropolitan Indonesia.",
        "select_city": "Pilih Kota Hub untuk Filter",
        "all_cities": "Semua Kota",
        "demand_dist": "[BarChart] Distribusi Permintaan",
        "city_hub": "Hub Kota",
        "request_count": "Jumlah Permintaan",
        "total_in_view": "Total Permintaan dalam Tampilan",
        "avg_lat": "Rata-rata Lintang",
        "avg_lon": "Rata-rata Bujur",
        "hotspot": "[Volcano] Analisis Titik Panas (Peta Interaktif)",
        "pro_tip": "[Lightbulb] Tips Pro: Klik dua kali pada kategori peta untuk mengisolasi hub tertentu. Anda dapat menarik dan memperbesar untuk menganalisis densitas tingkat distrik.",
        
        # Fleet
        "fleet_title": "[Tractor] Operasi Armada & Logistik",
        "fleet_subtitle": "Menganalisis metrik pemenuhan ride-sharing dan logistik, distribusi kapasitas, dan kinerja pengemudi.",
        "fleet_size": "Ukuran Armada Aktif",
        "fleet_rating": "Rating Armada Rata-rata",
        "fulfillment_sla": "SLA Pemenuhan",
        "fleet_comp": "[Donut] Komposisi Armada",
        "driver_perf": "[Star] Distribusi Kinerja Pengemudi",
        "city_density": "[Building] Densitas Permintaan Logistik per Hub Kota",
        "drivers": "Pengemudi",
        
        # SLA
        "sla_title": "[Shield] Pusat Kualitas & SLA Kontrak Data",
        "sla_subtitle": "Pantau tingkat akurasi validasi historis dan tingkat kepatuhan SLA di seluruh batch ingesti.",
        "rolling_sla": "SLA PLATFORM BERGULIR",
        "total_runs": "TOTAL EKSEKUSI PIPELINE",
        "passed": "KONTRAK LULUS",
        "failed": "KONTRAK GAGAL",
        "sla_trend": "[Trendline] Tren Kepatuhan SLA (Target: 99.5%)",
        "sla_chart_title": "Tingkat Kelulusan Validasi Ingesti",
        "exec_time": "Waktu Eksekusi",
        "pass_rate": "Tingkat Kelulusan (%)",
        "job_history": "[History] Log Riwayat Pekerjaan Ingesti",
        "no_history": "Tidak ada riwayat validasi SLA. Jalankan generasi data untuk menangkap metrik.",
    }
}
