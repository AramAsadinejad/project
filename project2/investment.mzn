% portfolio.mzn

% === Indices ===

int: B = 4;                                  % bond-lock queue length (weeks)
set of int: BONDS = 1..B;

% === Data (to be filled in .dzn) ===

float: capital;                              % cash available to spend today
float: spent;                                % cash spent today
array[BONDS] of float: bonds;                % b_{t-3} … b_{t}

float: p_g;                                  % predicted price of gold
float: p_b;                                  % predicted price of bitcoin
float: p_e;                                  % predicted price of ethereum
float: p_bm;                                 % predicted price of bitcoin in margin
float: p_em;                                 % predicted price of ethereum in margin

float: c_g;                                  % current price of gold
float: c_b;                                  % current price of bitcoin
float: c_e;                                  % current price of ethereum


float: r_b = 0.0055;                         % bond yield per 28 days

int: Gmax = 10000;                           % gold granularity (0.01% steps)

% === Decision variables ===

array[1..3] of var float: bit;               % bitcoin units - bit[0]= no margin, bit[1]= margin with leverage 1, bit[2]= margin with leverage 2, bit[3]= margin with leverage 3
array[1..3] of var float: eth;               % ethereum units - eth[0]= no margin, eth[1]= margin with leverage 1, eth[2]= margin with leverage 2, eth[3]= margin with leverage 3
var float: gold;                             % gold units

var 0..Gmax: g;                              % gold in 0.01% increments (integer)
var float: b_new;                            % new bonds purchased today

% === Link gold units to integer granularity ===

constraint
  gold = g / 10000.0;

% === Nonnegativity ===

constraint forall(i in 0..3) (bit[i] >= 0.0);
constraint forall(i in 0..3) (eth[i] >= 0.0);
constraint gold >= 0.0;
constraint b_new >= 0.0;

% === Budget constraint ===

constraint
  (gold) * c_g
+ (bit[0]) * c_b
+ (eth[0]) * c_e
+ (bit[1]) * c_b
+ (eth[1]) * c_e
+ (bit[2]) * c_b * ( 1/2 )
+ (eth[2]) * c_e * ( 1/2 )
+ (bit[3]) * c_b * ( 1/3 )
+ (eth[3]) * c_e * ( 1/3 )
+  b_new
<= capital;

constraint
  (gold) * c_g
+ (bit[0]) * c_b
+ (eth[0]) * c_e
+ (bit[1]) * c_b
+ (eth[1]) * c_e
+ (bit[2]) * c_b * ( 1/2 )
+ (eth[2]) * c_e * ( 1/2 )
+ (bit[3]) * c_b * ( 1/3 )
+ (eth[3]) * c_e * ( 1/3 )
+  b_new
= spent;

constraint
  (bit[2]) * c_b * ( 1/2 )
+ (eth[2]) * c_e * ( 1/2 )
<= ( capital * 1/2 );

constraint
  (bit[3]) * c_b * ( 1/3 )
+ (eth[3]) * c_e * ( 1/3 )
<= ( capital * 1/3 );

% === Objective: maximize next-period value ===

var float: bond_payoffs = sum(k in 1..B-1)( bonds[k] * (1.0 + r_b) );
var float: asset_value  = bit * p_b
                       + eth * p_e
                       + bit * p_bm
                       + eth * p_em
                       + gold * p_g;

solve maximize asset_value + bond_payoffs;
