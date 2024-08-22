import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import MetadataQuery
from weaviate.classes.query import Filter
from weaviate.classes.query import MetadataQuery
from dotenv import load_dotenv
import os

load_dotenv()
headers = {"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
weaviateClient = weaviate.connect_to_wcs(
    cluster_url=os.getenv("WEAVIATE_CLUSTER_URL"),
    auth_credentials=weaviate.auth.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY")),
    headers=headers,
)

shorts = weaviateClient.collections.get("ChannelShortsTranscript")
response = shorts.generate.near_text(
    query="fitness",
    filters=Filter.by_property("transcript").contains_all(["fitness"]),
    limit=2,
    single_prompt="Extract painpoint about a product, service, system if it exists. Write them into bullet points style: {transcript}",
    return_metadata=MetadataQuery(distance=True)
)

print("="*20)
print(response)
print("="*20)

weaviateClient.close()