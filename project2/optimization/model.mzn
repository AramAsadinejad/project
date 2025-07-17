int: weeks;
float: initial_capital;
array[1..weeks] of float: gold_price;
array[1..weeks] of float: bitcoin_price;
array[1..weeks] of float: eth_price;
float: weekly_bond_return;

% وضعیت بازار طلا در هر هفته (1: فعال، 0: تعطیل)
array[1..weeks] of int: gold_market_open;

% -----------------------------
% متغیرهای تصمیم‌گیری
% -----------------------------
array[1..weeks] of var 0.0..100.0: gold_percent;
array[1..weeks] of var 0.0..100.0: btc_percent;
array[1..weeks] of var 0.0..100.0: eth_percent;
array[1..weeks] of var 0.0..100.0: bond_percent;

% -----------------------------
% محدودیت‌ها
% -----------------------------
constraint forall(w in 1..weeks) (
  gold_percent[w] + btc_percent[w] + eth_percent[w] + bond_percent[w] <= 100.0
);

% فقط در هفته‌هایی که بازار طلا باز است، اجازه خرید طلا داریم
constraint forall(w in 1..weeks) (
  gold_market_open[w] = 1 <-> gold_percent[w] > 0.0
);

% درصد سرمایه‌گذاری روی طلا باید عدد صحیح باشد
constraint forall(w in 1..weeks) (
  gold_percent[w] = round(gold_percent[w])
);

% BTC و ETH فقط در هفته اول خریده می‌شوند و تا هفته آخر نگه داشته می‌شوند
constraint forall(w in 2..weeks-1) (
  btc_percent[w] = btc_percent[1] /\ eth_percent[w] = eth_percent[1]
);

% Bonds فقط در هفته اول خریداری می‌شوند و برای کل دوره نگه داشته می‌شوند
constraint forall(w in 2..weeks) (
  bond_percent[w] = bond_percent[1]
);

% -----------------------------
% محاسبه سرمایه نهایی
% -----------------------------
var float: final_gold_value =
  sum(w in 1..weeks)(gold_percent[w] * gold_price[w]);
var float: final_btc_value = btc_percent[1] * bitcoin_price[weeks];
var float: final_eth_value = eth_percent[1] * eth_price[weeks];
var float: final_bond_value = bond_percent[1] * initial_capital * pow(1.0 + weekly_bond_return, weeks);

var float: final_value = (final_gold_value + final_btc_value + final_eth_value + final_bond_value) / 100.0;

solve maximize final_value;
