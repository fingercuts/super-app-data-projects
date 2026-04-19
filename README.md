# SwiftHub Super App - Anonymized Dataset for Analytics

An anonymized, high-volume dataset from **SwiftHub**, a multi-service *super app* operating in Indonesia.  
This dataset is designed for **data engineering pipelines**, **business intelligence dashboards**, and **machine learning experiments**, providing a realistic view of super app operations while adhering to strict NDA and privacy standards.

---

## 🚀 Project Status

This repository contains the **initial V1.0 release** of the SwiftHub dataset.  
Future updates will focus on:
- Adding more complex data scenarios
- Providing pre-built analytics examples and starter notebooks

---

## 📈 Key Features of the Dataset

- **Large-Scale** → Millions of records across multiple interconnected tables, reflecting extensive real-world operations.  
- **Realistic & Dynamic** → Transaction volumes mirror seasonal trends, with peaks during major Indonesian holidays (Lebaran, Harbolnas, and recurring "Double Date" shopping events).  
- **Geographically Representative** → User, driver, and merchant distributions reflect Indonesia’s population density, with hubs in **Java and Bali**.  
- **Comprehensive Schema** → Covers all core aspects of a super app: users, drivers, merchants, services, promotions, transactions, payments, and fulfillment locations.  
- **NDA Compliant & Anonymized** → All sensitive details (names, IDs, services, company references) replaced with **consistent fictional aliases**.

---

## 🏢 The SwiftHub Business Model

SwiftHub operates as a **single company** with multiple specialized departments offering digital and on-demand services across Indonesia.

```text
+--------------+---------------------------+-------------------------------------------+
| Department   | Category                  | Services Offered                          |
+--------------+---------------------------+-------------------------------------------+
| RideWay      | Transport / Ride-hailing  | RideWay Go, RideWay Car, RideWay Lux      |
| Foodora      | Food Delivery             | Foodora Express, Foodora Feast            |
| QuickMart    | Grocery Delivery          | QuickMart Essentials, QuickMart Fresh     |
| ParcelPro    | Courier / Logistics       | ParcelPro Express, ParcelPro Standard     |
| PayLink      | Digital Payments / Wallet | PayLink Wallet, PayLink PayLater          |
| LifeConnect  | Lifestyle / E-commerce    | LifeConnect Travel, LifeConnect Shopping  |
+--------------+---------------------------+-------------------------------------------+
```

---

## 🚀 Getting Started

1. **Download the Data** → Go to the [Releases](../../releases) tab and download the latest release (`swifthub_data.zip`).  
2. **Unzip the File** → Extract to access all `.csv` files.  
3. **Load & Analyze** → Use your preferred tools (**Pandas, R, SQL, Tableau, Power BI, etc.**) to explore and build analytics.

---

## 📊 Data Schema

The dataset includes the following CSVs. Each CSV section below shows the field names and short descriptions as an ASCII boxed table (copy-paste safe).

**users.csv**

```text
+---------+-----------------------------------------+
| Field   | Description                             |
+---------+-----------------------------------------+
| user_id | Unique identifier for the user          |
| name    | Anonymized user's full name             |
| gender  | User's gender                           |
| age     | User's age                              |
| city    | User's city of residence                |
| region  | User's region / province                |
+---------+-----------------------------------------+
```

**drivers.csv**

```text
+-------------+----------------------------------------+
| Field       | Description                            |
+-------------+----------------------------------------+
| driver_id   | Unique identifier for the driver       |
| name        | Anonymized driver's full name          |
| gender      | Driver's gender                        |
| age         | Driver's age                           |
| city        | Driver's city of operation             |
| vehicle_type| Vehicle type (Motorcycle or Car)       |
| rating      | Driver's average rating (1.0 - 5.0)    |
+-------------+----------------------------------------+
```

**merchants.csv**

```text
+---------------+---------------------------------------------+
| Field         | Description                                 |
+---------------+---------------------------------------------+
| merchant_id   | Unique identifier for the merchant          |
| merchant_name | Anonymized merchant/store name              |
| service_type  | General category (e.g., Food Delivery)      |
| department    | SwiftHub department the merchant belongs to |
| city          | Merchant's city of operation                |
| rating        | Merchant's average rating (1.0 - 5.0)       |
+---------------+---------------------------------------------+
```

**services.csv**

```text
+--------------+-----------------------------------------+
| Field        | Description                             |
+--------------+-----------------------------------------+
| service_id   | Unique identifier for the service       |
| service_name | Specific service name (e.g., RideWay Go)|
| category     | Service sub-category                    |
| department   | Department offering the service         |
+--------------+-----------------------------------------+
```

**promotions.csv**

```text
+---------------------+-------------------------------------------+
| Field               | Description                               |
+---------------------+-------------------------------------------+
| promotion_id        | Unique identifier                         |
| promotion_name      | Campaign name (e.g., Harbolnas 11.11 2024)|
| campaign_type       | Seasonal, Monthly, etc.                   |
| discount_percentage | Discount as decimal (e.g., 0.15)          |
| start_date          | Promotion start date (ISO format)         |
| end_date            | Promotion end date (ISO format)           |
+---------------------+-------------------------------------------+
```

**transactions.csv**

```text
+-------------------+-------------------------------------------------+
| Field             | Description                                     |
+-------------------+-------------------------------------------------+
| transaction_id    | Unique identifier for the transaction           |
| date              | Transaction timestamp (ISO datetime)            |
| user_id           | FK → users.csv                                  |
| driver_id         | FK → drivers.csv (nullable for non-ride orders) |
| merchant_id       | FK → merchants.csv (nullable if not applicable) |
| service_id        | FK → services.csv                               |
| quantity          | Quantity (e.g., item count)                     |
| base_amount       | Original price before discounts                 |
| discounted_amount | Amount discounted by promotions                 |
| total_amount      | Final amount charged to the user                |
| payment_method    | Payment method used (e.g., PayLink Wallet)      |
| department        | SwiftHub department handling the service        |
| city              | City where the transaction occurred             |
| region            | Region/province of the transaction              |
| promotion_id      | FK → promotions.csv (nullable)                  |
+-------------------+-------------------------------------------------+
```

Plus two related CSVs: `payments.csv` and `locations.csv` (see the dataset release for full columns and examples).

---

## 🗺️ Project Roadmap

- [ ] **Advanced Pricing Models**
  - Add surge pricing for RideWay during peak hours
  - Tiered pricing for Foodora & QuickMart

- [ ] **Data Quality Scenarios**
  - Release dataset version with intentional data-quality issues for cleaning practice

- [ ] **Advanced User Behavior Metrics**
  - Add loyalty tiers, churn signals, and richer purchase-pattern fields

- [ ] **Analytics Starter Kits**
  - Provide sample notebooks (customer segmentation, promo effectiveness)
  - Starter BI dashboards for Tableau & Power BI

---

## 🙌 How to Contribute

Contributions are welcome!
- Open an **Issue** for bugs, dataset requests, or feature ideas
- Submit a **Pull Request** for fixes, new scenario data, or starter notebooks
- For sensitive or large changes (new heavy dataset files), please open an issue first to discuss

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## ℹ️ Short Repo Description (for GitHub "description" field)

`📊 An anonymized, large-scale dataset simulating SwiftHub — a multi-service super app in Indonesia. Ideal for ETL, BI dashboards, and ML experiments.`

