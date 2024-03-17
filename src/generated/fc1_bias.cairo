use array::ArrayTrait;
use orion::operators::tensor::{TensorTrait, Tensor, I32Tensor};
use orion::numbers::i32;


fn fc1_bias() -> Tensor<i32> {
    let mut shape = ArrayTrait::<usize>::new();
    shape.append(10);
    let mut data = ArrayTrait::<i32>::new();
    data.append(i32 { mag: 154, sign: false });
    data.append(i32 { mag: 668, sign: true });
    data.append(i32 { mag: 2854, sign: false });
    data.append(i32 { mag: 1871, sign: false });
    data.append(i32 { mag: 5127, sign: false });
    data.append(i32 { mag: 1825, sign: false });
    data.append(i32 { mag: 3455, sign: false });
    data.append(i32 { mag: 287, sign: false });
    data.append(i32 { mag: 4991, sign: false });
    data.append(i32 { mag: 2722, sign: false });
    TensorTrait::new(shape.span(), data.span())
}
