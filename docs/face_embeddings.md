# Face Embeddings & Detection Mechanics

This document explains the algorithms, machine learning models, and mathematical comparisons used by this system for facial detection and verification.

---

## 🧠 Model Pipeline: InsightFace

The application uses **InsightFace** (specifically the `buffalo_l` model bundle), which relies on ONNX Runtime for high-performance execution. The pipeline performs two sequential neural network tasks on each frame:

1. **Face Detection (RetinaFace)**:
   - Locates any human faces in the frame.
   - Outputs the bounding box coordinate array `[xmin, ymin, xmax, ymax]` and 5 facial landmark points (eyes, nose, mouth corners).
2. **Face Feature Extraction (ArcFace)**:
   - Normalizes (warps/crops) the detected face region based on facial landmarks.
   - Extracts a unique **512-dimensional vector** (called an embedding) representing the face's features.

---

## 📐 Cosine Similarity Matcher

Once a live face embedding is generated, it must be compared to the registered student embeddings stored in SQLite. This comparison uses **Cosine Similarity**.

### Mathematical Formula
Cosine similarity measures the cosine of the angle between two multi-dimensional vectors. It evaluates directional orientation rather than magnitude:

$$\text{Similarity}(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

In python, this is implemented in `utils/face_utils.py`:
```python
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
```

### Matching Ranges
* **`1.0`**: Exact same face orientation/features (identical vectors).
* **`> 0.6`**: Good match confidence. The threshold is set to `0.6` in `main.py` which balances between False Accept Rate (FAR) and False Reject Rate (FRR).
* **`< 0.4`**: Completely different faces.

---

## ⚡ Execution Providers

InsightFace runs using **ONNX Runtime**, supporting both hardware accelerators and CPU targets. In `utils/face_utils.py`, the model is initialized with:

```python
model = insightface.app.FaceAnalysis(
    name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)
```

1. **`CUDAExecutionProvider`**: Runs inference on Nvidia GPUs (such as the GeForce RTX 3070). This requires CUDA Toolkit and cuDNN libraries to be matched on the host machine.
2. **`CPUExecutionProvider`**: The fallback option. If CUDA drivers are missing or incompatible, ONNX Runtime automatically falls back to CPU execution, preventing program crashes.
