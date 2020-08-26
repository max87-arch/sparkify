# Sparkify Project
This project has the purpose of predicting the churn rate of Sparkify's service.

## Description of the project
The purpose of this project is predicting the churn rate of Sparkify's service. The dataset contains the action logs of each user.
In particular, it tracks each listened song, each visited page, and other related data.
Between the visited pages, there is the 'Submit Cancellation' page visited by the user in order to leave the service.
It permits us to create a new feature to define if a user is going to leave the service or not.
Aggregating the user actions by day, we can observe that in the 250 days since the registration date there is the highest concentration of the users who discontinue the service.
Based on this data, we create two models with finality to predict if a user will leave the service using the daily aggregated data as predictors.
The first model uses Naive Bayes's algorithm. The second uses logistic regression.
To compare the two models, we use two strategies:
* Use standard metrics: F1 Score, Accuracy Score, and Weighted Recall score. Additionally, we use the ratio of predicted users who leave the service over the total users who discontinue the service.
* Use custom metrics: the ultimate goal is to predict as soon as possible if the user is going to leave the service. Let us assume that the duration of one account is n days. We know the daily user actions from registration to the cancellation. It means that we can count how many times the user is predicted as "churn user" since registration to n/2 days (half-life of account). Consequently, it became relevant to compare different values to understand how many "churn users" we can detect.
Using the standard metrics, the best model is the logistic regression. In the custom metrics case, the result depends on the importance of false positives.
If we send an email to ask the churn user opinion on the service, the false positive may be irrelevant, and the best model is the Naive Bayes.
However, if we offer a promotion to the user, the false-positive became important, and the best model is the Logistic Regression.
These considerations are to be compared with some limitations:
* First, the arbitrary selection of aggregated data by day. Other criteria could be the session ID.
* Second, the exclusion of users’ listened songs as predictors. This can create some difficulties, like overfitting or an excessive number of predictors.
* Third, the consideration of only the first 250 days of user events. This prevents an imbalanced dataset, but we lost information on the user.

The generated models are exported in [PMML](https://en.wikipedia.org/wiki/Predictive_Model_Markup_Language) format so that they can be reused.

In this case, the models are used in a web app. It shows an interactive table with the user actions log and it permits to predicts if the user is going to leave the service.

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
