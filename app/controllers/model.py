import os


def bind_image(image):
    tensors = {
        "input": image.flatten(),
    }

    os.makedirs(os.path.join(os.environ["CAIRO_PATH"], "generated"), exist_ok=True)

    for tensor_name, tensor in tensors.items():
        with open(os.path.join(os.environ["CAIRO_PATH"], "generated", f"{tensor_name}.cairo"), "w") as f:
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
    
    # python run scarb --target-dir os.environ["CAIRO_PATH"] + "/output" build

if not os.path.exists(os.path.join(os.environ["CAIRO_PATH"], "nn.cairo")):
    
    os.environ['TF_USE_LEGACY_KERAS'] = '0'


    import numpy as np
    import tensorflow_model_optimization as tfmot
    from keras.datasets import mnist
    from tensorflow import keras

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    from scipy.ndimage import zoom


    def resize_images(images):
        return np.array([zoom(image, 0.5) for image in images])
    x_train = resize_images(x_train)
    x_test = resize_images(x_test)
    x_train = x_train.reshape(60000, 14*14)
    x_test = x_test.reshape(10000, 14*14)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    from tensorflow.keras import layers

    num_classes = 10
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=(14*14,)),
        keras.layers.Dense(10, activation='relu'), 
        keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy', 
                metrics=['accuracy'])
    batch_size = 256
    epochs = 10
    history = model.fit(x_train, y_train,
                        epochs=epochs,
                        validation_split=0.2)    
    quantize_model = tfmot.quantization.keras.quantize_model
    q_aware_model = quantize_model(model)
    q_aware_model.compile(optimizer='adam',
                        loss='sparse_categorical_crossentropy',
                        metrics=['accuracy'])

    print(q_aware_model.summary())
    batch_size = 256
    epochs = 10
    history = q_aware_model.fit(x_train, y_train,
                                epochs=epochs,
                                validation_split=0.2)

    scores, acc = q_aware_model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', scores)
    print('Test accuracy:', acc)

    import tensorflow as tf
    converter = tf.lite.TFLiteConverter.from_keras_model(q_aware_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    def representative_data_gen():
        for i in range(500):
            yield [x_test[i:i+1]]
    converter.representative_dataset = representative_data_gen
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8
    tflite_model = converter.convert()
    out_path = os.path.join(os.environ["CAIRO_PATH"], "q_aware_model.tflite")
    open(out_path, "wb").write(tflite_model)
    interpreter = tf.lite.Interpreter(model_path=out_path)
    interpreter.allocate_tensors()

    import os

    import numpy as np
    import tensorflow as tf

    interpreter = tf.lite.Interpreter(model_path=out_path)
    interpreter.allocate_tensors()
    (_, _), (x_test_image, y_test_label) = mnist.load_data()
    x_test_image = resize_images(x_test_image)

    tensors = {
        "input": x_test_image[0].flatten(),
        "fc1_weights": interpreter.get_tensor(1), 
        "fc1_bias": interpreter.get_tensor(2), 
        "fc2_weights": interpreter.get_tensor(4), 
        "fc2_bias": interpreter.get_tensor(5)
    }

    os.makedirs(os.path.join(os.environ["CAIRO_PATH"], "generated"), exist_ok=True)

    for tensor_name, tensor in tensors.items():
        with open(os.path.join(os.environ["CAIRO_PATH"], "generated", f"{tensor_name}.cairo"), "w") as f:
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
            
    with open(os.path.join(os.environ["CAIRO_PATH"],  'generated.cairo'), 'w') as f:
        for param_name in tensors.keys():
            f.write(f"mod {param_name};\n")

    with open(os.path.join(os.environ["CAIRO_PATH"], 'nn.cairo'), 'w') as f:
        f.write(""" use orion::operators::tensor::core::Tensor;
use orion::numbers::signed_integer::{integer_trait::IntegerTrait, i32::i32};
use orion::operators::nn::{NNTrait, I32NN};

fn fc1(i: Tensor<i32>, w: Tensor<i32>, b: Tensor<i32>) -> Tensor<i32> {
    let x = NNTrait::linear(i, w, b);
    NNTrait::relu(@x)
}

fn fc2(i: Tensor<i32>, w: Tensor<i32>, b: Tensor<i32>) -> Tensor<i32> {
    NNTrait::linear(i, w, b)
}            """)
    
    package_name = "tensorroyale"
    with open(os.path.join(os.environ["CAIRO_PATH"], 'Scrab.toml'), 'w') as f:
        f.write("""[package]
name = "tensorroyale"
version = "0.1.0"
                
[dependencies]
orion = { git = "https://github.com/gizatechxyz/orion.git", tag = "v0.2.0" }
""")
        
    # create inference.cairo
    with open(os.path.join(os.environ["CAIRO_PATH"], 'inference.cairo'), 'w') as f:
        f.write("""use orion::operators::tensor::core::TensorTrait;

use core::array::{SpanTrait, ArrayTrait};

use tensorroyale::nn::fc1;
use tensorroyale::nn::fc2;
use tensorroyale::generated::input::input;
use tensorroyale::generated::fc1_bias::fc1_bias;
use tensorroyale::generated::fc1_weights::fc1_weights;
use tensorroyale::generated::fc2_bias::fc2_bias;
use tensorroyale::generated::fc2_weights::fc2_weights;

use orion::operators::tensor::implementations::impl_tensor_fp::Tensor_fp;

fn main() -> u32 {
    let input = input();
    let fc1_bias = fc1_bias();
    let fc1_weights = fc1_weights();
    let fc2_bias = fc2_bias();
    let fc2_weights = fc2_weights();

    let x = fc1(input, fc1_weights, fc1_bias);
    let x = fc2(x, fc2_weights, fc2_bias);
    
    let x = *x.argmax(0, Option::None(()), Option::None(())).data.at(0);

    x
}""")
        
    generated_file = ['generated.cairo', 'nn.cairo', 'inference.cairo']
    with open(os.path.join(os.environ["CAIRO_PATH"], 'lib.cairo'), 'w') as f:
        for file in generated_file:
            f.write(f"mod {file.split('.')[0]};\n")