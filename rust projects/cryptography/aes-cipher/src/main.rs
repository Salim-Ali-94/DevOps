mod utility;


fn main() {

    let (x, y, z) = utility::aesKeyGenerator(999);
    println!("the aes key is = {} / {}", x, x.len());
    println!("hex key is = {:?}", y);
    println!("number of rounds = {}", z);

}
