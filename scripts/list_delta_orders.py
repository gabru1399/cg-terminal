import json

data = json.load(open('C:/Users/SIGMA/.gemini/antigravity/brain/566267b2-a02c-4896-b021-b1e756f57654/.system_generated/steps/32313/output.txt'))
orders = data.get('result', [])
print(f"Total Delta Open Orders: {len(orders)}")
for o in orders:
    print(f"ID: {o.get('id')} | Sym: {o.get('product_symbol'):<8} | Side: {o.get('side'):<4} | Size: {o.get('size')} | Price: {o.get('limit_price')} | SL: {o.get('bracket_stop_loss_price')} | TP: {o.get('bracket_take_profit_price')} | State: {o.get('state')}")
