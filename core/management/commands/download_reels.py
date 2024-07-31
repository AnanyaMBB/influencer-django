from django.core.management.base import BaseCommand
import core.models
import requests
from pydub import AudioSegment
import yt_dlp
# from openai import OpenAI
import os
import whisper
import weaviate 
import weaviate.classes as wvc
from weaviate.classes.config import Configure
import uuid

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


class Command(BaseCommand):
    help = "Download data from Instagram API and store it in the database"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weaviateClient = None

    def handle(self, *args, **options):
        self.stdout.write("Starting Instagram reels downlaoad...")
        self.embedder = BertEmbedder()
        self.model = whisper.load_model("small.en")        
        headers = {"X-Openai-Api-Key": "sk-proj-oJ90ayJJp94Y0mg7iSscT3BlbkFJVEL3hZ7kP6XeJvVstayT"}
        self.weaviateClient = weaviate.connect_to_wcs(
            cluster_url="https://tqlqkkhqaaoyr5kvqg1iq.c0.us-west3.gcp.weaviate.cloud",
            auth_credentials=weaviate.auth.AuthApiKey(api_key="HOGwYb0eOrq38VkLe3kiPClt2UMwy8NPMKPB"),
            headers=headers
        )
        try:
            if self.weaviateClient.is_ready():
                print("Successfully connected to Weaviate")
                print("Creating schema")
                self.create_schema()
                self.get_data()
            else:
                print("Weaviate is not ready")
            
        except Exception as e:
            print(f"Error connecting to Weaviate: {e}")
        finally: 
            self.weaviateClient.close()
        # self.get_data()

    def create_schema(self):
        # class_obj = {
        #     "class": "Transcription",
        #     "vectorizer": "text2vec-transformers",
        #     "properties": [
        #         {
        #             "name": "media_id",
        #             "dataType": ["string"],
        #         }, {
        #             "name": "text",
        #             "dataType": ["text"],
        #         }
        #     ]
        # }

        # try: 
        #     self.weaviateClient.schema.create_class(class_obj)
        #     print("Schema created")
        # except Exception as e:
        #     print(f"Error creating schema: {e}")

        try: 
            self.weaviateClient.collections.create(
                name="Transcription", 
                vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(
                    model="text-embedding-3-large",
                    dimensions=1024
                ),    # Set the vectorizer to "text2vec-openai" to use the OpenAI API for vector-related operations
                generative_config=Configure.Generative.openai(),
              
                properties=[
                    wvc.config.Property(
                        name="media_id", 
                        data_type=wvc.config.DataType.TEXT,
                        vectorize_property_name=False,
                        skip_vectorization=True,
                        tokenization=wvc.config.Tokenization.LOWERCASE
                    ),
                    wvc.config.Property(
                        name="transcript",
                        data_type=wvc.config.DataType.TEXT,
                        tokenization=wvc.config.Tokenization.LOWERCASE
                    ),
                ],
                vector_index_config=wvc.config.Configure.VectorIndex.hnsw(
                    distance_metric=wvc.config.VectorDistances.COSINE,
                    quantizer=wvc.config.Configure.VectorIndex.Quantizer.bq(),
                ),
            )
            print("====>Schema created")
        except Exception as e:
            print(f"Error creating schema: {e}")
        

    def add_to_weaviate(self, media_id, transcription):
        try: 
            self.weaviateClient.collections.get("Transcription").data.insert(
                properties={
                    "media_id": media_id,
                    "transcript": transcription,
                }
                # vector=self.embedder.generate_embeddings([transcription]).numpy()                                
            )
            print(f"Added transcription for media_id {media_id} to Weaviate")
        except Exception as e:
            print(f"Error adding transcription to Weaviate: {e}")
            
    def get_data(self):
        # url = "https://https://graph.facebook.com/v18.0/"
        instagramMediaData = core.models.InstagramMediaData.objects.filter(
            transcribed=False, media_product_type="REELS"
        )
        print("Retrieved Data", instagramMediaData)
        for mediaData in instagramMediaData:
            url = f"https://graph.facebook.com/v18.0/{mediaData.media_id}?fields=media_url,media_type,media_product_type&access_token={mediaData.influencer_instagram_information.long_access_token}"
            response = requests.get(url)
            response = response.json()
            if (
                response
                and "error" not in response
                and response["media_product_type"] == "REELS"
            ):
                print(response)
                mediaUrl = response["media_url"]
                audio_path = f'.\\reels\\{response["id"]}'
                
                try:
                    self.download_audio(mediaUrl, audio_path)
                except Exception as e:
                    print("Error downloading audio", e)

                try:
                    resultText = self.transcribe(audio_path)
                    self.add_to_weaviate(mediaData.media_id, resultText)
                    mediaData.transcribed = True
                    mediaData.save()
                except Exception as e:
                    print("Error transcribing audio", e)

    def download_audio(self, mediaUrl, audio_path):
        ydl_opts = {
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": audio_path,
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([mediaUrl])

    def transcribe(self, audio_path):
        # locally running whisper model
        audio_file = open(audio_path + ".mp3", "rb")
        result = self.model.transcribe(audio_path + ".mp3")
        audio_file.close()
        print("Transcription result", result["text"])
        return result["text"]

        # using openai api
        # client = OpenAI(api_key="sk-proj-SE0HLH27YshBsku7JhccT3BlbkFJRsPqjXMrnVHxt5YQndzd")
        # transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
        # print(transcription.text)
