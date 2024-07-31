# import weaviate
# from weaviate.auth import AuthApiKey

# def test_weaviate_connection():
#     try:
#         # Initialize the Weaviate client
#         client = weaviate.Client(
#             url="https://tqlqkkhqaaoyr5kvqg1iq.c0.us-west3.gcp.weaviate.cloud",
#             auth_client_secret=AuthApiKey("HOGwYb0eOrq38VkLe3kiPClt2UMwy8NPMKPB")
#         )

#         # Check if the client is ready
#         if client.is_ready():
#             print("Weaviate client is ready")
#         else:
#             print("Weaviate client is not ready")

#         # List all classes in the Weaviate instance
#         schema = client.schema.get()
#         classes = schema['classes']
#         print("Available classes in Weaviate:")
#         for cls in classes:
#             print(f" - {cls['class']}")

#     except Exception as e:
#         print(f"Error connecting to Weaviate: {e}")

# if __name__ == "__main__":
#     test_weaviate_connection()


# import weaviate
# from weaviate.embedded import EmbeddedOptions

# client = weaviate.connect_to_wcs(
#     cluster_url="https://tqlqkkhqaaoyr5kvqg1iq.c0.us-west3.gcp.weaviate.cloud",  # Replace with your actual cluster URL
#     auth_credentials=weaviate.auth.AuthApiKey(api_key="HOGwYb0eOrq38VkLe3kiPClt2UMwy8NPMKPB"),  # Replace with your actual API key
# )

# # Test the connection
# try:
#     if client.is_ready():
#         print("Successfully connected to Weaviate")
#     else:
#         print("Weaviate is not ready")
# except Exception as e:
#     print(f"Error connecting to Weaviate: {e}")
# finally:
#     client.close()


import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import MetadataQuery
from transformers import BertTokenizer, BertModel
import torch 

class BertEmbedder: 
    def __init__(self, model_name="bert-base-uncased"):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        # self.model.eval()

    def generate_embeddings(self, text_list):
        inputs = self.tokenizer(text_list, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        with torch.no_grad(): 
            outputs = self.model(**inputs)

        embeddings = outputs.last_hidden_state

        sentence_embeddings = torch.mean(embeddings, dim=1)
        return sentence_embeddings

headers = {
    "X-OpenAI-Api-Key": "sk-proj-oJ90ayJJp94Y0mg7iSscT3BlbkFJVEL3hZ7kP6XeJvVstayT"
}
weaviateClient = weaviate.connect_to_wcs(
    cluster_url="https://tqlqkkhqaaoyr5kvqg1iq.c0.us-west3.gcp.weaviate.cloud",
    auth_credentials=weaviate.auth.AuthApiKey(
        api_key="HOGwYb0eOrq38VkLe3kiPClt2UMwy8NPMKPB"
    ),
    headers=headers,
)

try: 
    if weaviateClient.is_ready():
        print("Successfully connected to Weaviate")
        transcriptions = weaviateClient.collections.get("ReelsTranscript")
        # embedder = BertEmbedder()
        # query = embedder.generate_embeddings(["grateful to viewer"]).numpy()
        # print(query.shape)
        # response = transcriptions.query.near_vector(
        #     near_vector=query[0],
        #     return_metadata=wvc.query.MetadataQuery(certainty=True)
        # )
        response = transcriptions.query.near_text(
            query="online business",  # The model provider integration will automatically vectorize the query
            target_vector="transcript_vector",
            limit=2,
            return_metadata=wvc.query.MetadataQuery(certainty=True), 
        )


        print(response)
        # response = transcriptions.query.fetch_objects(include_vector=True, limit=1)
        # print("Response:", response)
        # for o in response.objects: 
        #     print(o)
        #     print(o.properties)
        #     print(o.metadata.distance)
    else:
        print("Weaviate is not ready")
except Exception as e:
    print(f"Error connecting to Weaviate: {e}")
finally:
    weaviateClient.close()