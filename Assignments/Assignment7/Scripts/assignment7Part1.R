print("Assignment 7 - Schmitt Schowing")

#setwd("C:/Users/thsch/Desktop/Bioinformatics3/Assignments/Assignment7/Scripts")


data = read.table("ms_toy.txt", header=TRUE)
summary(data)
# class(data) -> data.frame


# Takes a dataframe and the col name and calculate the values for the missing data
# as if they were data "under the detection threshold"
impute_missing_data <- function(data, colname, QUANTILE_VALUE, FRACTION, replace = FALSE){
  
  current_sd <- apply(data[colname], 2, sd, na.rm = TRUE)
  current_mean <- apply(data[colname], 2, mean, na.rm = TRUE)
  
  str = sprintf("Current sd: %f", current_sd)
  print(str)
  str = sprintf("Current mean: %f", current_mean)
  print(str)
  
  
  # Chosing the mean of the new distribution -> the 5% quantile for instance ?!?!?!
  #QUANTILE_VALUE <- 5
  
  quant <- quantile(data[colname], QUANTILE_VALUE/100, na.rm = TRUE)
  str = sprintf("Current %d percent quantile: %f", QUANTILE_VALUE, quant)
  print(str)
  
  # New mean equals the above quantile
  new_mean = quant
  
  # New sd -> fraction of the current sd
  #FRACTION <- 1/3
  new_sd <- FRACTION * current_sd
  
  print(paste0("New mean: ", new_mean))
  print(paste0("New sd: ", new_sd))
  
  
  # Display the distribution with the chosen mean
  hist(as.matrix(data[colname]), main = "Distribution of the Data", xlab = "Value")
  abline(v=quant,col="red")
  
  # We have sd and mean -> rnorm(nb, sd, mean) will generage numbers in the distribution
  
  # Numbers of NA in the column (nb of data to generate):
  nb_na <- sum(is.na(data[colname]))
  
  generated_data = rnorm(nb_na, mean = new_mean, sd = new_sd)
  
  
  
  # Trying to make the plots nice but will work for ONE distribution
  p1 <- hist(generated_data, breaks = 30, freq = TRUE)
  p2 <- hist(as.matrix(data[colname]), breaks = 60, freq = TRUE)
  
  # Acceptable graphs for any distribution
  #p1 <- hist(generated_data, freq = TRUE)
  #p2 <- hist(as.matrix(data[colname]), freq = TRUE)
  
  plot(p2, main = "Distribution of the Data", xlab = "Value", col = "blue")
  plot(p1, main = "Distribution of the Data", xlab = "Value", col = "red", add=T)
  
  
  # Replace the data a copy of the original dataframe if the parameter "replace" is set to TRUE.
  # Also print the information of the data (copy) before and after the replacement
  # By default it's FALSE.
  
  
  if (replace){
    data.replace <- data
    print(summary(data.replace))
    data.replace[[colname]][which(is.na(data[colname]))] <- generated_data
    
    #data[[colname]][which(is.na(data[colname]))] <- generated_data
    p <- hist(as.matrix(data.replace[colname]),breaks = 60, freq = TRUE)
    plot(p, main = "Distribution of the data after replacement", xlab = "Value", col = "blue")
    print(summary(data.replace))
  }
  
  
}


# Playing with the new mean and sd values
impute_missing_data(data = data, 'ctrl.1', 1, 1/3)
impute_missing_data(data = data, 'ctrl.1', 5, 1/3)
impute_missing_data(data = data, 'ctrl.1', 10, 1/3)
impute_missing_data(data = data, 'ctrl.1', 15, 1/3)
impute_missing_data(data = data, 'ctrl.1', 20, 1/3)

# 5 looks like the best new mean
impute_missing_data(data = data, 'ctrl.1', 5, 1)
impute_missing_data(data = data, 'ctrl.1', 5, 1/2)
impute_missing_data(data = data, 'ctrl.1', 5, 1/3)
impute_missing_data(data = data, 'ctrl.1', 5, 1/4)
impute_missing_data(data = data, 'ctrl.1', 5, 1/5)



# We chose the 5% quartile for the mean and 1 third of the standard deviation for the new sd.
impute_missing_data(data = data, 'ctrl.1', 5, 1/3)

# Plot and information of the distribution after data replacement.
impute_missing_data(data = data, 'ctrl.1', 5, 1/3, TRUE)

# As we have to chose one of the 6, the plot are adapted especially for the first column of data.
# If you want to have good looking plots for any data, switch the two commented lines
# in the impute_missing_data function.

# impute_missing_data(data = data, 'ctrl.2')
# impute_missing_data(data = data, 'ctrl.3')
# impute_missing_data(data = data, 'kout.1')
# impute_missing_data(data = data, 'kout.2')
# impute_missing_data(data = data, 'kout.3')









