# Sparkify Project

This project has the purpose of predicting the churn rate of Sparkify's service.
One mandatory requirement of this project is the use of SPARK.
The project has two components:

* Sparkify notebook: it's the python notebook that contains the analysis and the export of the models in PMML. The notebook is developed for Amazon EMR.
* FLASK Web App: it's to make available the result to everyone. The webapp uses the model generated in the Sparkify notebook to predict the users leaving the service.

## Getting start

### (Optional) Launch python notebook on Amazon EMR
1. Initialize the Amazon EMR with Spark (v2.4), Hive, Zeppelin, Livy and 3 nodes (m3.xlarge).
   Remember to select a Key to access in the master node via SSH. Use setup_emr.json to configure your cluster.

2. Go to [Pyspark2pmml github](https://github.com/jpmml/pyspark2pmml#configuration-and-usage) and download the JPMML-SparkML jar version 1.5.x. It's a dependency to export the models as PMML file.

3. Log in inside the master node (via SSH). Create the directory /home/hadoop/extrajars and upload jpmml-sparkml-executable-1.5.x.jar in /home/hadoop/extrajars. [For more details](https://aws.amazon.com/it/premiumsupport/knowledge-center/emr-spark-classnotfoundexception/)

4. Launch jupyter and upload Sparkify.ipynb

5. Run all cells

6. Download the models from master nodes. The files are /tmp/lr.pmml and /tmp/bayes.pmml

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

## Steps of the project
In this project, the dataset contains the action logs of the users.
Starting from this point, we will understand how "churn users" are distributed.
In the next step, we will aggregate the data to define the daily actions of the users.
After, we will create two different models to predict when a user leaves the service.
Built the models, we will export them in PMML format.
As the last point, we will create a web app to show as a model may be used to predict if a user will leave the system.
Now, if you are interested to explore it, then you can read the [notebook](Sparkify.html)

## License
This code is release under [MIT License](LICENSE).