# MT5 Bulk TP/SL Setter

A simple Python tool to **apply TP and SL to all open trades** in your MetaTrader 5 account in bulk.

---

## 📦 Features

- Connects to MetaTrader 5 using the official `MetaTrader5` Python API.
- Lists all current open trades.
- Lets you enter **target TP/SL in price format** (not pips).
- Automatically applies TP and SL to each position.


---

## 🚀 Requirements

- MetaTrader 5
- Python
- MT5 must have "Algo Trading" enabled

Install dependencies:

```bash
pip install MetaTrader5
```

---

## ▶️ How to Use

1. Open your MT5 terminal and make sure trades are active.
2. Run the script:

```bash
python bulk_tp_sl_setter.py
```

3. You'll see all your open trades listed.
4. Enter **TP and SL as prices** (e.g., `TP = 3285.00`, `SL = 3296.00`). Use `0` to skip either field.
5. Script applies the values to all trades.

---

## ❗ Troubleshooting

- **Algo Trading Disabled**  
  If you see:
  ```
  RetCode: 10027 | AutoTrading disabled by client
  ```
  Go to MetaTrader 5 and enable `Algo Trading`.

- **No Trades**  
  The script only works with open positions.

---

## 📬 Contact

Have suggestions or issues? Reach out on Telegram: [@Haise](https://t.me/hazyx7)
