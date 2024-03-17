use array::ArrayTrait;
use orion::operators::tensor::{TensorTrait, Tensor, I32Tensor};
use orion::numbers::i32;


fn fc2_bias() -> Tensor<i32> {
    let mut shape = ArrayTrait::<usize>::new();
    shape.append(10);
    let mut data = ArrayTrait::<i32>::new();
    data.append(i32 { mag: 623, sign: true });
    data.append(i32 { mag: 277, sign: false });
    data.append(i32 { mag: 673, sign: false });
    data.append(i32 { mag: 415, sign: true });
    data.append(i32 { mag: 132, sign: false });
    data.append(i32 { mag: 1046, sign: false });
    data.append(i32 { mag: 403, sign: true });
    data.append(i32 { mag: 861, sign: false });
    data.append(i32 { mag: 1844, sign: true });
    data.append(i32 { mag: 34, sign: true });
    TensorTrait::new(shape.span(), data.span())
}
