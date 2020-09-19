# Sparkify Project
This project has the purpose of predicting the churn rate of Sparkify's service.

## Description of the project

### Project Overview

In this project, we analyze a dataset of Sparkify's service to detect the churn rate. 
The dataset contains the action logs of each customer. In particular, it tracks each listened song, each visited page, and other related data.
A requirement of this project is the use of Spark.
In this particular implementation, we run Spark on an AWS EMR cluster.
It composes of three nodes with m3.xlarge EC2 instances.

### Problem Statement

As mentioned above, the goal is to detect the churn rate. It means that we want to build a model that can predict which user is going to leave the service. In particular, the model should be able to predict it from partial action logs of the customer. Because in the real world, we have only a portion of information, or rather we have only the user's action since the registration date until the current day. However in the dataset, the knowledge is complete because there are all actions of the users.

### Metrics

It's very significant to understand how to evaluate the model. First, however, we need to consider that we accept that the user's actions are mostly similar between the faithful customers and the users who are going to leave the service.
It means that model could have a relevant rate of false-positives. Additionally, we accept there are few customers who leave the service over the total users. In other words, we accept the dataset is imbalanced.
So we use the metrics: F1 Score, Accuracy, and Weighted Recall score.
However, these metrics are applied to the actions log, not to the users. 
We can consider another metric. It's the ratio between predicted users who leave the service and the total users who abandon the service. It shows us how many users the model doesn't detect.
A more accurate metric should consider that the ultimate goal is to predict as soon as possible if the user is going to leave the service.
Let us assume that the duration of one account is n days. We know the daily user actions from registration to the cancellation. It means that we can count how many times the user is predicted as "churn user" since registration to n/2 days (half-life of account). Consequently, it became relevant to compare different values to understand how many "churn users" we can detect.

### Data Exploration

We can observe that in the dataset there are:

* The total number of customers is 22278. The users who leave the service are 5003
* There are two levels of service: the premium service (paid) and the free service (free)
* The customers use 86 different types of browsers
* There are only two genders: M or F

Between the pages that a user can navigate, there is the page 'Cancellation Confirmation'. This page is relevant to understand which user is leaving the service. 
Analyzing the user's actions of last year before the account cancellation, we can observe that majority of people leave the service in the first 250 days from registration, with a mean of 63.68 days and a standard deviation of 41.28 days.

### Data Preprocessing

The first point that we need to handle is the presence of NA values.
In the dataset, 778479 rows miss some relevant features like registration, user agent, location, firstName, lastName, and gender.
Dropping the rows with NA in the registration column, we can observe the same result in the other features.
Like already previously observed, we can consider only the first 250 days since the registration date. This choice has some impacts:
* We reduce the amount of data to analyze.
* We lose data on faithful customers.
* We reduce the number of rows of faithful customers. It permits us to limit the problem of the imbalanced dataset. Because this type of customer uses the service over the 250 days, thus we have many action logs for these users.
We add two new features in the dataset:
1. It's is_churn attribute that defines if a user leaves the service.
2. It's n_days attribute that counts the elapsed days since registration date. It permits us to normalize the action date. 
In the next step, we aggregate data using a pivot table. For each row, we count how many times each value occurs for each userId and n_days. In other words, each row contains the user id, the n_days, how many times the user has visited a specific page during the day, etc.
Some columns are not idoneous for the pivot table, and we exclude them.
If a feature has many distinct values, we can encounter some difficulties:
1. We can have an overfitting problem. A particular value (like user id) can be mapped on a specific pattern if we have many columns.
2. We can have a memory problem. 
The columns to exclude are:
* Location: in this column, we find the list of many cities. For 22503 users, the granularity is too fine. 
* Songs: in this column, there are too many different values.
* Artists: in this column, it similar to the songs column's problem.
For the user agent column, we can adopt another solution. The column has 83 distinct values. Each browser has many versions, but it has only one family. So we can map the user agent on its family browser.

### Implementation

