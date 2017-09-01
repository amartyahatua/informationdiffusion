% load iddata9 z9
% Ts = z9.Ts;
% y = cumsum(z9.y);
% model = ar(y,4,'ls','Ts',Ts,'IntegrateNoise', true);
% % 5 step ahead prediction
% compare(y,model,5)

load PredPreyCrowdingData
z = iddata(y,[],0.1,'TimeUnit','years','Tstart',0);
plot(z)
title('Predator-Prey Population Data')
ylabel('Population (thousands)')