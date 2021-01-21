load PredPreyCrowdingData
z = iddata(y,[],0.1,'TimeUnit','years','Tstart',0);
plot(z)
title('Predator-Prey Population Data')
ylabel('Population (thousands)')