The first step to build a model is to split the dataset between the train set and test set. In our case, it's necessary to preserve the integrity of action logs. It means that we split the data by user id. Some users will be in the train set, and the other in the test set.
A good ratio to split the dataset may be that 70% of users go in the train set, and 30% of users go in the test set.
The full dataset is about 12GB. It's too big to fit into a single computer. To overcome this problem, we can proceed to the next step:
1. We use a small dataset to experiment on the local machine
2. We use the full dataset on a remote cluster like AWS EMR
However, the systems are different, and we can encounter some problems:
* The setup of the environment is different.
* With a big dataset, we should be careful about memory allocations. It's a best practice to free the cluster from cached data frames.
To maximize performance, we can create two models with different algorithms.
The first model uses the Naive Bayes Algorithm. The second model uses a Logistic Regression.
To obtain the best results, we must use a hyperparameters tuning.
For each model, we can test different parameters to obtain the best model relative to a metric.
In our case, we can use the BinaryClassificationEvaluator class. It's a standard evaluator of Spark.
The evaluation occurs using a cross-validation approach.
However, in our case, we tune a few parameters to limit the computation time of models.
For the Naive Bayes, we tune the smoothing parameter. Instead, we optimize the max iteration number for the Logistic Regression.

### Refinement

In the early stage, we can proceed by analyzing the standard metrics to apply to logistic regression. However, this approach generates a model that predicts if, in one specific day, the user is classified as a churned user.
In the next step, we can optimize the model by adding a specific metric that considers how many times the user is classified as a churned user.
In other words, we can build another metric that considers not only the single record but all predictions on the user. This approach permits us to be more compliant with our goal.
To emphasize this aspect, we can compare two different algorithms to show as evaluation of standard metrics, it may change considering a custom metric.

### Model Evaluation and Validation

Before going to the conclusion, we shall evaluate our models. We can begin to analyze them by using the standard metrics:
* Naive Bayes: 
    * F1 Score: 0.6763166451101013
    * Accuracy Score: 0.644754635759245
    * Weighted Recall: 0.644754635759245
    * Total churn users: 4901
    * Number predicted churn users: 4553
    * Ratio: 0.9289940828402367
* Logistic Regression: 
    * F1 Score: 0.7604781055264619
    * Accuracy Score: 0.8235508605979934
    * Weighted Recall: 0.8235508605979934
    * Total churn users: 4901
    * Number predicted churn user
    * Ratio: 0.9779636808814528
We observe that the logistic regression model has better results in respect to the Naive Bayes model. 
An important aspect is that the F1 score is low. And therefore, the predictions have a considerable amount of false-positive cases.
However, we can observe a good number of predicted users leaving the service. This observation is useful for the custom metric described above.

