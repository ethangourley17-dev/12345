import tensorflow as tf
from tensorflow.keras import layers, models
import os

def build_and_save_model():
    print("Building prototype CNN for Roof Damage Classification...")

    # 1. Define a simple CNN Architecture
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    # 2. Compile
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # 3. Determine Save Path (Vertex AI vs Local)
    # Vertex AI sets 'AIP_MODEL_DIR' env var
    output_path = os.environ.get('AIP_MODEL_DIR', 'roof_damage_model')

    print(f"Saving model to {output_path}...")
    try:
        # Save in TensorFlow SavedModel format (preferred for Vertex)
        model.save(output_path)
        print(f"\u2705 Model successfully saved to {output_path}")
    except Exception as e:
        print(f"\u274c Error saving model: {e}")

if __name__ == "__main__":
    build_and_save_model()
