clf;            % Clears the current figure
close all;      % Closes all figure windows
clear;          % Clears variables from the workspace



% Define the range for x
x = linspace(-10, 10, 100);  % Creates a range from -10 to 10 with 100 points

% Define the function you want to plot
y = sin(x);  % Example function

% Plot the function
hold on;
plot(x, y);
drawnow;
hold off;

title('Plot of sin(x)');
xlabel('x');
ylabel('sin(x)');