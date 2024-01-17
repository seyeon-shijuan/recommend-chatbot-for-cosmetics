import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import operator


class CollaborationFilter():
    def __init__(self, filepath):
        self.original_cosmetics = pd.read_csv(filepath)
        self.cosmetics = self.original_cosmetics.drop_duplicates(subset='brand_id')
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

    def get_most_famous_product_by_skin_type(self):
        df = self.original_cosmetics
        famous_products_df = pd.DataFrame(columns=df.columns)

        # 'skin_type'이 '지성에 좋아요'인 행 필터링
        filtered_df = df[df['skin_type'] == self.skin_type]

        # 'brand'를 기준으로 group by
        grouped_df = filtered_df.groupby('brand').size().reset_index(name='count')
        grouped_df = grouped_df.sort_values(by='count', ascending=False)
        selected = grouped_df[:3]

        for item in selected['brand'].tolist():
            to_add = df.loc[df['brand'] == item].iloc[0, :].to_frame().T
            famous_products_df = pd.concat([famous_products_df, to_add], axis=0, ignore_index=True)

        return famous_products_df

    def infer(self, rating_matrix, current_user=226):
        top_users_similarities = self.similar_users(current_user, rating_matrix)
        print(f"{top_users_similarities=}")
        similar_user_indices = [u[0] for u in top_users_similarities]

        self.candidates = self.get_most_famous_product_by_skin_type()
        # top K(5명) 번호
        recommended = self.recommend_item(current_user, similar_user_indices, rating_matrix, self.candidates)

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
        filtered_index_similarity = {index: similarity for index, similarity in index_similarity.items() if
                                     similarity != 0.0}

        # sort by similarity
        index_similarity_sorted = sorted(filtered_index_similarity.items(), key=operator.itemgetter(1))
        index_similarity_sorted.reverse()

        # grab k users off the top
        top_users_similarities = index_similarity_sorted[:k]


        return top_users_similarities

    def recommend_item(self, user_index, similar_user_indices, matrix, candidates=None, items=3):
        # load vectors for similar users
        similar_users = matrix[matrix.index.isin(similar_user_indices)]
        # calc avg ratings across the 3 similar users
        similar_users = similar_users.mean(axis=0)
        # convert to dataframe so its easy to sort and filter
        similar_users_df = pd.DataFrame(similar_users, columns=['mean'])

        # load vector for the current user
        user_df = matrix[matrix.index == user_index]
        # transpose it so its easier to filter
        user_df_transposed = user_df.transpose()
        # rename the column as 'rating'
        user_df_transposed.columns = ['rate']
        # remove any rows without a 0 value. Anime not watched yet
        user_df_transposed = user_df_transposed[user_df_transposed['rate'] == 0]
        # generate a list of animes the user has not seen
        animes_unseen = user_df_transposed.index.tolist()
        # filter avg ratings of similar users for only anime the current user has not seen
        similar_users_df_filtered = similar_users_df[similar_users_df.index.isin(animes_unseen)]

        # order the dataframe
        similar_users_df_ordered = similar_users_df_filtered.sort_values(by=['mean'], ascending=False)
        similar_users_df_ordered = similar_users_df_ordered[similar_users_df_ordered['mean'] != 0]

        # 0인것 제거한 후 row개수가 3개 미만인경우 추가
        # similar_users_df_ordered = similar_users_df_ordered[similar_users_df_ordered['mean'] !=0]
        # if len(similar_users_df_ordered) < 3:

        # brand_df = self.cosmetics[['brand', 'rate']]
        # brand_group_df = brand_df.groupby(by="brand")

        # 'brand' 및 'skin_type'으로 그룹화하고 최빈값 찾기
        # result = self.original_cosmetics.groupby(['brand', 'skin_type']).size().reset_index(name='count')
        # idx = result.groupby('brand')['count'].idxmax()
        # most_common_skin_type = result.loc[idx, ['brand', 'skin_type']]
        # most_common_skin_type = most_common_skin_type.drop_duplicates(subset=['brand', 'skin_type'])

        # first_brand_id = similar_users_df_ordered.iloc[0, 0]
        # first_skin_type = self.original_cosmetics[self.original_cosmetics['brand'] == first_brand_id]['skin_type']

        # brand_df = self.original_cosmetics.groupby('brand')[''].max()

        # print(most_common_skin_type)

        # max_item = self.cosmetics[['brand', 'rate']].value_counts().head(10)

        # grab the top n brand
        top_n_brand = similar_users_df_ordered.head(items)
        top_n_brand_indices = top_n_brand.index.tolist()

        # lookup these anime in the other dataframe to find names
        brand_information = self.cosmetics[self.cosmetics['brand_id'].isin(top_n_brand_indices)]

        n_brand_information = len(brand_information)
        if n_brand_information < items:
            to_append = candidates[:items - n_brand_information]
            brand_information = pd.concat([brand_information, to_append])

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

    def set_my_skintype(self, product_list):
        filtered_df = self.original_cosmetics[self.original_cosmetics['brand'].isin(product_list)]
        most_common_skin_type = filtered_df['skin_type'].mode().iloc[0]
        self.skin_type = most_common_skin_type
        print(f"{self.skin_type=}")

    def get_filter_list(self, product_name) -> list[str]:
        '''추천 리스트 반환 api'''
        product_list = product_name.split(', ')
        self.set_my_skintype(product_list)

        new_user_id = 99999

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


collabo_filter = CollaborationFilter(filepath="collabo_filtering_dataset2.csv")
# to_recommended = collabo_filter.get_filter_list('AHC 온리 포맨 토너')
# to_recommended = collabo_filter.get_filter_list('식물나라 카렌둘라 진정 토너, 라운드랩 소나무 진정 시카 토너, 라네즈 워터뱅크 블루히알루로닉 세럼')
# to_recommended = collabo_filter.get_filter_list('구달 맑은 어성초 진정 수분크림, 피캄 베리어 사이클 락토P 토너') #
# print(to_recommended)