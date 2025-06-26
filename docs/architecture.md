# System Architecture & Flow

This document details the system design, data flow, and interactions between the components of the Face Recognition Attendance System.

## High-Level System Overview
The system follows a modular architectural pattern consisting of three core layers:
1. Perception Layer (OpenCV & Camera/Video Feed)
2. Analysis Layer (InsightFace & ONNX Runtime)
3. Storage & Log Layer (SQLite)
