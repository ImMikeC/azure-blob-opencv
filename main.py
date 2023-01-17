# "DefaultEndpointsProtocol=https;AccountName=stgehspocdev001;AccountKey=+oNAbn7yAhJ0aCP3ZQ7TWBpPBD28q56r+sUECY6roMUObsMGDo97aiXcj88DWwSGNGODx+ejVmmY+ASt6pFUYA==;EndpointSuffix=core.windows.net"

from fastapi import FastAPI
from azure.storage.blob import BlobServiceClient, BlobClient
import cv2
import numpy as np

app = FastAPI()

@app.post("/overlay")
async def overlay_images(file1: str, file2: str):
    try:
        # conexion al Azure Blob storage
        print("uno")
        blob_service_client = BlobServiceClient.from_connection_string(
            "DefaultEndpointsProtocol=https;AccountName=stgehspocdev001;AccountKey=+oNAbn7yAhJ0aCP3ZQ7TWBpPBD28q56r+sUECY6roMUObsMGDo97aiXcj88DWwSGNGODx+ejVmmY+ASt6pFUYA==;EndpointSuffix=core.windows.net"
        )
        print("dos")
        # obtener container
        container_client = blob_service_client.get_container_client("files-demo")
        print("tres")
        # blob para imagen 1
        blob_client1 = container_client.get_blob_client(file1)
        # Read the first image and save it as a numpy array
        print("cuatro")
        image1 = cv2.imdecode(
            np.asarray(bytearray(blob_client1.download_blob().readall()), dtype=np.uint8),
            cv2.IMREAD_COLOR
        )
        print("cinco")
        # blob para imagen 2
        blob_client2 = container_client.get_blob_client(file2)
        print("seis")
        # Read the second image and save it as a numpy array
        image2 = cv2.imdecode(
            np.asarray(bytearray(blob_client2.download_blob().readall()), dtype=np.uint8),
            cv2.IMREAD_COLOR
        )
        print("siete")
        # ajusta tamano de la imagen 2 al tamano de la imagen 1
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
        print("ocho")
        # predefine alpha y beta
        alpha = 0.5
        beta = 1 - alpha
        
        # overlay usando cv2.addWeighted()
        overlay = cv2.addWeighted(image1, alpha, image2, beta, 0)
        
        print("nueve")
        # comprime imagen antes de subirla al Azure Blob storage
        _, img_encoded = cv2.imencode('.jpg', overlay)
        img_bytes = img_encoded.tobytes()

        container_client.upload_blob(data=img_bytes, name="overlay.jpg")
        print("diez")
        return {"message": "Overlay image uploaded to Azure Blob storage successfully."}
    except Exception as e:
        return {"error": str(e)}


