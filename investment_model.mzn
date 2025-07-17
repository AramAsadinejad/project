
% ================================
% Investment Optimization Model
% ================================

% ---------- Parameters ----------
float: gold_return;
float: crypto_spot_return;
float: crypto_margin_return;
float: bond_return;

% ---------- Decision Variables ----------
var 0..100: gold_percent;  % Only integer percentages allowed for gold
var 0.0..1.0: crypto_spot_fraction;
var 0.0..1.0: crypto_margin_fraction;
var 1..3: leverage;
var 0.0..1.0: bond_fraction;

% ---------- Constraints ----------
% Total investment must not exceed 100%
constraint
    (gold_percent / 100.0) + crypto_spot_fraction + crypto_margin_fraction + bond_fraction <= 1.0;

% If margin used, leverage must be >= 2
constraint
    (crypto_margin_fraction > 0.0 -> leverage >= 2);

% ---------- Objective Function ----------
solve maximize
    (gold_percent / 100.0) * gold_return +
    crypto_spot_fraction * crypto_spot_return +
    crypto_margin_fraction * crypto_margin_return * leverage +
    bond_fraction * bond_return;
