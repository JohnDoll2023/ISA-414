# Databricks notebook source
# File location and type
file_location = "/FileStore/tables/bol.csv"

# inferSchema := detect data types
# header := whether first row contains column names
raw_data = spark.read.load(file_location, format="csv", inferSchema="true", header="true")

# We keep raw_data intact because we will use it later
df = raw_data

#adjust the column dimensions and create summed columns
from pyspark.sql.functions import col
df = df.withColumn("PPR_1",100 - col("PPR_1"))
df = df.withColumn("PIR_1",100 - col("PIR_1"))
df = df.withColumn("PIR_2",100 - col("PIR_2"))
df = df.withColumn("PIR_3",100 - col("PIR_3"))
df = df.withColumn("PIR_4",100 - col("PIR_4"))
df = df.withColumn("PER_2",100 - col("PER_2"))
df = df.withColumn("PPR", (col("PPR_1") + col("PPR_2") + col("PPR_3") + col("PPR_4") + col("PPR_5")) / 5)
df = df.withColumn("PIR", (col("PIR_1") + col("PIR_2") + col("PIR_3") + col("PIR_4") + col("PIR_5")) / 5)
df = df.withColumn("PER", (col("PER_1") + col("PER_2") + col("PER_3") + col("PER_4") + col("PER_5")) / 5)
df = df.withColumn("PI", (col("PI_1") + col("PI_2") + col("PI_3") + col("PI_4") + col("PI_5")) / 5)
df = df.withColumn("PS", (col("PS_1") + col("PS_2") + col("PS_3") + col("PS_4") + col("PS_5")) / 5)
df = df.withColumn("PB", (col("PB_1") + col("PB_2") + col("PB_3") + col("PB_4") + col("PB_5")) / 5)
df = df.withColumn("WTB", (col("WTB_1") + col("WTB_2") + col("WTB_3") + col("WTB_4") + col("WTB_5")) / 5)

#do the linear analysis and get statistics from the resulting regression
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
predictors = ["PPR", "PIR", "PER", "PI", "PS", "PB"]
assembler = VectorAssembler(inputCols=predictors, outputCol="predictors")
df = assembler.transform(df)
lr = LinearRegression(featuresCol = "predictors", labelCol="WTB")
model = lr.fit(df)
print(model.coefficients)
print(model.summary.pValues)

#The perceived integrity, perceived security, and perceived benelovence were all significant factors in a customer's willingness buy from bol.com. We know that each of these three topics are important to customers as each of their p-values are significant at 0.0059, 0.0141, and 2.72 * 10^-7 respectively. Relatably, they also have the three biggest impacts per unit increase on a customer's willingness to buy at 0.283, 0.181 and 0.445 per unit respectively. If bol.com wants to increase its customer base and get more orders coming in, it should bolster its perceived integrity, perceived security and perceived benelovence. To make customers feel that the site has more integrity, bol.com could add a policy of something to the effect of "love it or 100% money back guarantee". By adding a policy like this one, it would let customers know that bol.com takes their customers' happiness and satisfaction into account, and make it appear as they are not only concerned about the bottom line. Bol.com could make customers feel safer using their site if they added statements across their website that promote the efforts they put into securing their customer data. For example, when you enter your username and password to sign in, it could have a statement like "Protected by OneSecure" or whatever example replacement they might use for 'OneSecure' to let their customers know that as soon as they come to the site, their info is being safely guarded. Finally, to increase the perceived benevolence of bol.com to customers, bol.com could add a page to their website or perhaps a banner with testimonies from customers who had an issue with bol.com get resolved quickly and effectively. Knowing that even when other customers faced issues, they were able to easily get them resolved would increase the trust that customers have when dealing with the site.
