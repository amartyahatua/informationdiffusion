library(TSPred)
library(data.table)
library(tseries)
library(forecast)
setwd("..\\TwitterSocialNetworkAnalysis\\PredictInformationDiffusionModel\\processed_features\\")
data <- read.csv("Hashtag_Count_Hourly_NegScore.csv", header = TRUE, row.names = 1)  # read text file
outRMSEFileName = "RMSE_ARIMA_NegScore.csv"
tmp_data = apply(data>0, 1, sum)
filtered_data = data[tmp_data >= 0.1*nrow(data),]

norm_data <- t(apply(filtered_data, 1, function(x)(x-min(x))/(max(x)-min(x))))
t_data <- t(norm_data)
colnames(t_data) <- rownames(norm_data)
rownames(t_data) <- colnames(norm_data)

#train arima models and calculate total RMSE
vRMSE <- matrix(0, ncol(t_data), 1)
totalRMSE = 0.0
for(colIdx in 1:ncol(t_data)) {
  trainEndIdx = round(nrow(t_data)*0.7)
  train <- window(t_data[,colIdx], start=1, end=trainEndIdx)
  test <- window(t_data[,colIdx],  start=trainEndIdx+1)
  
  #fit arima model
  fit <- auto.arima(train)
  #tsdisplay(residuals(fit), lag.max=15, main='Seasonal Model Residuals')
  
  #forecast the last 30%
  fcast <- forecast(fit, h=nrow(t_data) - trainEndIdx)
  #plot(fcast)
  #lines(ts(t_data[1:nrow(t_data),colIdx]))
  
  yHat <- fcast$mean
  accFit <- accuracy(yHat, test)
  #paste(sprintf("Column %d  RMSE: %f", colIdx, accFit[2]))
  vRMSE[colIdx] = accFit[2]
  totalRMSE = totalRMSE + accFit[2]
}

paste("Total RMSE", totalRMSE)
write.csv(vRMSE, file = outRMSEFileName, row.names=TRUE)