The result of our custom metric for the Naive Bayes model is:
* Counting at least one positive value at 50.0% of the lifetime of the account, it predicts the 0.34931646602734134
* Counting at least one positive value at 70.0% of the lifetime of the account, it predicts the 0.5164252193429912
* Counting at least one positive value at 80.0% of the lifetime of the account, it predicts the 0.6000816159967354
* Counting at least one positive value at 90.0% of the lifetime of the account, it predicts the 0.6768006529279739
* Counting at least one positive value at 99.0% of the lifetime of the account, it predicts the 0.7500510099979596
* Counting at least one positive value at 50.0% of the lifetime of the account, it predicts false positive 0.48690511380431567
* Counting at least one positive value at 70.0% of the lifetime of the account, it predicts false positive 0.6310966597694354
* Counting at least one positive value at 80.0% of the lifetime of the account, it predicts false positive 0.6671002069169376
* Counting at least one positive value at 90.0% of the lifetime of the account, it predicts false positive 0.6937629323086019
* Counting at least one positive value at 99.0% of the lifetime of the account, it predicts false positive 0.7142181495713863
* Counting at least two positive values at 50.0% of the lifetime of the account, it predicts the 0.2501530299938788
* Counting at least two positive values at 70.0% of the lifetime of the account, it predicts the 0.39359314425627423
* Counting at least two positive values at 80.0% of the lifetime of the account, it predicts the 0.46806774127729034
* Counting at least two positive values at 90.0% of the lifetime of the account, it predicts the 0.5339726586410937
* Counting at least two positive values at 99.0% of the lifetime of the account, it predicts the 0.5974290961028361
* Counting at least two positive values at 50.0% of the lifetime of the account, it predicts false positive 0.33490984333431867
* Counting at least two positive values at 70.0% of the lifetime of the account, it predicts false positive 0.46071534141294707
* Counting at least two positive values at 80.0% of the lifetime of the account, it predicts false positive 0.5003251551877033
* Counting at least two positive values at 90.0% of the lifetime of the account, it predicts false positive 0.5294117647058824
* Counting at least two positive values at 99.0% of the lifetime of the account, it predicts false positive 0.5538279633461425
* Counting at least three positive values at 50.0% of the lifetime of the account, it predicts the 0.1834319526627219
* Counting at least three positive values at 70.0% of the lifetime of the account, it predicts the 0.3076923076923077
* Counting at least three positive values at 80.0% of the lifetime of the account, it predicts the 0.3717608651295654
* Counting at least three positive values at 90.0% of the lifetime of the account, it predicts the 0.4284839828606407
* Counting at least three positive values at 99.0% of the lifetime of the account, it predicts the 0.4894919404203224
* Counting at least three positive values at 50.0% of the lifetime of the account, it predicts false positive 0.23570795152231747
* Counting at least three positive values at 70.0% of the lifetime of the account, it predicts false positive 0.3452556902157848
* Counting at least three positive values at 80.0% of the lifetime of the account, it predicts false positive 0.38368312148980194
* Counting at least three positive values at 90.0% of the lifetime of the account, it predicts false positive 0.4150753768844221
* Counting at least three positive values at 99.0% of the lifetime of the account, it predicts false positive 0.4402601241501626
The result of our custom metric for the Naive Bayes model is:
* Counting at least one positive value at 50.0% of the lifetime of the account, it predicts the 0.029993878800244848
* Counting at least one positive value at 70.0% of the lifetime of the account, it predicts the 0.04998979800040808
* Counting at least one positive value at 80.0% of the lifetime of the account, it predicts the 0.0612119975515201
* Counting at least one positive value at 90.0% of the lifetime of the account, it predicts the 0.06937359722505611
* Counting at least one positive value at 99.0% of the lifetime of the account, it predicts the 0.08182003672719854
* Counting at least one positive value at 50.0% of the lifetime of the account, it predicts false positive 0.010050251256281407
* Counting at least one positive value at 70.0% of the lifetime of the account, it predicts false positive 0.013715637008572272
* Counting at least one positive value at 80.0% of the lifetime of the account, it predicts false positive 0.014898019509311262
* Counting at least one positive value at 90.0% of the lifetime of the account, it predicts false positive 0.015725687259828553
* Counting at least one positive value at 99.0% of the lifetime of the account, it predicts false positive 0.0164942358853089
* Counting at least two positive values at 50.0% of the lifetime of the account, it predicts the 0.0071413997143440116
* Counting at least two positive values at 70.0% of the lifetime of the account, it predicts the 0.011426239542950418
* Counting at least two positive values at 80.0% of the lifetime of the account, it predicts the 0.013466639461334421
* Counting at least two positive values at 90.0% of the lifetime of the account, it predicts the 0.01693531932258723
* Counting at least two positive values at 99.0% of the lifetime of the account, it predicts the 0.01938379922464803
* Counting at least two positive values at 50.0% of the lifetime of the account, it predicts false positive 0.0010641442506650902
* Counting at least two positive values at 70.0% of the lifetime of the account, it predicts false positive 0.001418859000886787
* Counting at least two positive values at 80.0% of the lifetime of the account, it predicts false positive 0.0017735737511084836
* Counting at least two positive values at 90.0% of the lifetime of the account, it predicts false positive 0.0021874076263671298
* Counting at least two positive values at 99.0% of the lifetime of the account, it predicts false positive 0.002246526751404079
* Counting at least three positive values at 50.0% of the lifetime of the account, it predicts the 0.0022444399102224035
* Counting at least three positive values at 70.0% of the lifetime of the account, it predicts the 0.003672719853091206
* Counting at least three positive values at 80.0% of the lifetime of the account, it predicts the 0.004488879820444807
* Counting at least three positive values at 90.0% of the lifetime of the account, it predicts the 0.005713119771475209
* Counting at least three positive values at 99.0% of the lifetime of the account, it predicts the 0.005713119771475209
* Counting at least three positive values at 50.0% of the lifetime of the account, it predicts false positive 0.0002364765001477978
* Counting at least three positive values at 70.0% of the lifetime of the account, it predicts false positive 0.0002955956251847473
* Counting at least three positive values at 80.0% of the lifetime of the account, it predicts false positive 0.0004729530002955956
* Counting at least three positive values at 90.0% of the lifetime of the account, it predicts false positive 0.0004729530002955956
* Counting at least three positive values at 99.0% of the lifetime of the account, it predicts false positive 0.0004729530002955956
In this case, the result depends on the importance of false positives. If we send an email to ask the churn user’s opinion on the service, the false positive may be irrelevant. Otherwise, if we offer a promotion to the user, the false-positive became important. 

