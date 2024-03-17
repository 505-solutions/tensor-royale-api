import os
import random
import string

import numpy as np
import tensorflow as tf


def encode(model):
    # create a folder to store the generated files
    folder_name = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    folder = os.path.join(os.environ['CAIRO_PATH'], folder_name)
    os.makedirs(folder, exist_ok=True)

    # retrive this from file coin
    model_file = 'some_saved_keras_model.h5' # retrive from filecoin
    test_data = './data' # retrive from filecoin

    # Create a converter
    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    # Indicate that you want to perform default optimizations,
    # which include quantization
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    # Define a generator function that provides your test data's numpy arrays
    def representative_data_gen():
        for i in range(500):
            yield [test_data[i:i+1]]

    # Use the generator function to guide the quantization process
    converter.representative_dataset = representative_data_gen

    # Ensure that if any ops can't be quantized, the converter throws an error
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

    # Set the input and output tensors to int8
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    # Convert the model
    tflite_model = converter.convert()

    # Save the model to disk
    model_location = 'converted_model.tflite'
    open(model_location, "wb").write(tflite_model)


    # Load the TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=model_location)
    interpreter.allocate_tensors()

    # Create an object with all tensors (an input + all weights and biases)
    tensors = {
        "input": test_data[0].flatten(), #7
        "fc1_weights": interpreter.get_tensor(1), 
        "fc1_bias": interpreter.get_tensor(2), 
        "fc2_weights": interpreter.get_tensor(4), 
        "fc2_bias": interpreter.get_tensor(5)
    }

    # Create the directory if it doesn't exist
    os.makedirs('src/generated', exist_ok=True)

    for tensor_name, tensor in tensors.items():
        with open(os.path.join('src', 'generated', f"{tensor_name}.cairo"), "w") as f:
            f.write(
                "use array::ArrayTrait;\n" +
                "use orion::operators::tensor::{TensorTrait, Tensor, I32Tensor};\n" +
                "use orion::numbers::i32;\n\n" +
                "\nfn {0}() -> Tensor<i32> ".format(tensor_name) + "{\n" +
                "    let mut shape = ArrayTrait::<usize>::new();\n"
            )
            for dim in tensor.shape:
                f.write("    shape.append({0});\n".format(dim))
            f.write(
                "    let mut data = ArrayTrait::<i32>::new();\n"
            )
            for val in np.nditer(tensor.flatten()):
                f.write("    data.append(i32 {{ mag: {0}, sign: {1} }});\n".format(abs(int(val)), str(val < 0).lower()))
            f.write(
                "    TensorTrait::new(shape.span(), data.span())\n" +
                "}\n"
            )
        
    with open(os.path.join('src', 'generated.cairo'), 'w') as f:
        for param_name in tensors.keys():
            f.write(f"mod {param_name};\n")



