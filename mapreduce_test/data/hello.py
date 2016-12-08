from pyspark import SparkContext

def group_values(input_list):
    value_list = []
    for i in range(len(input_list)):
        for j in range(i,len(input_list)):
            value_list.append((input_list[i], input_list[j]))
    return value_list

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[0], pair[1]))      # step 1: name, id
pages = pages.groupByKey() #step 2
pages = pages.map(lambda pair: (pair[0], group_values(list(pair[1]))))

#pages = pages.flatMap(group_values)

#3 Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
#Use flatmap??lambda function??


#4 Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
##Essentially reverse the k,v pairs:
#for (user, list in map)
#   for (each co-view in value)
#       coviews.map.add(co-view, 1)

#5 Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
#reducebyKey()


#6 Filter out any results where less than 3 users co-clicked the same pair of items
#filter by value > 3


##reverses pages
#pages_reversed = pages.map(lambda s: reverse(s))
#pages_reversed.groupByKey()




#/count = pages.reduceByKey(lambda x,y: x+y)        # shuffle the data so that each key is only on one worker
                                                  # and then reduce all the values by adding them together

output = pages.collect()                          # bring the data back to the master node so we can print it out
for page_id, count in output:
    print("user :" + str(page_id))
    for item in count:
        print ("page_id " + str(item))
print ("Popular items done")

sc.stop()