### Conclusion

In the previous sections, we have analyzed the dataset, and we have built different models to detect which users will leave the service. This process has led to some assumptions. The most relevant is to consider only the first 250 days since the registration date.
This choice has made it possible to create a uniform dataset between users avoiding the creation of an imbalanced dataset. However, it's relevant to consider that the assumption is valid on this dataset that snapshots out data in a specific moment. It's reasonable to expect that this scenario may change in the future.
Another aspect to consider is that our model describes how the users leave the services. To improve the service should be desirable to understand why.
These considerations can be as follows:
* Build a model that considers the whole lifetime of the account
* Build a model using a different algorithm
* Request of the user their motivation for account cancellation. Next, we can apply the NLP technique to understand why. 

### As to return usable the analysis

We have created a model, but this only one aspect of our job. It's also essential to put into practice the built model.
It's necessary to export the model from Apache Spark, thus we can reuse it inside another application. A possible solution is to export it in the [PMML](https://en.wikipedia.org/wiki/Predictive_Model_Markup_Language) format using the Pyspark2pmml module. 
In this way, we can reuse the model and embed it inside a web app. To show the model at work, we created a web app where you can find some daily logs of the user activities inside a table. The data are editable so you can experiment to identify which values influence if the user will leave the service.

## Structure of the repository
In this repository you can find:

* Python notebook: In the involved file you find the analysis. The notebook is developed for running on Spark cluster of Amazon EMR. There two files:
    * Sparkify.ipynb: the notebook python file
    * Sparkify.html: the output of of the notebook
    * setup_emr.json: it's a configuration file for spark cluster on Amazon AMR
     
* PMML Models: in the models directory you find the model generated from Sparkify notebook
 
* FLASK Web App: Inside the app directory, there is the webapp. It shows an interactive table with the user actions log. Using a button you can know if the user is going to leaving the service.

## Getting start

### (Optional) Launch python notebook on Amazon EMR
1. Initialize the Amazon EMR with Spark (v2.4), Hive, Zeppelin, Livy and 3 nodes (m3.xlarge).
   Remember to select a Key to access in the master node via SSH. Use setup_emr.json to configure your cluster.

2. Go to [Pyspark2pmml github](https://github.com/jpmml/pyspark2pmml#configuration-and-usage) and download the JPMML-SparkML jar version 1.5.x. It's a dependency to export the models as PMML file.

3. Log in inside the master node (via SSH). Inside the master node create the directory /home/hadoop/extrajars and upload jpmml-sparkml-executable-1.5.x.jar in /home/hadoop/extrajars. [For more details](https://aws.amazon.com/it/premiumsupport/knowledge-center/emr-spark-classnotfoundexception/)

4. Launch jupyter and upload Sparkify.ipynb

5. Run all cells

6. Download the models from master node. The files are /tmp/lr.pmml and /tmp/bayes.pmml

7. Put the models inside the project directory models

### Install and launch the webapp

#### Manual installation:
Before proceeding with installation, the software requires the following dependencies:
```bash
pip3 install Flask pypmml numpy
```

and install Java >= 8

1. Run the following command in the app's directory to run your web app.
    `python run.py`

2. Go to http://0.0.0.0:3001/

### via Docker:
In project's root directory:

1. Run `compose-docker up`

2. Go to http://localhost:3001/


## License
This code is release under [MIT License](LICENSE).
