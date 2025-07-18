% portfolio.mzn

% === Indices ===
int: A = 3;                      % 1=BTC, 2=ETH, 3=Gold
set of int: ASSETS = 1..A;

int: B = 4;                      % bond-lock queue length (weeks)
set of int: BONDS = 1..B;

% === Data (to be filled in .dzn) ===
float: capital;                              % cash available today (incl. matured bond)
array[ASSETS] of float: price_t;             % today’s prices p^t[i]
array[ASSETS] of float: price_pred;          % forecasts p^{t+1}[i]
array[ASSETS] of float: prev_h;              % current holdings h^t[i]
array[BONDS] of float: bonds;                % b_{t-3} … b_{t}

float: r_b = 0.0055;                         % bond yield per 28 days

int: Gmax = 10000;                           % gold granularity (0.01% steps)

% === Decision variables ===
array[1..2] of var float: x;    % x[1]=BTC units, x[2]=ETH units
var float: x3;                  % gold units
var 0..Gmax: g;                 % gold in 0.01% increments (integer)
var float: b_new;               % new bonds purchased today

% === Link gold units to integer granularity ===
constraint
  x3 = g / 10000.0;

% === Nonnegativity ===
constraint forall(i in 1..2) (x[i] >= 0.0);
constraint x3 >= 0.0;
constraint b_new >= 0.0;

% === Budget constraint ===
constraint
  (x[1] - prev_h[1]) * price_t[1]
+ (x[2] - prev_h[2]) * price_t[2]
+ (x3    - prev_h[3]) * price_t[3]
+  b_new
<= capital;

% === Objective: maximize next-period value ===
var float: bond_payoffs = sum(k in 1..B-1)( bonds[k] * (1.0 + r_b) );
var float: asset_value  = x[1]*price_pred[1]
                       + x[2]*price_pred[2]
                       + x3*   price_pred[3];

solve maximize asset_value + bond_payoffs;
