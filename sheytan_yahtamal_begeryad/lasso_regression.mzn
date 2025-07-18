%% ridge_regression.mzn

% Parameters
int: n_samples;
int: n_features;
float: lambda;  % Default regularization strength
array[1..n_samples] of float: y;
array[1..n_samples, 1..n_features] of float: X;

% Decision variables with practical bounds
array[1..n_features] of var -5.0..5.0: weights;
var -100.0..100.0: intercept;

% Linear prediction (identical to your OLS)
array[1..n_samples] of var float: y_pred = 
    [sum(j in 1..n_features)(X[i,j] * weights[j]) + intercept | i in 1..n_samples];

% --- KEY DIFFERENCE: Linear approximation of L2 regularization ---
% Absolute values for weights (L1-like penalty)
array[1..n_features] of var float: abs_weights = 
    [abs(weights[j]) | j in 1..n_features];

% Hybrid objective: MAE + L1-approximated L2 penalty
var float: total_loss = 
    sum([abs(y_pred[i] - y[i]) | i in 1..n_samples]) +  % MAE term
    lambda * sum(abs_weights);                          % Regularization

% Solve statement
solve minimize total_loss;

% Output
output [
    "Weights: [", join(", ", [show_float(6,4,weights[j]) | j in 1..n_features]), "]",
    "\nIntercept: ", show_float(6,4,intercept),
    "\nMAE: ", show_float(6,4, sum([abs(y_pred[i] - y[i]) | i in 1..n_samples])/n_samples),
    "\nRegularization term: ", show_float(6,4, sum(abs_weights))
];