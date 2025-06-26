# utils/face_utils.py
import insightface
import numpy as np

# Load model using buffalo_l architecture on CUDA
model = insightface.app.FaceAnalysis(
    name="buffalo_l", providers=["CUDAExecutionProvider"]
)
model.prepare(ctx_id=0)


def get_face_embedding(frame):
    """Extract single face detection landmarks and embedding vector from image frame."""
    faces = model.get(frame)
    if faces:
        face = faces[0]
        return face, face.embedding
    return None, None


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity score between two 512D arrays."""
    # Explicitly calculate norms using float32 precision
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1).astype(np.float32) * np.linalg.norm(vec2).astype(np.float32))
