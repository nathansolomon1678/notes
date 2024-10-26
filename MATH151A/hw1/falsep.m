clear all
close all
a=1.75; %%%%%%%%%%%
a=1; %%%%%%%%%%%
b=2.95; %%%%%%%%%%%
b=1.2; %%%%%%%%%%%
%b=2; %%%%%%%%%%%
tol = 1e-6;
Nmax = 100;
%f=@(x) (x-1)*(x-2)*(x-3); %%%%%%%%%%%
f=@(x) x^6 - x - 1; %%%%%%%%%%%

i = 1;
success = 0;
while (i<=Nmax) && (success==0)
    midpoint = (a+b)/2; %%%%%%%%%%%
    %midpoint=(f(a)*b - f(b)*a) / (f(a) - f(b)); %%%%%%%%%%%
    if (abs(f(midpoint)) < tol)
        success = 1;
    else
        i = i + 1;
        midpoint = (a+b)/2; %%%%%%%%%%%
        %midpoint=(f(a)*b - f(b)*a) / (f(a) - f(b)); %%%%%%%%%%%
        % disp([a midpoint b])
        if (sign(f(midpoint)) == sign(f(a)))
            a = midpoint;
        else
            b = midpoint;
        end
    end
end
if (success == 1)
    disp('success!');
else
    disp('did not converge');
end
i
format long
display(midpoint)
format long
numericalsolution = fzero(f, midpoint)