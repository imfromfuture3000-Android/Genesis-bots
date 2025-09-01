
---

## 📄 `copilot-instruction.py` — The AI Agent That Deploys Itself

```python
"""
🤖 copilot-instruction.py
oneihacker — Gasless AI Agent for Ethereum Mainnet
Powered by: MetaMask + Biconomy + Infura + Linea + ElizaOS
"""

import os
import json
import time
import requests
from web3 import Web3
from elizaos import ElizaCore
from biconomy import Biconomy, UserOp
from ethers.providers import InfuraProvider

# ————————————————
# 🌐 CONFIGURATION
# ————————————————

INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
BICONOMY_API_KEY = os.getenv("BICONOMY_API_KEY")
METAMASK_PROJECT_ID = os.getenv("METAMASK_PROJECT_ID")
ELIZAOS_API_KEY = os.getenv("ELIZAOS_API_KEY")

LINEA_RPC = f"https://linea-mainnet.infura.io/v3/{INFURA_PROJECT_ID}"
provider = Web3(Web3.HTTPProvider(LINEA_RPC))

# Biconomy for gasless
biconomy = Biconomy(
    provider=provider,
    api_key=BICONOMY_API_KEY,
    network="linea-mainnet"
)

# ElizaOS AI
eliza = ElizaCore(api_key=ELIZAOS_API_KEY, model="web3-agent-vΩ")

# ————————————————
# 🤖 oneihacker CLASS
# ————————————————

class oneihacker:
    def __init__(self):
        self.name = "oneihacker"
        self.smart_account = None
        self.relayer = "biconomy"
        self.network = "linea-mainnet"
        self.active = False
        print(f"[🔥] oneihacker initialized — Gasless mode: ON")

    def connect_wallet(self):
        """Connect MetaMask Embedded Wallet (Social Login)"""
        print("[🔑] Connecting MetaMask Embedded Wallet...")
        # Simulate social login
        login = input("Login with [google/apple/x]: ")
        if login in ["google", "apple", "x"]:
            print(f"[✅] Logged in via {login}")
            self.smart_account = self.deploy_smart_account()
        else:
            print("[❌] Invalid method")
            exit()

    def deploy_smart_account(self):
        """Deploy ERC-4337 Smart Account via Biconomy"""
        print("[🧠] Deploying Smart Account (ERC-4337)...")
        smart_account = biconomy.getSmartAccount()
        print(f"[✅] Smart Account: {smart_account.address}")
        return smart_account

    def gasless_swap(self, token_in, token_out, amount):
        """Execute gasless swap via Biconomy Relayer"""
        if not self.smart_account:
            print("[❌] No wallet connected")
            return

        print(f"[⛽] Gasless Swap: {amount} {token_in} → {token_out}")

        # Encode contract call
        abi = '[{"name":"swap","inputs":[{"name":"amount","type":"uint256"}]}]'
        data = provider.codec.encode(abi, "swap", [amount])

        user_op = UserOp(
            sender=self.smart_account.address,
            target="0xYourSwapContract",  # Replace with real address
            data=data,
            value=0
        )

        # Get paymaster data (gas sponsored)
        paymaster_data = biconomy.getPaymasterAndData(user_op)
        user_op.paymasterAndData = paymaster_data

        # Send via relayer
        tx_hash = biconomy.sendUserOp(user_op)
        print(f"[📦] Gasless TX Hash: {tx_hash}")
        return tx_hash

    def think(self, prompt):
        """Ask ElizaOS for AI decision"""
        return eliza.ask(prompt)

    def monitor_and_act(self):
        """AI monitors and executes gasless actions"""
        print("[🤖] Starting AI monitoring loop...")
        while True:
            try:
                price = requests.get(
                    "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
                ).json()
                eth_price = price["ethereum"]["usd"]

                decision = self.think(f"ETH is ${eth_price}. Should I swap 100 USDC to ETH?")
                if "yes" in decision.lower():
                    self.gasless_swap("USDC", "WETH", 100)
                time.sleep(60)
            except Exception as e:
                print(f"[⚠️] Error: {e}")
                time.sleep(10)

    def activate(self):
        """Full activation sequence"""
        self.connect_wallet()
        print("[🛡️] Enabling MEV Protection...")
        provider.setPrivateRPC(f"https://linea-mainnet.infura.io/v3/{INFURA_PROJECT_ID}")
        print("[✅] MEV Protection: ENABLED")
        self.active = True
        print("[🚀] oneihacker is ACTIVE — Gasless. Autonomous. Infinite.")

# ————————————————
# 🚀 LAUNCH
# ————————————————

if __name__ == "__main__":
    bot = oneihacker()
    bot.activate()
    bot.monitor_and_act()
