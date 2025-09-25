install.packages(c("readr", "ggplot2", "caret", "corrplot"))
install.packages("nnet")

library(readr)   
library(ggplot2) 
library(caret)   
library(corrplot)
library(nnet)    
library(reshape2)


dataset <- read_csv("ss.csv")

str(dataset)

summary(dataset)


#DATA PREPROCESSING

dataset <- na.omit(dataset)

dataset$`Sleep Disorder` <- as.factor(dataset$`Sleep Disorder`) 
dataset$Gender <- as.factor(dataset$Gender)                 
dataset$Occupation <- as.factor(dataset$Occupation)




#Exploratory Data Analysis

ggplot(dataset, aes(x = `Sleep Duration`)) + 
  geom_histogram(binwidth = 1, fill = "lightgreen", color = "black") + 
  theme_minimal() + 
  labs(title = "Distribution of Sleep Duration", 
       x = "Duration of Sleep (hours)", 
       y = "Frequency")


ggplot(dataset, aes(x = Gender, fill = `Sleep Disorder`)) + 
  geom_bar(position = "fill") + 
  labs(title = "Prevalence of Sleep Disorders by Gender", 
       y = "Proportion") + 
  scale_fill_manual(values = c("lightblue", "salmon", "lightgreen"),
                    labels = c("No Disorder", "Insomnia", "Sleep Apnea"))



numeric_vars <- dataset[sapply(dataset, is.numeric)]
corr_matrix <- cor(numeric_vars)
corrplot(corr_matrix, method = "circle", title = "Correlation Matrix")




#RANDOMIZATION: MODEL TRAINING

set.seed(123)  # For reproducibility
trainIndex <- createDataPartition(dataset$`Sleep Disorder`, 
                                  p = .8, 
                                  list = FALSE, 
                                  times = 1)
data_train <- dataset[trainIndex, ]
data_test <- dataset[-trainIndex, ]



# TRAINING: Multinomial Logistic Regression Model
model <- multinom(`Sleep Disorder` ~ `Sleep Duration` + `Quality of Sleep` + 
                    `Stress Level` + `Physical Activity Level` + Age + 
                    `BMI Category` + `Blood Pressure` + 
                    `Heart Rate` + `Daily Steps` + 
                    Gender + Occupation, 
                  data = data_train)
summary(model)




# TESTING: Predictions on the test set
predictions <- predict(model, newdata = data_test)



# MODEL EVALUATION: Confusion matrix

conf_matrix <- confusionMatrix(data = factor(predictions), 
                               reference = factor(sleep_test$`Sleep Disorder`))
print(conf_matrix)



# MODEL VISUALIZATION: Heat Map of Confusion Matrix


conf_matrix_table <- as.data.frame(conf_matrix$table)

# Create a heatmap of the confusion matrix
ggplot(conf_matrix_table, aes(x = Reference, y = Prediction)) +
  geom_tile(aes(fill = Freq), color = "white") +
  scale_fill_gradient(low = "white", high = "blue") +
  geom_text(aes(label = Freq), color = "black") +
  labs(title = "Confusion Matrix Heatmap", x = "Actual", y = "Predicted") +
  theme_minimal()