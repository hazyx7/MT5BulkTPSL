import MetaTrader5 as mt5
import time
import os

# Console setup
os.system("chcp 65001 >nul")
os.system("title MT5 Bulk TP/SL Setter")

# ──────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    print("╔══════════════════════════════════════════════╗")
    print("║         MT5 Bulk TP/SL Setter v1.0          ║")
    print("╚══════════════════════════════════════════════╝\n")

def get_open_positions():
    positions = mt5.positions_get()
    if positions is None or len(positions) == 0:
        print("No open positions found.")
        input("Press Enter to exit...")
        exit()
    return positions

def show_positions(positions):
    print(f"Found {len(positions)} open trade(s):\n")
    for i, pos in enumerate(positions, start=1):
        direction = "BUY " if pos.type == mt5.ORDER_TYPE_BUY else "SELL"
        print(f" {i}. {pos.symbol} | {direction} | Volume: {pos.volume:.2f} | Open: {pos.price_open:.5f} | TP: {pos.tp:.5f} | SL: {pos.sl:.5f}")
    print()

def get_tp_sl():
    try:
        tp = float(input("TP Price (0 to skip): "))
        sl = float(input("SL Price (0 to skip): "))
        tp = None if tp == 0 else tp
        sl = None if sl == 0 else sl
        return tp, sl
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return get_tp_sl()

def apply_tp_sl(tp, sl, positions):
    print("\nApplying TP/SL to all positions...\n")
    time.sleep(0.5)
    for pos in positions:
        already_tp = (tp is None or abs(pos.tp - tp) < 0.00001)
        already_sl = (sl is None or abs(pos.sl - sl) < 0.00001)

        if already_tp and already_sl:
            print(f"{pos.symbol} → Already Set.")
            continue

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": pos.ticket,
            "tp": tp,
            "sl": sl,
            "symbol": pos.symbol,
            "magic": 234000,
            "comment": "Bulk TP/SL Setter",
        }

        result = mt5.order_send(request)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"{pos.symbol} → Updated.")
        elif result.retcode == 10027:
            print("\nAutoTrading is disabled in MT5.")
            input("Enable AutoTrading and press Enter to retry...")
            return apply_tp_sl(tp, sl, positions)
        elif result.retcode == 10025 and already_tp and already_sl:
            print(f"{pos.symbol} → Already Set.")
        else:
            print(f"✗ {pos.symbol} FAILED | RetCode: {result.retcode}")

        time.sleep(0.2)

    print("\n╔══════════════════════════════╗")
    print("║        UPDATE COMPLETE       ║")
    print("╚══════════════════════════════╝")

# ──────────────────────────────────────────────────────────
# Main Flow
# ──────────────────────────────────────────────────────────

def main():
    clear()
    display_header()

    if not mt5.initialize():
        print("Failed to connect to MetaTrader 5.")
        print(f"Error: {mt5.last_error()}")
        input("Press Enter to exit...")
        return

    positions = get_open_positions()
    show_positions(positions)
    tp, sl = get_tp_sl()
    apply_tp_sl(tp, sl, positions)

    mt5.shutdown()
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
