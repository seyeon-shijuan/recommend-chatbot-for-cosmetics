import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import operator

class CollaborationFilter():
    def __init__(self):
        cosmetics = pd.read_csv('resource/data/collabo_filtering_dataset.csv')
        self.cosmetics = cosmetics.drop_duplicates(subset='brand_id')
        rating_matrix = self.cosmetics.pivot_table(index='user_id', columns='brand_id', values='rate')
        
        # replace NaN values with 0
        self.rating_matrix = rating_matrix.fillna(0)

    def add_new_user_ratings(self, user_id, ratings):
        # Check if the user already exists in the ratings DataFrame
        if user_id in self.rating_matrix.index:
            print(f"User {user_id} already exists in the rating matrix.")
            return

        # Create a new row for the user with NaN values
        new_user_row = pd.Series(index=self.rating_matrix.columns, name=user_id)
        new_user_row = new_user_row.fillna(0)

        # Update the new user row with the provided anime ratings
        for anime_id, rating in ratings.items():
            if anime_id in self.rating_matrix.columns:
                new_user_row[anime_id] = rating
            else:
                print(f"Ignoring unknown anime_id {anime_id}.")

        # Add the new user row to the rating matrix
        transposed = pd.DataFrame(new_user_row).transpose()
        new_rating_matrix = pd.concat([self.rating_matrix, transposed])
        print(f"New user {user_id} added to the rating matrix.")
        return new_rating_matrix

    def infer(self, rating_matrix, current_user=226):
        top_users_similarities = self.similar_users(current_user, rating_matrix)
        print(f"{top_users_similarities=}")
        similar_user_indices = [u[0] for u in top_users_similarities]
        
        # top K(5명) 번호
        recommended = self.recommend_item(current_user, similar_user_indices, rating_matrix)
        return recommended

    def similar_users(self, user_id, matrix, k=5):
        # create a df of just the current user
        user = matrix[matrix.index == user_id]

        # and a df of all other users
        other_users = matrix[matrix.index != user_id]

        # calc cosine similarity between user and each other user
        similarities = cosine_similarity(user, other_users)[0].tolist()

        # create list of indices of these users
        indices = other_users.index.tolist()

        # create key/values pairs of user index and their similarity
        index_similarity = dict(zip(indices, similarities))
        
        # filter out entries with similarity equal to 0.0
        filtered_index_similarity = {index: similarity for index, similarity in index_similarity.items() if similarity != 0.0}

        # sort by similarity
        index_similarity_sorted = sorted(filtered_index_similarity.items(), key=operator.itemgetter(1))
        index_similarity_sorted.reverse()

        # grab k users off the top
        top_users_similarities = index_similarity_sorted[:k]
        
        return top_users_similarities

    def recommend_item(self, user_index, similar_user_indices, matrix, items=3):
        # load vectors for similar users
        similar_users = matrix[matrix.index.isin(similar_user_indices)]
        # calc avg ratings across the 3 similar users
        similar_users = similar_users.mean(axis=0)
        # convert to dataframe so its easy to sort and filter
        similar_users_df = pd.DataFrame(similar_users, columns=['mean'])

        # load vector for the current user
        #user_df = matrix[matrix.index == user_index]
        # transpose it so its easier to filter
        #user_df_transposed = user_df.transpose()
        # rename the column as 'rating'
        #user_df_transposed.columns = ['rate']
        # remove any rows without a 0 value. Anime not watched yet
        #user_df_transposed = user_df_transposed[user_df_transposed['rate'] == 0]
        # generate a list of animes the user has not seen
        #animes_unseen = user_df_transposed.index.tolist()
        # filter avg ratings of similar users for only anime the current user has not seen
        #similar_users_df_filtered = similar_users_df[similar_users_df.index.isin(animes_unseen)]
        
        # order the dataframe
        similar_users_df_ordered = similar_users_df.sort_values(by=['mean'], ascending=False)
        
        # grab the top n brand
        top_n_brand = similar_users_df_ordered.head(items)
        top_n_brand_indices = top_n_brand.index.tolist()
        
        # lookup these anime in the other dataframe to find names
        brand_information = self.cosmetics[self.cosmetics['brand_id'].isin(top_n_brand_indices)]

        return brand_information  # items

    def parse_dataframe(self, df):
        product_list = []

        for index, row in df.iterrows():
            product_info = {
                "id": row['brand_id'],
                "name": row['brand']
            }
            product_list.append(product_info)

        result = product_list
        return result

    def get_filter_list(self, product_name) -> list[str]:

        '''추천 리스트 반환 api'''

        product_list = product_name.split(',')

        # Usage example:
        new_user_id = 99999
        print(len(self.rating_matrix))

        # product_list를 id로 변환
        new_cosme_ratings = dict()
        for product in product_list:
            product = product.strip()
            selected_rows = self.cosmetics[self.cosmetics['brand'] == product]
            if selected_rows.shape[0] > 0:
                new_cosme_ratings[selected_rows['brand_id'].item()] = 5


        # new_brand_ratings = {204: 5, 506: 4, 393: 3}
        new_matrix = self.add_new_user_ratings(new_user_id, new_cosme_ratings)

        recommended = self.infer(rating_matrix=new_matrix, current_user=new_user_id)

        to_recommend = self.parse_dataframe(recommended)
        return to_recommend


collabo_filter = CollaborationFilter()
# to_recommended = collabo_filter.get_filter_list('리얼베리어 익스트림 크림')
# print(to_recommended)