import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2

def predict_diseases(image_path):
    """
    Predicts the disease of a rice plant from an image.

    Args:
        image_path (str): The path to the image file.
        model_path (str): The path to the trained Keras model file.

    Returns:
        str: The predicted disease name.
    """
    
    model_path='model/trained_models.keras'

    # Load the model
    model = tf.keras.models.load_model(model_path)

    # Read and preprocess the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to a batch

    # Make the prediction
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)

    # Disease class names
    class_name = [
        'Aggregate sheath',
        'Bacterial_leaf_blight',
        'Bacterial_leaf_streak',
        'Blast',
        'Brown spot',
        'Eye spot',
        'False smut',
        'Kernel smut',
        'Leaf smut',
        'Leaf smut (1)',
        'Narrow brown leaf spot',
        'Narrow brown leaf spot (1)',
        'Sheath rot',
        'Sheath spot',
        'Tungro1',
        'crown sheath rot',
        'flag leaf sheath',
        'foot_rot',
        'grassy stunt virus',
        'leaf scald',
        'leaf scald (1)',
        'pecky_rice_kernel_spotting',
        'pecky_rice_kernel_spotting (1)',
        'powdery mildew',
        'ragged stunt virus',
        'sheath blight',
        'sheath_brown_rot',
        'yellow mottle1'
    ]

    # Get the predicted disease name
    model_prediction = class_name[result_index]

    #Display the image and result.
    # plt.imshow(img)
    # plt.title(f"Disease Name: {model_prediction}")
    # plt.xticks()
    # plt.yticks()
    # plt.show()
    print(f"Predicted disease: {model_prediction}")
    return model_prediction

# Example usage:
# image_path = "/content/drive/MyDrive/Colab Notebooks/aicrop/Dataset/Kernel smut/1 (18).JPG"
# predicted_disease = predict_diseases(image_path)
