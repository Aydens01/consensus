// essai scilab

function Y = chgt_var(X, A, ag, k)
    for i=0:ag-1
        for j=1:k
            Y(i*k+j) = 0
            for t=0:ag-1
                Y(i*k + j) =Y(i*k+j)+A(i+1, t+1)*(X(i*k+j)-X(t*k+j)) 
            end
        end
    end
endfunction

function rep = phi_alpha(Y, alpha)
    n = size(Y)
    rep = zeros(n(1))
    for i=1:n(1)
        rep(i) = sign(Y(i))*(Y(i)^alpha)
    end
endfunction

function dY = consensus(t, Y, alpha,L, I, F, B, C)
    dY = (L.*.I)*F - (L.*.(B*C))*phi_alpha(t, Y, alpha)
endfunction

function [Y]=pasEuler(systeme, n, h, t, Yn, alpha, L, I, F, B, C)
    dY = systeme(t, Yn, alpha, L, I, F, B, C)
    for i=1:n
        Y(i) = Yn(i)+h*dY(i)
    end
endfunction

function [mt, mY]=euler(Yi, alpha, L, I, F, B, C, T, N, systeme)
    h = T/N
    n = size(Yi)
    mY = zeros(n(1), N+1)
    mt = zeros(N+1)
    mY(:, 1) = Yi
    mt(1)=0
    for k=1:N
         mY(:,k+1) = pasEuler(systeme, n(1), h, mt(k), mY(:, k),alpha, L, I, F, B, C)
         mt(k+1) = mt(k)+h
    end
endfunction
