clear;

//Conditions initiales

x0 =zeros(16,1)
//x0 = [3;2;1;5; 6;4;8;2; 7;3;4;5; 1;0;4;3]
x0(1,1)=1
A=[0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0; -2 0 -2 0 1 0 1 0 1 0 1 0 0 0 0 0; 0 -2 0 -2 0 1 0 1 0 1 0 1 0 0 0 0; 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0;  0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0; 1 0 1 0 -1 0 -1 0 0 0 0 0 0 0 0 0; 0 1 0 1 0 -1 0 -1 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0; 1 0 1 0 0 0 0 0 -2 0 -2 0 1 0 1 0; 0 1 0 1 0 0 0 0 0 -2 0 -2 0 1 0 1; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1; 0 0 0 0 0 0 0 0 1 0 1 0 -1 0 -1 0; 0 0 0 0 0 0 0 0 0 1 0 1 0 -1 0 -1]

//fonction d'euler

function rep = phi_alpha(Y, alpha)
    n = size(Y)
    rep = zeros(n(1))
    for i=1:n(1)
        if modulo(i, 4)==3 | modulo(i, 4)==0 then
            rep(i) = sign(Y(i))*abs(Y(i)^alpha)
        else
            rep(i) = Y(i)
        end
    end
endfunction

function [X] = euler(X0,A, step_rate, T, alpha)
    t=0
    h=step_rate
    N = T/h
    Y = zeros(16, N)
    Z=x0
    n = 1
    while t<=T
        Z=Z+h*phi_alpha(A*Z, alpha)
        t=t+h
        Y(:, n) = Z
        n = n+1
    end
    X=Y
endfunction

h = 1
T = 5
alpha = 1
X=euler(x0,A, h, T, alpha)
//on trace les graphes

//premier graphe: convergence de la position selon la première variable


for k=1:T/h
    plot(k*h, X(3, k), 'r*')
    plot(k*h, X(7, k), 'b*')
    plot(k*h, X(11, k), 'g*')
    plot(k*h, X(15, k), 'm*')
end

/*
for k=1:T/h
    plot(X(1, k), X(2, k), 'r*')
    plot(X(5, k), X(6, k), 'b*')
    plot(X(9, k), X(10, k), 'g*')
    plot(X(13, k), X(14, k), 'm*')
end
*/


//deuximème graphe: convergence de la position selon la seconde variable



//troisième graphe: convergence de la vitesse selon la première variable



//quatrième graphe: convergence de la vitesse selon la seconde variable
