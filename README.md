<table align="center">
  <tr>
    <td align="center">
        <img src="https://img.shields.io/badge/python-3.13-d6123c?color=white&labelColor=d6123c&logo=python&logoColor=white" alt="python">
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/HTML-d6123c?color=white&labelColor=d6123c&logo=html5&logoColor=white" alt="HTML">
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/CSS-d6123c?color=white&labelColor=d6123c&logo=css3&logoColor=white" alt="CSS">
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/JavaScript-d6123c?color=white&labelColor=d6123c&logo=javascript&logoColor=white" alt="JavaScript">
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/SQL-d6123c?style=flat&color=white&labelColor=d6123c&logo=database&logoColor=white" alt="SQL">
    </td>
  </tr>
  <tr>
  <td colspan="5" align="center">
    <table>
      <tr>
        <td align="center">
          <img src="https://img.shields.io/badge/aiogram-3.17.0-d6123c?color=white&labelColor=d6123c" alt="aiogram">
        </td>
        <td align="center">
          <img src="https://img.shields.io/badge/pandas-2.2.3-d6123c?color=white&labelColor=d6123c" alt="pandas">
        </td>
        <td align="center">
          <img src="https://img.shields.io/badge/plotly-5.24.1-d6123c?color=white&labelColor=d6123c" alt="plotly">
        </td>
      </tr>
    </table>
  </td>
</tr>
  <tr>
    <td colspan="5" align="center">
      <img src="https://img.shields.io/badge/SQLite-Database-d6123c?style=flat&logo=sqlite&logoColor=white&labelColor=d6123c&color=white" alt="SQLite">
    </td>
  </tr>
</table>

---

## Table of Contents

- [Introduction](#introduction)
- [Screenshots](#screenshots)
  - [Menu panels by role](#menu-panels-by-role)
  - [Example of phones menu](#example-of-phones-menu)
  - [Phone menu for admin](#phone-menu-for-admin)
  - [Statistic by Plotly](#statistic-by-plotly)
    - [Statistic menu and summary statistic](#statistic-menu-and-summary-statistic)
    - [Chart of profit relative to phones sold](#chart-of-profit-relative-to-phones-sold)
    - [Profit/quantity graph relative to models sold](#profitquantity-graph-relative-to-models-sold)
    - [Profit/quantity graph relative to corrected defects of sold models](#profitquantity-graph-relative-to-corrected-defects-of-sold-models)
    - [Revenue/quantity graph vs number of phone sold by users who downloaded them](#revenuequantity-graph-vs-number-of-phone-sold-by-users-who-downloaded-them)
- [To start the project](#to-start-the-project)

# Introduction

This project is a commercial CRM system implemented as a Telegram Bot, designed to streamline the management of processes involved in buying used phones, repairing them, and selling them. The system leverages auto-generated statistics with interactive diagrams powered by [Plotly](https://plotly.com/) for enhanced data visualization.

The project was created when I started learning Python. It uses plain SQL as well, without an ORM.

# Screenshots
## Menu panels by role
<table>
  <tr>
    <td align="center">
      <img src="images/user_panel.png" alt="User panel" width="250">
      <p>User panel</p>
    </td>
    <td align="center">
      <img src="images/courier_panel.png" alt="Courier panel" width="250">
      <p>Courier panel</p>
    </td>
    <td align="center">
      <img src="images/manager_panel.png" alt="Manager panel" width="250">
      <p>Manager panel</p>
    </td>
    <td align="center">
      <img src="images/admin_panel.png" alt="Admin panel" width="250">
      <p>Admin panel</p>
    </td>
  </tr>
</table>

## Example of phones menu
<div align="center">
  <img src="images/phones_menu.png" alt="Phones menu" width="400">
</div>

## Phone menu for admin
<div align="center">
  <img src="images/phone.png" alt="Phone menu" width="400">
</div>

## Statistic by [Plotly](https://plotly.com/)
### Statistic menu and summary statistic
<div align="center">
  <img src="images/statistic1.png" alt="Statistic" width="600">
</div>

### Chart of profit relative to phones sold
<div align="center">
  <img src="images/statistic2.png" alt="Statistic" width="600">
</div>

### Profit/quantity graph relative to models sold
<div align="center">
  <img src="images/statistic3.png" alt="Statistic" width="600">
</div>

### Profit/quantity graph relative to corrected defects of sold models
<div align="center">
  <img src="images/statistic4.png" alt="Statistic" width="600">
</div>

### Revenue/quantity graph vs number of phone sold by users who downloaded them
<div align="center">
  <img src="images/statistic5.png" alt="Statistic" width="600">
</div>

# To start the project
1. **Rename** `.env example` to `.env` and set your variables.
2. **Install dependencies** (if not yet):
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the bot:**
   ```sh
   python main.py
   ```