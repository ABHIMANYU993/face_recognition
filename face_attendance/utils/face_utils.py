import insightface
import numpy as np

model = insightface.app.FaceAnalysis(
    name="buffalo_l", providers=["CUDAExecutionProvider"]
)
model.prepare(ctx_id=0)


def get_face_embedding(frame):
    faces = model.get(frame)
    if faces:
        face = faces[0]
        return face, face.embedding
    return None, None


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
