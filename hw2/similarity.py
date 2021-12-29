import math
import sys
import time

try:
    #initializing variables from the command line
    data_file = sys.argv[1]
    output_file = sys.argv[2]
    if len(sys.argv) == 3:
        user_thresh = 5
    else:
        user_thresh = int(sys.argv[3])
except IndexError:
    #printing usage error and exit if incorrect input numbers
    print("Usage:\n $ python3 generatedata.py <data_file>" \
         " <output_file> [user_thresh (default = 5)]")
    sys.exit(1)

print('Input MovieLens file: {}'.format(data_file))
print('Output file for similarity data: {}'.format(output_file))
print('Minimum number of common users: {}'.format( user_thresh))

#The following function reads the dataset into the text editor one by one and calculates
#the number of lines read, the number of users, and the number of movies.
def read_function(data_file, num_lines, num_movies, num_users, movie_dict):
    with open(data_file, 'r') as movies:
        while True:
            movie_data = movies.readline().strip()
            if movie_data == '':
                break;
            num_lines += 1
            #reading in movie_id, user_id, and rating
            movie_delim = movie_data.split()
            user_id, movie_id = int(movie_delim[0]), int(movie_delim[1])
            movie_rating = int(movie_delim[2])
            #calculating the number of movies, users, and lines read
            if movie_id not in num_movies:
                num_movies.append(movie_id)
            if user_id not in num_users:
                num_users.append(user_id)
            #appending movies to a nested dictionary. Movie_id is the key, the value is
            # another dictionary with user_id as the key and rating as the value.
            if movie_id not in movie_dict:
               movie_dict[movie_id] = {}
            movie_dict[movie_id][user_id] = movie_rating
    return num_lines, num_movies, num_users, movie_dict

#calling read function
num_lines, num_movies, num_users, movie_dict = read_function(data_file, \
    0, [], [], {})

print('Read {} lines with a total of {} movies and {} users'. \
    format(num_lines, len(num_movies), len(num_users)))

start = time.time()
#the following function computes the similarity score of two movies using cosine similrity
#and returns a dictionary with the max similarities for each movie. The dictionary has
#movie one as the key, and a tuple with (most similar movie, similarity score for those
#two movies, number of common users) as the value.
def movie_similarity(movie_dict):
    results = {}
    for id1 in movie_dict:
        mean_id1 = sum(movie_dict[id1].values())/ \
            len(movie_dict[id1].values())
        #initializing max similarity. setting initial similarity to -10. this tuple
        # will be replaced by a tuple of (most similar movie, similarity score for
        # those two movies, number of common users).
        max_sim = (0, -10, 0)
        for id2 in movie_dict:
            if id1 != id2:
                #finding the list of common users between two movies
                common_users = set(movie_dict[id1].keys() \
                    & movie_dict[id2].keys())
                if len(common_users) >= user_thresh:
                   mean_id2 = sum(movie_dict[id2].values()) \
                       /len(movie_dict[id2].values())
                   #computing the similarity between movie1 and movie2 for each common user
                   num, denom1, denom2, denom = 0, 0, 0, 0
                   for user in common_users:
                       num += (movie_dict[id1][user] - mean_id1) \
                       * (movie_dict[id2][user] - mean_id2)
                       denom1 += (movie_dict[id1][user] - mean_id1)**2
                       denom2 += (movie_dict[id2][user] - mean_id2)**2
                       denom = math.sqrt(denom1 * denom2)
                       try:
                           similarity = round(num/denom, 2)
                       except:
                           similarity = 0
                   #asserting similarity is in the appropriate range
                   assert abs(similarity) <= 1.00
                   if similarity > max_sim[1]:
                       max_sim = (id2, similarity, len(common_users))
            if max_sim == -10:
                results[id1] = ()
            else:
                results[id1] = max_sim
    return results

#calling the function and returning a max similarity dictionary
results = movie_similarity(movie_dict)

end = time.time()

time_elapsed = round((end-start), 3)

print('Computed similarities in {} seconds'.format(time_elapsed))

#created a function to write the data in the proper format into the output file.
def write_function(output_dict):
    with open(output_file, 'w') as similarities:
        for movie in sorted(results.keys()):
            if results[movie][1] == -10:
                to_write = "{}".format(movie)
            else:
                to_write = "{} ({},{},{})".format(movie, results[movie][0], \
                    results[movie][1], results[movie][2])
            similarities.write(to_write + '\n')


write_function(results)
