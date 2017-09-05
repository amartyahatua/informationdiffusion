#sc <- read.table("C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\synthetic_control.data", header=F, sep="")
library(dtw)
library(dtwclust)
library(clusterSim)



########################################################
#################TADPole################################
########################################################

sc <- read.csv("C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\result_hourly_matrix\\Hashtag_Count_Hourly_NegScore.csv",header=F, sep="," )
sc_numeric = sc[2:1688,2:467]
repc.tadp <- tsclust(sc_numeric, type = "tadpole", k = 6L,
                     trace = TRUE,
                     control = tadpole_control(dc = 1.5, window.size = 24L))
plot(repc.tadp)

sc <- read.csv("C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\result_hourly_matrix\\Hashtag_Count_Hourly_NegScore.csv",header=F, sep="," )
sc_numeric = sc[2:1688,2:467]
repc.tadp <- tsclust(sc_numeric, type = "tadpole", k = 4L:10L,
                     trace = TRUE,
                     control = tadpole_control(dc = 1.5, window.size = 24L))
names(repc.tadp) <- paste0("k_", 4L:10L)
sapply(repc.tadp, cvi, type = "internal")



##############################################################################################################
###########################################DTW FOR INFLUENCE #################################################
##############################################################################################################



sc <- read.csv("..\\result_hourly_matrix\\Hashtag_Count_Hourly_NeuPercentage.csv",header=F, sep="," )
sc_numeric = sc[2:nrow(sc),2:ncol(sc)]

temp_df = sc_numeric
result = apply(temp_df, 1, function(c)sum(c>0))
rows_indexes = result >= 0.105*ncol(temp_df)
temp_df = temp_df[rows_indexes,]

repc.tadp <- tsclust(temp_df, type = "tadpole", k = 4L,
                     trace = TRUE,
                     control = tadpole_control(dc = 1.5, window.size = 24L))
plot(repc.tadp)

hc.clust <- data.frame(dtwclust = repc.tadp@cluster)

write.csv(hc.clust, file = '..\\result_hourly_matrix\\temp_cluster_label.csv')


















#######################################################



repc.tadp <- tsclust(sc_numeric, type = "tadpole", k = 4L:10L,
                     trace = TRUE,
                     control = tadpole_control(dc = 1.5, window.size = 48L))
names(repc.tadp) <- paste0("k_", 4L:10L)
sapply(repc.tadp, cvi, type = "internal")










sc <- read.csv("C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\result_hourly_matrix\\Hashtag_Count_Hourly_NegScore.csv",header=F, sep="," )
sc_numeric = sc[2:1624,2:467]
repc.tadp <- tsclust(sc_numeric, type = "tadpole", k = 4L:10L,
                     trace = TRUE,
                     control = tadpole_control(dc = 0.5, window.size = 24L))
names(repc.tadp) <- paste0("k_", 4L:10L)
sapply(repc.tadp, cvi, type = "internal")












