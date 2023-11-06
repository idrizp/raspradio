% PWM model of a frequency modulated signal.

[y, Fs] = audioread("test_audio.wav");

y = y.';
y = y / max(abs(y));
t = (0:length(y) - 1)/Fs;

% 10KHz
f_c = 10E3;
max_f = max(abs(fft(y)));

intg = cumsum(y);
beta = 0.7;
f_d = beta * max_f;

signal = cos(2*pi*f_c*t + 2*pi*f_d*intg);
plot(t, round(signal));
xlim([0, t(end)]);
ylim([-5, 5]);

% Now, for the PWM signal:
% I need to create a sawtooth wave and multiply it with the signal.
% I'll need to find where the signal is _higher_ than the sawtooth wave,
% and that'll be on, if it's less, it's off.

saw = sawtooth(2*pi*f_c*t);
pwm = (0:length(signal) - 1)/ f_c;

pwm(signal > saw) = 1;
pwm(signal < saw) = 0;

plot(t, pwm);
xlim([1, 1.15]);

