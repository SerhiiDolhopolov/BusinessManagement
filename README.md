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
  - [Example of Phones Menu](#example-of-phones-menu)
  - [Phone Menu for Admin](#phone-menu-for-admin)
  - [Statistic by Plotly](#statistic-by-plotly)
    - [Statistic Menu and Summary Statistic](#statistic-menu-and-summary-statistic)
    - [Chart of Profit Relative to Phones Sold](#chart-of-profit-relative-to-phones-sold)
    - [Profit/Quantity Graph Relative to Models Sold](#profitquantity-graph-relative-to-models-sold)
    - [Profit/Quantity Graph Relative to Corrected Defects of Sold Models](#profitquantity-graph-relative-to-corrected-defects-of-sold-models)
    - [Revenue/Quantity Graph vs Number of Phones Sold by Users Who Downloaded Them](#revenuequantity-graph-vs-number-of-phones-sold-by-users-who-downloaded-them)
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

## Example of Phones Menu
<div align="center">
  <img src="images/phones_menu.png" alt="Phones menu" width="400">
</div>

## Phone Menu for Admin
<div align="center">
  <img src="images/phone.png" alt="Phone menu" width="400">
</div>

## Statistic by [Plotly](https://plotly.com/)
### Statistic Menu and Summary Statistic
<div align="center">
  <img src="images/statistic1.png" alt="Statistic menu" width="600">
</div>

### Chart of Profit Relative to Phones Sold
<div align="center">
  <img src="images/statistic2.png" alt="Profit chart" width="600">
</div>

### Profit/Quantity Graph Relative to Models Sold
<div align="center">
  <img src="images/statistic3.png" alt="Profit vs models" width="600">
</div>

### Profit/Quantity Graph Relative to Corrected Defects of Sold Models
<div align="center">
  <img src="images/statistic4.png" alt="Profit vs defects" width="600">
</div>

### Revenue/Quantity Graph vs Number of Phones Sold by Users Who Downloaded Them
<div align="center">
  <img src="images/statistic5.png" alt="Revenue vs downloads" width="600">
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