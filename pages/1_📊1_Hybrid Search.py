import streamlit as st , os, requests, pandas as pd, singlestoredb as s2
from streamlit_extras.stateful_button import button
from utils import st_def, hallucinations
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title='👋 AI', page_icon="🚀")
st.title('🔍 AI')
st_def.st_logo()
st.markdown("📄Rule Extraction📚: Python Libraries  Approaches🍨 ")
#+--------------------------------------------------------------------------------------------
model = SentenceTransformer('flax-sentence-embeddings/all_datasets_v3_mpnet-base')
#+--------------------------------------------------------------------------------------------
# Input box for URL
tab1, tab2, tab3 = st.tabs(["🍨CSV", "📰Embedding and saving to SingleStore", "🚀Query"])
with tab1:
    data = hallucinations.df_csv(file_path='./data/AG_news_samples.csv', url = 'https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/data/AG_news_samples.csv')
    descriptions = [row['description'] for row in data]
    st.write(data[0])
    st.write(data)

with tab2:
    if button("See Embedding to Table?", key="button2"):

        st.divider()
        all_embeddings = model.encode(descriptions)
        st.write(all_embeddings.shape)
        st.divider()

        for row, embedding in zip(data, all_embeddings):
            row['embedding'] = embedding

        filtered_data = [{'title': row['title'], 'description': row['description'],'genre': row['label'],'embedding': row['embedding']} for row in data]
        data_tuples =  [(d["title"], d["description"], d["genre"], d["embedding"]) for d in filtered_data]

        st.write(data_tuples)

        conn = s2.connect(host="svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com",
                      port=3333, user="aixpertlab2", password=os.environ.get("SINGLE_STORE_DB_PASSWORD"),database="database_92772", results_type="tuples")
        stmt = "INSERT INTO news_articles (title,description,genre,embedding)  VALUES (%s, %s, %s, %s)"

        with conn:
            conn.autocommit(True)
            with conn.cursor() as cur:
                # cur.execute("CREATE TABLE IF NOT EXISTS news_articles (title TEXT,description TEXT,genre TEXT,embedding BLOB,FULLTEXT(title, description))")

                cur.executemany(stmt, data_tuples)
                # cur.execute("""SELECT * FROM news_articles""")
                # rows = cur.fetchall()
                # st.code(rows)

with tab3:
    search_query = 'Aussie'
    search_embedding = model.encode(search_query)
    query_statement = '''
        SELECT title, description, genre, DOT_PRODUCT(embedding, %s) AS score
        FROM news_articles
        ORDER BY score DESC
        LIMIT 10
    '''

    conn = s2.connect(host="svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com",
                      port=3333, user="aixpertlab2", password=os.environ.get("SINGLE_STORE_DB_PASSWORD"),
                      database="database_92772", results_type="tuples")

    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            cur.execute(query_statement, (search_embedding,))
            results = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            results_df = pd.DataFrame(results, columns=columns)

    st.write(results_df)

    if button("Final Query?", key="button4"):
        hyb_query = 'Articles about Aussie captures'
        hyb_embedding = model.encode(hyb_query)

        # Create the SQL statement.
        hyb_statement = '''
            SELECT
                title,description,genre,
                DOT_PRODUCT(embedding, %s) AS semantic_score,
                MATCH(title, description) AGAINST (%s) AS keyword_score,
                (semantic_score + keyword_score) / 2 AS combined_score
            FROM news_articles
            ORDER BY combined_score DESC
            LIMIT 20
        '''
        conn = s2.connect(host="svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com",
                          port=3333, user="aixpertlab2", password=os.environ.get("SINGLE_STORE_DB_PASSWORD"),
                          database="database_92772", results_type="tuples")

        with conn:
            conn.autocommit(True)
            with conn.cursor() as cur:
                cur.execute(hyb_statement, (hyb_embedding, hyb_query))
                results = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                results_df = pd.DataFrame(results, columns=columns)

        # Execute the SQL statement.
        st.write(results_df)
